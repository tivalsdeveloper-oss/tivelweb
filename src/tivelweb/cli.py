"""TivelWeb command line interface."""

import argparse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os


STARTER = '''from tivelweb import Site, hero, section

site = Site("My Website")
home = site.page("Home", description="My first TivelWeb website")
home.add(hero("Built with Python", "A fast responsive website.", "Get started", "#about"))
home.add(section("About", "Edit app.py to make this website yours."))
print(f"Website built at: {site.build()}")
'''


def main() -> None:
    parser = argparse.ArgumentParser(prog="tivelweb")
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new", help="create a starter project")
    new.add_argument("name")
    serve = sub.add_parser("serve", help="preview a built website")
    serve.add_argument("directory", nargs="?", default="dist")
    serve.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.command == "new":
        folder = Path(args.name)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "app.py").write_text(STARTER, encoding="utf-8")
        print(f"Created {folder.resolve()}")
    else:
        os.chdir(args.directory)
        print(f"Serving http://127.0.0.1:{args.port} — press Ctrl+C to stop")
        ThreadingHTTPServer(("127.0.0.1", args.port), SimpleHTTPRequestHandler).serve_forever()

