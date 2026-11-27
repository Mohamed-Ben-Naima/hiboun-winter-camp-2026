"""Teaser «من البحر… لوين؟» — builds the animated page that render.py films.

The Reel is one HTML page (1080x1920) with a seek(t, variant) function: every frame is drawn
from the time alone, so any frame can be checked or re-rendered on its own.

  python make_teaser.py            -> _build/teaser.html
  python render.py check           -> _build/check/*.jpg (key frames)
  python render.py                 -> ../../exports/teaser/*.mp4

Story (teaser, 15.5 s, loops):
  0.0  Hook     night sea at Mahdia, the lighthouse turning. «من البحر…» then «لوين؟» slams in.
  2.1  Journey  the camera tilts down the map: beach, Sahel olive groves, steppe, dunes, an oasis
                with a «؟» pin. The scout trail draws itself along. «4 تلميحات».
  4.75 Clues    a scout logbook page; four polaroids land one by one, vague to precise:
                palms (real photo) · Deglet Nour dates · brick patterns · the salt lake.
  11.15 Ask     «عرفتوها؟ اكتبوها في الكومنتار»  (teaser)   |  stamp «دقاش · توزر» (reveal)
  13.1 End      camp name, dates, «الحكاية قريب تبدا…»; fades back into the first frame.
"""
import json, math, random, shutil
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUILD = HERE / '_build'
ID = ROOT / '03-identity'

C = dict(night='#141833', night2='#1A2150', sky='#2A3470', cream='#F6EBD7', sand='#D9CBB0',
         amber='#F2B544', ember='#E2552D', emberdeep='#B83D1C', brick='#C98E4E', brickhi='#E9C48A',
         mortar='#7A4A22', sea='#7FB3E0', seadeep='#2C5F8A', palm='#3B4A8C', ink='#241F3A')

W, WH = 1080, 5120          # stage width, world height (sky+sea on top, the map below)
CAM_END = 3200              # how far the camera travels down the world

rnd = random.Random(2026)

# ---------------------------------------------------------------- helpers

