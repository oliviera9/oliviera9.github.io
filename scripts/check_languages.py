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
        self.forms, self.fields, self.labels, self.robots = [], {}, set(), []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'form':
            self.forms.append(attrs)
        if tag in ('input', 'select', 'textarea'):
            self.fields[attrs.get('name')] = attrs
        if tag == 'label':
            self.labels.add(attrs.get('for'))
        if tag == 'meta' and attrs.get('name') == 'robots':
            self.robots.append(attrs.get('content', ''))
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
routes = json.loads((ROOT / '_data/routes.json').read_text())
details = json.loads((ROOT / '_data/contact.json').read_text())
assert translations['it'].keys() == translations['en'].keys()
for language in ('it', 'en'):
    home_html = (ROOT / '_site' / language / 'index.html').read_text()
    thanks_html = (ROOT / '_site' / language / 'thanks/index.html').read_text()
    for page_type in ('home', 'contact'):
        route = routes[page_type][language]
        html = (ROOT / '_site' / route.lstrip('/') / 'index.html').read_text()
        page = Page()
        page.feed(html)
        assert page.language == language
        assert len(page.canonical) == 1 and page.canonical[0].endswith(route)
        assert set(page.alternates) == {'it', 'en', 'x-default'}
        assert page.alternates['x-default'] == page.alternates['it']
        for target_language in ('it', 'en'):
            assert page.alternates[target_language].endswith(routes[page_type][target_language])
        assert '{{' not in html and '{%' not in html
        assert 'aria-current="page"' in html
        assert len(page.forms) == 1
        assert page.forms[0]['method'] == 'post'
        assert page.forms[0]['action'] == 'https://formsubmit.co/oliviera9@gmail.com'
        for name in ('name', 'email', 'message'):
            assert 'required' in page.fields[name]
            assert page.fields[name]['id'] in page.labels
        assert page.fields['email']['type'] == 'email'
        assert page.fields['group_size']['min'] == '1'
        assert page.fields['group_size']['step'] == '1'
        assert page.fields['_next']['value'].endswith('/' + language + '/thanks/')
        assert page.fields['language']['value'] == language
        assert page.fields['_honey']['tabindex'] == '-1'
        assert '_captcha' not in page.fields
        for name in ('activity', 'dates', 'group_size'):
            assert page.fields[name]['id'] in page.labels
        # Validate same-site links against the actual destination page, including
        # links from Contacts back to sections of the homepage.
        for href in page.links:
            if href.startswith('/') or href.startswith('#'):
                path, _, fragment = href.partition('#')
                destination = ROOT / '_site' / (path or route).lstrip('/')
                if destination.is_dir():
                    destination = destination / 'index.html'
                assert destination.exists(), href
                if fragment:
                    target = Page()
                    target.feed(destination.read_text())
                    assert fragment in target.ids, href
        if page_type == 'home':
            assert html.count('<article class="experience">') == 3
        else:
            for key in ('professional_register_number', 'vat_number', 'pec', 'instagram', 'whatsapp'):
                assert details[key] in html, key
            assert 'contact-page-title' in page.ids
            assert routes['contact'][language] in page.links
            contact_html = html
    thanks = Page()
    thanks.feed(thanks_html)
    assert thanks.language == language
    assert any('noindex' in value for value in thanks.robots)
    combined_html = home_html + contact_html + thanks_html
    for key, value in translations[language].items():
        if key.startswith('not_found'):
            continue
        assert value in combined_html or value.replace('&', '&amp;') in combined_html, (language, key)

sitemap = ET.parse(ROOT / '_site/sitemap.xml')
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
assert len(sitemap.findall('s:url', ns)) == 4
redirect = (ROOT / '_site/index.html').read_text()
assert 'window.location.hash' in redirect and 'window.location.replace' in redirect
print('Italian and English pages, contact details, SEO, links, enquiry forms and sitemap passed.')
