from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tivelweb import Site, hero


class SiteTests(unittest.TestCase):
    def test_builds_page(self):
        with TemporaryDirectory() as folder:
            site = Site("Test", output=folder)
            site.page("Home").add(hero("Hello"))
            site.build()
            html = (Path(folder) / "index.html").read_text()
            self.assertIn("Hello", html)
            self.assertIn("Powered by tivalsdeveloper", html)


if __name__ == "__main__":
    unittest.main()

