import os, re, json, time, math, pathlib
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss

EMBED_MODEL = os.getenv("CAPSTONE_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
RERANK_MODEL = os.getenv("CAPSTONE_RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
GEMINI_JUDGE_MODEL = os.getenv("GEMINI_JUDGE_MODEL", GEMINI_MODEL)
LOCAL_BASE_URL = os.getenv("LOCAL_LLM_BASE_URL", "http://127.0.0.1:8080/v1")
LOCAL_MODEL = os.getenv("LOCAL_LLM_MODEL", "qwen3.5-0.8b")

BASE_DIR = pathlib.Path(__file__).resolve().parent
with open(BASE_DIR / "data" / "eval_cases.json", "r", encoding="utf-8") as f:
    EVAL_CASES = json.load(f)

RULE_DOCS = [
    {"id":"R1","text":"A decision requires commitment, approval, agreement, selection, rejection, or an explicit statement that a course of action will be followed."},
    {"id":"R2","text":"A suggestion, possibility, brainstorm, or hypothetical such as maybe, could, might, consider, or what if is not a confirmed decision unless a later turn explicitly commits to it."},
    {"id":"R3","text":"An action item is future work assigned or accepted by a person or team. Capture the work and the owner; do not invent an owner when none is supported."},
    {"id":"R4","text":"Owner resolution may require cross-speaker context. Phrases such as 'I'll do it' refer to the current speaker even when the task was introduced in an earlier turn."},
    {"id":"R5","text":"A blocker is a concrete condition preventing, delaying, or risking progress. General background or ordinary status is not automatically a blocker."},
    {"id":"R6","text":"A follow-up question is an unresolved question that still needs an answer after the meeting. A question answered during the transcript should not remain open."},
    {"id":"R7","text":"Every extracted decision, action, blocker, and follow-up question should be grounded in transcript evidence. Preserve uncertainty instead of filling missing facts."},
    {"id":"R8","text":"The executive summary should synthesize only confirmed operational outcomes and important unresolved risks; it should not elevate brainstorming into commitments."},
]

FEW_SHOT_EXAMPLES = [
    {"text":"A: Maybe we could delay launch. B: No, keep Friday. A: Okay.","label":"decision","output":"Keep the Friday launch schedule; the delay was only a suggestion."},
    {"text":"A: Could we use vendor B? B: Let's compare legal terms first.","label":"context","output":"No vendor decision was made."},
    {"text":"A: The export is missing IDs. B: I'll ask Finance to correct them.","label":"action_item","output":"Owner B will ask Finance to correct the missing IDs."},
    {"text":"A: The date ranges differ, so the numbers do not match.","label":"blocker","output":"Mismatched date ranges are preventing consistent report numbers."},
    {"text":"A: Is customer ID present on every record?","label":"follow_up_question","output":"Open question: Is customer ID present on every record?"},
    {"text":"A: We agreed to keep human review before email is sent.","label":"decision","output":"Generated email requires human review before sending."},
    {"text":"A: The mapping failed. B: I will fix the three invalid dates today.","label":"action_item","output":"Owner B will fix the invalid dates today."},
    {"text":"A: Maybe remove the notes field. B: Not yet.","label":"context","output":"Removing the notes field was discussed but not approved."},
    {"text":"A: Legal has not reviewed the vendor terms.","label":"blocker","output":"Legal review of vendor terms is still outstanding."},
    {"text":"A: Which agreement can Legal clear this week?","label":"follow_up_question","output":"Open question: Which agreement can Legal clear this week?"},
    {"text":"A: Use September 1 through September 30 for both reports. B: Got it.","label":"decision","output":"Both reports will use September 1 through September 30."},
    {"text":"A: We need a key before proposal generation. B: I'll test domain plus customer ID.","label":"action_item","output":"Owner B will test domain plus customer ID as the matching key."},
]

BASE_INSTRUCTIONS = """You convert meeting transcripts into operational briefs.
Rules:
- Report only confirmed decisions, not suggestions or possibilities.
- Capture future work as action items and identify the supported owner.
- Do not invent an owner. Use \"Unknown\" when the transcript does not support one.
- A blocker must materially prevent, delay, or risk progress.
- A follow-up question must still be unresolved at the end of the transcript.
- Every extracted item must include concise transcript evidence.
- Return JSON only.

JSON shape:
{
  \"executive_summary\": \"string\",
  \"decisions\": [{\"decision\": \"string\", \"evidence\": \"string\"}],
  \"action_items\": [{\"description\": \"string\", \"owner\": \"string\", \"evidence\": \"string\"}],
  \"blockers\": [{\"blocker\": \"string\", \"evidence\": \"string\"}],
  \"follow_up_questions\": [{\"question\": \"string\", \"evidence\": \"string\"}]
}
"""

STOP = {"the","a","an","to","of","and","or","for","in","on","by","with","is","are","be","as","at","this","that"}
HEDGE_CUES = ["maybe","could","might","consider","possibly","what if","i think","we should look at","would rather"]
COMMIT_CUES = ["agreed","approved","decided","we will","we'll","keep","use ","go with","no schedule change","do not","don't","not choose","requires","required"]

_embedder = None
_reranker = None
_rule_index = None
_few_index = None


def load_models():
    global _embedder, _reranker, _rule_index, _few_index
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
        _reranker = CrossEncoder(RERANK_MODEL)
        rv = _embedder.encode([x["text"] for x in RULE_DOCS], normalize_embeddings=True).astype("float32")
        fv = _embedder.encode([x["text"] for x in FEW_SHOT_EXAMPLES], normalize_embeddings=True).astype("float32")
        _rule_index = faiss.IndexFlatIP(rv.shape[1]); _rule_index.add(rv)
        _few_index = faiss.IndexFlatIP(fv.shape[1]); _few_index.add(fv)
    return _embedder, _reranker


def dense_retrieve(query, docs, index, k=6):
    load_models()
    qv = _embedder.encode([query], normalize_embeddings=True).astype("float32")
    scores, ids = index.search(qv, min(k, len(docs)))
    return [{"doc":docs[int(i)],"dense_score":float(s)} for s,i in zip(scores[0],ids[0]) if int(i)>=0]


def rerank(query, candidates, top_k=4):
    load_models()
    scores = _reranker.predict([(query,c["doc"]["text"]) for c in candidates])
    out=[]
    for c,s in zip(candidates,scores):
        x=dict(c); x["rerank_score"]=float(s); out.append(x)
    return sorted(out,key=lambda x:x["rerank_score"],reverse=True)[:top_k]


def retrieve_rules(transcript, top_k=4):
    load_models(); return rerank(transcript,dense_retrieve(transcript,RULE_DOCS,_rule_index),top_k)


def retrieve_examples(transcript, top_k=3):
    load_models(); return rerank(transcript,dense_retrieve(transcript,FEW_SHOT_EXAMPLES,_few_index),top_k)


def _client(base_url=None, api_key=None):
    from openai import OpenAI
    return OpenAI(api_key=api_key or os.getenv("GEMINI_API_KEY","local"),base_url=base_url or "https://generativelanguage.googleapis.com/v1beta/openai/")


def parse_json_text(text):
    text=text.strip()
    text=re.sub(r"^```(?:json)?\s*","",text,flags=re.I)
    text=re.sub(r"\s*```$","",text)
    return json.loads(text)


def validate_brief(obj):
    errors=[]
    required={"executive_summary":str,"decisions":list,"action_items":list,"blockers":list,"follow_up_questions":list}
    if not isinstance(obj,dict): return False,["top-level output is not an object"]
    for k,t in required.items():
        if k not in obj: errors.append(f"missing field: {k}")
        elif not isinstance(obj[k],t): errors.append(f"{k} must be {t.__name__}")
    for i,x in enumerate(obj.get("decisions",[]) if isinstance(obj.get("decisions"),list) else []):
        for k in ("decision","evidence"):
            if not isinstance(x,dict) or not isinstance(x.get(k),str) or not x.get(k," ").strip(): errors.append(f"decisions[{i}].{k} invalid")
    for i,x in enumerate(obj.get("action_items",[]) if isinstance(obj.get("action_items"),list) else []):
        for k in ("description","owner","evidence"):
            if not isinstance(x,dict) or not isinstance(x.get(k),str) or not x.get(k," ").strip(): errors.append(f"action_items[{i}].{k} invalid")
    for field,key in (("blockers","blocker"),("follow_up_questions","question")):
        for i,x in enumerate(obj.get(field,[]) if isinstance(obj.get(field),list) else []):
            for k in (key,"evidence"):
                if not isinstance(x,dict) or not isinstance(x.get(k),str) or not x.get(k," ").strip(): errors.append(f"{field}[{i}].{k} invalid")
    return len(errors)==0,errors


def gemini_extract(transcript, config="A"):
    if not os.getenv("GEMINI_API_KEY"): raise RuntimeError("GEMINI_API_KEY is not set")
    blocks=[BASE_INSTRUCTIONS]; log={"rules":[],"examples":[]}
    if config in ("B","C"):
        log["rules"]=retrieve_rules(transcript,4)
        blocks.append("Retrieved operational guidance:\n"+"\n".join("- "+x["doc"]["text"] for x in log["rules"]))
    if config=="C":
        log["examples"]=retrieve_examples(transcript,3)
        blocks.append("Retrieved examples:\n"+"\n".join(f"- Input: {x['doc']['text']}\n  Interpretation: {x['doc']['output']}" for x in log["examples"]))
    blocks.append("Transcript:\n"+transcript)
    t0=time.perf_counter()
    resp=_client().chat.completions.create(model=GEMINI_MODEL,messages=[{"role":"user","content":"\n\n".join(blocks)}],temperature=0)
    latency=time.perf_counter()-t0
    raw=resp.choices[0].message.content
    try: brief=parse_json_text(raw); parse_error=None
    except Exception as e: brief={}; parse_error=f"{type(e).__name__}: {e}"
    valid,errors=validate_brief(brief)
    usage=getattr(resp,"usage",None)
    return {"brief":brief,"raw":raw,"valid":valid,"validation_errors":errors,"parse_error":parse_error,"latency_s":latency,"prompt_tokens":getattr(usage,"prompt_tokens",None) if usage else None,"completion_tokens":getattr(usage,"completion_tokens",None) if usage else None,"retrieval":log}


def tokens(s): return [x for x in re.findall(r"[a-z0-9]+",str(s).lower()) if x not in STOP]

def token_jaccard(a,b):
    A,B=set(tokens(a)),set(tokens(b))
    if not A and not B: return 1.0
    if not A or not B: return 0.0
    return len(A&B)/len(A|B)


def best_match_pairs(pred,gold,threshold=0.42):
    pairs=[]; unused=set(range(len(gold)))
    for pi,p in enumerate(pred):
        scored=[(token_jaccard(p,gold[gi]),gi) for gi in unused]
        if scored:
            score,gi=max(scored)
            if score>=threshold: pairs.append((pi,gi,score)); unused.remove(gi)
    return pairs


def prf(pred,gold,threshold=0.42):
    pairs=best_match_pairs(pred,gold,threshold); tp=len(pairs)
    p=tp/len(pred) if pred else (1.0 if not gold else 0.0)
    r=tp/len(gold) if gold else (1.0 if not pred else 0.0)
    f=2*p*r/(p+r) if p+r else 0.0
    return p,r,f,pairs


def flatten_brief(brief):
    return {"decisions":[x.get("decision","") for x in brief.get("decisions",[]) if isinstance(x,dict)],"actions":[x.get("description","") for x in brief.get("action_items",[]) if isinstance(x,dict)],"owners":[x.get("owner","") for x in brief.get("action_items",[]) if isinstance(x,dict)],"blockers":[x.get("blocker","") for x in brief.get("blockers",[]) if isinstance(x,dict)],"questions":[x.get("question","") for x in brief.get("follow_up_questions",[]) if isinstance(x,dict)]}


def evidence_supported(brief,transcript):
    t=re.sub(r"\s+"," ",transcript.lower()); ev=[]
    for field in ("decisions","action_items","blockers","follow_up_questions"):
        ev.extend(x.get("evidence","") for x in brief.get(field,[]) if isinstance(x,dict))
    if not ev: return 1.0
    return sum(bool(e) and re.sub(r"\s+"," ",e.lower()).strip() in t for e in ev)/len(ev)


def score_case(case,result):
    gold=case["gold"]; pred=flatten_brief(result["brief"]) if result.get("valid") else {"decisions":[],"actions":[],"owners":[],"blockers":[],"questions":[]}
    dp,dr,df,_=prf(pred["decisions"],gold["decisions"])
    ap,ar,af,apairs=prf(pred["actions"],[x["description"] for x in gold["actions"]])
    _,_,bf,_=prf(pred["blockers"],gold["blockers"]); _,_,qf,_=prf(pred["questions"],gold["follow_up_questions"])
    hits=[]
    for pi,gi,_ in apairs:
        po=pred["owners"][pi].strip().lower() if pi<len(pred["owners"]) else ""; go=gold["actions"][gi]["owner"].strip().lower(); hits.append(po==go)
    owner=sum(hits)/len(hits) if hits else (1.0 if not gold["actions"] else 0.0)
    return {"case_id":case["id"],"decision_precision":dp,"decision_recall":dr,"decision_f1":df,"action_precision":ap,"action_recall":ar,"action_f1":af,"owner_accuracy":owner,"blocker_f1":bf,"question_f1":qf,"valid":float(result.get("valid",False)),"evidence_support":evidence_supported(result["brief"],case["transcript"]) if result.get("valid") else 0.0,"latency_s":result.get("latency_s",math.nan)}


def run_ablation():
    results={}; rows=[]
    for cfg in ("A","B","C"):
        results[cfg]={}
        for case in EVAL_CASES:
            try: r=gemini_extract(case["transcript"],cfg)
            except Exception as e: r={"brief":{},"raw":"","valid":False,"validation_errors":[str(e)],"parse_error":str(e),"latency_s":math.nan,"prompt_tokens":None,"completion_tokens":None,"retrieval":{"rules":[],"examples":[]}}
            results[cfg][case["id"]]=r; s=score_case(case,r); s["config"]=cfg; rows.append(s)
    return results,pd.DataFrame(rows)

JUDGE_PROMPT="""Score the candidate meeting brief from 1 to 5 on exactly three dimensions: correctness, grounding, operational_usefulness. Return JSON only: {\"correctness\":1,\"grounding\":1,\"operational_usefulness\":1,\"reason\":\"brief reason\"}."""

def gemini_judge(case,candidate):
    payload={"transcript":case["transcript"],"gold_reference":case["gold"],"candidate":candidate}
    resp=_client().chat.completions.create(model=GEMINI_JUDGE_MODEL,messages=[{"role":"user","content":JUDGE_PROMPT+"\n\n"+json.dumps(payload)}],temperature=0)
    return parse_json_text(resp.choices[0].message.content)


def run_judge(results):
    rows=[]
    for cfg in ("A","B","C"):
        for case in EVAL_CASES:
            try: j=gemini_judge(case,results[cfg][case["id"]]["brief"])
            except Exception as e: j={"correctness":np.nan,"grounding":np.nan,"operational_usefulness":np.nan,"reason":str(e)}
            rows.append({"config":cfg,"case_id":case["id"],**j})
    return pd.DataFrame(rows)


def trace_failure(results):
    scores={cfg:{c["id"]:score_case(c,results[cfg][c["id"]]) for c in EVAL_CASES} for cfg in ("A","B","C")}
    chosen=None; component=None
    for c in EVAL_CASES:
        cid=c["id"]
        if scores["C"][cid]["decision_f1"]<scores["B"][cid]["decision_f1"]: chosen=cid; component="dynamic few-shot context (configuration C)"; break
    if chosen is None:
        for c in EVAL_CASES:
            cid=c["id"]
            if scores["B"][cid]["decision_f1"]<scores["A"][cid]["decision_f1"]: chosen=cid; component="retrieved/reranked rule context (configuration B)"; break
    if chosen is None:
        chosen=min((c["id"] for c in EVAL_CASES),key=lambda cid:scores["C"][cid]["decision_f1"]+scores["C"][cid]["action_f1"]); component="generation/extraction stage; no retrieval-induced regression observed"
    return {"case_id":chosen,"component":component,"scores":scores,"case":next(c for c in EVAL_CASES if c["id"]==chosen)}


def mitigate_decisions(brief):
    out=json.loads(json.dumps(brief)); kept=[]; removed=[]
    for item in out.get("decisions",[]):
        ev=item.get("evidence","").lower(); hedged=any(x in ev for x in HEDGE_CUES); committed=any(x in ev for x in COMMIT_CUES)
        (removed if hedged and not committed else kept).append(item)
    out["decisions"]=kept
    return out,removed

LOCAL_EVAL=[
("Maybe we should move the launch to Monday.","context"),("No schedule change right now.","decision"),("I'll send the final QA result by 3 PM.","action_item"),("The engineering effort is unknown.","blocker"),("What is the engineering effort for SSO?","follow_up_question"),("There is no decision on dashboard cadence today.","context"),("Keep the current import mapping for this release.","decision"),("I'll correct the dates and rerun the import today.","action_item"),("Legal has not reviewed Vendor B's terms.","blocker"),("Which agreement can Legal clear this week?","follow_up_question"),("We agreed to keep the shorter form for the pilot.","decision"),("I'll measure completion time for another week.","action_item"),("The report numbers don't match because the date ranges differ.","blocker"),("Use September 1 through September 30 for both sources.","decision"),("Could we automate the email after generation?","context"),("Generated drafts will require human review.","decision"),("I'll test domain plus customer ID as the matching key.","action_item"),("Is customer ID populated for every record?","follow_up_question"),("The owner field is wrong on two cases.","blocker"),("Do we need a separate coreference model?","follow_up_question")]

def local_classify(text):
    prompt=f"Classify into exactly one label: decision, action_item, blocker, follow_up_question, context. Return only the label.\nSpan: {text}"
    t0=time.perf_counter(); resp=_client(LOCAL_BASE_URL,"local").chat.completions.create(model=LOCAL_MODEL,messages=[{"role":"user","content":prompt}],temperature=0,max_tokens=20)
    return re.sub(r"[^a-z_]","",resp.choices[0].message.content.strip().lower()),time.perf_counter()-t0


def run_local_comparison():
    rows=[]
    for text,gold in LOCAL_EVAL:
        try: pred,latency=local_classify(text)
        except Exception as e: pred,latency=f"ERROR:{e}",math.nan
        rows.append({"text":text,"gold":gold,"pred":pred,"correct":pred==gold,"latency_s":latency})
    return pd.DataFrame(rows)
