# Editorial illustrations for Creator Turning Points, one per edition.
# Palette: ink #1D1A2C, vermilion #E2533F, deep red #A8352A, lilac #E8E1F0, saffron #D99A2B, paper #F7F4EF.

SERIF = "'Fraunces', Georgia, serif"
SANS = "'Instrument Sans', Arial, sans-serif"
INK, RED, DEEP, LILAC, SAFFRON, PAPER = '#1D1A2C', '#E2533F', '#A8352A', '#E8E1F0', '#D99A2B', '#F7F4EF'


def _frame(title, body):
    return (f'<svg viewBox="0 0 920 560" preserveAspectRatio="xMidYMid slice" role="img" aria-labelledby="art-title">'
            f'<title id="art-title">{title}</title>'
            f'<defs><filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#000" flood-opacity=".4"/></filter></defs>'
            f'<path d="M0 0h920v560H0z" fill="{INK}"/>{body}</svg>')


def _label(text, y=52):
    return f'<text x="460" y="{y}" text-anchor="middle" font-family="{SANS}" font-size="14" letter-spacing="3" fill="{LILAC}">{text}</text>'


def play_art():
    # A play button the size of a room, with the view counter underneath ticking past where it was built to stop.
    grid = ''.join(f'<path d="M{x} 0v560"/>' for x in range(40, 920, 40))
    return _frame(
        'Illustration of a large play button inside a video frame. Underneath, a view counter reads 2,147,483,647, the number YouTube’s counter was built to stop at.',
        f'<g opacity=".14" stroke="{LILAC}" stroke-width="1">{grid}</g>'
        f'<g filter="url(#sh)"><rect x="190" y="96" width="540" height="304" rx="22" fill="#2A2640"/>'
        f'<circle cx="460" cy="248" r="92" fill="{RED}"/><path d="M432 200l78 48-78 48z" fill="{PAPER}"/>'
        f'<rect x="222" y="364" width="476" height="6" rx="3" fill="#4A4562"/><rect x="222" y="364" width="300" height="6" rx="3" fill="{RED}"/><circle cx="522" cy="367" r="9" fill="{RED}"/></g>'
        f'<text x="460" y="462" text-anchor="middle" font-family="{SERIF}" font-size="44" fill="{PAPER}">2,147,483,647 views</text>'
        f'<text x="460" y="504" text-anchor="middle" font-family="{SERIF}" font-size="22" font-style="italic" fill="{LILAC}">The counter was not built for this.</text>'
        + _label('EDITION 01 / FAME FIRST'))


def proof_art():
    # An audience retention curve, the creator's own proof, with one moment circled.
    pts = [(120, 170), (170, 215), (220, 232), (280, 240), (340, 250), (400, 256), (460, 262), (520, 236), (580, 270), (640, 282), (700, 296), (760, 310), (800, 318)]
    path = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
    area = path + ' L800 420 L120 420 Z'
    return _frame(
        'Illustration of an audience retention graph. The line falls slowly across the video, then rises at one point, which is circled and labelled as the moment people rewatched.',
        f'<g filter="url(#sh)"><rect x="80" y="90" width="760" height="380" rx="14" fill="{PAPER}"/></g>'
        f'<text x="120" y="138" font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="3" fill="{DEEP}">AUDIENCE RETENTION</text>'
        + ''.join(f'<path d="M120 {y}h680" stroke="#d9d3e3" stroke-width="1"/>' for y in (170, 250, 330, 420))
        + f'<path d="{area}" fill="{LILAC}"/><path d="{path}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        f'<circle cx="520" cy="236" r="30" fill="none" stroke="{RED}" stroke-width="4"/>'
        f'<text x="560" y="210" font-family="{SERIF}" font-size="22" font-style="italic" fill="{DEEP}">They watched it again.</text>'
        f'<text x="120" y="450" font-family="{SANS}" font-size="12" letter-spacing="2" fill="#6b6578">0:00</text>'
        f'<text x="800" y="450" text-anchor="end" font-family="{SANS}" font-size="12" letter-spacing="2" fill="#6b6578">END</text>'
        + _label('EDITION 02 / PROOF FIRST', 54))


