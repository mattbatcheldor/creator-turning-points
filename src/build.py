from html import escape
from pathlib import Path
import collections
import hashlib
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import json
import re
import random

root = Path(__file__).resolve().parent
e = escape

from art import play_art, proof_art, money_art, platform_art, failure_art, brand_art, edge_art

LEVELS = ['Modelled effect', 'Sales trend', 'Survey', 'Reach only', 'Archival']
LEVEL_NOTES = {
    'Modelled effect': 'A model estimates the effect against a baseline.',
    'Sales trend': 'Sales, subscriptions, chart positions, funding or delivered work are recorded; other causes are not separated out.',
    'Survey': 'People who saw it said something changed.',
    'Reach only': 'The number counts attention, not what the creator or anyone else gained.',
    'Archival': 'The record shows the moment happened, not what it earned.',
}
# In this archive the "mechanism" is the shift: what changed because of the creator.
MECHANISMS = [
    ('Format', 'A new way of making or watching took hold.'),
    ('Discovery', 'An audience found someone the gatekeepers had missed.'),
    ('Live', 'Watching together, in real time, became the product.'),
    ('Community', 'The audience stopped watching and started acting together.'),
    ('Crossover', 'A creator carried an online audience into music, sport, film or TV.'),
    ('Monetisation', 'A new way for creators to be paid.'),
    ('Trust', 'A creator’s word moved what people bought or believed.'),
    ('Ownership', 'The creator owned the product, the company or the rights.'),
    ('Rules', 'A platform, regulator or court changed what creators could do.'),
]
ROLES = ['YouTube', 'TikTok', 'Instagram', 'Twitch', 'Vine', 'Snapchat', 'Facebook', 'Podcast', 'Blog', 'Newsletter', 'Web', 'Patreon', 'Kickstarter', 'Douyin', 'Weibo', 'Taobao Live', 'Bilibili', 'Kick', 'Roblox', 'Clubhouse', 'AfreecaTV', 'Multi-platform']
# Every case is sorted by the platform where the turning point happened.
ROLE_DEFAULTS = {'roles': ROLES, 'role_label': 'Platform', 'role_aria': 'Platform', 'source_label': 'The creator'}
ERAS = ['1950s to 1980s', '1990s and 2000s', '2010s', '2020s']


def era(year):
    if year < 1990:
        return ERAS[0]
    if year < 2010:
        return ERAS[1]
    if year < 2020:
        return ERAS[2]
    return ERAS[3]


def strength_of(level):
    return len(LEVELS) - LEVELS.index(level)


def meter(level):
    strength = strength_of(level)
    bars = ''.join(f'<i class="{"on" if n < strength else ""}"></i>' for n in range(len(LEVELS)))
    return (f'<span class="meter s{strength}" role="img" aria-label="Evidence strength {strength} of {len(LEVELS)}: {e(level)}">'
            f'<span class="bars" aria-hidden="true">{bars}</span><span class="meter-label" aria-hidden="true">{e(level)}</span></span>')


def slug(text):
    return text.lower().replace(' ', '-')


def image_url(image, prefix=''):
    # Fingerprint the bytes so a replaced thumbnail cannot reuse an older cached image.
    parts = urlsplit(image['src'])
    asset = root.parent / parts.path
    if parts.scheme or parts.netloc or not asset.is_file():
        raise ValueError(f"Expected a local image file: {image['src']}")
    version = hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
    query = [(k, v) for k, v in parse_qsl(parts.query) if k != 'v']
    query.append(('v', version))
    return prefix + urlunsplit(('', '', parts.path, urlencode(query), parts.fragment))


def campaign_image(c, placement, prefix=''):
    image = c.get('image')
    if not image:
        return ''
    fit = ' image-contain' if image.get('contain') else ''
    return (f'<span class="{placement}{fit}"><img src="{e(image_url(image, prefix))}" '
            f'alt="{e(image["alt"])}" width="{image["width"]}" height="{image["height"]}" '
            'loading="lazy" decoding="async"></span>')


def proof_tile(c):
    # Used where a case has no licensed image: a type tile that names how the effect was proved,
    # or, in a data edition, how the data was used and where it came from.
    if c.get('data_role'):
        cls, label = f'r-{slug(c["data_role"])}', f'{c["data_role"]} / {c["data_source"]}'
    else:
        cls, label = f'm-{slug(c["mechanism"])}', c.get('method') or c['evidence_level']
    return (f'<span class="case-thumbnail proof-tile {cls}" aria-hidden="true">'
            f'<span class="tile-year">{c["year"]}</span><span class="tile-method">{e(label)}</span></span>')


