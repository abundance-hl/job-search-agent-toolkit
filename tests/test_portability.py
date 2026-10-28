"""Small regression checks for the reusable builder interfaces."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from pypdf import PdfReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_resume import apply_profile, parse_resume, render_latex
from validate_resume import load_expected, normalize_extracted_text


class PortabilityTests(unittest.TestCase):
    def test_sample_pdfs_preserve_full_summary_word_boundaries(self):
        for profile_path in sorted((ROOT / "examples/sample-candidate/profiles").glob("*.json")):
            with self.subTest(profile=profile_path.stem):
                profile = json.loads(profile_path.read_text())
                document = PdfReader(ROOT / "examples/sample-candidate/pdf" / (profile_path.stem + ".pdf"))
                text = normalize_extracted_text(" ".join(page.extract_text() for page in document.pages))
                self.assertIn(normalize_extracted_text(profile["summary"]), text)

    def test_template_uses_its_own_identity_and_bundled_font(self):
        data = parse_resume(ROOT / "templates/master-resume.md")
        profile = json.loads((ROOT / "templates/profile.json").read_text())
        data, sections, page_break = apply_profile(data, profile)
        rendered = render_latex(data, sections, page_break)
        self.assertEqual(data["name"], "Your Name")
        self.assertIn("you@example.com", rendered)
        self.assertIn(r"\setmainfont{texgyretermes}", rendered)
        self.assertNotIn("@@", rendered)

    def test_expected_file_rejects_wrong_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expected.json"
            path.write_text('{"name": "Your Name"}')
            with self.assertRaises(ValueError):
                load_expected(path)

    def test_validator_uses_caller_expected_text(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pdf = root / "resume.pdf"
            document = canvas.Canvas(str(pdf))
            document.setFont("Helvetica", 11)
            document.drawString(70, 700, "Avery Example resume with verified experience.")
            document.save()
            expected = root / "expected.json"
            expected.write_text('["Avery Example"]')
            command = [sys.executable, str(ROOT / "scripts/validate_resume.py"), str(pdf), "--expected", str(expected)]
            passed = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
            expected.write_text('["A phrase absent from this document"]')
            failed = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("Missing expected extracted text", failed.stderr)

    def test_cover_letter_uses_supplied_identity_in_content_and_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "letter.md"
            source.write_text("# Cover letter\n\nStatus: Draft\n\nDear hiring team,\n\nThis is a format test.\n")
            output = root / "letter.pdf"
            result = subprocess.run([
                sys.executable, str(ROOT / "scripts/build_cover_letter_pdf.py"), str(source), str(output),
                "--title", "Example letter", "--name", "Avery & Example", "--contact", "avery@example.com | Example City",
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            document = PdfReader(output)
            text = " ".join(page.extract_text() for page in document.pages)
            self.assertIn("Avery & Example", text)
            self.assertIn("avery@example.com", text)
            self.assertEqual(document.metadata.author, "Avery & Example")


if __name__ == "__main__":
    unittest.main()
