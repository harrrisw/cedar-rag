# Audit handoff for Mingxi Wang

All preparatory work is complete: the code and real retrieval evidence are saved, the 141-word reflection is recorded, the two original answer prompts were run in fresh conversations, the Q1 failure was preserved and retried once, and the project is published privately at [harrrisw/cedar-rag](https://github.com/harrrisw/cedar-rag).

Mingxi Wang's supplied audit is now recorded in [student-audit.md](evidence/student-audit.md), including the original wording, an edited version, and an accuracy clarification. The participant accepts the overall accuracy with reservations about logical connections and depth of understanding. Detailed numerical and claim checks below remain identified as assistant assessments rather than newly performed student calculations.

## 1. Confirm retrieval evidence judgments

Open [results.csv](results.csv) and the [actual retrieval output](evidence/retrieval-runs.txt).

| Question | Evidence to check | Proposed judgment |
| --- | --- | --- |
| Q1 | Needs both A1 and A2. Keywords return A1/A2; embeddings return A2/T1. | Keyword complete (2/2); embeddings partial (1/2). |
| Q2 | Needs A2. Both methods return it. | Both complete (1/1). |
| Q3 | Needs T1. Both methods return it; embedding T1 score is 0.74202764. | Both complete (1/1). |
| Q4 | No passage specifies wavelength; embedding T1 still scores 0.34772146. | Neither retrieves answer evidence; nearest passages are not an answer. |

Also confirm Q1/A1's keyword score by counting `00`, `graduate`, and `trained` once each. In the [k experiment](evidence/k-experiment.txt), check that adding T1 and then B1 never recovers A1: coverage stays 1/2 at k=1, 2, and 3.

**Participant decision recorded:** The evidence is sufficient for evaluating this project's scope. This does not change the per-question findings: Q1 embeddings remain partial and Q4 remains unanswerable from the sources. See the preserved audit and accuracy clarification in `evidence/student-audit.md`.

## 2. Personally audit the actual generated answers

Read [Q1's complete audit](evidence/answer-audit-q1.md), including its preserved original fresh response and single correction, and [Q4's complete audit](evidence/answer-audit-q4.md). The raw inputs, outputs, thread IDs, and event logs are indexed in [answer-generation provenance](evidence/answer-generation.md).

| Answer claim or omission | Words to inspect in the supplied evidence | Proposed verdict |
| --- | --- | --- |
| Q1: two trained people are required during operation. | A2: "two trained people to be present whenever the laser is operating" | Supported by A2. |
| Q1: training renews every 12 months; a current record is required. | T1 states both requirements explicitly. | Supported by T1. |
| Original fresh Q1 answer omits the access-hours limitation. | Neither A2 nor T1 gives the general access-hours window. | Original incomplete for the requested time explanation; preserve the failure. |
| Revised Q1 answer says permission to enter at 19:00 cannot be established. | A2/T1 omit the access-hours window and individual training status. | Correct missing-information acknowledgment. |
| Q4 answer says neither supplied passage specifies wavelength. | Inspect the complete T1 and A2 passages; neither gives a wavelength. | Correct abstention; no numerical value is justified. |

For each claim, confirm that its cited passage supports it. Distinguish a conclusion about missing information from an explicit statement in a source. Check that the revised Q1 answer does not import unseen A1 or claim that 19:00 is within permitted access hours. The Q1 correction has already been run with the same passages; no additional answer-generation work is required unless your audit finds another issue.

**Participant Q1 decision recorded:** The revised answer provides a better explanation of the relationship between operation and time. Accuracy clarification: its improvement is the distinction between the supported operating condition and the missing access-hours window; permission to enter at 19:00 is not established.

**Participant Q4 decision recorded:** The requested evidence was not supplied. The participant's overall accuracy assessment is generally acceptable, with reservations about reasoning depth. The answer's abstention is consistent with the missing wavelength.

## 3. Confirm your reflection

Read [reflections.md](reflections.md). It is your supplied reflection, edited to **141 words**. Confirm that it represents your understanding and that k=4 and hybrid retrieval are proposals, not completed experiments.

**Reflection status:** The participant's supplied reflection is recorded and edited to 141 words. No new personal reflection was invented. The subsequent audit above is recorded separately rather than changing the reflection or increasing its word count.

## Access and final submission after your audit

The repository is **private**. Confirm whether the instructor already has access, provide the instructor's GitHub username for an invitation, or authorize public visibility. No visibility change or invitation has been assumed.

The actual [course sign-up sheet](https://docs.google.com/spreadsheets/d/1ZewIG5udWWpk3Kdrab5yDbsWDV4gnH3liKobIAp7HG4/edit?usp=sharing) was recovered from the handout's hyperlink. After your audit and instructor-access check, the entry to submit is:

- Participant: **Mingxi Wang**
- Repository: **https://github.com/harrrisw/cedar-rag**
- Working arrangement: **Individual**

The participant's overall audit is recorded with its reservations. Instructor access still needs a decision before final course submission. No invitation, public visibility change, or course entry is claimed.