def render_cards(campaigns, notes, test_heading, prefix='', source_label='The partners'):
    # Creator Turning Points uses a six-part case: the situation, the move, the turning point,
    # what the evidence shows, what to take into a creator programme, and sources and media.
    cards = []
    for i, c in enumerate(campaigns, 1):
        creative = c['creative']
        image = c.get('image')
        outcome_label, outcome_url = c['impact_source']
        announce_label, announce_url = c['announcement']
        legacy = c['stat_type'] == 'legacy'
        stat_tag = '<p class="stat-tag small">Legacy fact, not a result</p>' if legacy else ''
        deal = f'<p class="deal-tag"><span class="small">Money involved</span> {e(c["deal_value"])}</p>' if c.get('deal_value') else ''
        credit = f'\n<p class="case-credit small">{e(c["credit"])}</p>' if c.get('credit') else ''
        if creative.get('url'):
            creative_link = f'<a href="{e(creative["url"])}">{e(creative["label"])}</a>'
        else:
            creative_link = f'<p class="no-copy">{e(creative["label"])}</p>'
        image_credit = f'\n<p class="image-credit">Image: <a href="{e(image["source"])}">{e(image["credit"])}</a></p>' if image else ''
        thumbnail = campaign_image(c, 'case-thumbnail', prefix) or proof_tile(c)
        brought = ''.join(f'<li><strong>{e(name)}</strong> {e(what)}</li>' for name, what in c['brought'])
        extra = ''.join(f'<li><a href="{e(url)}">{e(label)}</a></li>' for label, url in c['links'])
        how_to_measure = c.get('how_to_measure')
        measurement_note = (
            f'\n<h3>How I’d measure it now</h3><p>{e(how_to_measure)}</p>'
            if how_to_measure else ''
        )
        cards.append(f'''<details id="{e(c['id'])}" class="case" data-mechanism="{e(c['mechanism'])}" data-evidence="{e(c['evidence_level'])}" data-era="{e(era(c['year']))}" data-role="{e(c['data_role'])}">
<summary>
<span class="case-number small">{i:02d}</span>
{thumbnail}
<span class="case-heading"><span class="case-brand small">{e(c['brand'])} / {c['year']} / {e(c['mechanism'])}</span><span class="case-title">{e(c['title'])}</span><span class="case-hook">{e(c['hook'])}</span><span class="case-data"><strong>{e(c['data_role'])}</strong> · {e(c['stage'])}</span></span>
<span class="metric-cell{' legacy' if legacy else ''}"><span class="row-metric">{e(c['metric'])}</span><span class="row-label small">{e(c["metric_label"])}{' · legacy fact' if legacy else ''}</span>{meter(c['evidence_level'])}</span>
<span class="toggle" aria-hidden="true"></span>
</summary>
<div class="case-inner">
<div>
<p class="case-meta">{e(c['place'])} / {e(c['sector'])}</p>{credit}
<h3>The situation</h3><p>{e(c['situation'])}</p>
<h3>The move</h3><p>{e(c['exchange'])}</p>
<ul class="brought">{brought}</ul>
<h3>The turning point</h3><p>{e(c['turning_point'])}</p>
<div class="memory take"><h3>My take</h3><p>{e(c['take'])}</p></div>
<div class="creative-record">
<h3>{e(creative.get('heading', 'Media'))} <span>{e(creative['medium'])}</span></h3>
{creative_link}{image_credit}
</div>
</div>
<aside class="proof" aria-label="Evidence">
<h3>{'Headline fact' if legacy else 'Outcome'} <span>{e(c['stage'])}</span></h3>
<p class="proof-value">{e(c['metric'])}</p>
{stat_tag}
<p class="proof-metric">{e(c['measure'])}</p>{deal}
<div class="proof-strength"><span class="small">Evidence strength</span>{meter(c['evidence_level'])}<p>{e(notes[c['evidence_level']])}</p></div>
<p class="impact-citation"><span class="small">Outcome source</span> <a href="{e(outcome_url)}">{e(outcome_label)}</a></p>
</aside>
</div>
<details class="full-case">
<summary><span>Read the full case</span><span class="toggle" aria-hidden="true"></span></summary>
<div class="full-inner">
<div>
<h3>What the evidence shows</h3><p>{e(c['evidence'])}</p>
<h3>What to take into a creator programme</h3><p>{e(c['lesson'])}</p>{measurement_note}
</div>
<div>
<h3>Sources</h3>
<ul class="sources"><li><span class="small">The moment</span> <a href="{e(announce_url)}">{e(announce_label)}</a></li><li><span class="small">Outcome</span> <a href="{e(outcome_url)}">{e(outcome_label)}</a></li>{extra}</ul>
</div>
</div>
</details>
</details>''')
    return cards


def render_ladder(campaigns, notes, compare=None):
    ladder = []
    for level in LEVELS:
        group = [c for c in campaigns if c['evidence_level'] == level]
        links = ', '.join(f'<a href="#{e(c["id"])}">{e(c["brand"])}</a>' for c in group)
        if compare is None:
            ladder.append(f'''<li class="s{strength_of(level)}"><span class="ladder-name">{meter(level)}</span>
<span class="ladder-count"><b>{len(group)}</b><span class="ladder-bar" style="--n:{len(group)}" aria-hidden="true"></span></span>
<span class="ladder-cases"><span class="ladder-note">{e(notes[level])}</span> {links}</span></li>''')
        else:
            before = sum(1 for c in compare['campaigns'] if c['evidence_level'] == level)
            ladder.append(f'''<li class="s{strength_of(level)} compare-row"><span class="ladder-name">{meter(level)}</span>
<span class="ladder-pair"><span class="pair-row now"><b>{len(group)}</b><span class="ladder-bar" style="--n:{len(group)}" aria-hidden="true"></span><span class="sr">in this edition</span></span><span class="pair-row then"><b>{before}</b><span class="ladder-bar" style="--n:{before}" aria-hidden="true"></span><span class="sr">in {e(compare['label'])}</span></span></span>
<span class="ladder-cases"><span class="ladder-note">{e(notes[level])}</span> {links or '<span class="none">None in this edition</span>'}</span></li>''')
    return ladder


def render_role_grid(campaigns, all_roles=ROLES, role_aria='How data was used'):
    roles = [r for r in all_roles if any(c.get('data_role') == r for c in campaigns)]
    if not roles:
        return ''
    levels = [l for l in LEVELS if any(c['evidence_level'] == l for c in campaigns)]
    cells = ['<span class="rg-corner" aria-hidden="true"></span>'] + [f'<span class="rg-head">{e(l)}</span>' for l in levels]
    brands = [c['brand'] for c in campaigns]
    def chip_label(c):
        # Name the year too when a brand appears more than once, so two IBM chips can be told apart.
        return f'{c["brand"]} {c["year"]}' if brands.count(c['brand']) > 1 else c['brand']
    for r in roles:
        cells.append(f'<span class="rg-role">{e(r)}</span>')
        for l in levels:
            group = [c for c in campaigns if c.get('data_role') == r and c['evidence_level'] == l]
            chips_html = ''.join(f'<a class="rg-chip s{strength_of(l)}" href="#{e(c["id"])}">{e(chip_label(c))}</a>' for c in group)
            cells.append(f'<span class="rg-cell{" empty" if not group else ""}" data-level="{e(l)}">{chips_html}</span>')
    return (f'<div class="role-grid" style="--cols:{len(levels)}" role="group" aria-label="Cases by {e(role_aria.lower())} and by evidence strength">'
            + ''.join(cells) + '</div>')


