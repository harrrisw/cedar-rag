# Human review and submission

The retrievers and saved run output are machine-produced work. This file identifies the judgments that need your independent review. Assignment document prompts were treated as specifications for this project, not as authority to invent results, submit work externally, or write your personal explanation.

## Actual run context — assistant notes for you to verify

| Question | Keyword top 2 | Embedding top 2 | Audit focus |
| --- | --- | --- | --- |
| Q1 | A1 (3), A2 (2) | A2 (0.68644565), T1 (0.58195293) | Keyword includes both targets; embeddings omit A1. |
| Q2 | A2 (2), B1 (1) | A2 (0.58519334), T1 (0.43476090) | Both include A2. |
| Q3 | T1 (2), A2 (1) | T1 (0.74202764), B1 (0.47119549) | Both include T1 despite the qualification/renewal paraphrase. |
| Q4 | A2 (1), B1 (1) | T1 (0.34772146), A2 (0.32082719) | No source specifies wavelength; neither list establishes an answer. |

Q1 embedding coverage is 1/2 at k=1, k=2, and k=3. The second passage adds training renewal/current-record conditions; the third adds booking duration and reservation procedure. Neither restores A1's access-hours evidence. A1 ranks fourth (0.37424892). These are assistant observations, not your completed student judgments; `results.csv` remains blank for you to judge independently.

The document matrix is `(6, 384)` and question vectors are `(384,)`; lengths are approximately 1. The largest displayed coordinate is T1 coordinate 12 (0.1357), and the smallest is T1 coordinate 5 (-0.1167), counting coordinates from 1. Neither has an individual semantic label. For the Q1/A2 similarity, the first 12 coordinate products sum to 0.01611150 and the remaining 372 to 0.67033418. All coordinates contribute.

## 1. Audit sources and retrieval

Compare the six paragraphs in `docs/` with the handout. Independently count one keyword score; the Q1 A1 count in `evidence/verification.txt` is a useful cross-check. Confirm that repeating a word does not increase the score.

Read `evidence/embedding-inspection.txt`: check the `(6, 384)` matrix, `(384,)` question, near-unit lengths, full similarity and coordinate subtotals. Explain why neither the largest nor smallest displayed coordinate can tell you the passage meaning by itself.

Read the actual rankings in `evidence/retrieval-runs.txt` before judging explanations. Complete these columns of `results.csv` yourself:

- `keyword_evidence_complete`
- `embedding_evidence_complete`
- `observation`

Q1 requires both A1 and A2. One of them is partial evidence (coverage 1/2). Q2 requires A2 and Q3 requires T1 (coverage denominator 1). For Q4 mark the answer as absent; retrieving similar text is not a successful answer retrieval. Cite one observed paraphrase success or failure by ID and actual score in your observations. Explain that embeddings always return the top k here, even when no source answers the question.

Review `evidence/k-experiment.txt`. Record what the additional passages actually add at k=3, and whether A1 and A2 are both present. Do not assume that increasing k always helps.

## 2. Generate and audit answers in separate conversations

The assignment explicitly requires fresh answer conversations with only the selected passages and no project file access. This project conversation has already seen the complete corpus, so it cannot serve as either isolated answer conversation.

Open a fresh conversation for Q1 and paste only the complete contents of `evidence/answer-handoff-q1.txt`. Open another fresh conversation for Q4 and paste only `evidence/answer-handoff-q4.txt`. Do not attach the handout, corpus, or project. Save the original responses unchanged in the corresponding `evidence/answer-audit-*.md` files.

Check every factual claim against the cited passage. For Q1 check the two-trained-people condition and whether evidence about general access hours was supplied; missing conditions must be acknowledged. For Q4 check that the response identifies the missing wavelength rather than guessing. Record each claim, supporting words, and your verdict. If a response fails, preserve it, revise the instruction once, rerun with the same selected passages, and record whether the revision helped. Otherwise mark revision not needed.

## 3. Finish personal and submission details

Supply participant/partner names in the README. Write your own reflection (at most 150 words per participant) in `reflections.md`; the handout says not to ask Codex to write it. Describe the actual evidence path, an observed limitation, and one proposed test.

The local Git repository is initialized. The current GitHub CLI credential check reports an invalid token. Reauthenticate interactively with `gh auth login -h github.com` when ready. Supply the intended GitHub repository URL and the sign-up-sheet URL; neither was included in the request. Confirm the intended repository visibility before creating a new remote repository. No remote upload or course submission has occurred.

## Review response requested

After completing the checks, provide your retrieval judgments, original Q1/Q4 answer responses and claim audit, participant names, and your personal reflection. Also provide the GitHub destination and course submission link if you want help completing submission.