def money_art():
    # A payout statement: the creator's share and the platform's share, with the line for the brand left blank.
    return _frame(
        'Illustration of a creator payout statement. A bar is split into the creator’s share, 55 per cent, and the platform’s share, 45 per cent. A line underneath for everything else is left blank.',
        f'<g transform="rotate(-3 460 290)" filter="url(#sh)"><rect x="210" y="70" width="500" height="430" fill="{PAPER}"/>'
        f'<text x="250" y="124" font-family="{SANS}" font-size="13" letter-spacing="3" fill="{DEEP}">EDITION 03 / MONEY FIRST</text>'
        f'<text x="250" y="174" font-family="{SERIF}" font-size="36" fill="{INK}">Creator payout</text>'
        f'<rect x="250" y="214" width="231" height="56" fill="{RED}"/><rect x="481" y="214" width="189" height="56" fill="#cfc6dc"/>'
        f'<text x="266" y="250" font-family="{SANS}" font-size="18" font-weight="700" fill="{PAPER}">CREATOR 55%</text>'
        f'<text x="497" y="250" font-family="{SANS}" font-size="18" font-weight="700" fill="{INK}">PLATFORM 45%</text>'
        + ''.join(f'<rect x="250" y="{304 + i * 24}" width="{380 - i * 50}" height="7" fill="{LILAC}"/>' for i in range(4))
        + f'<text x="250" y="440" font-family="{SANS}" font-size="14" font-weight="700" letter-spacing="2" fill="{INK}">EVERYTHING ELSE</text>'
        f'<line x1="430" y1="442" x2="670" y2="442" stroke="{INK}" stroke-width="2" stroke-dasharray="6 6"/>'
        f'<text x="250" y="476" font-family="{SERIF}" font-size="18" font-style="italic" fill="{DEEP}">Merch, memberships, deals, a company.</text></g>')


def platform_art():
    # Screens turning on their side: a wide screen, then a tall one, then a live one.
    return _frame(
        'Illustration of three screens in a row: a wide landscape video, a square photo and a tall vertical video with a red live badge. Each is taller and narrower than the last.',
        f'<g filter="url(#sh)">'
        f'<rect x="96" y="196" width="260" height="146" rx="12" fill="#2A2640" stroke="{LILAC}" stroke-width="3"/>'
        f'<path d="M210 244l40 25-40 25z" fill="{LILAC}"/>'
        f'<rect x="396" y="160" width="190" height="190" rx="12" fill="#2A2640" stroke="{LILAC}" stroke-width="3"/>'
        f'<circle cx="491" cy="255" r="44" fill="none" stroke="{SAFFRON}" stroke-width="5"/>'
        f'<rect x="626" y="96" width="196" height="348" rx="26" fill="#2A2640" stroke="{PAPER}" stroke-width="4"/>'
        f'<rect x="650" y="124" width="64" height="26" rx="5" fill="{RED}"/><text x="682" y="142" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="2" fill="{PAPER}">LIVE</text>'
        + ''.join(f'<circle cx="{700 + (i % 3) * 30}" cy="{360 - i * 34}" r="9" fill="{RED}" opacity="{.35 + i * .12}"/>' for i in range(6))
        + '</g>'
        f'<text x="460" y="508" text-anchor="middle" font-family="{SERIF}" font-size="26" font-style="italic" fill="{PAPER}">Every few years the screen turns.</text>'
        + _label('EDITION 04 / PLATFORM FIRST'))


