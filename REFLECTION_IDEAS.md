# Reflection ideas for Mingxi Wang

Assistant suggestions, not a personal reflection or completed experiments.

## Assistant idea notes — not the submitted reflection

- Workflow to explain in your words: question -> tokenize or encode -> score six passages -> select top k -> supply only selected evidence to an answer conversation -> check each cited claim and identify missing information. Retrieval supplies context; it does not change model weights.
- Task 1 finding: Q1 selects A1 and A2. A1 scores 3 from `00`, `graduate`, and `trained`. The accidental `00` overlap between clock times illustrates that keyword overlap is not an understanding of time.
- Task 2 finding: the six passages form a `(6, 384)` matrix and the question a `(384,)` vector. Lengths are approximately 1, and all 384 coordinates contribute to similarity. One displayed coordinate cannot identify meaning.
- Task 3 finding: embeddings are not always more complete. Q1 keyword retrieval covers 2/2 required passages, while embeddings cover only 1/2 at k=1, 2, and 3. Q3 does retrieve T1 despite the qualification/renewal paraphrase (embedding score 0.74202764); keyword retrieval also finds it.
- Task 4 finding: Q4 correctly requires abstention because wavelength is unspecified. A positive similarity score is not proof of answerability. The original project-chat Q1 answer also named unseen A1; the correction shows that even a true claim must respect the supplied-evidence boundary.
- Possible next test: run Q1 at k=4, where the existing ranking places A1 fourth, and evaluate evidence coverage versus extra context. This additional k=4 experiment has not been run. Alternatively, compare a combined keyword/embedding candidate set with either method alone; this hybrid experiment has not been run either.

Choose the points you understand and find most informative. A concise reflection can explain the workflow, discuss one observed limitation, and propose one test; it does not need to cover every suggested finding.
