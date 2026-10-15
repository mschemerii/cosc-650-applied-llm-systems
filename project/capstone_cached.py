import os, json, pathlib, hashlib
import pandas as pd

import capstone_core as core
from capstone_core import *

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
GEMINI_JUDGE_MODEL = os.getenv("GEMINI_JUDGE_MODEL", GEMINI_MODEL)

BASE_DIR = pathlib.Path(__file__).resolve().parent
CACHE_PATH = BASE_DIR / "data" / "response_cache.json"
MAX_SYNTHESIS_LIVE_CALLS = int(os.getenv("CAPSTONE_MAX_SYNTHESIS_CALLS", "36"))
MAX_JUDGE_LIVE_CALLS = int(os.getenv("CAPSTONE_MAX_JUDGE_CALLS", "36"))
_live_synthesis_calls = 0
_live_judge_calls = 0


def _load_cache():
    if not CACHE_PATH.exists():
        return {"synthesis": {}, "judge": {}}
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("synthesis", {})
        data.setdefault("judge", {})
        return data
    except Exception:
        return {"synthesis": {}, "judge": {}}


def _save_cache():
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(_CACHE, f, indent=2, ensure_ascii=False)


def _key(payload):
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


_CACHE = _load_cache()


def cache_summary():
    return {
        "synthesis_cached": len(_CACHE["synthesis"]),
        "judge_cached": len(_CACHE["judge"]),
        "live_synthesis_calls_this_run": _live_synthesis_calls,
        "live_judge_calls_this_run": _live_judge_calls,
        "cache_path": str(CACHE_PATH),
    }


def gemini_extract(transcript, config="A"):
    global _live_synthesis_calls
    model = GEMINI_MODEL
    cache_key = _key({"kind": "synthesis", "model": model, "config": config, "transcript": transcript})
    if cache_key in _CACHE["synthesis"]:
        cached = dict(_CACHE["synthesis"][cache_key])
        cached["cache_hit"] = True
        cached["retrieval"] = {"rules": [], "examples": []}
        if config in ("B", "C"):
            cached["retrieval"]["rules"] = core.retrieve_rules(transcript, 4)
        if config == "C":
            cached["retrieval"]["examples"] = core.retrieve_examples(transcript, 3)
        return cached
    if _live_synthesis_calls >= MAX_SYNTHESIS_LIVE_CALLS:
        raise RuntimeError(f"Synthesis live-call cap reached ({MAX_SYNTHESIS_LIVE_CALLS})")
    old_model = core.GEMINI_MODEL
    core.GEMINI_MODEL = model
    try:
        result = core.gemini_extract(transcript, config)
    finally:
        core.GEMINI_MODEL = old_model
    _live_synthesis_calls += 1
    result["cache_hit"] = False
    to_cache = dict(result)
    to_cache["retrieval"] = {"rules": [], "examples": []}
    _CACHE["synthesis"][cache_key] = to_cache
    _save_cache()
    return result


def run_ablation(configs=("A", "B", "C")):
    results = {}
    rows = []
    for cfg in configs:
        results[cfg] = {}
        for case in EVAL_CASES:
            result = gemini_extract(case["transcript"], cfg)
            results[cfg][case["id"]] = result
            score = core.score_case(case, result)
            score["config"] = cfg
            score["cache_hit"] = bool(result.get("cache_hit", False))
            rows.append(score)
    return results, pd.DataFrame(rows)


def gemini_judge(case, candidate):
    global _live_judge_calls
    model = GEMINI_JUDGE_MODEL
    payload = {"transcript": case["transcript"], "gold_reference": case["gold"], "candidate": candidate}
    cache_key = _key({"kind": "judge", "model": model, "payload": payload})
    if cache_key in _CACHE["judge"]:
        cached = dict(_CACHE["judge"][cache_key])
        cached["cache_hit"] = True
        return cached
    if _live_judge_calls >= MAX_JUDGE_LIVE_CALLS:
        raise RuntimeError(f"Judge live-call cap reached ({MAX_JUDGE_LIVE_CALLS})")
    old_model = core.GEMINI_JUDGE_MODEL
    core.GEMINI_JUDGE_MODEL = model
    try:
        result = core.gemini_judge(case, candidate)
    finally:
        core.GEMINI_JUDGE_MODEL = old_model
    _live_judge_calls += 1
    result["cache_hit"] = False
    _CACHE["judge"][cache_key] = {k: v for k, v in result.items() if k != "cache_hit"}
    _save_cache()
    return result


def run_judge(ablation_results, configs=("A", "B", "C")):
    rows = []
    case_map = {x["id"]: x for x in EVAL_CASES}
    for cfg in configs:
        for case_id, result in ablation_results[cfg].items():
            judged = gemini_judge(case_map[case_id], result["brief"])
            rows.append({"config": cfg, "case_id": case_id, **judged})
    return pd.DataFrame(rows)