def catmull(points, n=24):
    out = []
    P = [points[0]] + points + [points[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
        for k in range(n):
            t = k / n; t2, t3 = t*t, t*t*t
            x = 0.5*((2*p1[0]) + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2 + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y = 0.5*((2*p1[1]) + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2 + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    out.append(points[-1]); return out

def pathd(poly):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in poly)

def x3d(face, side, depth=16, blur=True):
    """Chunky extruded type, like a sticker standing up off the page."""
    sh = ','.join(f'{i}px {i}px 0 {side}' for i in range(1, depth+1))
    if blur:
        sh += f',{depth+6}px {depth+12}px 28px rgba(5,8,25,.55)'
    return f'color:{face};text-shadow:{sh}'

TRAIL_PTS = [(770, 1846), (650, 2040), (440, 2270), (380, 2520), (560, 2770), (730, 3010),
             (650, 3270), (430, 3490), (400, 3730), (560, 3970), (640, 4190), (540, 4392)]
TRAIL = catmull(TRAIL_PTS, 30)
PIN = TRAIL_PTS[-1]

def near_trail(x, y, d):
    return any((x-px)**2 + (y-py)**2 < d*d for px, py in TRAIL[::3])

# ---------------------------------------------------------------- the world (S1-S2)

def world_svg():
    g = []
    a = g.append
    a(f'''<svg id="worldsvg" width="{W}" height="{WH}" viewBox="0 0 {W} {WH}" style="position:absolute;left:0;top:0">
<defs>
<linearGradient id="gSky" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1160">
 <stop offset="0" stop-color="#090D25"/><stop offset=".55" stop-color="#141833"/><stop offset=".86" stop-color="#232C62"/><stop offset="1" stop-color="#3A4A8C"/></linearGradient>
<radialGradient id="gGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{C['amber']}" stop-opacity=".22"/><stop offset="1" stop-color="{C['amber']}" stop-opacity="0"/></radialGradient>
<radialGradient id="gMoonGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFF3D6" stop-opacity=".32"/><stop offset="1" stop-color="#FFF3D6" stop-opacity="0"/></radialGradient>
<linearGradient id="gSea" gradientUnits="userSpaceOnUse" x1="0" y1="1150" x2="0" y2="1850">
 <stop offset="0" stop-color="#2B3F7C"/><stop offset=".35" stop-color="#1D2E62"/><stop offset="1" stop-color="#122049"/></linearGradient>
<linearGradient id="gLand" gradientUnits="userSpaceOnUse" x1="0" y1="1900" x2="0" y2="{WH}">
 <stop offset="0" stop-color="#1A2350"/><stop offset=".3" stop-color="#262C5A"/><stop offset=".48" stop-color="#4A3D5E"/>
 <stop offset=".62" stop-color="#8A5A44"/><stop offset=".74" stop-color="#B57A48"/><stop offset="1" stop-color="#C98E4E"/></linearGradient>
<linearGradient id="gBeamL" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#FFD98A" stop-opacity=".42"/><stop offset=".55" stop-color="#FFD98A" stop-opacity=".12"/><stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></linearGradient>
<linearGradient id="gBeamR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFD98A" stop-opacity=".42"/><stop offset=".55" stop-color="#FFD98A" stop-opacity=".12"/><stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></linearGradient>
<linearGradient id="gRoad" gradientUnits="userSpaceOnUse" x1="0" y1="1840" x2="0" y2="4400"><stop offset="0" stop-color="{C['sea']}"/><stop offset="1" stop-color="{C['amber']}"/></linearGradient>
<clipPath id="cSky"><rect x="0" y="0" width="{W}" height="1152"/></clipPath>
<mask id="mMoon"><circle cx="190" cy="300" r="62" fill="#fff"/><circle cx="216" cy="282" r="54" fill="#000"/></mask>
<mask id="mTrail"><path id="trailMaskPath" d="{pathd(TRAIL)}" fill="none" stroke="#fff" stroke-width="60" stroke-linecap="round"/></mask>
</defs>
<rect width="{W}" height="1160" fill="url(#gSky)"/>
<ellipse cx="330" cy="1150" rx="760" ry="170" fill="url(#gGlow)"/>''')
    # stars
    for i in range(150):
        x, y = rnd.uniform(10, W-10), rnd.uniform(10, 1080)**1.0
        y = 1080 * (rnd.random() ** 1.35)
        r = rnd.choice([1.2, 1.5, 1.8, 2.2, 2.6]) if rnd.random() > .08 else 3.4
        a(f'<circle class="tw" data-p="{rnd.uniform(0,6.28):.2f}" data-s="{rnd.uniform(1.5,4.5):.2f}" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#FFF3D6"/>')
    for x, y, s in [(880, 210, 1.0), (640, 120, .7), (420, 430, .6), (960, 520, .55), (90, 640, .6), (760, 330, .45)]:
        a(f'<path class="tw" data-p="{rnd.uniform(0,6.28):.2f}" data-s="2.2" transform="translate({x} {y}) scale({s})" '
          f'd="M0,-22 C2,-6 6,-2 22,0 C6,2 2,6 0,22 C-2,6 -6,2 -22,0 C-6,-2 -2,-6 0,-22Z" fill="{C["amber"]}"/>')
    # moon
    a('<circle cx="190" cy="300" r="190" fill="url(#gMoonGlow)"/>')
    a('<circle cx="190" cy="300" r="62" fill="#FFF1CF" mask="url(#mMoon)"/>')
    # lighthouse beam (behind the tower, clipped to the sky)
    lx, ly = 975, 860
    a(f'<g clip-path="url(#cSky)"><g id="beam">'
      f'<path d="M{lx},{ly-6} L{lx-1600},{ly-210} L{lx-1600},{ly+170} L{lx},{ly+6}Z" fill="url(#gBeamL)"/>'
      f'<path d="M{lx},{ly-6} L{lx+1600},{ly-210} L{lx+1600},{ly+170} L{lx},{ly+6}Z" fill="url(#gBeamR)"/></g></g>')
    # sea
    a(f'<rect x="0" y="1150" width="{W}" height="720" fill="url(#gSea)"/>')
    a(f'<line x1="0" y1="1151" x2="{W}" y2="1151" stroke="#5E78B8" stroke-width="2" opacity=".6"/>')
    # moon reflection
    for i in range(16):
        y = 1165 + i*30 + rnd.uniform(-6, 6)
        w = 18 + i*4 + rnd.uniform(-6, 10)
        x = 190 + rnd.uniform(-20, 20)
        a(f'<rect class="rf" data-p="{rnd.uniform(0,6.28):.2f}" x="{x-w/2:.1f}" y="{y:.1f}" width="{w:.1f}" height="{2+i*0.25:.1f}" rx="2" fill="#FFF1CF"/>')
    # wave rows (animated in JS)
    for k in range(12):
        f = (k+1)/12
        y = 1150 + 700 * (f ** 1.7)
        P = 50 + 190*f; A = 2 + 9*f; sw = 1.4 + 3.6*f
        n = int((W + 4*P) / P) + 2
        d = f'M{-2*P:.1f},{y:.1f} ' + ' '.join(f'q{P/4:.1f},{-A:.1f} {P/2:.1f},0 t{P/2:.1f},0' for _ in range(n))
        a(f'<path class="wave" data-P="{P:.1f}" data-v="{(14+40*f)*(1 if k%2 else -1):.1f}" d="{d}" fill="none" stroke="{C["sea"]}" '
          f'stroke-width="{sw:.1f}" stroke-linecap="round" stroke-dasharray="{P*.55:.1f} {P*.45:.1f}" opacity="{.22+.5*f:.2f}"/>')
    # a Mahdia fishing boat (flouka) with its lantern
    a(f'<g id="boat" data-x="360" data-y="1430">'
      f'<circle cx="18" cy="-74" r="46" fill="url(#gGlow)"/>'
      f'<path d="M-92,-18 L96,-18 C84,6 60,16 40,16 L-60,16 C-78,10 -88,0 -92,-18Z" fill="#0C1130"/>'
      f'<path d="M-92,-18 L96,-18 L92,-12 L-88,-12Z" fill="{C["ember"]}"/>'
      f'<path d="M4,-18 L4,-118" stroke="#0C1130" stroke-width="5"/>'
      f'<path d="M8,-112 L8,-30 L70,-30Z" fill="{C["cream"]}" opacity=".92"/>'
      f'<path d="M0,-108 L0,-34 L-46,-34Z" fill="{C["sand"]}" opacity=".75"/>'
      f'<circle cx="18" cy="-74" r="6" fill="#FFF3C8"/>'
      f'<path d="M-130,22 q22,-8 44,0 t44,0 t44,0 t44,0 t44,0" fill="none" stroke="{C["sea"]}" stroke-width="3" opacity=".6"/></g>')
    # rock point + lighthouse
    a('<path d="M690,1158 C730,1130 770,1118 820,1106 C870,1096 900,1090 960,1088 C1010,1086 1050,1090 1080,1094 L1080,1172 L690,1172Z" fill="#0C1130"/>')
    a('<path d="M720,1150 C760,1132 800,1124 840,1118" stroke="#2A3470" stroke-width="3" fill="none" opacity=".7"/>')
    tx, by, ty = 975, 1094, 900
    a(f'<path d="M{tx-36},{by} L{tx-25},{ty} L{tx+25},{ty} L{tx+36},{by}Z" fill="{C["cream"]}"/>')
    for y0, y1 in [(1010, 1040), (950, 976)]:
        f0, f1 = (by-y0)/(by-ty), (by-y1)/(by-ty)
        w0, w1 = 36-11*f0, 36-11*f1
        a(f'<path d="M{tx-w0:.1f},{y0} L{tx-w1:.1f},{y1} L{tx+w1:.1f},{y1} L{tx+w0:.1f},{y0}Z" fill="{C["ember"]}"/>')
    a(f'<rect x="{tx-31}" y="{ty-12}" width="62" height="12" rx="3" fill="{C["cream"]}"/>')
    a(f'<circle id="lampGlow" cx="{lx}" cy="{ly}" r="95" fill="url(#gGlow)"/>')
    a(f'<rect x="{tx-20}" y="{ty-46}" width="40" height="34" rx="4" fill="{C["amber"]}"/>')
    a(f'<circle cx="{lx}" cy="{ly-2}" r="9" fill="#FFF8DE"/>')
    a(f'<path d="M{tx-26},{ty-46} L{tx},{ty-72} L{tx+26},{ty-46}Z" fill="{C["ember"]}"/>')
    # beach (where the map begins)
    a(f'<path d="M0,1872 C180,1850 330,1880 520,1858 C700,1838 860,1866 1080,1846 L1080,1920 L0,1920Z" fill="#CDB892"/>')
    a(f'<path id="foam" d="M-200,1862 ' + ' '.join('q35,-12 70,0 t70,0' for _ in range(22)) + '" fill="none" stroke="#F6EBD7" stroke-width="5" stroke-linecap="round" opacity=".75"/>')
    # land
    a(f'<rect x="0" y="1912" width="{W}" height="{WH-1912}" fill="url(#gLand)"/>')
    a(f'<path d="M0,1912 C200,1925 420,1904 640,1918 C820,1930 960,1908 1080,1916 L1080,1940 L0,1940Z" fill="#CDB892" opacity=".55"/>')
    # Sahel olive groves: fields of trees in rows
    fields = [((60, 1990, 470, 380), -9), ((560, 1975, 460, 300), 6), ((40, 2420, 330, 420), 4),
              ((620, 2330, 420, 480), -5), ((90, 2860, 420, 300), 8), ((690, 2860, 360, 200), -3)]
    for (fx, fy, fw, fh), ang in fields:
        cx, cy = fx+fw/2, fy+fh/2
        a(f'<g transform="rotate({ang} {cx} {cy})">')
        a(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="14" fill="#2C3558" opacity=".7"/>')
        a(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="10" fill="none" stroke="#7E9A70" stroke-width="6" stroke-dasharray="2 12" stroke-linecap="round" opacity=".55"/>')
        sp = 58
        for ix in range(int(fw//sp)):
            for iy in range(int(fh//sp)):
                x = fx + sp/2 + ix*sp + rnd.uniform(-5, 5); y = fy + sp/2 + iy*sp + rnd.uniform(-5, 5)
                # rotate point to world to test against the trail
                ra = math.radians(ang); dx, dy = x-cx, y-cy
                wx, wy = cx + dx*math.cos(ra) - dy*math.sin(ra), cy + dx*math.sin(ra) + dy*math.cos(ra)
                if near_trail(wx, wy, 44): continue
                if rnd.random() < .12: continue
                r = rnd.uniform(14, 22)
                blob = ' '.join(f'{x + r*(1+rnd.uniform(-.18,.18))*math.cos(k*math.pi/4):.0f},{y + r*(1+rnd.uniform(-.18,.18))*math.sin(k*math.pi/4):.0f}' for k in range(8))
                a(f'<circle cx="{x+6:.0f}" cy="{y+7:.0f}" r="{r:.0f}" fill="#0B1230" opacity=".5"/>'
                  f'<polygon points="{blob}" fill="#55755F" stroke="#55755F" stroke-width="8" stroke-linejoin="round"/>'
                  f'<circle cx="{x-5:.0f}" cy="{y-6:.0f}" r="{r*.45:.0f}" fill="#93AE84" opacity=".55"/>')
        a('</g>')
    # steppe: alfa tufts and hills
    for _ in range(150):
        x, y = rnd.uniform(20, W-20), rnd.uniform(3120, 3560)
        if near_trail(x, y, 34): continue
        s = rnd.uniform(.7, 1.3)
        a(f'<path transform="translate({x:.0f} {y:.0f}) scale({s:.2f})" d="M0,0 L-7,-12 M0,0 L-2,-15 M0,0 L4,-14 M0,0 L9,-10" stroke="#9C8C9A" stroke-width="2.4" stroke-linecap="round" opacity=".55" fill="none"/>')
    for cx, cy, rx, ry in [(190, 3260, 150, 70), (900, 3400, 130, 60), (820, 3180, 90, 40)]:
        for k in range(4):
            a(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx-k*30}" ry="{ry-k*14}" fill="none" stroke="#B9A4B2" stroke-width="2" opacity="{.25+.08*k:.2f}"/>')
    # dunes (barchans)
    for _ in range(26):
        x, y = rnd.uniform(40, W-40), rnd.uniform(3620, 4080)
        if near_trail(x, y, 90): continue
        s = rnd.uniform(.7, 1.5)
        a(f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})">'
          f'<path d="M-70,10 C-40,-34 40,-34 70,10 C40,-8 -40,-8 -70,10Z" fill="#E2B57A" opacity=".9"/>'
          f'<path d="M-70,10 C-40,-8 40,-8 70,10 C38,22 -38,22 -70,10Z" fill="#8E5C3C" opacity=".75"/></g>')
    # oasis: water channels, palm crowns from above, brick houses
    for k in range(5):
        y0 = 4250 + k*170
        d = f'M0,{y0} C250,{y0-40} 420,{y0+50} 640,{y0+10} C820,{y0-20} 960,{y0+40} 1080,{y0+20}'
        a(f'<path d="{d}" fill="none" stroke="{C["sea"]}" stroke-width="5" opacity=".55"/>')
    houses = []
    for _ in range(16):
        hx, hy = rnd.uniform(250, 830), rnd.uniform(4520, 4820)
        if any(abs(hx-x) < 90 and abs(hy-y) < 80 for x, y in houses): continue
        houses.append((hx, hy))
    def palm_top(x, y, r, rot):
        p = [f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f})">', f'<circle cx="7" cy="9" r="{r*.75:.0f}" fill="#3A2412" opacity=".35"/>']
        n = 11
        for i in range(n):
            ang = i * 360/n + rnd.uniform(-8, 8); L = r * rnd.uniform(.85, 1.05)
            col = '#1F4A4C' if i % 2 else '#2E6460'
            p.append(f'<path transform="rotate({ang:.0f})" d="M0,0 C{L*.3:.0f},-9 {L*.75:.0f},-7 {L:.0f},2 C{L*.7:.0f},2 {L*.3:.0f},5 0,0Z" fill="{col}"/>')
        p.append('<circle r="7" fill="#E2A955"/></g>')
        return ''.join(p)
    palms = []
    tries = 0
    while len(palms) < 120 and tries < 4000:
        tries += 1
        x, y = rnd.uniform(-20, W+20), rnd.uniform(4060, WH-20)
        if near_trail(x, y, 70): continue
        if any((x-hx)**2 + (y-hy)**2 < 85**2 for hx, hy in houses): continue
        if (x-PIN[0])**2 + (y-PIN[1])**2 < 140**2: continue
        if any((x-px)**2 + (y-py)**2 < 58**2 for px, py in palms): continue
        palms.append((x, y))
    for x, y in sorted(palms, key=lambda p: p[1]):
        a(palm_top(x, y, rnd.uniform(46, 66), rnd.uniform(0, 360)))
    for hx, hy in houses:
        w, h = rnd.uniform(70, 100), rnd.uniform(56, 80)
        a(f'<rect x="{hx-w/2+8:.0f}" y="{hy-h/2+10:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#4A2C16" opacity=".45"/>'
          f'<rect x="{hx-w/2:.0f}" y="{hy-h/2:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#E9C48A"/>'
          f'<rect x="{hx-w/4:.0f}" y="{hy-h/4:.0f}" width="{w/2:.0f}" height="{h/2:.0f}" fill="#B98048"/>'
          f'<rect x="{hx-w/2:.0f}" y="{hy-h/2:.0f}" width="{w:.0f}" height="6" fill="#F6DDAE"/>')
    # the trail (masked so it can draw itself)
    marks, acc = [], 0.0
    for (x1, y1), (x2, y2) in zip(TRAIL, TRAIL[1:]):
        seg = math.hypot(x2-x1, y2-y1); acc += seg
        if acc >= 120 and seg > 0:
            acc = 0.0
            an = math.degrees(math.atan2(y2-y1, x2-x1)); k = 13
            marks.append(f'<path d="M{-k},{-k} L0,0 L{-k},{k}" transform="translate({x2:.1f} {y2:.1f}) rotate({an:.1f})" fill="none" stroke="{C["cream"]}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    a(f'<g mask="url(#mTrail)"><path id="trailPath" d="{pathd(TRAIL)}" fill="none" stroke="url(#gRoad)" stroke-width="9" stroke-linecap="round" stroke-dasharray="1 21"/>{"".join(marks)}</g>')
    a(f'<circle id="headGlow" r="34" fill="url(#gGlow)" opacity="0"/><circle id="head" r="11" fill="{C["amber"]}" stroke="{C["cream"]}" stroke-width="4" opacity="0"/>')
    # the «؟» pin
    px, py = PIN
    a(f'<g id="pin" data-x="{px}" data-y="{py}" opacity="0">'
      f'<circle id="pinRing" cx="0" cy="0" r="40" fill="none" stroke="{C["amber"]}" stroke-width="5"/>'
      f'<ellipse cx="0" cy="6" rx="30" ry="10" fill="#3A2412" opacity=".4"/>'
      f'<path d="M0,0 C-22,-30 -50,-56 -50,-92 A50,50 0 1 1 50,-92 C50,-56 22,-30 0,0Z" fill="{C["ember"]}" stroke="{C["cream"]}" stroke-width="5"/>'
      f'<circle cx="0" cy="-92" r="34" fill="{C["cream"]}"/>'
      f'<text x="0" y="-70" text-anchor="middle" font-family="Lalezar" font-size="62" fill="{C["ember"]}">؟</text></g>')
    a('</svg>')
    return '\n'.join(g)

# ---------------------------------------------------------------- clue illustrations (692x692)

def clue_dates():
    r = random.Random(11)
    g = ['<svg viewBox="0 0 692 692" width="692" height="692" style="display:block">',
         '<defs><radialGradient id="dBg" cx=".55" cy=".35" r=".8"><stop offset="0" stop-color="#FFD98A"/><stop offset=".45" stop-color="#E8964A"/><stop offset="1" stop-color="#7A3A1C"/></radialGradient>',
         '<radialGradient id="dDate" cx=".38" cy=".3" r=".75"><stop offset="0" stop-color="#FFE3A2"/><stop offset=".35" stop-color="#E9A050"/><stop offset=".8" stop-color="#A65A26"/><stop offset="1" stop-color="#6E3514"/></radialGradient>',
         '<radialGradient id="dSun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFF6D8" stop-opacity=".9"/><stop offset="1" stop-color="#FFF6D8" stop-opacity="0"/></radialGradient></defs>',
         '<rect width="692" height="692" fill="url(#dBg)"/>', '<circle cx="420" cy="200" r="260" fill="url(#dSun)"/>']
    # fronds at the top
    for x0, ang, L in [(-30, 28, 420), (120, 10, 380), (720, 152, 430), (560, 170, 360)]:
        g.append(f'<g transform="translate({x0} -20) rotate({ang})">')
        g.append(f'<path d="M0,0 C{L*.4:.0f},-30 {L*.75:.0f},-10 {L},60" fill="none" stroke="#5A3418" stroke-width="7" opacity=".85"/>')
        for i in range(1, 16):
            t = i/16; x = L*t; y = -30*math.sin(t*math.pi) + 60*t*t
            for s in (-1, 1):
                g.append(f'<path d="M{x:.0f},{y:.0f} q{16:.0f},{s*34:.0f} {44:.0f},{s*64:.0f}" stroke="#5A3418" stroke-width="4.5" fill="none" stroke-linecap="round" opacity=".8"/>')
        g.append('</g>')
    # stalk and strands
    g.append('<path d="M300,-10 C320,90 330,150 336,210" stroke="#7A4A22" stroke-width="22" fill="none" stroke-linecap="round"/>')
    strands = []
    for i in range(15):
        ang = -70 + i*10 + r.uniform(-4, 4)
        L = r.uniform(330, 470)
        sx, sy = 336, 210
        ex = sx + L*math.sin(math.radians(ang)); ey = sy + L*math.cos(math.radians(ang))*0.95
        strands.append((sx, sy, ex, ey))
        g.append(f'<path d="M{sx},{sy} Q{(sx+ex)/2 + r.uniform(-20,20):.0f},{(sy+ey)/2 - 30:.0f} {ex:.0f},{ey:.0f}" stroke="#C9893F" stroke-width="4" fill="none"/>')
    dates = []
    for sx, sy, ex, ey in strands:
        for k in range(r.randint(4, 7)):
            t = r.uniform(.35, 1.0)
            x = sx + (ex-sx)*t + r.uniform(-14, 14); y = sy + (ey-sy)*t + r.uniform(-8, 8)
            dates.append((y, x, math.degrees(math.atan2(ex-sx, ey-sy))))
    for y, x, ang in sorted(dates):
        g.append(f'<g transform="translate({x:.0f} {y:.0f}) rotate({-ang + r.uniform(-25,25):.0f})">'
                 f'<ellipse cx="2" cy="4" rx="17" ry="31" fill="#4A220C" opacity=".35"/>'
                 f'<ellipse rx="17" ry="31" fill="url(#dDate)"/>'
                 f'<ellipse cx="-6" cy="-12" rx="4" ry="9" fill="#FFF1C8" opacity=".75"/></g>')
    g.append('</svg>')
    return ''.join(g)

def clue_bricks():
    """A Tozeur facade: yellow brick laid so that raised bricks draw diamonds and zigzags."""
    r = random.Random(5)
    bw, bh, gap = 60, 22, 5
    g = ['<svg viewBox="0 0 692 692" width="692" height="692" style="display:block">',
         '<defs><linearGradient id="bLight" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE2A6" stop-opacity=".35"/><stop offset=".6" stop-color="#FFE2A6" stop-opacity="0"/><stop offset="1" stop-color="#2A1206" stop-opacity=".35"/></linearGradient></defs>',
         f'<rect width="692" height="692" fill="#7A4A22"/>']
    rows = int(692 // (bh+gap)) + 2
    cx = 346
    for j in range(rows):
        y = j*(bh+gap) - 6
        off = 0 if j % 2 == 0 else -(bw+gap)/2
        for i in range(-1, int(692//(bw+gap))+2):
            x = off + i*(bw+gap)
            mx, my = x + bw/2, y + bh/2
            # diamonds: two rows of lozenges + a zigzag band
            dx, dy = abs(((mx - cx + 1000) % 230) - 115), abs(my - 230)
            v1 = abs(dx/115 + dy/95 - 1) < .16
            dy2 = abs(my - 470)
            dxz = abs(((mx + 1000) % 120) - 60)
            zig = abs(dy2 - (60 - dxz)*.55) < 9 and dy2 < 40
            band = abs(my - 360) < 14
            raised = v1 or zig or band
            base = r.choice(['#D39A58', '#C98E4E', '#BD8142', '#DCA867'])
            if raised:
                g.append(f'<rect x="{x+7:.0f}" y="{y+8:.0f}" width="{bw}" height="{bh}" rx="2" fill="#3A1C08" opacity=".55"/>')
                g.append(f'<rect x="{x-2:.0f}" y="{y-2:.0f}" width="{bw}" height="{bh}" rx="2" fill="#EBC07F"/>')
                g.append(f'<rect x="{x-2:.0f}" y="{y-2:.0f}" width="{bw}" height="5" fill="#FFE2A6" opacity=".8"/>')
            else:
                g.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw}" height="{bh}" rx="2" fill="{base}"/>')
                g.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw}" height="3" fill="#EBC07F" opacity=".35"/>')
    # a little arched window at the bottom
    g.append('<path d="M286,692 L286,610 A60,60 0 0 1 406,610 L406,692Z" fill="#2A1A10"/>')
    g.append('<path d="M286,610 A60,60 0 0 1 406,610" fill="none" stroke="#EBC07F" stroke-width="10"/>')
    g.append('<rect width="692" height="692" fill="url(#bLight)"/>')
    g.append('</svg>')
    return ''.join(g)

def clue_chott():
    """Chott el Jerid: a salt flat to the horizon, polygon cracks, a mirage of palms."""
    r = random.Random(3)
    H0 = 300  # horizon
    g = ['<svg viewBox="0 0 692 692" width="692" height="692" style="display:block">',
         '<defs><linearGradient id="cSkyG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7F9BD0"/><stop offset=".55" stop-color="#E7B8B0"/><stop offset="1" stop-color="#FFD9A0"/></linearGradient>',
         '<linearGradient id="cSalt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3E6E2"/><stop offset=".25" stop-color="#FBF4EC"/><stop offset="1" stop-color="#E9DDD2"/></linearGradient>',
         '<linearGradient id="cMir" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9FB6E0" stop-opacity=".85"/><stop offset="1" stop-color="#9FB6E0" stop-opacity="0"/></linearGradient></defs>',
         f'<rect width="692" height="{H0}" fill="url(#cSkyG)"/>',
         f'<circle cx="520" cy="{H0-30}" r="46" fill="#FFF3D0" opacity=".9"/>',
         f'<rect y="{H0}" width="692" height="{692-H0}" fill="url(#cSalt)"/>',
         f'<rect y="{H0}" width="692" height="44" fill="url(#cMir)"/>']
    # palms on the horizon and their mirage (upside down, shimmering)
    for x in [70, 104, 128, 170, 205, 600, 628, 660]:
        h = r.uniform(26, 44)
        for flip in (1, -1):
            op = '1' if flip == 1 else '.35'
            g.append(f'<g transform="translate({x} {H0}) scale(1 {flip})" opacity="{op}" fill="#5A4A6A">'
                     f'<path d="M-1.5,0 L-1,{-h} L1,{-h} L1.5,0Z"/>'
                     + ''.join(f'<path transform="translate(0 {-h}) rotate({a})" d="M0,0 C6,-3 12,-1 16,4 C11,2 6,2 0,0Z"/>' for a in (-160, -120, -60, -20, -90, 200)) + '</g>')
    # perspective polygon cracks: jittered hex grid in ground coordinates, projected
    def proj(u, v):
        # v: distance (1 near .. large far), u: lateral
        f = 380
        y = H0 + f / v
        x = 346 + u * f / v
        return x, y
    lines = []
    for iv in range(0, 26):
        for iu in range(-30, 31):
            u = iu*0.9 + (0.45 if iv % 2 else 0)
            v = 1.0 + iv*0.55
            pts = []
            for k in range(6):
                a_ = math.radians(60*k + 30)
                pu = u + 0.52*math.cos(a_) + r.uniform(-.08, .08)
                pv = v + 0.32*math.sin(a_) + r.uniform(-.05, .05)
                if pv <= 0.6: pv = 0.6
                pts.append(proj(pu, pv))
            if all(p[0] < -40 or p[0] > 732 for p in pts) or all(p[1] > 720 for p in pts): continue
            lines.append((v, pts))
    for v, pts in sorted(lines, key=lambda z: -z[0]):
        sw = max(.6, 4.2 / v)
        g.append(f'<path d="M{pts[0][0]:.1f},{pts[0][1]:.1f} ' + ' '.join(f'L{x:.1f},{y:.1f}' for x, y in pts[1:]) + 'Z" fill="none" '
                 f'stroke="#C8B6AE" stroke-width="{sw:.2f}" stroke-linejoin="round" opacity="{min(1, .35 + 1.4/v):.2f}"/>')
    # pink brine pools
    for cx, cy, rx, ry in [(150, 560, 90, 22), (520, 470, 70, 14), (420, 640, 120, 26)]:
        g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#F2B3A6" opacity=".55"/>')
    g.append('</svg>')
    return ''.join(g)

def photo_palms():
    """The real oasis at the camp (Espace Badi, Degache): palms and date bunches against the sky."""
    src = ROOT / '02-photos/venue/palm-grove-path.jpeg'
    im = Image.open(src).convert('RGB')
    im = im.crop((0, 40, 720, 760)).resize((692, 692), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.1)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    # a warm late-afternoon grade
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.05 + 6))); b = b.point(lambda v: int(v * .93))
    im = Image.merge('RGB', (r, g, b))
    im.save(BUILD / 'clue-palms.jpg', quality=92)
    return '<img src="clue-palms.jpg" width="692" height="692" style="display:block" alt="">'

# ---------------------------------------------------------------- page

CLUES = [
    ('نخيل على مدّ العين', 'photo', 'rgba(242,181,68,.62)'),
    ('دقلة… اسمها النور', 'dates', 'rgba(127,179,224,.62)'),
    ('طوب يرسم أشكال', 'bricks', 'rgba(226,85,45,.5)'),
    ('شطّ ملح… والسراب يلعب', 'chott', 'rgba(242,181,68,.62)'),
]

def end_sky(uid):
    r = random.Random(77)
    s = [f'<svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;inset:0">',
         f'<defs><radialGradient id="eBg{uid}" cx=".5" cy=".28" r=".9"><stop offset="0" stop-color="#2A3470"/><stop offset=".45" stop-color="#1A2150"/><stop offset="1" stop-color="#0C1029"/></radialGradient></defs>',
         f'<rect width="1080" height="1920" fill="url(#eBg{uid})"/>']
    for _ in range(110):
        s.append(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{1700*r.random()**1.2:.0f}" r="{r.choice([1.2,1.6,2,2.6])}" fill="#FFF3D6" opacity="{r.uniform(.35,.95):.2f}"/>')
    s.append('</svg>')
    return ''.join(s)

def page():
    BUILD.mkdir(exist_ok=True)
    F = '../../../../03-identity/fonts/'
    L = '../../../../03-identity/logos/'
    css = (HERE / 'teaser.css').read_text(encoding='utf-8').replace('{F}', F)
    js = (HERE / 'teaser.js').read_text(encoding='utf-8')
    shutil.copy(ID / 'motifs/grain.png', BUILD / 'grain.png')
    shutil.copy(ID / 'motifs/brick-frieze.svg', BUILD / 'brick-frieze.svg')
    art = {'photo': photo_palms(), 'dates': clue_dates(), 'bricks': clue_bricks(), 'chott': clue_chott()}
    cards = []
    for i, (cap, kind, tape) in enumerate(CLUES):
        cards.append(f'''<div class="card" id="card{i}">
  <div class="tape" style="background:{tape}"></div>
  <div class="ph">{art[kind]}</div>
  <div class="cap"><span id="cap{i}">{cap}</span></div>
  <div class="num">{i+1}</div>
</div>''')
    logos = f'''<div class="logos">
  <img src="{L}unit-scouts-abdelmajid-attia.png" alt="فرقة عبد المجيد عطية للكشافة" style="height:178px">
  <img src="{L}fawj-hiboun-seal.png" alt="الكشافة التونسية، جهة المهدية، فوج هيبون" class="sealimg" style="height:206px;width:206px">
  <img src="{L}unit-guides-bchira-ben-mrad.png" alt="مرشدات بشيرة بن مراد، فوج هيبون" style="height:166px">
</div>'''
    stamp = f'''<svg id="stamp" viewBox="0 0 640 300" width="640" height="300">
  <defs><filter id="ink"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.5 1.55"/><feComposite in="SourceGraphic" operator="in"/></filter></defs>
  <g filter="url(#ink)">
    <rect x="12" y="12" width="616" height="276" rx="26" fill="none" stroke="{C['ember']}" stroke-width="14"/>
    <rect x="34" y="34" width="572" height="232" rx="16" fill="none" stroke="{C['ember']}" stroke-width="4"/>
    <text x="320" y="180" text-anchor="middle" font-family="Lalezar" font-size="122" fill="{C['ember']}">دقاش · توزر</text>
    <text x="320" y="246" text-anchor="middle" font-family="Reem Kufi" font-weight="700" font-size="34" fill="{C['ember']}">12 · 13 · 14 ديسمبر 2026</text>
  </g></svg>'''
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<title>تيزر مخيم الشتاء — من البحر… لوين؟</title>
<style>{css}</style></head><body>
<div id="stage">
  <!-- S1-S2: the world -->
  <div id="cam"><div id="world">
    {world_svg()}
    <img id="hkSeal" src="{L}fawj-hiboun-seal.png" alt="فوج هيبون">
    <div id="hk1" class="big" style="{x3d(C["cream"], C["seadeep"], 14)}">من البحر...</div>
    <div id="hk2" class="big" style="{x3d(C['amber'], C['emberdeep'], 18)}">لوين؟</div>
    <div id="hk3" class="ruqaa">كان يا مكان… في شتاء 2026</div>
  </div></div>
  <div id="scrim"></div>
  <div id="jr1" class="ruqaa">نتبعو إشارات الطريق…</div>
  <div id="jr2" class="big" style="{x3d(C['amber'], C['emberdeep'], 14)}">4 تلميحات</div>

  <!-- S3-S6: the logbook -->
  <div id="book">
    <div class="paper"></div>
    <div id="bkHead">
      <img src="{L}fawj-hiboun-seal.png" class="bkSeal" alt="">
      <div class="bkTitle">كرّاس الرحلة</div>
      <div class="bkCount"><span id="bkN">تلميح 1 / 4</span></div>
    </div>
    <div id="bkNote" class="ruqaa">ركّزوا مليح… وخمّنوا وين!</div>
    <div id="night"></div>
    <div id="pileWrap"><div id="pile">{''.join(cards)}</div><div id="stampWrap">{stamp}</div></div>
  </div>

  <!-- S7 teaser: the question -->
  <div id="ask">
    <div id="ask1" class="big" style="{x3d(C['amber'], C['emberdeep'], 18)}">عرفتوها؟</div>
    <div id="ask2" class="pill">
      <svg width="58" height="58" viewBox="0 0 24 24" fill="none" stroke="{C['night']}" stroke-width="2.2" stroke-linejoin="round"><path d="M20 12a8 8 0 0 1-11.6 7.1L4 20l1-4.2A8 8 0 1 1 20 12z"/><text x="12" y="15.6" text-anchor="middle" font-family="Lalezar" font-size="10" fill="{C['night']}" stroke="none">؟</text></svg>
      <span>اكتبوها في الكومنتار</span></div>
    <svg id="arrow" width="300" height="260" viewBox="0 0 300 260"><path d="M30,20 C120,10 210,60 230,190" fill="none" stroke="{C['cream']}" stroke-width="9" stroke-linecap="round"/><path d="M196,170 L232,206 L262,160" fill="none" stroke="{C['cream']}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </div>

  <!-- S7 reveal: the tagline answers the hook -->
  <div id="ans">
    <div id="ans1" class="big" style="{x3d(C["cream"], C["seadeep"], 14)}">من البحر...</div>
    <div id="ans2" class="big" style="{x3d(C['amber'], C['emberdeep'], 18)}">إلى النخيل</div>
  </div>

  <!-- S8: end cards -->
  <div id="end" class="endcard">
    {end_sky('a')}
    {logos}
    <div class="e-title big" style="{x3d(C['cream'], C['seadeep'], 14)}">مخيم الشتاء</div>
    <div class="e-date">12 · 13 · 14 ديسمبر 2026</div>
    <div class="e-soon ruqaa">الحكاية قريب تبدا…</div>
    <div class="e-who">فتية وفتيات · من 12 إلى 17 سنة</div>
    <div class="e-org">فوج هيبون · الكشافة التونسية · جهة المهدية</div>
    <div class="frieze"></div>
  </div>
  <div id="endR" class="endcard">
    {end_sky('b')}
    {logos}
    <div class="e-title big" style="{x3d(C['cream'], C['seadeep'], 14)}">مخيم الشتاء</div>
    <div class="e-date">12 · 13 · 14 ديسمبر 2026</div>
    <div class="e-place">دقاش، توزر</div>
    <div class="e-who">فتية وفتيات · من 12 إلى 17 سنة</div>
    <div class="e-price"><span><b>100</b> د للمنخرطين</span><i></i><span><b>120</b> د لغير المنخرطين</span></div>
    <div class="e-call">للتسجيل <span dir="ltr">22 882 867</span></div>
    <div class="frieze"></div>
  </div>

  <div id="flash"></div>
  <div id="grain"></div>
  <div id="vig"></div>
</div>
<script>window.TEASER = {json.dumps({'camEnd': CAM_END, 'pin': PIN})};</script>
<script>{js}</script>
</body></html>'''
    (BUILD / 'teaser.html').write_text(html, encoding='utf-8')
    print('wrote', BUILD / 'teaser.html', f'{len(html)//1024} KB')

if __name__ == '__main__':
    page()
