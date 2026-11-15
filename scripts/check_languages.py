"""Check language pages after running `bundle exec jekyll build`."""
import json
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.canonical, self.alternates = set(), [], [], {}
        self.language = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.language = attrs.get('lang')
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs['href'])
        if tag == 'link' and attrs.get('rel') == 'alternate':
            self.alternates[attrs['hreflang']] = attrs['href']

translations = json.loads((ROOT / '_data/translations.json').read_text())
assert translations['it'].keys() == translations['en'].keys()
for language in ('it', 'en'):
    html = (ROOT / '_site' / language / 'index.html').read_text()
    page = Page()
    page.feed(html)
    assert page.language == language
    assert len(page.canonical) == 1 and page.canonical[0].endswith('/' + language + '/')
    assert set(page.alternates) == {'it', 'en', 'x-default'}
    assert page.alternates['x-default'] == page.alternates['it']
    assert '{{' not in html and '{%' not in html
    assert html.count('<article class="experience">') == 3
    assert 'aria-current="page"' in html
    for href in page.links:
        if '#' in href:
            assert href.split('#')[1] in page.ids, href
    for key, value in translations[language].items():
        # Contact CTA renders only when the owner supplies a public email.
        if key.startswith('not_found') or key == 'contact_cta':
            continue
        assert value in html or value.replace('&', '&amp;') in html, (language, key)

sitemap = ET.parse(ROOT / '_site/sitemap.xml')
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
assert len(sitemap.findall('s:url', ns)) == 2
redirect = (ROOT / '_site/index.html').read_text()
assert 'window.location.hash' in redirect and 'window.location.replace' in redirect
print('Italian and English content, language tags, SEO, section links, root redirect and sitemap passed.')
