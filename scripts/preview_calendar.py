"""Build a labelled calendar demo locally; never modifies the real activities data."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]

def example_activities(today):
    def activity(identifier, offset, kind='day', status='open', published=True, end_offset=None):
        item = {
            'id': identifier, 'published': published,
            'date': (today + timedelta(days=offset)).isoformat(),
            'kind': kind, 'status': status,
            'en': {'title': 'Example: a day on the trail', 'description': 'An illustrative outing for reviewing the calendar layout. Not a scheduled activity.', 'location': 'Dolomites — example location', 'difficulty': 'Moderate — example', 'duration': '5 hours — example'},
            'it': {'title': 'Esempio: una giornata sui sentieri', 'description': 'Un’uscita illustrativa per verificare il calendario. Non è un’attività programmata.', 'location': 'Dolomiti — luogo di esempio', 'difficulty': 'Media — esempio', 'duration': '5 ore — esempio'}
        }
        if end_offset is not None:
            item['end_date'] = (today + timedelta(days=end_offset)).isoformat()
        if kind == 'trek':
            item['en']['title'] = 'Example: hut-to-hut trek'
            item['it']['title'] = 'Esempio: trekking tra rifugi'
            item['en']['duration'] = '3 days — example'
            item['it']['duration'] = '3 giorni — esempio'
        return item
    return [
        activity('example-next-month', 35, status='full'),
        activity('example-expired', -10),
        activity('example-next-walk', 7),
        activity('example-draft', 10, published=False),
        activity('example-trek', 14, kind='trek', end_offset=16),
        activity('example-ongoing', -1, kind='trek', end_offset=0),
    ]

def build_demo(destination, today=None):
    today = today or datetime.now(ZoneInfo('Europe/Rome')).date()
    with tempfile.TemporaryDirectory(prefix='alain-calendar-') as temporary:
        source = Path(temporary).resolve()
        for name in ('_includes', '_layouts', '_data', 'assets', 'it', 'en'):
            shutil.copytree(ROOT / name, source / name)
        for name in ('_config.yml', 'index.html', '404.html', 'robots.txt', 'sitemap.xml'):
            shutil.copy2(ROOT / name, source / name)
        (source / '_data/activities.json').write_text(json.dumps(example_activities(today), ensure_ascii=False, indent=2))
        config = source / '_config.yml'
        config.write_text(config.read_text() + '\ncalendar_demo: true\n')
        environment = dict(os.environ)
        environment['BUNDLE_GEMFILE'] = str(ROOT / 'Gemfile')
        local_bundle = ROOT / '.gems/bin/bundle'
        if local_bundle.exists():
            bundle = str(local_bundle)
            environment['GEM_HOME'] = str(ROOT / '.gems')
            environment['GEM_PATH'] = str(ROOT / '.gems')
        else:
            bundle = 'bundle'
        subprocess.run([bundle, 'exec', 'jekyll', 'build', '--source', str(source),
                        '--destination', str(destination), '--config', str(config)],
                       cwd=source, env=environment, check=True)

if __name__ == '__main__':
    build_demo(ROOT / '.calendar-preview')
    print('Local example calendar built in .calendar-preview/. Real activities were not changed.')
    print('Preview with: python3 -m http.server 4001 --directory .calendar-preview')
