"""Protect completed reviews when regenerating retrieval evidence."""
import csv
import unittest
from uuid import uuid4

from run_assignment import ROOT, save_results


class ResultsPreservationTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".tmp"
        scratch.mkdir(exist_ok=True)
        self.path = scratch / f"results-test-{uuid4().hex}.csv"
        self.addCleanup(lambda: self.path.unlink(missing_ok=True))
        self.row = {
            "question_id": "Q1", "keyword_top_ids": "A1;A2", "keyword_scores": "3;2",
            "embedding_top_ids": "A2;T1", "embedding_scores": "0.68644565;0.58195293",
            "required_ids": "A1;A2", "keyword_evidence_complete": "",
            "embedding_evidence_complete": "", "observation": "",
        }

    def read(self):
        with self.path.open(newline="", encoding="utf-8") as stream:
            return next(csv.DictReader(stream))

    def reviewed(self):
        return {**self.row, "keyword_evidence_complete": "true",
                "embedding_evidence_complete": "false", "observation": "Review: partial evidence."}

    def test_new_results_leave_judgments_blank(self):
        save_results([self.row.copy()], self.path)
        self.assertEqual(self.read(), self.row)

    def test_identical_evidence_preserves_completed_review(self):
        save_results([self.reviewed()], self.path)
        save_results([self.row.copy()], self.path)
        self.assertEqual(self.read(), self.reviewed())

    def test_changed_selection_requires_new_review(self):
        save_results([self.reviewed()], self.path)
        changed = {**self.row, "embedding_top_ids": "A2;A1"}
        save_results([changed], self.path)
        self.assertEqual(self.read(), changed)

    def test_changed_score_requires_new_review(self):
        save_results([self.reviewed()], self.path)
        changed = {**self.row, "embedding_scores": "0.70000000;0.58195293"}
        save_results([changed], self.path)
        self.assertEqual(self.read(), changed)


if __name__ == "__main__":
    unittest.main()
