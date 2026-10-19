# Assignment requirements audit

Reviewed against `PS05 and Lesson 10 — RAG Systems.docx` on October 19, 2026. This project is technically runnable, but it is **not yet ready for final submission**. No student reflection, independent human judgment, isolated answer run, or remote submission is claimed without actual evidence.

## Setup and source preparation

| Requirement | Status and evidence |
| --- | --- |
| A cedar-rag working directory and local Git repository | Complete; this workspace is the repository. |
| Python, local virtual environment, sentence-transformers and numpy installed | Complete; Python 3.13.4, `.venv`, `requirements-lock.txt`, `evidence/environment.txt`. |
| Real all-MiniLM-L6-v2 CPU model loads; installed versions recorded | Complete; actual output in `evidence/embedding-inspection.txt`, package versions and model snapshot in README. |
| Use a Codex project capable of files and Python | The current project workspace has been used to create files and execute Python; any separate course-specific app setup should be confirmed by the participant. |
| Exactly six verbatim paragraphs in the three required files | Verified against DOCX; `docs/access.txt`, `docs/training.txt`, `docs/booking.txt`. IDs and filenames are separate metadata. |
| Partner agreement and halfway role swap if working in pairs | Pending applicability: participant must identify solo/partner status and confirm any actual role swap. No partner work is invented. |

## Task 1: keyword baseline

| Requirement | Status and evidence |
| --- | --- |
| Identify Q1's needed passages before retrieval | Assistant prediction recorded before the first retrieval in `evidence/pre-run-prediction.md`; participant should confirm their own reasoning. |
| Standard-library CLI with a question and k, default k=2 | Complete; `retriever.py keyword ... -k 2`. |
| Lowercase alphanumeric words, exactly the 17 specified stopwords, distinct overlap | Complete; `words()` and `keyword_rank()`. No stemming, synonyms, or embeddings in keyword mode. |
| Descending scores, ascending IDs for ties; print all six scores and matched words | Complete; actual Q1 output in `evidence/keyword-q1.txt`. |
| At most k positive-scoring passages, full metadata and text; no-match message | Complete; selected IDs/filenames/full texts printed; no-match behavior checked. |
| Actual Q1 run, plain-language explanation, code line references | Complete; saved output and README. Q1 selects A1 and A2. |
| Independently check a score and repeated-word rule | Assistant checks recorded: Q1/A1 shares `00`, `graduate`, `trained`, score 3. Student's independent check remains required. |

## Task 2: visible embeddings

| Requirement | Status and evidence |
| --- | --- |
| Real sentence-transformers/all-MiniLM-L6-v2 and numpy on CPU | Complete; downloaded model and actual run, not fabricated or borrowed. |
| encode_document/encode_query, normalized numpy vectors, same model, text only | Complete; `EmbeddingRetriever` in `retriever.py`. |
| Documents encoded once per comparison run and reused | Complete; one retriever instance in `run_assignment.py`. |
| Model, versions, actual shapes, first 12 coordinates to four decimals | Complete; `evidence/embedding-inspection.txt`, `(6, 384)` documents, `(384,)` question. |
| Vector lengths near 1; use all 384 coordinates without semantic labels | Complete; runtime checks, printed lengths and explanation. |
| Normalized dot product, all six scores sorted, ID tie-break; top k without threshold | Complete; implementation and saved actual rankings. |
| Q1 top passage's first 12 products and subtotal, remaining subtotal, full similarity | Complete; Q1/A2 inspection output. Calculations use unrounded model coordinates. |
| Direct cosine agrees within tolerance | Complete; runtime check; float32 ranking versus float64 inspection accumulation is explained. |
| Explain compatible dimensions, ranking/selection, displayed extremes, roles and weights | Complete in README and assistant review notes; student should be able to explain independently. |

## Task 3: comparison and experiment

