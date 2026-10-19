# Cedar Lab RAG assignment

Teaching workflow over six fictional classroom passages. This is not operational laboratory guidance. Participant/partner names: **pending human input**. Personal reflections belong in `reflections.md` and must be written by the participants.

## Setup and run (PowerShell)

Python 3.13.4 was found on this machine. A local `.venv` is used; the model runs on CPU without a model API key. Initial installation and model download require internet access.

Model: `sentence-transformers/all-MiniLM-L6-v2`, downloaded snapshot `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. Installed versions: `sentence-transformers==6.1.0`, `numpy==2.5.4`, `torch==2.14.1`, `transformers==5.20.2`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --no-compile -r requirements-lock.txt
$env:HF_HOME = Join-Path (Get-Location) '.cache\huggingface'
.\.venv\Scripts\python.exe retriever.py keyword 'May a trained graduate student operate the laser alone at 19:00?' -k 2
.\.venv\Scripts\python.exe retriever.py embedding 'May a trained graduate student operate the laser alone at 19:00?' -k 2 --inspect
.\.venv\Scripts\python.exe run_assignment.py
```

Use `requirements.txt` for an unpinned initial installation; `requirements-lock.txt` records the actual installed environment after a successful assignment run. `evidence/environment.txt` and the embedding output record exact versions. The keyword command also works with system Python and no third-party packages.

`run_assignment.py` encodes documents once and reuses that matrix for Q1–Q4 and the k experiment. It overwrites run evidence but preserves existing CSV judgments when all recorded evidence fields for that question are unchanged. New or changed rows have blank judgment fields for review. Existing answer audit files are preserved; if a rerun changes selected passages, their old audits must be reviewed against the new evidence.

## What the code does

`retriever.py` loads the three text files, splits on blank lines, and separates each ID from its paragraph. IDs and filenames remain metadata. Only paragraph text is searched or encoded.

- Loading: `load_chunks()`, lines 27–37.
- Keyword scoring: `words()` and `keyword_rank()`, lines 40–46. Words become sets, so repetitions do not add points. The exact specified stopword list is removed from both query and text. Each score counts the intersection of those sets.
- Keyword ranking: line 47 sorts by negative score, then chunk ID. Selection keeps up to k positive scores. No stemming or synonym expansion is used.
- Document encoding: `EmbeddingRetriever.__init__()`, especially line 76. `encode_document()` maps each of six passages to 384 coordinates and normalizes each vector.
- Question encoding: line 100 uses `encode_query()` with the same model. For this model, these role-specific methods use the same underlying encoding behavior.
- Similarity: line 103 multiplies matching coordinates and sums them. Line 106 sorts all six similarities, using ID to break ties. The first k records are returned without a relevance threshold.

The document matrix has shape `(6, 384)`; a question vector has shape `(384,)`. The dimensions and encoding space must agree to compare matching coordinates meaningfully. Sorting followed by taking the first k records turns six similarities into two selected passages.

The first 12 displayed coordinates are only a view into each vector. All 384 contribute to ranking; a single large or small coordinate cannot identify the passage's meaning. The inspection file includes lengths, a coordinate-product subtotal, the remaining-coordinate subtotal, and a direct-cosine cross-check. Calculations use unrounded model output; rounding is for display only.

The model returns float32 coordinates. The inspection accumulates their products in float64, so its final digits can differ slightly from the float32 ranking dot product; the script checks that they agree within tolerance.

The pretrained embedding model selects candidate evidence. A separate language model conversation writes the answer from those passages. This workflow supplies context without changing the generator's learned weights.

## Evidence and human review

- `evidence/pre-run-prediction.md`: Q1 evidence prediction made before retrieval.
- `evidence/keyword-q1.txt`: actual baseline output.
- `evidence/embedding-inspection.txt`: real model vectors and similarity calculation.
- `evidence/retrieval-runs.txt`: all four questions through both methods, k=2.
- `results.csv`: selected IDs and scores in rank order, with assistant evidence-completeness judgments and observations awaiting your independent review. Q4 is false for both methods because the answer is absent; successful abstention is a separate answer-audit result.
- `evidence/k-experiment.txt`: actual Q1 selections and required coverage for k=1, 2, 3.
- `evidence/answer-handoff-q1.txt` and `answer-handoff-q4.txt`: paste each into a separate fresh conversation with no project file access. Each contains only the assignment's answer instruction, question, and selected passages.
- `evidence/answer-audit-q1.md` and `answer-audit-q4.md`: original project-chat answers, revisions, and assistant claim audits. Q1 records a correction for referencing an unseen chunk. The required isolated answer runs and human audit remain pending. Append those actual outputs without overwriting the preserved responses.
- `evidence/answer-audit-q3.md`: additional answer and citation review requested by the user.
- `REQUIREMENTS_AUDIT.md`: requirement-by-requirement completion status and remaining submission gaps.
- `HUMAN_REVIEW.md`: review sequence and outstanding submission items.

Do not treat an embedding score as evidence that a passage answers the question, and do not compare raw keyword scores numerically with cosine scores. Q4's answer is absent from the corpus even though the embedding retriever always returns the top k passages. Q1 coverage counts both A1 and A2, even if A2 alone could support a yes/no decision.

The saved rankings show keyword coverage of 2/2 for Q1 versus embedding coverage of 1/2. Both methods cover Q2 and Q3 (1/1 each). At k=1, 2, and 3, Q1 embedding coverage stays 1/2: T1 adds training conditions and B1 adds booking information, while A1 remains fourth. The minimum and maximum displayed coordinates are T1's fifth (-0.1167) and twelfth (0.1357), counting from 1; neither coordinate individually labels meaning.

Verify CSV review preservation with `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`. Dependency consistency can be checked with `.\.venv\Scripts\python.exe -m pip check`.

## GitHub submission

The local repository is initialized. Review artifacts and finish human-only items before submission. Then create or identify your GitHub repository named `cedar-rag`, commit the source and evidence, and push. `.gitignore` excludes the virtual environment, temporary files, model cache, and bytecode. A GitHub destination and the sign-up-sheet URL were not supplied. No submission is claimed until the push and sign-up-sheet entry actually succeed.

A network-enabled GitHub authentication check succeeded for `harrrisw` during the completion audit. No remote is configured, and an authenticated check could not resolve `harrrisw/cedar-rag`; repository creation/destination and visibility remain to be confirmed.
