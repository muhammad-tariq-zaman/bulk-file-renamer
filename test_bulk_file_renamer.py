import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main


class TestRenamer(unittest.TestCase):
    def test_dry_run_makes_no_changes(self):
        with tempfile.TemporaryDirectory() as d:
            for n in ("a.txt", "b.txt"):
                open(os.path.join(d, n), "w").write("x")
            m = main.build_mapping(d, prefix="new_")
            self.assertEqual(m, {"a.txt": "new_a.txt", "b.txt": "new_b.txt"})
            self.assertEqual(sorted(os.listdir(d)), ["a.txt", "b.txt"])

    def test_apply_and_undo(self):
        with tempfile.TemporaryDirectory() as d:
            for n in ("a.txt", "b.txt"):
                open(os.path.join(d, n), "w").write("x")
            undo = os.path.join(d, "undo.json")
            main.apply_mapping(d, {"a.txt": "new_a.txt"}, undo)
            self.assertTrue(os.path.exists(os.path.join(d, "new_a.txt")))
            self.assertEqual(json.load(open(undo)), {"a.txt": "new_a.txt"})
            main.undo_rename(d, undo)
            self.assertTrue(os.path.exists(os.path.join(d, "a.txt")))

    def test_find_replace(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "report_old.txt"), "w").write("x")
            self.assertEqual(main.build_mapping(d, find="old", replace="new"),
                             {"report_old.txt": "report_new.txt"})


if __name__ == "__main__":
    unittest.main()
