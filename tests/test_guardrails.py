import copy
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run_script(*arguments):
    return subprocess.run(
        [PYTHON, *arguments],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class CitationGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        self.source = self.temp_dir / "source.md"
        self.source.write_text(
            "# 1. Scope\nThis sentence is long enough to be verified as an exact source quotation.\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def artifact(self, quote, start=2, end=2, section="1"):
        path = self.temp_dir / "artifact.json"
        path.write_text(
            json.dumps(
                {
                    "citation": {
                        "section": section,
                        "quote": quote,
                        "source_line_start": start,
                        "source_line_end": end,
                    }
                }
            ),
            encoding="utf-8",
        )
        return path

    def test_accepts_exact_quote_at_declared_location(self):
        quote = "This sentence is long enough to be verified as an exact source quotation."
        result = run_script("scripts/validate_citations.py", str(self.artifact(quote)), str(self.source))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_fabricated_quote(self):
        quote = "This fabricated sentence does not occur in the canonical source document."
        result = run_script("scripts/validate_citations.py", str(self.artifact(quote)), str(self.source))
        self.assertNotEqual(result.returncode, 0)

    def test_rejects_short_quote(self):
        result = run_script("scripts/validate_citations.py", str(self.artifact("long enough maybe")), str(self.source))
        self.assertNotEqual(result.returncode, 0)

    def test_rejects_wrong_line_location(self):
        quote = "This sentence is long enough to be verified as an exact source quotation."
        result = run_script("scripts/validate_citations.py", str(self.artifact(quote, 1, 1)), str(self.source))
        self.assertNotEqual(result.returncode, 0)

    def test_rejects_wrong_section_heading(self):
        quote = "This sentence is long enough to be verified as an exact source quotation."
        result = run_script("scripts/validate_citations.py", str(self.artifact(quote, section="9")), str(self.source))
        self.assertNotEqual(result.returncode, 0)


class SchemaGateTests(unittest.TestCase):
    def test_rejects_source_value_without_citation(self):
        baseline_path = REPO_ROOT / "examples" / "projects" / "acme-support-automation" / "baseline.json"
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        broken = copy.deepcopy(baseline)
        broken["client"] = "Acme Services"
        with tempfile.TemporaryDirectory() as temp:
            artifact = pathlib.Path(temp) / "broken.json"
            artifact.write_text(json.dumps(broken), encoding="utf-8")
            result = run_script(
                "scripts/validate_schema.py",
                str(artifact),
                "schemas/baseline.schema.json",
            )
        self.assertNotEqual(result.returncode, 0)


class PortabilityTests(unittest.TestCase):
    def test_installer_preserves_runtime_layout(self):
        with tempfile.TemporaryDirectory() as temp:
            target = pathlib.Path(temp) / "skills"
            result = run_script("scripts/install_skills.py", str(target))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((target / "sow-intake" / "SKILL.md").is_file())
            self.assertTrue((target / "scope-sentinel" / "agents" / "openai.yaml").is_file())
            self.assertTrue((target / ".delivery-guardrails" / "scripts" / "validate_schema.py").is_file())

    def test_prepare_sow_accepts_utf8_markdown(self):
        source = REPO_ROOT / "examples" / "projects" / "acme-support-automation" / "sow.md"
        result = run_script("scripts/prepare_sow.py", str(source))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(pathlib.Path(result.stdout.strip()), source.resolve())

    def test_prepare_sow_rejects_pdf_without_extractable_text(self):
        from pypdf import PdfWriter

        with tempfile.TemporaryDirectory() as temp:
            source = pathlib.Path(temp) / "scan.pdf"
            writer = PdfWriter()
            writer.add_blank_page(width=100, height=100)
            with source.open("wb") as handle:
                writer.write(handle)
            result = run_script("scripts/prepare_sow.py", str(source))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("OCR", result.stdout + result.stderr)


class EvaluationHarnessTests(unittest.TestCase):
    def test_example_predictions_cover_all_cases(self):
        result = run_script("eval/run_eval.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
