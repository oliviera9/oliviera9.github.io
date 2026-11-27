"""Validate real activity data and a temporary fixture build of the calendar."""
from datetime import date, datetime
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import tempfile
from zoneinfo import ZoneInfo
from preview_calendar import ROOT, build_demo, example_activities


def validate_activities(items):
    assert isinstance(items, list), 'activities.json must contain a list'
    seen = set()
    for item in items:
        identifier = item['id']
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', identifier), identifier
        assert identifier not in seen, 'Activity IDs must be unique'
        seen.add(identifier)
        assert type(item['published']) is bool
        assert item['status'] in ('open', 'full')
        assert item['kind'] in ('day', 'trek', 'snowshoe', 'custom')
        start = date.fromisoformat(item['date'])
        end = date.fromisoformat(item.get('end_date', item['date']))
        assert start.isoformat() == item['date'], 'Use YYYY-MM-DD dates'
        assert end.isoformat() == item.get('end_date', item['date'])
        assert end >= start, 'End date cannot precede the start date'
        for language in ('it', 'en'):
            for field in ('title', 'description', 'location', 'difficulty', 'duration'):
                assert isinstance(item[language][field], str) and item[language][field].strip(), (identifier, language, field)

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.events, self.months, self.enquiries = [], [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-calendar-event' in attrs:
            self.events.append(attrs)
        if 'data-calendar-month' in attrs:
            self.months.append(attrs)
        if 'data-planned-enquiry' in attrs:
            self.enquiries.append(attrs)

if __name__ == '__main__':
    validate_activities(json.loads((ROOT / '_data/activities.json').read_text()))
    today = datetime.now(ZoneInfo('Europe/Rome')).date()
    examples = example_activities(today)
    validate_activities(examples)
    # Invalid data must fail before being used in a published calendar.
    invalid = dict(examples[0], end_date='2000-01-01')
    try:
        validate_activities([invalid])
    except AssertionError:
        pass
    else:
        raise AssertionError('Invalid end dates were accepted')
    with tempfile.TemporaryDirectory(prefix='alain-calendar-test-') as temporary:
        output = Path(temporary) / 'site'
        build_demo(output, today)
        expected = sorted((item for item in examples if item['published'] and item.get('end_date', item['date']) >= today.isoformat()), key=lambda item: item['date'])
        for language in ('it', 'en'):
            html = (output / language / 'index.html').read_text()
            calendar = Calendar()
            calendar.feed(html)
            assert len(calendar.events) == len(expected) == 4
            assert len(calendar.months) == len({item['date'][:7] for item in expected})
            assert [item['data-event-id'] for item in calendar.enquiries] == [item['id'] for item in expected]
            assert all(link['href'] == '#enquiry-title' for link in calendar.enquiries)
            assert 'example-expired' not in html and 'example-draft' not in html
            assert 'calendar-demo' in html and 'is-full' in html
            for item in expected:
                assert item[language]['title'] in html
                assert item[language]['location'] in html
            for link, item in zip(calendar.enquiries, expected):
                assert link['data-event-title'] == item[language]['title']
                assert link['data-event-kind'] == item['kind']
                assert link['data-event-date'].startswith(item['date'])
    print('Calendar schema, ordering, month grouping, translations, draft/past filtering and enquiry links passed.')