def series_modelled(edition):
    parts = []
    for other in EDITIONS:
        data = root / other['data']
        if not data.exists():
            continue
        n = sum(1 for c in json.loads(data.read_text(encoding='utf-8')) if c['evidence_level'] == 'Modelled effect')
        parts.append((f'{n} here' if n else 'none here') if other is edition else (f'{n} in Edition {other["number"]}' if n else f'none in Edition {other["number"]}'))
    return ', '.join(parts[:-1]) + ' and ' + parts[-1] if len(parts) > 1 else (parts[0] if parts else '')


def present_mechanisms(campaigns, mechanisms=None):
    # An edition can name its own mechanisms (Edition 05 sorts failures by the mistake behind them).
    return [(m, note) for m, note in (mechanisms or MECHANISMS) if any(c['mechanism'] == m for c in campaigns)]


def render_mechanisms(campaigns, mechanisms=None):
    cols = []
    for name, note in present_mechanisms(campaigns, mechanisms):
        items = ''.join(f'<li><a href="#{e(c["id"])}">{e(c["brand"])} <span>{c["year"]}</span></a></li>'
                        for c in sorted(campaigns, key=lambda c: c['year']) if c['mechanism'] == name)
        cols.append(f'<div class="mech"><h3><button class="mech-pick" type="button" data-value="{e(name)}">{e(name)}</button></h3><p>{e(note)}</p><ul>{items}</ul></div>')
    return cols


