from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tivelweb import (
    Site,
    create_blog_site,
    create_business_site,
    create_news_site,
    create_portfolio_site,
    hero,
    style_preset,
    theme_color,
)


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

    def test_additional_templates(self):
        builders = [create_portfolio_site, create_business_site, create_blog_site]
        for builder in builders:
            with self.subTest(builder=builder.__name__), TemporaryDirectory() as folder:
                site = builder(output=folder)
                self.assertTrue((Path(folder) / "index.html").exists())
                self.assertGreaterEqual(len(site.pages), 4)

    def test_style_presets(self):
        self.assertEqual(theme_color("ocean"), "#087ea4")
        self.assertIn("--preset-primary", style_preset("forest"))
        with self.assertRaises(ValueError):
            style_preset("missing")


if __name__ == "__main__":
    unittest.main()