| Requirement | Status and evidence |
| --- | --- |
| Run Q1–Q4 with both methods at k=2 and save actual output | Complete; `evidence/retrieval-runs.txt`. |
| results.csv has exactly the requested columns and four ranked rows | Complete; original blank judgment fields have now been filled with explicitly labeled assistant judgments at the user's request. |
| Judge Q1 with both A1 and A2 required | Complete assistant judgment: keyword 2/2, embeddings 1/2. Student confirmation pending. |
| Identify Q2/Q3 paraphrase behavior with actual IDs and scores | Complete; CSV observations include A2=0.58519334 for Q2 and T1=0.74202764 for Q3; both methods cover each required passage. |
| Q4 required_ids=absent; nearest candidates are not successful evidence | Complete; both evidence-complete fields are false and observations explain why. Correct abstention is checked separately. |
| Rerun Q1 embeddings at k=1 and k=3; record effects and required coverage | Complete; `evidence/k-experiment.txt`. Coverage stays 1/2 at k=1, 2, 3; added T1/B1 do not restore A1. |
| Use small coverage measure appropriately, no Q4 ratio or forced winner | Complete in CSV, README, and review notes. |

## Task 4: answers and audits

| Requirement | Status and evidence |
| --- | --- |
| Prepare only the question, k=2 selected passages, and prescribed answer prompt | Complete; `evidence/answer-handoff-q1.txt` and `answer-handoff-q4.txt`. |
| Actually generate Q1 and Q4 in separate fresh conversations without project access | **Pending.** This project conversation has seen the corpus; its answers do not meet that isolation requirement. Paste each handoff into its own fresh conversation and append the unedited output to its audit file. |
| Preserve originals, check citations and missing conditions; record failures and revisions | Assistant audits complete in `evidence/answer-audit-q1.md` and `answer-audit-q4.md`. Q1 preserves and fixes an unseen-source reference. Q4 preserves correct abstention and a citation-clarity revision. These do not replace isolated runs. |
| Student personally audits every claim; reruns once if an actual isolated answer fails | **Pending human review and the isolated outputs.** No failed isolated response or student review is invented. |
| Extra Q3 answer review requested in chat | Complete; `evidence/answer-audit-q3.md`. T1 supports renewal every 12 months. |

## Submission and individual work

| Requirement | Status and evidence |
| --- | --- |
| Source files, retriever code, reproducible commands and package/model versions | Complete; README, requirements files, docs and scripts. |
| Evidence folder includes vectors, comparison, k experiment, two answer audits | Files exist and assistant audits are populated; isolated answer outputs and independent review remain pending. |
| Partner/participant names in README | **Pending actual names and solo/partner status.** Git account identity is not assumed to be the participant name. |
| Individual reflection no longer than 150 words per participant | **Pending participant writing** in `reflections.md`; the handout explicitly says not to ask Codex to write the personal explanation. |
| Source labels for borrowed output | Not applicable: recorded retrieval output was generated locally. |
| Push to the participant's GitHub repository of the same name | **Pending repository destination/creation.** Network-enabled authentication succeeds for `harrrisw`; no remote is configured. `harrrisw/cedar-rag` could not be resolved by the authenticated read-only check. |
| Submit repository link to the course sign-up sheet | **Pending sheet URL and the published repository.** No course submission has occurred. |

## Remaining inputs

1. Participant name(s), solo/partner status, and actual role-swap details if applicable.
2. Your own reflection, at most 150 words per participant, and confirmation or corrections to the assistant judgments.
3. Actual fresh-conversation Q1 and Q4 outputs and your claim audits.
4. GitHub destination or new repository visibility, and the course sign-up-sheet URL. Authentication is verified working.

The rubric allocates 3 points to visible embeddings, 3 to retrieval comparison, 2 to grounded answer audits, and 2 to reproducibility/explanation. Technical artifacts support assessment, but full marks are not claimed while required independent work and submission steps are pending.

## Verification of this completion pass

The real CPU assignment run was repeated successfully using the local model cache with networking disabled. The same selected IDs and scores were reproduced, and all four populated CSV judgments were preserved. Source paragraphs were compared again with the DOCX; metadata, stopwords, distinct overlap, tied-score order, and the manual Q1/A1 score were checked. `pip check` passed. Four regression tests passed for preserving reviews when evidence is unchanged and requiring new review when rankings or scores change. Original answer excerpts and supporting quotations were checked against the supplied passages.
