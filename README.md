# TivelWeb

TivelWeb is a lightweight Python library for building responsive static websites without writing all the HTML and CSS yourself.

## Install locally

```bash
cd tivelweb
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Build your first website

```python
from tivelweb import Site, hero, section

site = Site("My Website", theme_color="#6c5ce7")
home = site.page("Home", description="My first Python website")
home.add(hero("Welcome", "This website was built using Python.", "Learn more", "#about"))
home.add(section("About", "TivelWeb generates fast static HTML."))
site.build()
```

Run the file, then preview the generated `dist` folder:

```bash
python app.py
tivelweb serve dist
```

Open `http://127.0.0.1:8000`.

## Commands

```bash
tivelweb new mywebsite
cd mywebsite
python app.py
tivelweb serve dist
```

## Features

- Responsive pages and navigation
- Hero, section, card, button, and image components
- Multiple pages
- Custom theme colors
- Static asset copying
- Built-in local preview server
- No runtime dependencies

## Test

```bash
python -m unittest discover -s tests
```

## License

MIT

