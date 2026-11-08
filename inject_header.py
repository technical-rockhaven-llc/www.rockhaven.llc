"""Replace the thumbsup text title with the inline Rock Haven lockup on every page.

The lockup is inlined (not an <img>) so the Outfit web font loaded by the
page applies to its text; SVGs loaded as images cannot fetch web fonts.
Usage: python3 inject_header.py build_output/*.html
"""
import sys
from pathlib import Path

lockup = Path(__file__).with_name("logo-horizontal.svg").read_text().strip()
FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600&display=swap">')
OLD = '<h1><a href="index.html">Rock Haven Property LLC</a></h1>'
NEW = ('<h1><a href="index.html" class="rh-brand">' + lockup +
       '<span class="rh-sr">Rock Haven Property LLC</span></a></h1>')

for name in sys.argv[1:]:
    p = Path(name)
    html = p.read_text()
    if OLD not in html:
        sys.exit(f"{p}: header title not found")
    html = html.replace(OLD, NEW, 1).replace("<head>", "<head>\n    " + FONT, 1)
    p.write_text(html)
    print(f"{p}: header replaced")
