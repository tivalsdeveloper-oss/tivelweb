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
- Built-in responsive news website template
- Portfolio, business and blog templates
- Ocean, sunset, forest, midnight and rose style presets

## News website template

```python
from tivelweb import create_news_site

site = create_news_site(
    name="Tivals News",
    output="news_website",
    theme_color="#d71920",
)
```

```bash
python app.py
tivelweb serve news_website
```

## More templates

```python
from tivelweb import create_portfolio_site, create_business_site, create_blog_site

create_portfolio_site(name="Tivalsdeveloper", style="midnight")
create_business_site(name="Tivals Digital", style="ocean")
create_blog_site(name="Tivals Blog", author="Lufuno", style="rose")
```

## Style presets

```python
from tivelweb import Site, style_preset, theme_color

site = Site("My Site", theme_color=theme_color("forest"))
home = site.page("Home")
home.add(style_preset("forest"))
site.build()
```

## Test

```bash
python -m unittest discover -s tests
```

## License

MIT
