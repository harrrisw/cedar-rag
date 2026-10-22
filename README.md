# Cedar Lab RAG

**Mingxi Wang | Individual submission**

A classroom retrieval-augmented generation workflow over six fictional Cedar Lab passages. It compares keyword matching with real CPU embeddings, inspects retrieved evidence, and generates cited answers in fresh, tool-disabled conversations. The fictional rules are not operational laboratory guidance.

Repository: [harrrisw/cedar-rag](https://github.com/harrrisw/cedar-rag) (private). Mingxi Wang's [overall audit](evidence/student-audit.md) accepts the accuracy with reservations about reasoning quality. Final course submission still requires the instructor-access check; the recorded decisions are summarized in the [audit handoff](AUDIT_HANDOFF.md).

## Run the project

Tested with Python 3.13.4 on Windows. In PowerShell, from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --no-compile -r requirements-lock.txt
$env:HF_HOME = Join-Path (Get-Location) '.cache\huggingface'

.\.venv\Scripts\python.exe retriever.py keyword 'May a trained graduate student operate the laser alone at 19:00?' -k 2
.\.venv\Scripts\python.exe retriever.py embedding 'May a trained graduate student operate the laser alone at 19:00?' -k 2 --inspect
.\.venv\Scripts\python.exe run_assignment.py
```

The first model download needs internet access; no API key or GPU is needed. After the model is cached, set `$env:HF_HUB_OFFLINE = '1'` to run offline. The keyword command also works with system Python and no third-party packages. `requirements.txt` lists the two direct dependencies; `requirements-lock.txt` records the installed environment.

Model: `sentence-transformers/all-MiniLM-L6-v2`, downloaded snapshot `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. Recorded versions: sentence-transformers **6.1.0**, numpy **2.5.4**, torch **2.14.1**, transformers **5.20.2**. See [environment evidence](evidence/environment.txt) for the full list.

## Results

| Question | Keyword top 2 | Embedding top 2 | Evidence assessment |
| --- | --- | --- | --- |
| Q1: operate alone at 19:00? | A1, A2 | A2, T1 | Keyword covers 2/2 required passages; embeddings cover 1/2 and omit access hours. |
| Q2: laser without another person? | A2, B1 | A2, T1 | Both retrieve A2: coverage 1/1. |
| Q3: refresh laser qualification? | T1, A2 | T1, B1 | Both retrieve T1: coverage 1/1; embeddings score it 0.74202764. |
| Q4: laser wavelength? | A2, B1 | T1, A2 | No source specifies wavelength. Similar candidates do not establish an answer. |

The exact scores and evidence judgments are in [results.csv](results.csv), prepared with Codex assistance. Keyword counts and cosine similarities use different scales and must not be compared numerically across methods.

For Q1, embeddings select A2 at k=1, add T1 at k=2, and add B1 at k=3. Coverage remains 1/2 because A1 ranks fourth (0.37424892). T1 adds training/current-record conditions and B1 adds booking information; neither supplies the missing access-hours window. The proposed k=4 and hybrid experiments in the reflection have not been run.

## How retrieval works

Each blank-line-separated paragraph in `docs/` is one chunk. Its label and filename are metadata; only the paragraph text is searched or encoded.

- **Load:** `load_chunks()`, `retriever.py` lines 27-37, reads the three files and validates six unique labels.
- **Score keywords:** `words()` and `keyword_rank()`, lines 40-46, lowercase text, extract alphanumeric words, remove exactly the assigned stopwords, and count distinct shared query words. Repeating a word adds no points; there is no stemming or synonym expansion.
- **Rank keywords:** line 47 sorts by descending score, then ascending chunk ID. Selection keeps up to k positive results. Q1/A1 scores 3 from `00`, `graduate`, and `trained`; the shared clock token `00` does not mean the code understands time.
- **Encode:** line 76 uses `encode_document()` for passages; line 100 uses `encode_query()` for the question. Both normalize embeddings and return numpy arrays. The assignment runner encodes the documents once and reuses them across questions. These role-specific methods have the same underlying encoding behavior for this model.
- **Score embeddings:** line 103 computes a dot product across all matching coordinates. Line 106 ranks descending with an ID tie-break, then takes the first k without a relevance threshold. A cosine calculation using vector lengths cross-checks the scores.

The document matrix is `(6, 384)` and a question vector is `(384,)`. Compatible dimensions and the same encoding space allow matching coordinates to be compared. Near-unit vector lengths make dot products equal cosine similarity within numerical tolerance. All 384 coordinates contribute, although only 12 are displayed. Among displayed values, T1's fifth coordinate is the minimum (-0.1167) and its twelfth the maximum (0.1357), counting from 1. Neither individually labels the passage's meaning.

The model returns float32 coordinates. The product inspection accumulates them in float64, so final digits can differ slightly from the ranking dot product; agreement is checked within tolerance. Calculations use unrounded model output and round only for display.

Retrieval selects candidate evidence. A separate answer conversation turns the selected passages into a cited answer. This changes the context supplied to the generator, not its learned weights. A citation is accepted only if its passage supports the specific claim; missing evidence requires an explicit acknowledgment.

## Submission contents

| File or directory | Purpose |
| --- | --- |
| `docs/` | Six verbatim source passages across access, training, and booking files. |
| `retriever.py`, `run_assignment.py` | CLI retrieval and reproducible evidence generation. |
| `generate_answers.py` | Fresh, tool-disabled Codex answer generation outside the project directory; never overwrites earlier runs. |
| `results.csv` | All four comparisons, ranked scores, completeness judgments, observations. |
| `evidence/pre-run-prediction.md`, `keyword-q1.txt` | Initial Q1 evidence prediction and actual keyword run. |
| `evidence/embedding-inspection.txt` | Real vectors, dimensions, normalization, coordinate products, and similarity check. |
| `evidence/retrieval-runs.txt`, `k-experiment.txt` | Actual comparisons and Q1 k experiment. |
| `evidence/answer-handoff-q1.txt`, `answer-handoff-q4.txt` | Prescribed prompt, question, and only the selected passages for fresh answer conversations. |
| `evidence/answer-audit-q1.md`, `answer-audit-q4.md` | Preserved project-chat history plus actual fresh original answers, Q1's single correction, and proposed claim verdicts. |
| `evidence/answer-generation.md`, `answer-run-*/` | Fresh-thread provenance, exact inputs, unedited outputs, raw events, and manifests. |
| `evidence/answer-audit-q3.md` | Additional Q3 review requested during the project. |
| [reflections.md](reflections.md) | Mingxi Wang's supplied reflection, edited to the 150-word limit. |
| [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) | Completed artifacts and outstanding course requirements. |
| [AUDIT_HANDOFF.md](AUDIT_HANDOFF.md) | One place for the student's retrieval, claim-support, and reflection decisions, plus the final course entry. |
| [evidence/student-audit.md](evidence/student-audit.md) | Participant's original and edited audit, with an explicit clarification of evidence completeness. |

`run_assignment.py` regenerates retrieval output and handoffs. It preserves existing CSV judgments only when recorded evidence is unchanged; changed rows need a new review. Existing audit files are preserved and must be checked if the selected passages change. Output was generated locally, not borrowed.

The prescribed Q1/Q4 prompts have now been run in separate fresh Codex CLI conversations, each in an empty directory outside the project with command tools, browsing, apps, plugins, and delegation disabled. The original Q1 response omitted the missing access-hours window; it was preserved and corrected once using unchanged A2/T1 passages. Q4 abstained without inventing a wavelength. Separate thread IDs and zero tool executions are recorded in [answer-generation provenance](evidence/answer-generation.md). These machine checks and assistant prechecks do not replace the student's personal audit.

Saved answer output can be inspected without regenerating it. To reproduce original answers with an authenticated Codex CLI, run `.\.venv\Scripts\python.exe generate_answers.py`. To repeat the single-question correction, run `.\.venv\Scripts\python.exe generate_answers.py --questions q1 --instruction-file evidence/answer-revision-q1-instruction.txt`. New runs create unique evidence directories; generated wording can differ.

## Verification and remaining steps

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
```

The saved runs passed source-text, ranking, dimension, normalization, similarity, and CSV checks. The four regression tests protect existing reviews when evidence is regenerated. See [verification evidence](evidence/verification.txt).

**Before final course submission:** confirm instructor access to the private repository and submit its URL to the course sign-up sheet linked in the [handoff](AUDIT_HANDOFF.md). Answer generation, evidence preparation, repository publication, and recording the participant's supplied overall audit are complete. The audit does not change Q1's partial embedding coverage or Q4's absent wavelength evidence.
