"""Website and page builders."""

from dataclasses import dataclass, field
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from functools import partial
import shutil
import webbrowser


DEFAULT_CSS = """:root{--primary:#6c5ce7;--dark:#151522;--light:#f7f7fb;--text:#29293d;--radius:18px}*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,sans-serif;color:var(--text);background:var(--light);line-height:1.65}a{color:inherit}.container{width:min(1100px,92%);margin:auto}.navbar{background:var(--dark);color:white;padding:1rem 0}.navbar .container{display:flex;justify-content:space-between;align-items:center;gap:1rem}.brand{font-size:1.25rem;font-weight:800;text-decoration:none}.nav-links{display:flex;gap:1rem;flex-wrap:wrap}.nav-links a{text-decoration:none}.hero{padding:6rem 0;text-align:center;background:linear-gradient(135deg,#151522,#6c5ce7);color:white}.hero h1{font-size:clamp(2.4rem,7vw,5rem);line-height:1.05;margin:0}.hero p{font-size:1.2rem;opacity:.9}.section{padding:4rem 0}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1.25rem}.card{background:white;padding:1.5rem;border-radius:var(--radius);box-shadow:0 12px 35px #1d1d3512}.btn{display:inline-block;padding:.75rem 1.1rem;border-radius:999px;text-decoration:none;font-weight:700;margin-top:.5rem}.btn-primary{background:white;color:var(--primary)}.btn-secondary{background:var(--primary);color:white}.footer{padding:2rem;background:var(--dark);color:#ccc;text-align:center}@media(max-width:600px){.navbar .container{align-items:flex-start;flex-direction:column}.hero{padding:4rem 0}}"""


@dataclass
class Page:
    title: str
    path: str = "index.html"
    description: str = ""
    content: list[str] = field(default_factory=list)

    def add(self, html: str) -> "Page":
        self.content.append(html)
        return self


class Site:
    def __init__(
        self,
        name: str,
        *,
        theme_color: str = "#6c5ce7",
        output: str = "dist",
        background_image: str = "",
        background_overlay: float = 0.82,
    ):
        self.name = name
        self.theme_color = theme_color
        self.output = Path(output)
        self.background_image = background_image
        if not 0 <= background_overlay <= 1:
            raise ValueError("background_overlay must be between 0 and 1")
        self.background_overlay = background_overlay
        self.pages: list[Page] = []
        self.assets: list[tuple[Path, str]] = []

    def page(self, title: str, path: str = "index.html", description: str = "") -> Page:
        page = Page(title, path, description)
        self.pages.append(page)
        return page

    def add_asset(self, source: str, destination: str = "assets") -> "Site":
        self.assets.append((Path(source), destination))
        return self

    def _render(self, page: Page) -> str:
        links = "".join(
            f'<a href="/{escape(p.path, quote=True)}">{escape(p.title)}</a>' for p in self.pages
        )
        body = "\n".join(page.content)
        css = DEFAULT_CSS.replace("#6c5ce7", self.theme_color)
        if self.background_image:
            safe_url = self.background_image.replace("\\", "\\\\").replace('"', '\\"').replace(")", "\\)")
            opacity = self.background_overlay
            css += (
                f'body{{background-image:linear-gradient(rgba(247,247,251,{opacity}),'
                f'rgba(247,247,251,{opacity})),url("{safe_url}");'
                'background-size:cover;background-position:center;background-attachment:fixed}}'
            )
        return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(page.title)} | {escape(self.name)}</title><meta name="description" content="{escape(page.description, quote=True)}">
<style>{css}</style></head><body>
<nav class="navbar"><div class="container"><a class="brand" href="/">{escape(self.name)}</a><div class="nav-links">{links}</div></div></nav>
<main>{body}</main><footer class="footer">Powered by tivalsdeveloper</footer></body></html>"""

    def build(self, clean: bool = True) -> Path:
        if clean and self.output.exists():
            shutil.rmtree(self.output)
        self.output.mkdir(parents=True, exist_ok=True)
        for page in self.pages:
            target = self.output / page.path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(self._render(page), encoding="utf-8")
        for source, destination in self.assets:
            target = self.output / destination / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        return self.output.resolve()

    def run(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = 8000,
        open_browser: bool = True,
    ) -> Path:
        """Build, serve and optionally open the website in one command."""
        output = self.build()
        handler = partial(SimpleHTTPRequestHandler, directory=str(output))
        server = ThreadingHTTPServer((host, port), handler)
        url = f"http://{host}:{port}"
        print(f"Serving {self.name} at {url} — press Ctrl+C to stop")
        if open_browser:
            webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
        finally:
            server.server_close()
        return output
