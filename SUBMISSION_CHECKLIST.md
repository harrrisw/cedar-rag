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
- [x] Extra Q3 answer audit requested by the participant.
- [x] Participant's supplied reflection edited for clarity and the 150-word limit (`reflections.md`). Proposed k=4 and hybrid tests remain explicitly unrun.
- [x] Runnable commands, plain-language code explanation, pinned installed dependencies, and regression tests.
- [x] No invented or borrowed embedding output. Cache, virtual environment, bytecode, scratch files, and generated archives are excluded from Git.

## Required before final course submission

- [ ] Generate Q1 and Q4 in two fresh conversations without project file access. Paste only the corresponding `evidence/answer-handoff-*.txt` contents. Existing project-chat answers do not satisfy this isolation requirement.
- [ ] Append each unedited fresh response to its existing audit file; personally check every factual claim, citation, and missing-information statement. If an answer fails, preserve it, revise the instruction once, rerun with the same passages, and record whether it helped.
- [ ] Confirm the completeness judgments in `results.csv` and the final wording of the personal reflection.
- [ ] Choose the GitHub repository destination and visibility, then push the repository. Authentication was verified for `harrrisw`; no remote is configured. The latest authenticated lookup could not resolve `harrrisw/cedar-rag`.
- [ ] Submit the published repository URL to the course sign-up sheet. The sheet URL has not been supplied.

## Evidence checks to use during review

| Question | Required evidence | Keyword coverage | Embedding coverage at k=2 |
| --- | --- | --- | --- |
| Q1 | A1 and A2 | 2/2 | 1/2: A1 is missing |
| Q2 | A2 | 1/1 | 1/1 |
| Q3 | T1 | 1/1 | 1/1 |
| Q4 | Absent | Not applicable | Not applicable; nearest passages do not answer wavelength |

For Q1, the answer must retain the two-trained-people condition and acknowledge that the supplied A2/T1 passages do not specify an access-hours window. It must not name unseen A1 or assert that 19:00 is permitted. For Q4, the answer must identify the missing wavelength and provide no guessed value.

The saved assistant audits and CSV assessments document assisted work. The participant's reflection is based on the text supplied in chat and edited for length and clarity. No independent answer run, personal claim audit, publication, or course submission is marked complete without its actual result.
