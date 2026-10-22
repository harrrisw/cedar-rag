# Cedar Lab RAG

**Mingxi Wang | Individual submission**

A teaching RAG workflow over six fictional Cedar Lab passages: prepare chunks, compare keyword and embedding retrieval, generate cited answers from selected evidence, and audit claims and missing information. These fictional rules are not operational laboratory guidance.

Repository: [harrrisw/cedar-rag](https://github.com/harrrisw/cedar-rag) (private). The participant's [audit](evidence/student-audit.md) accepts overall accuracy with reservations about reasoning quality. Instructor access and the final course entry are still outstanding; see the submission note below.

## Setup and run

Tested on Windows with **Python 3.13.4**. Run from the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --no-compile -r requirements-lock.txt
$env:HF_HOME = Join-Path (Get-Location) '.cache\huggingface'

.\.venv\Scripts\python.exe retriever.py keyword 'May a trained graduate student operate the laser alone at 19:00?' -k 2
.\.venv\Scripts\python.exe retriever.py embedding 'May a trained graduate student operate the laser alone at 19:00?' -k 2 --inspect
.\.venv\Scripts\python.exe run_assignment.py
```

The first model download requires internet access; embeddings need no API key or GPU. After caching, `$env:HF_HUB_OFFLINE = '1'` enables offline runs. Keyword retrieval uses only the standard library and also runs with system Python. `requirements.txt` lists direct dependencies; `requirements-lock.txt` pins the installed environment.

Model: **sentence-transformers/all-MiniLM-L6-v2**, CPU, downloaded snapshot `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. Recorded versions: **sentence-transformers 6.1.0**, **numpy 2.5.4**, **torch 2.14.1**, **transformers 5.20.2**.

## Findings

| Question | Keyword top 2 | Embedding top 2 | Required evidence assessment |
| --- | --- | --- | --- |
| Q1: operate alone at 19:00? | A1, A2 | A2, T1 | Needs A1 and A2: keyword coverage 2/2, embedding coverage 1/2. |
| Q2: laser without another person? | A2, B1 | A2, T1 | Needs A2: both methods cover 1/1. Embedding A2 scores 0.58519334. |
| Q3: refresh laser qualification? | T1, A2 | T1, B1 | Needs T1: both cover 1/1 despite the paraphrase. Embedding T1 scores 0.74202764. |
| Q4: laser wavelength? | A2, B1 | T1, A2 | Wavelength is absent. Neither method retrieves answer evidence; no coverage ratio applies. |

[results.csv](results.csv) records exact ranked IDs/scores, evidence completeness, and observations. Judgments were prepared with Codex assistance; the [participant audit](evidence/student-audit.md) records Mingxi Wang's supplied assessment separately. Keyword counts and cosine similarities use different scales and should not be compared numerically.

For Q1, embedding k=1 selects A2, k=2 adds T1, and k=3 adds B1. Coverage stays 1/2 because A1 ranks fourth (0.37424892). T1 adds training/current-record conditions; B1 adds booking duration and reservation procedure. Neither supplies access hours. The reflection's k=4 and hybrid retrieval proposals have not been run.

The revised Q1 answer retains the two-trained-people condition and explicitly acknowledges that the selected A2/T1 passages cannot establish access at 19:00. It does not assert that 19:00 is permitted. Q4 appropriately abstains. Similarity alone does not establish answerability.

## Code explanation

Each paragraph in `docs/` is one chunk. Its ID and filename are retained as metadata; only paragraph text is searched or encoded.

- **Load:** `load_chunks()` in `retriever.py`, lines 27-37, reads the three files and validates six unique labels.
- **Keyword score:** `words()` and `keyword_rank()`, lines 40-46, lowercase text, extract alphanumeric words, remove exactly the assigned 17 stopwords, and count distinct shared words. Repeated words add no points. There is no stemming or synonym expansion.
- **Keyword rank:** line 47 sorts by descending score and ascending ID for ties. Selection keeps up to k positive scores; an unmatched query prints `No matching passages.` Q1/A1 scores 3 from `00`, `graduate`, and `trained`. The clock token `00` is an accidental lexical match, not an understanding of time.
- **Encode:** line 76 calls `encode_document()` for passage texts; line 100 calls `encode_query()` for the question. Both use the same model with normalization and numpy output. For this model the two methods have the same underlying encoding behavior. The assignment runner encodes documents once and reuses them across questions.
- **Similarity and selection:** line 103 computes dot products across all matching coordinates; line 106 ranks descending with an ID tie-break. Embeddings always return the top k without a relevance threshold. Cosine computed using vector lengths is checked against the normalized dot product.

The document matrix is `(6, 384)` and each question vector `(384,)`. Matching dimensions and a compatible encoding space permit meaningful coordinate comparisons. Near-unit lengths make dot products equal cosine similarity within tolerance. Sorting six scores and taking the first k selects the passages.

All 384 coordinates contribute, though only 12 are displayed. Among displayed values, T1's fifth coordinate is the minimum (-0.1167) and twelfth the maximum (0.1357), counting from 1. Neither coordinate alone identifies meaning. The model returns float32 coordinates; the product inspection accumulates in float64, so final digits can differ slightly from the ranking score. Calculations use unrounded output; rounding is for display only.

Retrieval selects evidence; a language model writes the answer. Supplying retrieved context does not change the generator's learned weights. A citation is valid only when its passage supports the specific claim, and missing information must be acknowledged.

## Evidence and assignment rubric

| Criterion | Available points | Submission evidence |
| --- | --- | --- |
| Visible embedding process | 3 | [embedding-inspection.txt](evidence/embedding-inspection.txt): actual shapes, vectors, lengths, first-12 coordinate products and subtotal, remaining subtotal, full similarity, cosine check, model and versions. |
| Retrieval comparison | 3 | [retrieval-runs.txt](evidence/retrieval-runs.txt), [results.csv](results.csv), [k-experiment.txt](evidence/k-experiment.txt): all four questions, judgments, actual scores, required coverage and k effects. |
| Grounded answer audit | 2 | [Q1 audit](evidence/answer-audit-q1.md) and [Q4 audit](evidence/answer-audit-q4.md): actual answers, claim/citation checks, missing information, preserved failures and one Q1 correction; [participant audit](evidence/student-audit.md). |
| Reproducibility and explanation | 2 | Commands and explanation above, source files, retriever code, pinned requirements, and the participant's [141-word reflection](reflections.md). |

Additional evidence is limited to the [pre-run Q1 prediction](evidence/pre-run-prediction.md), [initial keyword output](evidence/keyword-q1.txt), exact original [Q1](evidence/answer-handoff-q1.txt)/[Q4](evidence/answer-handoff-q4.txt) answer inputs, the [single Q1 instruction revision](evidence/answer-revision-q1-instruction.txt), and [consolidated answer provenance](evidence/answer-provenance.json). No embedding output was fabricated or borrowed. Available rubric points are not a claimed grade.

The actual Q1 and Q4 prompts ran in distinct fresh Codex CLI conversations outside the project, with execution tools, browsing, apps, plugins, and delegation disabled. Original Q1 omitted the missing access-hours window; that failed answer and one actual correction with unchanged A2/T1 passages are preserved. Q4 abstained and required no correction. The provenance file consolidates exact inputs, unedited outputs, raw event objects, thread IDs, configuration, and text hashes; it records zero tool executions and the intentionally disabled code-mode host's fail-closed diagnostic. The earlier failed project-chat Q1 draft is also retained in its audit. Other drafts and setup logs have been removed.

To repeat answer generation, start separate fresh conversations without project access and paste only the corresponding handoff file. If Q1 fails, replace its instruction once using the saved revision while keeping the question/passages identical. Save the new responses without overwriting the original evidence. The supplied reflection and participant audit are edited user text; detailed assistant checks are attributed separately.

## Verification and submission

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
```

`run_assignment.py` regenerates retrieval output and handoff files. It preserves existing judgments only when the recorded question evidence is unchanged; changed rows need review. It leaves final answer audits and provenance untouched. The four regression tests protect this review-preservation behavior. The virtual environment, model cache, scratch files, bytecode, and export archive are ignored by Git.

Final checks on October 22, 2026: the offline CPU rerun reproduced the saved vectors, rankings, scores, and k experiment exactly; all six source texts matched the handout; CSV judgments, response provenance, failed-answer preservation, reflection length, and documentation links were verified. Four regression tests, the standard-library-only no-match command, Python compilation, and dependency checks passed.

**Final course steps:** give the instructor access to the private repository (or authorize public visibility), then submit **Mingxi Wang - https://github.com/harrrisw/cedar-rag - Individual** to the [course sign-up sheet](https://docs.google.com/spreadsheets/d/1ZewIG5udWWpk3Kdrab5yDbsWDV4gnH3liKobIAp7HG4/edit?usp=sharing). Neither an instructor invitation nor a course-sheet entry is claimed as completed.
