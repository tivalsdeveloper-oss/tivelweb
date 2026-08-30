from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import MagicMock, patch

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

    def test_background_image(self):
        with TemporaryDirectory() as folder:
            site = Site(
                "Background Test",
                output=folder,
                background_image="https://example.com/background.jpg",
                background_overlay=0.7,
            )
            site.page("Home")
            site.build()
            html = (Path(folder) / "index.html").read_text()
            self.assertIn("https://example.com/background.jpg", html)
            self.assertIn("background-attachment:fixed", html)

    def test_background_overlay_validation(self):
        with self.assertRaises(ValueError):
            Site("Invalid", background_overlay=2)

    @patch("tivelweb.site.webbrowser.open")
    @patch("tivelweb.site.ThreadingHTTPServer")
    def test_run_builds_and_serves(self, server_class, browser_open):
        server = MagicMock()
        server_class.return_value = server
        with TemporaryDirectory() as folder:
            site = Site("Run Test", output=folder)
            site.page("Home")
            output = site.run(port=8123)
            self.assertTrue((output / "index.html").exists())
        server.serve_forever.assert_called_once()
        server.server_close.assert_called_once()
        browser_open.assert_called_once_with("http://127.0.0.1:8123")


if __name__ == "__main__":
    unittest.main()
