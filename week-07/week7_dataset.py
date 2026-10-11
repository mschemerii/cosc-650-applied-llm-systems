import pandas as pd

LABELS = ["decision", "action_item", "blocker", "follow_up_question", "context"]
SUBJECTS = ["renewals workflow", "AEO report", "sales automation", "training series", "customer dashboard"]
OWNERS = ["Michael", "Brittany", "Finance", "Product", "Customer Success"]

TRAIN_TEMPLATES = {
    "decision": [
        "We decided to use {o} for the {s}.",
        "The team approved {o} as owner of the {s}.",
        "We will keep the {s} human-reviewed by {o}.",
        "Final decision: {o} will lead the {s}.",
        "The selected direction is {o} for the {s}.",
        "We agreed the {s} will use {o}.",
        "The choice is to have {o} own the {s}.",
        "The group committed to {o} for the {s}.",
        "We are going forward with {o} on the {s}.",
        "The approved approach assigns the {s} to {o}.",
    ],
    "action_item": [
        "{o} should test the {s}.",
        "Please have {o} validate the {s}.",
        "{o} needs to update the {s}.",
        "Action item: {o} will document the {s} results.",
        "Have {o} review the {s} before Friday.",
        "{o} should confirm the {s} fields.",
        "Ask {o} to compare the {s} output.",
        "{o} needs to prepare the {s} demo.",
        "Please have {o} verify the {s} source.",
        "{o} will follow up on the {s}.",
    ],
    "blocker": [
        "The {s} cannot proceed because {o} access is missing.",
        "The {s} is blocked until {o} approves it.",
        "Work on the {s} is delayed by the {o} dependency.",
        "The remaining issue is missing {o} data for the {s}.",
        "We cannot finish the {s} while {o} access is unavailable.",
        "The {s} is waiting on {o}.",
        "Progress on the {s} is stopped by the {o} issue.",
        "The {s} cannot move forward until {o} responds.",
        "The {s} is held up because {o} has not confirmed access.",
        "The unresolved {o} dependency blocks the {s}.",
    ],
    "follow_up_question": [
        "Can {o} confirm the source for the {s}?",
        "Which metric should {o} use for the {s}?",
        "Does {o} have access to the {s}?",
        "Who should approve the {s} for {o}?",
        "What does {o} still need for the {s}?",
        "Is the {s} source authoritative for {o}?",
        "When can {o} review the {s}?",
        "Which dataset should drive the {s} for {o}?",
        "Can {o} confirm ownership of the {s}?",
        "How should {o} calculate the {s} metric?",
    ],
    "context": [
        "{o} discussed the {s} during the meeting.",
        "The team reviewed the {s} with {o}.",
        "{o} described the current {s} process.",
        "The meeting covered background on the {s} for {o}.",
        "{o} shared information about the {s}.",
        "The group compared options for the {s} with {o}.",
        "{o} summarized the history of the {s}.",
        "The team talked through the {s} with {o}.",
        "{o} presented the current state of the {s}.",
        "The discussion included the {s} and {o}.",
    ],
}

EVAL_STANDARD_TEMPLATES = {
    "decision": [
        "That settles it: {o} is the path forward for the {s}.",
        "No need to revisit options; {o} owns the {s}.",
    ],
    "action_item": [
        "Before next week, {o} needs to check the {s}.",
        "Someone from {o} should verify the {s}.",
    ],
    "blocker": [
        "Everything else is ready; the {s} still cannot proceed without {o}.",
        "The {s} is ready except for the unresolved {o} dependency.",
    ],
    "follow_up_question": [
        "We still need an answer from {o} about the {s}.",
        "It is unclear whether {o} can approve the {s}.",
    ],
    "context": [
        "One option discussed was involving {o} in the {s}.",
        "{o} mentioned the {s} as possible future work.",
    ],
}

CHALLENGE_ROWS = [
    {
        "id": "ev-dec-challenge",
        "text": "The open question was ownership of the AEO report. There is nothing left to answer now: Product is the owner.",
        "label": "decision",
        "directness": "implicit",
        "slice": "contrastive_challenge",
        "source": "synthetic",
    },
    {
        "id": "ev-act-challenge",
        "text": "There is no decision about the sales automation today; before next week Brittany still has to verify it.",
        "label": "action_item",
        "directness": "implicit",
        "slice": "contrastive_challenge",
        "source": "synthetic",
    },
    {
        "id": "ev-blo-challenge",
        "text": "Ownership of the renewals workflow is settled with Finance, but nothing can move until Finance access is available.",
        "label": "blocker",
        "directness": "implicit",
        "slice": "contrastive_challenge",
        "source": "synthetic",
    },
    {
        "id": "ev-fol-challenge",
        "text": "No one is blocked yet, but the team still does not know which customer-dashboard metric Customer Success should use.",
        "label": "follow_up_question",
        "directness": "implicit",
        "slice": "contrastive_challenge",
        "source": "synthetic",
    },
    {
        "id": "ev-con-challenge",
        "text": "Brittany walked through the decision another team had made on the training series; our group only reviewed that background.",
        "label": "context",
        "directness": "implicit",
        "slice": "contrastive_challenge",
        "source": "synthetic",
    },
]


def build_dataset():
    train_rows = []
    for label in LABELS:
        for template_index, template in enumerate(TRAIN_TEMPLATES[label]):
            for subject_index, subject in enumerate(SUBJECTS):
                owner = OWNERS[(template_index + subject_index) % len(OWNERS)]
                train_rows.append({
                    "id": f"tr-{label[:3]}-{template_index:02d}-{subject_index:02d}",
                    "text": template.format(o=owner, s=subject),
                    "label": label,
                    "directness": "explicit" if template_index < 5 else "implicit",
                    "slice": "standard",
                    "source": "synthetic",
                })

    eval_rows = []
    for label in LABELS:
        made = 0
        for template_index, template in enumerate(EVAL_STANDARD_TEMPLATES[label]):
            for subject_index, subject in enumerate(SUBJECTS):
                if made >= 9:
                    break
                owner = OWNERS[(template_index + 2 * subject_index) % len(OWNERS)]
                eval_rows.append({
                    "id": f"ev-{label[:3]}-{template_index:02d}-{subject_index:02d}",
                    "text": template.format(o=owner, s=subject),
                    "label": label,
                    "directness": "implicit" if template_index else "explicit",
                    "slice": "standard",
                    "source": "synthetic",
                })
                made += 1
            if made >= 9:
                break

    train_df = pd.DataFrame(train_rows)
    eval_df = pd.concat([pd.DataFrame(eval_rows), pd.DataFrame(CHALLENGE_ROWS)], ignore_index=True)

    assert len(train_df) == 250
    assert len(eval_df) == 50
    assert (train_df["label"].value_counts() == 50).all()
    assert (eval_df["label"].value_counts() == 10).all()
    assert (eval_df["slice"] == "contrastive_challenge").sum() == 5

    return train_df, eval_df


if __name__ == "__main__":
    train_df, eval_df = build_dataset()
    train_df.to_csv("week7_train.csv", index=False)
    eval_df.to_csv("week7_eval.csv", index=False)
    print(f"training rows: {len(train_df)}")
    print(f"evaluation rows: {len(eval_df)}")