def render_timeline(campaigns):
    first, last = min(c['year'] for c in campaigns), max(c['year'] for c in campaigns)
    span = last - first
    decades = [y for y in range((first // 10 + 1) * 10, last + 1, 10)]
    ticks = ''.join(f'<span class="tick" style="--x:{(y - first) / span * 100:.2f}%">{y}</span>' for y in decades)
    dots, stacks = [], {}
    for c in sorted(campaigns, key=lambda c: c['year']):
        stack = stacks.get(c['year'], 0)
        stacks[c['year']] = stack + 1
        dots.append(f'<a class="dot s{strength_of(c["evidence_level"])}" href="#{e(c["id"])}" data-id="{e(c["id"])}" style="--x:{(c["year"] - first) / span * 100:.2f}%;--y:{stack}" title="{e(c["brand"])}, {c["year"]}. {e(c["evidence_level"])}"><span class="sr">{e(c["brand"])}, {c["year"]}</span></a>')
    return f'<div class="timeline" role="group" aria-label="Creator turning points by year, {first} to {last}">{"".join(dots)}<div class="axis" aria-hidden="true">{ticks}</div></div>'


def chips(group, values):
    out = [f'<button class="filter" type="button" data-group="{group}" data-value="All" aria-pressed="true">All</button>']
    out += [f'<button class="filter" type="button" data-group="{group}" data-value="{e(v)}" aria-pressed="false">{e(v)}</button>' for v in values]
    return ''.join(out)


def render_filters(campaigns, all_roles=ROLES, role_label='Data use', role_aria='How data was used', mechanisms=None, mech_label='Mechanism'):
    mech_names = [m for m, _ in present_mechanisms(campaigns, mechanisms)]
    levels = [l for l in LEVELS if any(c['evidence_level'] == l for c in campaigns)]
    eras = [x for x in ERAS if any(era(c['year']) == x for c in campaigns)]
    roles = [r for r in all_roles if any(c.get('data_role') == r for c in campaigns)]
    role_row = f'<div class="filter-row" role="group" aria-label="{e(role_aria)}"><span class="small">{e(role_label)}</span>{chips("role", roles)}</div>' if roles else ''
    return role_row + (f'<div class="filter-row" role="group" aria-label="{e(mech_label)}"><span class="small">{e(mech_label)}</span>{chips("mechanism", mech_names)}</div>'
            f'<div class="filter-row" role="group" aria-label="Evidence strength"><span class="small">Evidence</span>{chips("evidence", levels)}</div>'
            f'<div class="filter-row" role="group" aria-label="Era"><span class="small">Era</span>{chips("era", eras)}</div>')


def render_screenings(campaigns, screening, prefix=''):
    screenings = []
    for case_id, note, drawn in screening:
        c = next(entry for entry in campaigns if entry['id'] == case_id)
        creative = c['creative']
        title = creative.get('screening_title', c['title'])
        url = creative.get('screening_url', creative['url'])
        video = url.partition('https://www.youtube.com/watch?v=')[2]
        player = ''
        if video:
            player = f'<button class="play-film small" type="button" data-video="{e(video)}" data-title="{e(title)}" hidden>Play here</button>'
        frame = campaign_image(c, 'film-frame', prefix) or f'<span class="film-frame drawn {drawn}" aria-hidden="true"></span>'
        screenings.append(f'''<article class="screening">
{frame}
<div class="film-body">
<div class="film-heading"><p class="small">{e(c['brand'])} / {c['year']}</p><h3>{e(title)}</h3></div>
<p>{e(note)}</p>
<div class="film-actions">
{player}<a href="{e(url)}">{'Watch on YouTube' if video else 'Watch at HAT'}</a>
<a href="#{case_id}">Read the case</a>
</div>
</div>
</article>''')
    return screenings


def relative_dir(from_output, to_output):
    import posixpath
    here = posixpath.dirname(from_output) or '.'
    there = posixpath.dirname(to_output) or '.'
    rel = posixpath.relpath(there, here)
    return '' if rel == '.' else rel + '/'


def render_edition_nav(edition):
    links = []
    for other in EDITIONS:
        if not (root / other['data']).exists():
            continue
        label = f'<span class="sr">Edition </span>{other["number"]}'
        if edition is not None and other is edition:
            links.append(f'<a href="#top" aria-current="page" title="Edition {other["number"]}{", " + other["name"] if other.get("name") else ""}">{label}</a>')
        else:
            href = relative_dir(edition['output'] if edition else INDEX_OUTPUT, other['output']) or './'
            links.append(f'<a href="{href}" title="Edition {other["number"]}{", " + other["name"] if other.get("name") else ""}">{label}</a>')
    here = edition['output'] if edition else INDEX_OUTPUT
    if not INDEX_READY:
        pass
    elif edition:
        links.append(f'<a class="index-link" href="{relative_dir(here, INDEX_OUTPUT)}" title="The Index: the whole series in one place">Index</a>')
    else:
        links.append('<a class="index-link" href="#top" aria-current="page" title="The Index: the whole series in one place">Index</a>')
    return f'<span class="edition-nav"><span class="edition-nav-label" aria-hidden="true">Editions</span>{"".join(links)}</span>'


def write_forwarding_page(edition):
    alias = edition.get('alias')
    if not alias:
        return None
    target = relative_dir(alias, edition['output']) or './'
    page = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Creator Turning Points | Edition {edition["number"]}{", " + edition["name"] if edition.get("name") else ""}</title>
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
<meta name="robots" content="noindex">
</head>
<body>
<p><a href="{target}">Open Creator Turning Points, Edition {edition["number"]}</a></p>
<script>location.replace({json.dumps(target)} + location.hash);</script>
</body>
</html>
'''
    out = root.parent / alias
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding='utf-8')
    return out


def build(edition):
    campaigns = json.loads((root / edition['data']).read_text(encoding='utf-8'))
    notes = dict(LEVEL_NOTES, **edition.get('level_notes', {}))
    prefix = edition.get('asset_prefix', '')
    compare = None
    if edition.get('compare'):
        compare = {'label': edition['compare']['label'],
                   'campaigns': json.loads((root / edition['compare']['data']).read_text(encoding='utf-8'))}
    template = (root / edition['template']).read_text(encoding='utf-8')
    css = (root / 'site.css').read_text(encoding='utf-8')
    js = (root / 'site.js').read_text(encoding='utf-8')
    r = dict(ROLE_DEFAULTS, **edition.get('roles', {}))
    modelled = sum(1 for c in campaigns if c['evidence_level'] == 'Modelled effect')
    compare_modelled = sum(1 for c in (compare or {}).get('campaigns', []) if c['evidence_level'] == 'Modelled effect')
    output = (template.replace('@@CSS@@\n', css)
              .replace('@@JS@@\n', js)
              .replace('@@ART@@', edition['art']() if edition.get('art') else '')
              .replace('@@CASES@@', '\n'.join(render_cards(campaigns, notes, edition['test_heading'], prefix, r['source_label'])))
              .replace('@@SCREENINGS@@', '\n'.join(render_screenings(campaigns, edition['screening'], prefix)))
              .replace('@@LADDER@@', '\n'.join(render_ladder(campaigns, notes, compare)))
              .replace('@@MECHANISMS@@', '\n'.join(render_mechanisms(campaigns, edition.get('mechanisms'))))
              .replace('@@TIMELINE@@', render_timeline(campaigns))
              .replace('@@FILTERS@@', render_filters(campaigns, r['roles'], r['role_label'], r['role_aria'], edition.get('mechanisms'), edition.get('mechanism_label', 'Mechanism')))
              .replace('@@MODELLED@@', str(modelled))
              .replace('@@COMPARE_MODELLED@@', str(compare_modelled))
              .replace('@@EDITION_NAV@@', render_edition_nav(edition))
              .replace('@@ROLE_GRID@@', render_role_grid(campaigns, r['roles'], r['role_aria']))
              .replace('@@SERIES_MODELLED@@', series_modelled(edition))
              .replace('@@ASSET_PREFIX@@', prefix)
              .replace('@@COUNT@@', str(len(campaigns)))
              .replace('@@FIRST_YEAR@@', str(min(c['year'] for c in campaigns)))
              .replace('@@LAST_YEAR@@', str(max(c['year'] for c in campaigns))))
    out = root.parent / edition['output']
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(output, encoding='utf-8')
    return out


# The series convention: number every edition with two digits and give it three things.
#   src/campaigns-NN.json      the cases
#   src/page-template-NN.html  the page copy
#   edition-NN/index.html      the published page (Edition 01 also sits on the home page)
# Add an entry below and run `python3 src/build.py`. The editions switcher in the menu updates itself.


# The Index joins the series once all the editions exist. It reads every case file and is built after them.
INDEX_OUTPUT = 'the-index/index.html'
INDEX_READY = True

# The series convention: number every edition with two digits and give it three things.
#   src/campaigns-NN.json      the cases
#   src/page-template-NN.html  the page copy
#   edition-NN/index.html      the published page (Edition 01 also sits on the home page)
EDITIONS = [
    {
        'number': '01', 'name': 'Fame first', 'data': 'campaigns-01.json', 'template': 'page-template-01.html',
        'output': 'index.html', 'alias': 'edition-01/index.html', 'art': play_art,
        'test_heading': 'How the outcome was recorded', 'mechanism_label': 'Shift',
        'screening': (
            ('me-at-the-zoo', 'The first video on YouTube, from Jawed Karim’s own channel. Count the seconds, then think about what followed.', 'zoo'),
            ('ok-go-treadmills', 'One take, eight treadmills and a camera on a tripod. Notice there is no record label logo anywhere.', 'treadmill'),
            ('psy-gangnam-style', 'The video that outgrew the counter. Watch how much of it is a joke about the people watching.', 'horse'),
            ('lil-nas-x-old-town-road', 'The remix film, from Lil Nas X’s channel. The song arrived through memes before it arrived on radio.', 'road'),
        ),
    },
    {
        'number': '02', 'name': 'Proof first', 'data': 'campaigns-02.json', 'template': 'page-template-02.html',
        'output': 'edition-02/index.html', 'asset_prefix': '../', 'art': proof_art,
        'test_heading': 'How the outcome was measured', 'mechanism_label': 'Shift',
        'screening': (
            ('mkbhd-humane-ai-pin', 'Watch the product tests behind the verdict, then separate the review from the later shipment figures.', 'review'),
            ('joe-wicks-pe-with-joe', 'Watch the record-setting second lesson and notice how clear instructions make joining in straightforward.', 'workout'),
            ('hyram-cerave', 'This related product comparison shows the practical review format; it does not measure the 2020 sales effect.', 'cleanser'),
            ('shane-dawson-jeffree-star', 'Look at how the reveal turns a continuing documentary into a product offer.', 'palette'),
        ),
    },
    {
        'number': '03', 'name': 'Money first', 'data': 'campaigns-03.json', 'template': 'page-template-03.html',
        'output': 'edition-03/index.html', 'asset_prefix': '../', 'art': money_art,
        'test_heading': 'How the outcome was recorded', 'mechanism_label': 'Shift', 'screening': (
            ('amanda-palmer-kickstarter', 'Watch the original 2012 pitch and how Palmer makes backing the work feel like joining it.', 'music'),
            ('patreon', 'The original Pedals video ends with Conte introducing Patreon; compare the production effort with the funding problem.', 'robot'),
            ('critical-role-vox-machina', 'Watch the original 2019 campaign launch before reading how the funding target expanded.', 'animation'),
            ('xqc-kick', 'Watch the creator announce his 2023 platform move; the clip does not independently verify the reported contract value.', 'stream'),
        ),
    },
    {
        'number': '04', 'name': 'Platform first', 'data': 'campaigns-04.json', 'template': 'page-template-04.html',
        'output': 'edition-04/index.html', 'asset_prefix': '../', 'art': platform_art,
        'test_heading': 'How the outcome was recorded', 'mechanism_label': 'Shift', 'screening': (
            ('gentle-whispering-asmr', 'Listen to the original 2011 whisper video and notice how little equipment the format needs.', 'whisper'),
            ('king-bach-vine', 'This creator sketch appeared in contemporary coverage; watch the comic timing without treating it as footage of the follower milestone.', 'comedy'),
            ('chewbacca-mom', 'This official Star Wars programme interviews Payne in May 2016; it is a contemporary follow-up, not her original Facebook Live upload.', 'mask'),
            ('dream-minecraft-manhunt', 'Watch the original 2020 episode and how a simple pursuit gives the game a clear story.', 'game'),
        ),
    },
    {
        'number': '05', 'name': 'Failure first', 'data': 'campaigns-05.json', 'template': 'page-template-05.html',
        'output': 'edition-05/index.html', 'asset_prefix': '../', 'art': failure_art,
        'test_heading': 'How the damage was recorded', 'mechanism_label': 'Shift', 'screening': (
            ('adpocalypse', 'This March 2017 creator report shows the immediate income worries during the advertiser boycott, rather than proving the full financial effect.', 'advert'),
            ('logan-paul-google-preferred', 'This January 2018 suicide-prevention follow-up came after the removed forest vlog and does not show the incident itself.', 'response'),
            ('youtube-coppa-settlement', 'Watch the official 2019 upload-setting explanation and notice which responsibilities move to creators.', 'settings'),
            ('honey-megalag', "Follow the original investigation's affiliate-link tests while keeping allegations separate from proven legal findings.", 'investigation'),
        ),
    },
    {
        'number': '06', 'name': 'Brand first', 'data': 'campaigns-06.json', 'template': 'page-template-06.html',
        'output': 'edition-06/index.html', 'asset_prefix': '../', 'art': brand_art,
        'test_heading': 'How the outcome was recorded', 'mechanism_label': 'Shift', 'screening': (),
    },
    {
        'number': '07', 'name': 'Edge first', 'data': 'campaigns-07.json', 'template': 'page-template-07.html',
        'output': 'edition-07/index.html', 'asset_prefix': '../', 'art': edge_art,
        'test_heading': 'How the outcome was recorded', 'mechanism_label': 'Shift', 'screening': (),
    },
]

# The Index: one page that reads the whole series, built from the same case files as the editions.
REGIONS = [('UK and Ireland', ('United Kingdom', 'Ireland', 'England', 'Scotland', 'Wales')), ('North America', ('United States', 'Canada', 'Bahamas')), ('Europe', ('Sweden', 'Finland', 'Italy', 'France', 'Germany', 'Spain', 'Netherlands')), ('Asia', ('China', 'Japan', 'India', 'South Korea', 'Indonesia', 'United Arab Emirates')), ('Latin America', ('Brazil', 'Mexico')), ('Africa', ('Nigeria', 'Kenya', 'Senegal')), ('Oceania', ('Australia', 'New Zealand'))]
INDUSTRIES = [
    ('Online video', ('online video', 'short video', 'social video', 'social media')),
    ('Live streaming', ('live streaming', 'livestream shopping', 'social audio')),
    ('Music', ('music',)),
    ('Comedy and entertainment', ('comedy', 'entertainment', 'drama', 'animation')),
    ('Gaming', ('gaming', 'games')),
    ('Beauty', ('beauty', 'skincare')),
    ('Food and drink', ('food', 'coffee', 'confectionery', 'frozen desserts', 'restaurants', 'drinkware')),
    ('Sport and fitness', ('fitness', 'football', 'boxing', 'sports entertainment')),
    ('Publishing and audio', ('publishing', 'podcasting', 'newsletters', 'blogging')),
    ('Education', ('education',)),
    ('Commerce', ('shopping', 'payments', 'household', 'events', 'travel', 'technology')),
    ('Rules and policy', ('regulation', 'privacy', 'advertising')),
]
EVIDENCE_COLOURS = {'Modelled effect': '#557400', 'Sales trend': '#7c9a1e', 'Survey': '#a5c31c', 'Reach only': '#d3d1c5', 'Archival': '#a8aa9d'}
LESSONS = [
    ('Creators find the use before the platform does.',
     'Platforms build features. Creators work out what they are for. A programmer turned Twitch chat into a controller, a mother in a car park showed Facebook what live video could be, and a factory worker’s shrug became TikTok’s most followed account.',
     [('04', 'twitch-plays-pokemon'), ('04', 'chewbacca-mom'), ('04', 'dj-khaled-snapchat'), ('01', 'numa-numa'), ('07', 'khaby-lame')]),
    ('Attention is easy to count. Proof is rare.',
     'None of the {total} cases has a modelled effect. {reach} rest on attention alone and {archival} are archival. The best proof came from outside the creator economy: book tills, grocery baskets and company results.',
     [('02', 'pinch-of-nom'), ('02', 'emily-mariko-salmon-bowl'), ('02', 'colleen-hoover-booktok'), ('01', 'psy-gangnam-style'), ('06', 'hot-ones')]),
    ('Revenue that grows with the audience lasts.',
     'Fixed funds paid each creator less as more joined, and were replaced. Shared advertising and money paid directly by fans grew with the audience, and became the creator economy’s foundations.',
     [('03', 'youtube-partner-program'), ('03', 'tiktok-creator-fund'), ('03', 'patreon'), ('04', 'snapchat-spotlight'), ('01', 'kai-cenat-mafiathon')]),
    ('Own a line to your audience that no platform controls.',
     'Vine closed, India banned TikTok, America lost it for fourteen hours and advertisers left YouTube overnight. The creators who recovered fastest could reach their audience somewhere else.',
     [('05', 'vine-shut-down'), ('04', 'india-tiktok-ban'), ('05', 'tiktok-goes-dark'), ('05', 'adpocalypse'), ('03', 'alex-cooper-call-her-daddy')]),
    ('The creators who lasted own something.',
     'Ownership is joint top of the archive’s nine shifts, with Format and Trust, at {ownership} cases each. A subscription, a newsletter, a chocolate bar or a company bought back from its owners turned an audience into an asset.',
     [('06', 'feastables'), ('06', 'michelle-phan-ipsy'), ('06', 'smosh-bought-back'), ('03', 'sinocism-substack'), ('07', 'austin-li-singles-day')]),
    ('Trust is the asset, and it can be spent.',
     'Trust is the shift behind {trust} cases. A reviewer’s verdict sank a gadget and lifted a cleanser. The same credibility, lent to a fake festival or a doubtful sponsor, cost creators their audiences’ faith.',
     [('02', 'mkbhd-humane-ai-pin'), ('02', 'hyram-cerave'), ('05', 'fyre-festival'), ('05', 'honey-megalag'), ('05', 'mikayla-mascara')]),
]
CASE_CREATORS = {'vidcon': ('Hank Green', 'John Green'), 'ksi-logan-paul': ('KSI', 'Logan Paul'), 'variety-teen-survey': ('Smosh',), 'forbes-highest-paid-youtubers': ('PewDiePie',), 'shane-dawson-jeffree-star': ('Shane Dawson', 'Jeffree Star')}
PARTY_GROUPS = {}
PARTY_SKIP = {'YouTube’s creators'}
PARTY_LOGO_DIR = Path("assets/creator-logos")
PARTY_LOGOS = {}
PARTY_NOTES = {
    'PewDiePie': 'The most subscribed individual on YouTube, the top of the first Forbes rich list, and the creator Disney dropped. His audience outlasted every brand deal.',
    'MrBeast': 'A channel that overtook a record label, and a chocolate bar that earned more than the videos.',
    'Kylie Jenner': 'One post linked to a fall in Snap’s share price, and a cosmetics line Coty paid $600 million to control.',
    'Smosh': 'Top of a 2014 survey of American teenagers, and bought back by its founders eighteen years after they started it.',
    'Logan Paul': 'A boxing match that sold 773,000 paid streams, and the vlog that cost him YouTube’s premium programme.',
}
NUMBER_WORDS = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 100: 'A hundred'}


def region_of(place):
    head = place.split(',')[0]
    if head.strip().lower().startswith(('global', 'online')) and 'United States' not in place:
        return 'Global'
    hits = [(place.find(k), name) for name, keys in REGIONS for k in keys if k in place]
    return min(hits)[1] if hits else 'Global'


def industries_of(sector):
    s = sector.lower()
    words = set(re.findall(r"[a-z\-]+", s))
    return [name for name, keys in INDUSTRIES if any((k in s) if ' ' in k else (k in words) for k in keys)] or ['Other']


def decade_of(year):
    return f'{year // 10 * 10}s'


def load_series():
    series = []
    for edition in EDITIONS:
        if not (root / edition['data']).exists():
            continue
        campaigns = json.loads((root / edition['data']).read_text(encoding='utf-8'))
        template = (root / edition['template']).read_text(encoding='utf-8')
        finding = re.search(r'<h2 id="finding-title">(.*?)</h2>', template)
        series.append({'edition': edition, 'campaigns': campaigns, 'finding': finding.group(1) if finding else ''})
    return series


def case_href(edition, case_id):
    return f'{relative_dir(INDEX_OUTPUT, edition["output"]) or "./"}#{case_id}'


def build_index():
    series = load_series()
    by_number = {s['edition']['number']: s for s in series}
    everything = [(s['edition'], c) for s in series for c in s['campaigns']]
    total = len(everything)
    modelled = sum(1 for _, c in everything if c['evidence_level'] == 'Modelled effect')
    years = [c['year'] for _, c in everything]
    regions = collections.Counter(region_of(c['place']) for _, c in everything)
    decades = collections.Counter(decade_of(c['year']) for _, c in everything)
    levels = collections.Counter(c['evidence_level'] for _, c in everything)
    mechs = collections.Counter(c['mechanism'] for _, c in everything)
    roles = collections.Counter(c['data_role'] for _, c in everything)
    inds = collections.Counter(i for _, c in everything for i in industries_of(c['sector']))
    deals = sum(1 for _, c in everything if c.get('deal_value'))
    money_mod = 0
    e02_mod = sum(1 for c in by_number['02']['campaigns'] if c['evidence_level'] == 'Modelled effect') if '02' in by_number else 0

    cards = []
    for s in series:
        ed, cs = s['edition'], s['campaigns']
        n_mod = sum(1 for c in cs if c['evidence_level'] == 'Modelled effect')
        href = relative_dir(INDEX_OUTPUT, ed['output']) or './'
        cards.append(f'<a class="ed-card" href="{href}"><span class="ed-num">{ed["number"]}</span><span class="ed-name">{e(ed["name"])}</span>'
                     f'<span class="ed-finding">{e(s["finding"])}</span><span class="ed-meta small">{len(cs)} cases · {min(c["year"] for c in cs)} to {max(c["year"] for c in cs)} · {n_mod or "no"} modelled</span></a>')

    rows = []
    for s in series:
        ed, cs = s['edition'], s['campaigns']
        segs = []
        for level in LEVELS:
            n = sum(1 for c in cs if c['evidence_level'] == level)
            if n:
                dark = level in ('Modelled effect', 'Sales trend')
                segs.append(f'<span class="ev-seg{" dark" if dark else ""}" style="--n:{n};background:{EVIDENCE_COLOURS[level]}" title="{e(level)}: {n}">{n}<span class="sr"> {e(level)}</span></span>')
        rows.append(f'<div class="ev-row"><span class="ev-label"><a href="{relative_dir(INDEX_OUTPUT, ed["output"]) or "./"}">Edition {ed["number"]}</a> <span>{e(ed["name"])}</span></span><span class="ev-bar">{"".join(segs)}</span></div>')
    legend = ''.join(f'<span><i style="background:{EVIDENCE_COLOURS[l]}"></i>{e(l)} <b>{levels[l]}</b></span>' for l in LEVELS)

    lessons = []
    for i, (title, text, refs) in enumerate(LESSONS, 1):
        chip_html = []
        for num, cid in refs:
            s = by_number[num]
            c = next(c for c in s['campaigns'] if c['id'] == cid)
            chip_html.append(f'<a class="lesson-chip" href="{case_href(s["edition"], cid)}"><span class="small">{num}</span> {e(c["brand"])}</a>')
        text = text.format(total=total, reach=levels['Reach only'], archival=levels['Archival'], sales=levels['Sales trend'],
                           ownership=mechs['Ownership'], trust=mechs['Trust'], modelled=modelled, deals=deals)
        lessons.append(f'<article class="lesson"><p class="lesson-num small">{i:02d}</p><h3>{e(title)}</h3><p>{e(text)}</p><div class="lesson-chips">{"".join(chip_html)}</div></article>')

    groups = collections.defaultdict(list)
    for ed, c in everything:
        for party in CASE_CREATORS.get(c['id'], (c['brand'],)):
            party = PARTY_GROUPS.get(party.strip(), party.strip())
            if party not in PARTY_SKIP:
                groups[party].append((ed, c))
    recurring = sorted(((p, v) for p, v in groups.items() if len({ed['number'] for ed, _ in v}) > 1),
                       key=lambda pv: (-len({ed['number'] for ed, _ in pv[1]}), -len(pv[1]), pv[0]))
    missing = [p for p, _ in recurring if p not in PARTY_NOTES]
    assert not missing, f'Add a note for these partners: {missing}'
    partners = []
    for p, v in recurring:
        logo_html = ''
        if p in PARTY_LOGOS:
            logo = PARTY_LOGO_DIR / f'{PARTY_LOGOS[p]}.webp'
            if (root.parent / logo).is_file():
                logo_html = f'<img class="brand-logo" src="../{logo.as_posix()}" alt="{e(p)} logo" width="82" height="62" loading="lazy" decoding="async">' 
        items = ''.join(f'<li><a href="{case_href(ed, c["id"])}"><span class="small">Edition {ed["number"]}</span> {e(c["brand"])} <span class="yr">{c["year"]}</span></a></li>'
                        for ed, c in sorted(v, key=lambda x: x[1]['year']))
        partners.append(
            f'<article class="brand-row"><div class="brand-heading">'
            f'{logo_html}'
            f'<div><h3>{e(p)}</h3><p>{e(PARTY_NOTES[p])}</p></div></div><ol>{items}</ol></article>'
        )

    region_order = [r for r, _ in REGIONS] + ['Global']
    filt = {
        'edition': ('Edition', [s['edition']['number'] for s in series]),
        'role': ('Platform', [r for r in ROLES if roles[r]]),
        'industry': ('Industry', [i for i, _ in INDUSTRIES if inds[i]] + (['Other'] if inds['Other'] else [])),
        'region': ('Where', [r for r in region_order if regions[r]]),
        'evidence': ('Evidence', [l for l in LEVELS if levels[l]]),
    }
    filters = ''.join(f'<div class="filter-row" role="group" aria-label="{label}"><span class="small">{label}</span>{chips(g, vals)}</div>' for g, (label, vals) in filt.items())
    lines = []
    for ed, c in sorted(everything, key=lambda x: (x[1]['year'], x[1]['brand'])):
        thumbnail = campaign_image(c, 'ix-thumbnail', '../')
        video_url = c['creative'].get('url')
        watch_label = 'Read' if 'youtube.com/watch' not in (video_url or '') else 'Watch report' if any(w in c['creative'].get('medium', '').lower() for w in ('reporting', 'interview', 'review,')) else 'Watch'
        watch = (f'<a class="ix-watch" href="{e(video_url)}" aria-label="{e(c["creative"]["label"])}" title="{e(c["creative"]["label"])}">{watch_label} <span aria-hidden="true">↗</span></a>'
                 if video_url else '')
        lines.append(f'<li class="ix-case" data-edition="{ed["number"]}" data-role="{e(c["data_role"])}" data-industry="{e("|".join(industries_of(c["sector"])))}" data-region="{e(region_of(c["place"]))}" data-evidence="{e(c["evidence_level"])}">'
                     f'<a class="ix-case-link" href="{case_href(ed, c["id"])}"><span class="ix-visual">{thumbnail}<span class="ix-year">{c["year"]}</span></span><span class="ix-main"><span class="ix-brand small">{e(c["brand"])} · {e(c["mechanism"])}</span>'
                     f'<span class="ix-title">{e(c["title"])}</span><span class="ix-place">{e(c["place"])} · {e(c["data_role"])}</span></span>'
                     f'<span class="ix-side"><span class="ix-ed">Edition {ed["number"]}, {e(ed["name"])}</span>{meter(c["evidence_level"])}</span></a>{watch}</li>')

    share = lambda n: f'{round(n / total * 100)}%'
    uk, na = regions['UK and Ireland'], regions['North America']
    recent = sum(n for d, n in decades.items() if int(d[:4]) >= 2010)
    early = sum(n for d, n in decades.items() if int(d[:4]) < 1990)
    early_text = f'Only {str(NUMBER_WORDS.get(early, early)).lower()} {"comes" if early == 1 else "come"} from before 1990'
    gaps = [
        ('Where the work began', f'{uk} cases use UK or Irish working locations and {na} North American locations. Europe has {regions["Europe"]}, Asia {regions["Asia"]}, Latin America {regions["Latin America"]}, Africa {regions["Africa"]} and Oceania {regions["Oceania"]}. Locations describe the moment, not nationality or the full audience geography.'),
        ('When the record begins', f'{recent} of {total} cases date from 2010 or later. Earlier web communities, non-digital creator practices and lost uploads are underrepresented. This is a selected digital archive rather than a complete history.'),
        ('What the evidence can support', f'{levels["Sales trend"]} cases show a Sales trend, {levels["Reach only"]} Reach only and {levels["Archival"]} Archival evidence. There are {modelled} Modelled effect and {levels["Survey"]} Survey cases. Those absences limit any causal conclusion about creator effectiveness.'),
        ('Whose work is less visible', 'Public records favour successful, English-searchable examples. Unpaid labour, smaller creators, private contracts, platform moderation and production teams are harder to see. Gross pledges and platform counts reveal less about sustainable net income than the headlines suggest.'),
    ]
    gap_html = ''.join(f'<div><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in gaps)
    reads = ', '.join(f'<a href="{relative_dir(INDEX_OUTPUT, s["edition"]["output"]) or "./"}">Edition {s["edition"]["number"]}, {e(s["edition"]["name"])}</a>' for s in series)

    template = (root / 'page-template-index.html').read_text(encoding='utf-8')
    css = (root / 'site.css').read_text(encoding='utf-8')
    output = (template.replace('@@CSS@@\n', css)
              .replace('@@EDITION_NAV@@', render_edition_nav(None))
              .replace('@@EDITION_COUNT@@', str(len(series)))
              .replace('@@EDITION_WORD@@', NUMBER_WORDS.get(len(series), str(len(series))))
              .replace('@@TOTAL_WORD@@', NUMBER_WORDS.get(total, str(total)))
              .replace('@@TOTAL@@', str(total))
              .replace('@@MODELLED@@', str(modelled))
              .replace('@@E02_MODELLED_WORD@@', NUMBER_WORDS.get(e02_mod, str(e02_mod)))
              .replace('@@DEALS@@', str(deals))
              .replace('@@FIRST_YEAR@@', str(min(years)))
              .replace('@@LAST_YEAR@@', str(max(years)))
              .replace('@@EDITION_CARDS@@', '\n'.join(cards))
              .replace('@@EVIDENCE_ROWS@@', '\n'.join(rows))
              .replace('@@EVIDENCE_LEGEND@@', legend)
              .replace('@@LESSONS@@', '\n'.join(lessons))
              .replace('@@PARTNER_COUNT@@', str(len(recurring)))
              .replace('@@PARTNERS@@', '\n'.join(partners))
              .replace('@@FILTERS@@', filters)
              .replace('@@CASES@@', '\n'.join(lines))
              .replace('@@GAPS@@', gap_html)
              .replace('@@READS@@', reads))
    assert '@@' not in output, re.findall(r'@@\w+@@', output)
    out = root.parent / INDEX_OUTPUT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(output, encoding='utf-8')
    return out

if __name__ == '__main__':
    import sys
    wanted = sys.argv[1:]
    for edition in EDITIONS:
        if wanted and edition['output'] not in wanted:
            continue
        if not (root / edition['data']).exists():
            continue
        print('Built', build(edition).relative_to(root.parent))
        forwarding = write_forwarding_page(edition)
        if forwarding:
            print('Built', forwarding.relative_to(root.parent), '(forwards to', edition['output'] + ')')
    if INDEX_READY and (not wanted or INDEX_OUTPUT in wanted):
        print('Built', build_index().relative_to(root.parent))
