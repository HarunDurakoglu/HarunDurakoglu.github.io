import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RoadMirrorPrivacyPageTests(unittest.TestCase):
    def test_home_page_lists_roadmirror_as_third_app(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn('<span class="section-count">03 apps</span>', home)
        self.assertIn('id="roadmirror-title">RoadMirror</h3>', home)
        self.assertIn('href="/roadmirror/privacy/"', home)

    def test_privacy_page_matches_current_app_behavior(self):
        privacy = (ROOT / "roadmirror/privacy/index.html").read_text(encoding="utf-8")

        self.assertIn("uses ReplayKit to record up to 15 seconds", privacy)
        self.assertIn("does not capture other apps", privacy)
        self.assertIn("does not provide live CarPlay screen mirroring", privacy)
        self.assertNotIn("captures the display you select", privacy)

    def test_privacy_page_keeps_operational_routes_on_firebase(self):
        privacy = (ROOT / "roadmirror/privacy/index.html").read_text(encoding="utf-8")

        self.assertIn('href="https://roadmirror.web.app/support/"', privacy)
        self.assertIn('href="https://roadmirror.web.app/delete-account/"', privacy)

    def test_readme_documents_public_roadmirror_privacy_url(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn(
            "https://harundurakoglu.github.io/roadmirror/privacy/", readme
        )

    def test_every_root_relative_link_resolves_to_a_file(self):
        pages = [ROOT / "index.html", *ROOT.glob("*/*/index.html")]

        for page in pages:
            html = page.read_text(encoding="utf-8")
            for target in re.findall(r'(?:href|src)="(/[^"]+)"', html):
                if target == "/":
                    destination = ROOT / "index.html"
                elif target.endswith("/"):
                    destination = ROOT / target.removeprefix("/") / "index.html"
                else:
                    destination = ROOT / target.removeprefix("/")
                with self.subTest(page=page.relative_to(ROOT), target=target):
                    self.assertTrue(destination.is_file(), destination)


if __name__ == "__main__":
    unittest.main()
