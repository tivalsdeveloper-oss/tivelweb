from tivelweb import Site, card, hero, section

site = Site("Tivalsdeveloper", theme_color="#00b894")
home = site.page("Home", description="Developer portfolio")
home.add(hero("Hello, I build with Python", "Websites, libraries, and AI tools.", "My projects", "#projects"))
projects = '<div id="projects" class="cards">' + card("TivelWeb", "Build websites using Python.") + card("TivelText", "Colorful terminal applications.") + '</div>'
home.add(section("Projects", projects, raw=True))
site.page("About", "about.html").add(section("About me", "I am a Python developer."))
print(site.build())

