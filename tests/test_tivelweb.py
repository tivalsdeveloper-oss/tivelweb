from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tivelweb import Site, create_news_site, hero


class SiteTests(unittest.TestCase):
    def test_builds_page(self):
        with TemporaryDirectory() as folder:
            site = Site("Test", output=folder)
            site.page("Home").add(hero("Hello"))
            site.build()
            html = (Path(folder) / "index.html").read_text()
            self.assertIn("Hello", html)
            self.assertIn("Powered by tivalsdeveloper", html)

    def test_news_template(self):
        with TemporaryDirectory() as folder:
            site = create_news_site(output=folder)
            self.assertTrue((Path(folder) / "index.html").exists())
            self.assertTrue((Path(folder) / "technology.html").exists())
            self.assertEqual(len(site.pages), 7)


if __name__ == "__main__":
    unittest.main()
