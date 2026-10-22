# Submission checklist

Participant: **Mingxi Wang**, working individually. Partner role swapping is not applicable.

## Completed project artifacts

- [x] Six source paragraphs saved verbatim in the required three files, with separate ID and filename metadata.
- [x] Q1 evidence prediction recorded before the first retrieval (`evidence/pre-run-prediction.md`).
- [x] Standard-library keyword CLI: exact stopwords, distinct overlap, all scores and matches, deterministic ties, positive-only selection, and no-match behavior.
- [x] Real CPU MiniLM embeddings: document/query encoding, normalized vectors, shapes, coordinates, lengths, dot products, cosine check, and top-k selection without a threshold.
- [x] Actual Q1 vector inspection and Q1-Q4 comparison output, with model and installed package versions.
- [x] Four-row `results.csv` with ranked IDs/scores, required evidence, completeness judgments, and observations.
- [x] Actual Q1 k=1 and k=3 experiments, alongside k=2, with evidence coverage and interpretation in the README.
- [x] Original project-chat Q1/Q4 answers preserved with claim audits and revised responses; the Q1 unseen-source failure is retained.
- [x] Q1 and Q4 generated in distinct fresh, tool-disabled Codex conversations outside the project directory, with exact inputs and raw logs saved.
- [x] Fresh Q1's missing access-hours acknowledgment preserved as a failure; one revised instruction rerun with identical A2/T1 passages. Q4 correctly abstains in the assistant precheck.
- [x] Extra Q3 answer audit requested by the participant.
- [x] Participant's supplied reflection edited for clarity and the 150-word limit (`reflections.md`). Proposed k=4 and hybrid tests remain explicitly unrun.
- [x] Runnable commands, plain-language code explanation, pinned installed dependencies, and regression tests.
- [x] No invented or borrowed embedding output. Cache, virtual environment, bytecode, scratch files, and generated archives are excluded from Git.
- [x] Private GitHub repository created and project history pushed to [harrrisw/cedar-rag](https://github.com/harrrisw/cedar-rag).
- [x] Actual course sign-up-sheet URL recovered from the assignment hyperlink, and the final course entry prepared in [AUDIT_HANDOFF.md](AUDIT_HANDOFF.md).

## Required before final course submission

- [x] Record the participant's overall audit, explicit revised-Q1 and Q4 judgments, and reservations about reasoning quality in [student-audit.md](evidence/student-audit.md), preserving the original wording. Detailed assistant claim checks remain separately attributed.
- [x] Incorporate the participant's evidence-sufficiency assessment without changing Q1's partial embedding coverage or Q4's absent answer. The participant-supplied reflection remains 141 words.
- [ ] Confirm instructor access to the private repository: an instructor invitation or authorization to make it public requires the participant's choice.
- [ ] After the audit, submit the prepared repository entry to the [course sign-up sheet](https://docs.google.com/spreadsheets/d/1ZewIG5udWWpk3Kdrab5yDbsWDV4gnH3liKobIAp7HG4/edit?usp=sharing). This final submission is deferred until approval; no course entry is claimed.

## Evidence checks to use during review

| Question | Required evidence | Keyword coverage | Embedding coverage at k=2 |
| --- | --- | --- | --- |
| Q1 | A1 and A2 | 2/2 | 1/2: A1 is missing |
| Q2 | A2 | 1/1 | 1/1 |
| Q3 | T1 | 1/1 | 1/1 |
| Q4 | Absent | Not applicable | Not applicable; nearest passages do not answer wavelength |

For Q1, the answer must retain the two-trained-people condition and acknowledge that the supplied A2/T1 passages do not specify an access-hours window. It must not name unseen A1 or assert that 19:00 is permitted. For Q4, the answer must identify the missing wavelength and provide no guessed value.

The saved assistant audits and CSV assessments document assisted work. The participant's reflection and overall audit are based on text supplied in chat and edited for clarity. Actual fresh answer-generation logs and GitHub publication exist. Instructor-access choice and final course submission remain; no new student calculation or claim-by-claim review beyond the supplied evaluation is invented.
