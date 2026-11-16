"""Check generated navigation and local assets before publishing (standard library only)."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import json
import re
import struct

ROOT = Path(__file__).resolve().parent.parent

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.refs = set(), []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        field = 'href' if tag in ('a', 'link') else 'src' if tag in ('img', 'script') else None
        if field and attrs.get(field):
            self.refs.append((tag, attrs[field]))


def main():
    errors, images, cases = [], set(), []
    pages = {p.resolve(): Page(p.read_text()) for p in ROOT.rglob('*.html') if 'src' not in p.relative_to(ROOT).parts}
    for page, parsed in pages.items():
        for tag, url in parsed.refs:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc:
                continue
            target = (ROOT / unquote(parts.path.lstrip('/'))) if parts.path.startswith('/') else (page.parent / unquote(parts.path)).resolve()
            if target.is_dir():
                target /= 'index.html'
            if not target.is_file():
                errors.append(f'{page.relative_to(ROOT)}: missing {url}')
            elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
                errors.append(f'{page.relative_to(ROOT)}: missing anchor {url}')
            if tag == 'img':
                images.add(target)
    for path in sorted((ROOT / 'src').glob('campaigns-*.json')):
        entries = json.loads(path.read_text())
        expected = 10 if path.stem.endswith('07') else 15
        if len(entries) != expected:
            errors.append(f'{path.name}: expected {expected} cases, got {len(entries)}')
        for case in entries:
            cases.append(case['id'])
            allowed = {'Format', 'Discovery', 'Live', 'Community', 'Crossover', 'Monetisation', 'Trust', 'Ownership', 'Rules'}
            platforms = {'YouTube', 'TikTok', 'Instagram', 'Twitch', 'Vine', 'Snapchat', 'Facebook', 'Podcast', 'Blog', 'Newsletter', 'Web', 'Patreon', 'Kickstarter', 'Douyin', 'Weibo', 'Taobao Live', 'Bilibili', 'Kick', 'Roblox', 'Clubhouse', 'AfreecaTV', 'Multi-platform'}
            required = {'id','brand','title','year','place','sector','mechanism','data_role','data_source','stage','hook','situation','exchange','brought','turning_point','metric','metric_label','measure','evidence','evidence_level','stat_type','lesson','take','credit','creative','announcement','impact_source','links','image','how_to_measure'}
            if set(case) - (required | {'deal_value'}) or required - set(case):
                errors.append(f'{case["id"]}: unexpected or missing case fields')
            if case['mechanism'] not in allowed or case['data_role'] not in platforms:
                errors.append(f'{case["id"]}: invalid taxonomy')
            if case['evidence_level'] not in {'Modelled effect','Sales trend','Survey','Reach only','Archival'}:
                errors.append(f'{case["id"]}: invalid evidence level')
            if case['stat_type'] not in {'legacy','result'}:
                errors.append(f'{case["id"]}: invalid statistic type')
            if case['evidence_level'] == 'Archival' and case['stat_type'] != 'legacy':
                errors.append(f'{case["id"]}: archival fact presented as a result')
            if len(case['brought']) != 2 or any(len(pair) != 2 for pair in case['brought']):
                errors.append(f'{case["id"]}: expected two contribution pairs')
            if case['announcement'][1] == case['impact_source'][1]:
                errors.append(f'{case["id"]}: announcement and outcome must be different links')
            if case['creative'].get('heading') != 'Creator media' or not case['creative'].get('url'):
                errors.append(f'{case["id"]}: incomplete creator media')
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',case['id']):
                errors.append(f'{case["id"]}: invalid slug')

            image = case.get('image')
            if not image or not image.get('alt'):
                errors.append(f'{case["id"]}: missing thumbnail or description')
            elif not (ROOT / urlsplit(image['src']).path).is_file():
                errors.append(f'{case["id"]}: missing thumbnail file')
            if image and (ROOT / image['src']).is_file():
                data = (ROOT / image['src']).read_bytes()
                dimensions = None
                if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
                    chunk = data[12:16]
                    if chunk == b'VP8 ' and data[23:26] == bytes((157,1,42)):
                        dimensions = tuple(n & 16383 for n in struct.unpack('<HH',data[26:30]))
                    elif chunk == b'VP8X':
                        dimensions = (int.from_bytes(data[24:27],'little')+1,int.from_bytes(data[27:30],'little')+1)
                if dimensions != (800,450) or (image.get('width'),image.get('height')) != (800,450):
                    errors.append(f'{case["id"]}: thumbnail must be an 800 by 450 WebP')
                if not image.get('credit') or not image.get('source'):
                    errors.append(f'{case["id"]}: missing image attribution')
            for field in ('impact_source', 'announcement'):
                if case.get(field) and urlsplit(case[field][1]).scheme not in ('http', 'https'):
                    errors.append(f'{case["id"]}: invalid {field} URL')
    expected_total = sum(10 if p.stem.endswith('07') else 15 for p in (ROOT / 'src').glob('campaigns-*.json'))
    if len(cases) != expected_total or len(set(cases)) != expected_total:
        errors.append(f'Expected {expected_total} uniquely identified cases')
    # Every generated case thumbnail must carry the current file fingerprint.
    for page, parsed in pages.items():
        for tag, url in parsed.refs:
            if tag == 'img' and '?v=' in url:
                parts = urlsplit(url)
                target = (page.parent / parts.path).resolve()
                if target.is_file():
                    expected = hashlib.sha256(target.read_bytes()).hexdigest()[:12]
                    if parts.query != 'v=' + expected:
                        errors.append(f'{page.relative_to(ROOT)}: stale thumbnail fingerprint {url}')
    for file in ROOT.rglob('*'):
        if file.is_file() and file.suffix in {'.py','.json','.html','.css','.js','.md','.csv','.svg','.txt'}:
            text = file.read_text(encoding='utf-8')
            if any(chr(n) in text for n in (8211,8212)):
                errors.append(f'{file.relative_to(ROOT)}: prohibited dash character')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(pages)} pages, {len(cases)} cases, {len(images)} local images; all internal links, anchors and thumbnail fingerprints valid.')

if __name__ == '__main__':
    main()