def failure_art():
    # A video that is no longer there.
    return _frame(
        'Illustration of a video player with a cracked screen and a message reading this video is no longer available. A yellow dollar sign beside it has a line through it.',
        f'<g filter="url(#sh)"><rect x="150" y="100" width="560" height="316" rx="18" fill="#121019"/>'
        f'<path d="M150 210l190 40 80-60 120 90 170-30" fill="none" stroke="#3A3550" stroke-width="2"/>'
        f'<path d="M420 190l-40 120 90 60" fill="none" stroke="#3A3550" stroke-width="2"/>'
        f'<circle cx="430" cy="232" r="34" fill="none" stroke="{LILAC}" stroke-width="4"/><path d="M430 214v24M430 248v2" stroke="{LILAC}" stroke-width="5" stroke-linecap="round"/>'
        f'<text x="430" y="320" text-anchor="middle" font-family="{SANS}" font-size="20" fill="{LILAC}">This video is no longer available</text></g>'
        f'<g filter="url(#sh)"><circle cx="760" cy="420" r="62" fill="{SAFFRON}"/>'
        f'<text x="760" y="446" text-anchor="middle" font-family="{SERIF}" font-size="74" font-weight="600" fill="{INK}">$</text>'
        f'<path d="M712 372l96 96" stroke="{RED}" stroke-width="10" stroke-linecap="round"/></g>'
        + _label('EDITION 05 / FAILURE FIRST'))


def brand_art():
    # A product box with no logo on it, only a creator's handle.
    return _frame(
        'Illustration of a product box on a shelf. Where a company logo would usually be, the label carries only a creator’s handle, written as at-symbol, your name.',
        f'<rect x="0" y="420" width="920" height="140" fill="#2A2640"/><rect x="0" y="418" width="920" height="6" fill="{SAFFRON}"/>'
        f'<g filter="url(#sh)"><path d="M300 150l160-60 160 60v270H300z" fill="{RED}"/><path d="M300 150l160-60 160 60-160 60z" fill="#ef7a68"/>'
        f'<path d="M460 210v210" stroke="{DEEP}" stroke-width="2"/>'
        f'<rect x="330" y="250" width="110" height="120" fill="{PAPER}"/><text x="385" y="320" text-anchor="middle" font-family="{SERIF}" font-size="30" font-style="italic" fill="{INK}">@you</text></g>'
        f'<rect x="120" y="300" width="120" height="120" fill="#3A3550"/><rect x="680" y="270" width="130" height="150" fill="#3A3550"/>'
        f'<text x="460" y="500" text-anchor="middle" font-family="{SERIF}" font-size="26" font-style="italic" fill="{PAPER}">The audience came first. The product followed.</text>'
        + _label('EDITION 06 / BRAND FIRST'))


def edge_art():
    # A dotted globe, lit from outside the usual places.
    dots = []
    import math
    for lat in range(-60, 75, 12):
        r = 190 * math.cos(math.radians(lat))
        y = 280 - 190 * math.sin(math.radians(lat))
        n = max(4, int(r / 14))
        for i in range(n):
            x = 460 + r * math.cos(math.pi * i / (n - 1)) if n > 1 else 460
            dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{LILAC}" opacity=".35"/>')
    lit = [(520, 330), (600, 250), (360, 300), (430, 360), (640, 300), (300, 230), (560, 200)]
    glow = ''.join(f'<circle cx="{x}" cy="{y}" r="11" fill="{RED}"/><circle cx="{x}" cy="{y}" r="22" fill="none" stroke="{SAFFRON}" stroke-width="2" opacity=".7"/>' for x, y in lit)
    return _frame(
        'Illustration of a globe made of small dots, with seven bright points lit up away from Britain and North America.',
        f'<circle cx="460" cy="280" r="196" fill="#24203a"/>{"".join(dots)}{glow}'
        f'<text x="460" y="526" text-anchor="middle" font-family="{SERIF}" font-size="26" font-style="italic" fill="{PAPER}">Built far from the usual places.</text>'
        + _label('EDITION 07 / EDGE FIRST', 44))
