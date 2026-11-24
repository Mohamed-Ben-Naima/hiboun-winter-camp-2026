"""Builds the Winter Camp layouts, version 2: «كان يا مكان» — the poster tells the camp as a story.

  python build.py local   -> _build/prev_<Name>.html, rendered by export.py (local fonts and files)
  python build.py dc      -> _build/canvas/project/<Name>.dc.html, the artboards of the Design canvas
                             (Google Fonts + the canvas's /_blob urls from canvas_blob_urls.json)

The story, top to bottom, in every format:
  1. the characters  — the three logos: Abdelmajid Attia scouts troop, Fawj Hiboun, Bchira Ben Mrad guides
  2. the opening     — «كان يا مكان… في شتاء 2026»
  3. the departure   — Mahdia: sea, the Cap Afrique lighthouse, a little starfish
  4. the road        — a scout trail (trail-sign chevrons) running from the sea (blue) to the oasis (amber)
  5. the destination — the Djerid arch with the camp photo, stamped with the camp seal
  6. three chapters  — Saturday نرحل · Sunday نكتشف · Monday نعود, ending on the scout sign «gone home» ⊙
  7. the invitation  — «كونوا جزءًا من الحكاية», the phone and the prices
Version 1 (no logos, info row) is git tag `poster-v1`.
"""
import json, math, sys, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BUILD = HERE / '_build'

C = dict(night='#141833', night2='#1A2150', sky='#2A3470', cream='#F6EBD7', sand='#D9CBB0',
         amber='#F2B544', ember='#E2552D', brick='#C98E4E', brickhi='#E9C48A', ink='#141833', muted='#5A4A3A',
         sea='#7FB3E0', palm='#3B4A8C')

F = '../../../03-identity/fonts/'   # relative to _build/
FONTS_LOCAL = f"""@font-face{{font-family:Lalezar;src:url({F}Lalezar-Regular.ttf)}}
@font-face{{font-family:"Aref Ruqaa";src:url({F}ArefRuqaa-Bold.ttf);font-weight:700}}
@font-face{{font-family:Alexandria;src:url("{F}Alexandria[wght].ttf");font-weight:100 900}}
@font-face{{font-family:"Reem Kufi";src:url("{F}ReemKufi[wght].ttf");font-weight:400 700}}"""
FONTS_LINK = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alexandria:wght@400;600;700;800;900&amp;family=Aref+Ruqaa:wght@700&amp;family=Lalezar&amp;family=Reem+Kufi:wght@600;700&amp;display=swap">'

ICON = {
 'cal': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 'pin': '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 'people': '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.6"/><path d="M15.5 14.2c3 .2 5.5 2.6 5.5 5.8"/>',
 'phone': '<path d="M5 3h3l2 5-2.5 1.5a11 11 0 0 0 7 7L16 14l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
}
def icon(name, size, color, sw=2):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>')

# ---------------------------------------------------------------- shared pieces

def seal(size, uid, style=''):
    return f'''<svg style="{style};direction:ltr" width="{size}" height="{size}" viewBox="0 0 200 200" role="img" aria-label="شارة مخيم الشتاء، دقاش، توزر 2026">
<defs><path id="sealTop{uid}" d="M30,100 A70,70 0 0,1 170,100"></path><path id="sealBot{uid}" d="M22,100 A78,78 0 0,0 178,100"></path></defs>
<circle cx="100" cy="100" r="97" fill="{C['ember']}"></circle>
<circle cx="100" cy="100" r="90" fill="none" stroke="{C['cream']}" stroke-width="2" stroke-dasharray="3 5"></circle>
<circle cx="100" cy="100" r="50" fill="{C['cream']}"></circle>
<text font-family="Reem Kufi" font-weight="700" font-size="21" fill="{C['cream']}" text-anchor="middle"><textPath href="#sealTop{uid}" startOffset="50%">مخيم الشتاء</textPath></text>
<text font-family="Reem Kufi" font-weight="700" font-size="17" fill="{C['cream']}" text-anchor="middle"><textPath href="#sealBot{uid}" startOffset="50%">دقاش · توزر · 2026</textPath></text>
<circle cx="27" cy="100" r="3" fill="{C['amber']}"></circle><circle cx="173" cy="100" r="3" fill="{C['amber']}"></circle>
<g transform="translate(100,104)" fill="{C['night2']}">
<path d="M-2 30 C0 10 2 -6 6 -18 L9 -18 C5 -4 4 12 4 30Z"></path>
<path d="M7 -19 C-6 -30 -26 -26 -34 -12 C-20 -22 -6 -20 7 -15Z"></path>
<path d="M7 -19 C18 -32 36 -30 42 -16 C30 -24 18 -22 7 -15Z"></path>
<path d="M7 -19 C4 -36 -10 -42 -20 -40 C-8 -36 0 -28 5 -16Z"></path>
<path d="M7 -19 C14 -36 28 -40 36 -36 C24 -34 14 -28 9 -16Z"></path>
<circle cx="2" cy="-12" r="3.4" fill="{C['ember']}"></circle><circle cx="9" cy="-11" r="3.4" fill="{C['ember']}"></circle><circle cx="5" cy="-6" r="3.4" fill="{C['ember']}"></circle>
</g></svg>'''

def logos(s, U, top, h_seal=150, h_unit=124, gap=40, left=None, right=None, justify='center'):
    """The characters of the story, right to left: scouts troop · Fawj Hiboun · guides unit."""
    p = lambda v: round(v*s)
    l = f'left:{p(left)}px' if left is not None else 'left:0'
    r = f'right:{p(right)}px' if right is not None else 'right:0'
    return f'''<div style="position:absolute;top:{p(top)}px;{l};{r};display:flex;justify-content:{justify};align-items:center;gap:{p(gap)}px;direction:rtl">
<img src="{U['logo-scouts']}" alt="فرقة عبد المجيد عطية للكشافة" style="height:{p(h_unit+8)}px;width:auto">
<img src="{U['logo-fawj']}" alt="الكشافة التونسية، جهة المهدية، فوج هيبون" style="height:{p(h_seal)}px;width:{p(h_seal)}px;border-radius:50%;box-shadow:0 0 0 {max(2,p(4))}px rgba(246,235,215,.18)">
<img src="{U['logo-guides']}" alt="مرشدات بشيرة بن مراد، فوج هيبون" style="height:{p(h_unit)}px;width:auto">
</div>'''

def opener(s, top, size=40, sub=None, sub_size=24, width=None):
    p = lambda v: round(v*s)
    w = f'left:50%;transform:translateX(-50%);width:{p(width)}px' if width else 'left:0;right:0'
    subline = f'<p style="margin:{p(8)}px 0 0;font-weight:600;font-size:{p(sub_size)}px;line-height:1.45;color:{C["sand"]}">{sub}</p>' if sub else ''
    return f'''<div style="position:absolute;top:{p(top)}px;{w};text-align:center">
<p style="margin:0;font-family:'Aref Ruqaa',serif;font-weight:700;font-size:{p(size)}px;line-height:1.2;color:{C['amber']}">كان يا مكان… في شتاء 2026</p>{subline}
</div>'''

def lighthouse(s, x, y, w=210, label=True):
    """Mahdia: the Cap Afrique lighthouse on its point, waves, and a little starfish
    (a nod to «نجمة البحر الصغير», a children's story by Abdelmajid Attia)."""
    p = lambda v: round(v*s)
    H = 250
    lab = (f'<div style="position:absolute;left:0;right:0;top:{p(H*w/210-8)}px;text-align:center;font-family:\'Reem Kufi\',sans-serif;'
           f'font-weight:700;font-size:{p(22)}px;color:{C["sea"]}">المهدية</div>') if label else ''
    return f'''<div style="position:absolute;left:{p(x)}px;top:{p(y)}px;width:{p(w)}px;height:{p(H*w/210+24)}px">
<svg width="{p(w)}" height="{p(H*w/210)}" viewBox="0 0 210 250" aria-hidden="true">
<defs><linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['amber']}" stop-opacity=".55"></stop><stop offset="1" stop-color="{C['amber']}" stop-opacity="0"></stop></linearGradient></defs>
<path d="M112 52 L-10 18 L-10 74 Z" fill="url(#beam)" transform="translate(4 0) scale(-1 1) translate(-218 0)"></path>
<path d="M98 52 L-10 22 L-10 72 Z" fill="url(#beam)"></path>
<path d="M88 196 L94 70 L116 70 L122 196 Z" fill="{C['cream']}"></path>
<path d="M90.6 150 L119.4 150 L120.3 168 L89.7 168 Z" fill="{C['ember']}"></path>
<path d="M92.3 110 L117.7 110 L118.5 126 L91.5 126 Z" fill="{C['ember']}"></path>
<rect x="90" y="62" width="30" height="8" rx="2" fill="{C['cream']}"></rect>
<rect x="95" y="42" width="20" height="20" rx="3" fill="{C['amber']}"></rect>
<path d="M92 42 L105 28 L118 42 Z" fill="{C['ember']}"></path>
<circle cx="105" cy="52" r="5" fill="#FFF6D8"></circle>
<path d="M60 200 Q105 186 150 200 L150 206 L60 206 Z" fill="{C['palm']}"></path>
<path d="M0 214 q13 -9 26 0 t26 0 t26 0 t26 0 t26 0 t26 0 t26 0 t26 0" fill="none" stroke="{C['sea']}" stroke-width="4" stroke-linecap="round"></path>
<path d="M14 230 q13 -9 26 0 t26 0 t26 0 t26 0 t26 0 t26 0 t26 0" fill="none" stroke="{C['sea']}" stroke-width="3" stroke-linecap="round" opacity=".7"></path>
<path d="M30 245 q13 -8 26 0 t26 0 t26 0 t26 0 t26 0 t26 0" fill="none" stroke="{C['sea']}" stroke-width="2.5" stroke-linecap="round" opacity=".45"></path>
<g transform="translate(176 196) rotate(12)" fill="{C['amber']}"><path d="M0 -13 L3.6 -4.4 L12.4 -4 L5.6 2 L7.8 11 L0 6 L-7.8 11 L-5.6 2 L-12.4 -4 L-3.6 -4.4 Z" stroke="{C['amber']}" stroke-width="2.4" stroke-linejoin="round"></path></g>
</svg>{lab}
</div>'''

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

def trail(s, W, H, pts, end=None, uid='t', every=95, width=4):
    """The scout trail: a dashed road from the sea (blue) to the oasis (amber) with trail-sign chevrons
    pointing the way, and the trail sign «gone home» (a circle with a dot) where it ends."""
    p = lambda v: v*s
    poly = catmull([(p(x), p(y)) for x, y in pts])
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in poly)
    ys = [y for _, y in poly]
    marks, acc = [], 0.0
    for (x1, y1), (x2, y2) in zip(poly, poly[1:]):
        seg = math.hypot(x2-x1, y2-y1); acc += seg
        if acc >= p(every) and seg > 0:
            acc = 0.0
            a = math.degrees(math.atan2(y2-y1, x2-x1)); k = p(9)
            marks.append(f'<path d="M{-k:.1f},{-k:.1f} L0,0 L{-k:.1f},{k:.1f}" transform="translate({x2:.1f} {y2:.1f}) rotate({a:.1f})" '
                         f'fill="none" stroke="{C["cream"]}" stroke-width="{max(2,p(3)):.1f}" stroke-linecap="round" stroke-linejoin="round"></path>')
    endsign = ''
    if end:
        ex, ey = p(end[0]), p(end[1]); r = p(14)
        endsign = (f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{r:.1f}" fill="none" stroke="{C["amber"]}" stroke-width="{max(2,p(3)):.1f}"></circle>'
                   f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{p(4):.1f}" fill="{C["amber"]}"></circle>')
    return f'''<svg style="position:absolute;left:0;top:0" width="{round(W)}" height="{round(H)}" viewBox="0 0 {round(W)} {round(H)}" aria-hidden="true">
<defs><linearGradient id="road{uid}" gradientUnits="userSpaceOnUse" x1="0" y1="{min(ys):.0f}" x2="0" y2="{max(ys):.0f}"><stop offset="0" stop-color="{C['sea']}"></stop><stop offset="1" stop-color="{C['amber']}"></stop></linearGradient></defs>
<path d="{d}" fill="none" stroke="url(#road{uid})" stroke-width="{max(2,p(width)):.1f}" stroke-linecap="round" stroke-dasharray="{p(2):.1f} {p(14):.1f}"></path>
{''.join(marks)}{endsign}
</svg>'''

def arch(s, U, top, w, h, left=None, img='hero', pos='50% 58%', alt='خيمة من سعف النخيل وطاولة تحت نخيل واحة دقاش عند الغروب'):
    p = lambda v: round(v*s)
    frame = p(20)
    pos_css = f'left:{p(left)}px' if left is not None else f'left:{(round(1080*s)-p(w))//2}px'
    return f'''<div style="position:absolute;top:{p(top)}px;{pos_css};width:{p(w)}px;height:{p(h)}px;border-radius:{p(w)//2}px {p(w)//2}px 0 0;background-image:url({U['brick-tile']});background-size:{p(148)}px auto;padding:{frame}px;box-sizing:border-box;box-shadow:0 {p(30)}px {p(60)}px rgba(5,7,20,.55)">
<div style="position:relative;width:100%;height:100%;border-radius:{p(w)//2-frame}px {p(w)//2-frame}px 0 0;overflow:hidden;box-shadow:inset 0 0 0 {max(2,p(3))}px {C['cream']}">
<img src="{U[img]}" alt="{alt}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos}">
<div style="position:absolute;left:0;right:0;bottom:0;height:50%;background:linear-gradient(to top,rgba(17,21,47,.96),rgba(17,21,47,0))"></div>
</div></div>'''

def title(s, top, size=188, left=0, right=0, align='center', tag=54, gap=8):
    p = lambda v: round(v*s)
    return f'''<div style="position:absolute;top:{p(top)}px;left:{p(left)}px;right:{p(right)}px;text-align:{align}">
<h1 style="margin:0;font-family:Lalezar,sans-serif;font-weight:400;font-size:{p(size)}px;line-height:1;color:{C['cream']};text-shadow:0 {p(6)}px 0 {C['ember']},0 {p(18)}px {p(40)}px rgba(0,0,0,.45)">مخيم الشتاء</h1>
<p style="margin:{p(gap)}px 0 0;font-family:'Aref Ruqaa',serif;font-weight:700;font-size:{p(tag)}px;line-height:1.2;color:{C['amber']}">من البحر إلى النخيل</p>
</div>'''

def facts(s, top, size=24, left=0, right=0, justify='center'):
    p = lambda v: round(v*s)
    item = lambda ic, t: (f'<span style="display:inline-flex;align-items:center;gap:{p(10)}px">{icon(ic, p(28), C["amber"])}'
                          f'<span>{t}</span></span>')
    return f'''<div style="position:absolute;top:{p(top)}px;left:{p(left)}px;right:{p(right)}px;display:flex;justify-content:{justify};align-items:center;gap:{p(34)}px;font-weight:700;font-size:{p(size)}px;color:{C['cream']};direction:rtl">
{item('pin','دقاش، توزر')}<span style="width:{p(6)}px;height:{p(6)}px;border-radius:50%;background:{C['amber']}"></span>{item('people','فتية وفتيات من 12 إلى 17 سنة')}
</div>'''

CHAPTERS = [
    ('السبت 12 ديسمبر', 'نرحل', 'من بحر المهدية إلى واحة دقاش'),
    ('الأحد 13 ديسمبر', 'نكتشف', 'النخيل، الطوب ونجوم الجريد'),
    ('الإثنين 14 ديسمبر', 'نعود', 'بحكايات وأصدقاء جدد'),
]

def chapters(s, top, side, verb=46, desc=19, day=21):
    """Three chapters on one line, right to left; the trail's dots sit on top of each."""
    p = lambda v: round(v*s)
    cells = []
    for i, (d, v, t) in enumerate(CHAPTERS):
        cells.append(f'''<div style="display:flex;flex-direction:column;align-items:center;text-align:center;gap:{p(2)}px">
<div style="width:{p(22)}px;height:{p(22)}px;border-radius:50%;background:{C['night']};border:{max(2,p(4))}px solid {C['amber'] if i else C['sea']};box-sizing:border-box;margin-bottom:{p(8)}px"></div>
<div style="font-family:'Reem Kufi',sans-serif;font-weight:700;font-size:{p(day)}px;color:{C['amber']}">الفصل {('الأول','الثاني','الثالث')[i]} · {d}</div>
<div style="font-family:Lalezar,sans-serif;font-size:{p(verb)}px;line-height:1.05;color:{C['cream']}">{v}</div>
<div style="font-size:{p(desc)}px;line-height:1.35;color:{C['sand']}">{t}</div></div>''')
    return f'''<div style="position:absolute;top:{p(top)}px;right:{p(side)}px;left:{p(side)}px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:{p(12)}px;direction:rtl">
{''.join(cells)}</div>'''

def chapters_stack(s, top, right, width, verb=44, desc=22, day=22, gap=34):
    """The same three chapters stacked (16:9 video card), dots on a vertical road."""
    p = lambda v: round(v*s)
    rows = []
    for i, (d, v, t) in enumerate(CHAPTERS):
        rows.append(f'''<div style="display:flex;align-items:flex-start;gap:{p(22)}px">
<div style="flex:none;width:{p(26)}px;height:{p(26)}px;margin-top:{p(6)}px;border-radius:50%;background:{C['night']};border:{max(2,p(4))}px solid {C['amber'] if i else C['sea']};box-sizing:border-box"></div>
<div style="display:flex;flex-direction:column;gap:{p(2)}px">
<div style="font-family:'Reem Kufi',sans-serif;font-weight:700;font-size:{p(day)}px;color:{C['amber']}">الفصل {('الأول','الثاني','الثالث')[i]} · {d}</div>
<div style="display:flex;align-items:baseline;gap:{p(16)}px"><span style="font-family:Lalezar,sans-serif;font-size:{p(verb)}px;line-height:1.05;color:{C['cream']}">{v}</span>
<span style="font-size:{p(desc)}px;color:{C['sand']}">{t}</span></div></div></div>''')
    line_h = p(2*(verb*1.05+day*1.5+gap))
    return f'''<div style="position:absolute;top:{p(top)}px;right:{p(right)}px;width:{p(width)}px;direction:rtl">
<div style="position:absolute;right:{p(12)}px;top:{p(20)}px;height:{line_h}px;width:0;border-right:{max(2,p(4))}px dotted {C['amber']}"></div>
<div style="position:relative;display:flex;flex-direction:column;gap:{p(gap)}px">{''.join(rows)}</div></div>'''

def cta(s, num_size=46, label='للتسجيل · كونوا جزءًا من الحكاية'):
    p = lambda v: round(v*s)
    return f'''<div style="display:flex;align-items:center;gap:{p(18)}px;background:{C['cream']};color:{C['ink']};border-radius:999px;padding:{p(14)}px {p(34)}px {p(14)}px {p(18)}px">
<div style="width:{p(64)}px;height:{p(64)}px;border-radius:50%;background:{C['ember']};display:flex;align-items:center;justify-content:center;flex:none">{icon('phone', p(32), C['cream'], 2.2)}</div>
<div style="display:flex;flex-direction:column">
<div style="font-size:{max(13,p(19))}px;font-weight:700;color:{C['muted']}">{label}</div>
<div dir="ltr" style="font-weight:900;font-size:{p(num_size)}px;line-height:1.05;letter-spacing:1px;text-align:right">22 882 867</div>
</div></div>'''

def prices(s, d=132):
    p = lambda v: round(v*s)
    def one(amount, label, fill):
        bg = f'background:{C["amber"]};color:{C["ink"]};' if fill else f'border:{max(2,p(3))}px solid {C["amber"]};color:{C["cream"]};'
        rot = '-6deg' if fill else '5deg'
        return f'''<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;width:{p(d)}px;height:{p(d)}px;border-radius:50%;{bg}transform:rotate({rot});box-sizing:border-box">
<div style="font-weight:900;font-size:{p(46)}px;line-height:1">{amount}<span style="font-size:{p(20)}px;font-weight:700"> د</span></div>
<div style="font-size:{max(12,p(15))}px;font-weight:700;margin-top:{p(2)}px">{label}</div></div>'''
    return f'''<div style="display:flex;gap:{p(12)}px">{one('100','للمنخرطين',True)}{one('120','لغير المنخرطين',False)}</div>'''

def action_row(s, top, side, num=46, d=132):
    p = lambda v: round(v*s)
    return f'<div style="position:absolute;top:{p(top)}px;right:{p(side)}px;left:{p(side)}px;display:flex;justify-content:space-between;align-items:center;gap:{p(20)}px;direction:rtl">{cta(s,num)}{prices(s,d)}</div>'

def stars(s, U, w=1080, h=900, left=0):
    p = lambda v: round(v*s)
    return f'<img src="{U["stars"]}" alt="" style="position:absolute;top:0;left:{p(left)}px;width:{p(w)}px;height:{p(h)}px;opacity:.9">'

def palm(s, U, which, style):
    return f'<img src="{U[which]}" alt="" style="position:absolute;{style}">'

def frieze(s, U, h=46):
    p = lambda v: round(v*s)
    return f'<div style="position:absolute;bottom:0;left:0;right:0;height:{p(h)}px;background-image:url({U["brick-frieze"]});background-size:auto {p(h)}px;background-repeat:repeat-x;border-top:{max(2,p(3))}px solid {C["amber"]}"></div>'

def grain(U):
    return f'<div style="position:absolute;inset:0;background-image:url({U["grain"]});background-size:256px;opacity:.07;mix-blend-mode:overlay;pointer-events:none"></div>'

def root(W, H, inner, bgcss=None):
    bgcss = bgcss or f'radial-gradient(120% 70% at 50% 24%,{C["sky"]} 0%,{C["night2"]} 42%,#11152F 100%)'
    return f'''<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{bgcss};font-family:Alexandria,sans-serif;color:{C['cream']};direction:rtl">
{inner}
</div>'''

def chapter_dots_x(s, side, W):
    """x of the three chapter dots (right to left) for a grid between `side` margins."""
    inner = W/s - 2*side; col = (inner - 2*12)/3
    return [W/s - side - col/2, W/s - side - col - 12 - col/2, side + col/2]

# ---------------------------------------------------------------- formats

def feed(U):
    s = 1; W, H = 1080, 1350
    cx = chapter_dots_x(s, 56, W); dot_y = 1046
    road = [(942, 500), (1012, 590), (990, 700), (1040, 800), (1010, 930), (cx[0], dot_y)]
    parts = [
      stars(s, U),
      palm(s, U, 'palm-b', 'left:-200px;top:300px;width:560px;height:840px;opacity:.5'),
      palm(s, U, 'palm-a', 'right:-250px;top:560px;width:520px;height:780px;opacity:.35'),
      logos(s, U, 26, h_seal=154, h_unit=126, gap=46),
      opener(s, 196, size=40),
      lighthouse(s, 842, 236, w=200),
      arch(s, U, 262, 540, 600),
      trail(s, W, H, road + [(cx[1], dot_y), (cx[2], dot_y), (84, dot_y)], end=(70, dot_y), uid='F'),
      seal(150, 'F', style='position:absolute;top:262px;left:176px;transform:rotate(-10deg)'),
      title(s, 698, size=184, tag=52),
      facts(s, 968, size=24),
      chapters(s, 1035, 56),
      action_row(s, 1176, 56, num=44, d=124),
      frieze(s, U, 40), grain(U)]
    return W, H, root(W, H, '\n'.join(parts))

def a4(U):
    s = 794/1080; W, H = 794, 1123   # design units 1080 x 1528
    cx = chapter_dots_x(s, 64, W); dot_y = 1206
    road = [(946, 660), (1014, 760), (994, 860), (1044, 960), (1014, 1090), (cx[0], dot_y)]
    parts = [
      stars(s, U, h=1000),
      palm(s, U, 'palm-b', f'left:{round(-200*s)}px;top:{round(340*s)}px;width:{round(580*s)}px;height:{round(870*s)}px;opacity:.5'),
      palm(s, U, 'palm-a', f'right:{round(-250*s)}px;top:{round(660*s)}px;width:{round(540*s)}px;height:{round(810*s)}px;opacity:.35'),
      logos(s, U, 52, h_seal=172, h_unit=140, gap=52),
      opener(s, 248, size=44, sub='كشافة ومرشدات فوج هيبون يتركون بحر المهدية<br>ويتبعون النخيل إلى واحة دقاش', sub_size=24, width=760),
      lighthouse(s, 846, 402, w=200),
      arch(s, U, 396, 560, 614),
      trail(s, W, H, road + [(cx[1], dot_y), (cx[2], dot_y), (88, dot_y)], end=(74, dot_y), uid='A'),
      seal(round(156*s), 'A', style=f'position:absolute;top:{round(396*s)}px;left:{round(166*s)}px;transform:rotate(-10deg)'),
      title(s, 836, size=190, tag=54),
      facts(s, 1120, size=26),
      chapters(s, 1194, 64, verb=46, desc=20, day=21),
      action_row(s, 1346, 64, num=46, d=126),
      frieze(s, U, 52), grain(U)]
    return W, H, root(W, H, '\n'.join(parts))

def story(U):
    s = 1; W, H = 1080, 1920
    cx = chapter_dots_x(s, 56, W); dot_y = 1452
    road = [(948, 770), (1020, 870), (994, 990), (1044, 1110), (1014, 1290), (cx[0], dot_y)]
    parts = [
      stars(s, U, h=1300),
      palm(s, U, 'palm-b', 'left:-210px;top:480px;width:640px;height:960px;opacity:.5'),
      palm(s, U, 'palm-a', 'right:-260px;top:820px;width:560px;height:840px;opacity:.35'),
      logos(s, U, 150, h_seal=184, h_unit=148, gap=52),
      opener(s, 368, size=50, sub='كشافة ومرشدات فوج هيبون يتركون بحر المهدية<br>ويتبعون النخيل إلى واحة دقاش', sub_size=27),
      lighthouse(s, 846, 520, w=206),
      arch(s, U, 520, 620, 720),
      trail(s, W, H, road + [(cx[1], dot_y), (cx[2], dot_y), (84, dot_y)], end=(70, dot_y), uid='S'),
      seal(170, 'S', style='position:absolute;top:520px;left:128px;transform:rotate(-10deg)'),
      title(s, 1080, size=200, tag=58),
      facts(s, 1368, size=25),
      chapters(s, 1440, 56, verb=50, desc=20, day=22),
      action_row(s, 1600, 56, num=46, d=130),
      frieze(s, U, 56), grain(U)]
    return W, H, root(W, H, '\n'.join(parts))

def endcard(U):
    s = 1; W, H = 1920, 1080
    parts = [
      stars(s, U), stars(s, U, left=1080),
      palm(s, U, 'palm-b', 'left:-220px;top:140px;width:620px;height:930px;opacity:.5'),
      arch(s, U, 110, 600, 850, left=150),
      seal(176, 'E', style='position:absolute;top:96px;left:640px;transform:rotate(-10deg)'),
      logos(s, U, 70, h_seal=130, h_unit=104, gap=36, left=900, right=120, justify='flex-start'),
      f'''<div style="position:absolute;top:232px;right:120px;left:860px;text-align:right">
<p style="margin:0;font-family:'Aref Ruqaa',serif;font-weight:700;font-size:40px;line-height:1.2;color:{C['amber']}">كان يا مكان… في شتاء 2026</p>
<h1 style="margin:4px 0 0;font-family:Lalezar,sans-serif;font-weight:400;font-size:150px;line-height:1;color:{C['cream']};text-shadow:0 6px 0 {C['ember']},0 18px 40px rgba(0,0,0,.45)">مخيم الشتاء</h1>
<p style="margin:18px 0 0;font-family:'Aref Ruqaa',serif;font-weight:700;font-size:50px;line-height:1.2;color:{C['amber']}">من البحر إلى النخيل · دقاش، توزر</p></div>''',
      chapters_stack(s, 560, 120, 900, verb=44, desc=22, day=21, gap=22),
      f'<div style="position:absolute;top:880px;right:120px;left:860px;display:flex;justify-content:space-between;align-items:center;gap:20px;direction:rtl">{cta(s,44)}{prices(s,120)}</div>',
      frieze(s, U, 46), grain(U)]
    return W, H, root(W, H, '\n'.join(parts))

def countdown(U):
    s = 1; W, H = 1080, 1920
    inner = f'''<img src="{U['night']}" alt="خيام مضاءة تحت النخيل ليلا" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 40%">
<div style="position:absolute;inset:0;background:linear-gradient(to bottom,rgba(20,24,51,.82) 0%,rgba(20,24,51,.25) 24%,rgba(20,24,51,.55) 44%,rgba(20,24,51,.92) 66%,{C['night']} 100%)"></div>
{logos(s, U, 150, h_seal=170, h_unit=136, gap=48)}
{seal(200,'C',style='position:absolute;top:470px;left:440px;transform:rotate(-8deg)')}
<div style="position:absolute;top:740px;left:0;right:0;text-align:center">
<p style="margin:0;font-family:'Aref Ruqaa',serif;font-weight:700;font-size:72px;line-height:1.2;color:{C['amber']}">بقي على بداية الحكاية</p>
<div style="display:flex;justify-content:center;align-items:baseline;gap:28px;margin-top:6px">
<div style="font-family:Lalezar,sans-serif;font-size:440px;line-height:.95;color:{C['cream']};text-shadow:0 10px 0 {C['ember']}">{{{{days}}}}</div>
<div style="font-family:Lalezar,sans-serif;font-size:130px;line-height:1;color:{C['cream']}">{{{{unit}}}}</div>
</div>
<p style="margin:30px 0 0;font-weight:800;font-size:44px;color:{C['cream']}">مخيم الشتاء · 12 · 13 · 14 ديسمبر 2026</p>
<p style="margin:8px 0 0;font-weight:600;font-size:34px;color:{C['sand']}">دقاش، توزر · فتية وفتيات من 12 إلى 17 سنة</p>
</div>
<div style="position:absolute;top:1500px;left:0;right:0;display:flex;justify-content:center">{cta(s,52)}</div>
{frieze(s,U,56)}{grain(U)}'''
    return W, H, root(W, H, inner, bgcss=C['night'])

FORMATS = {
  'Main': ('مخيم الشتاء — منشور 4:5 (الحكاية)', feed),
  'Print-A4': ('مخيم الشتاء — ملصق A4 للطباعة (الحكاية)', a4),
  'Story': ('مخيم الشتاء — ستوري / حالة واتساب 9:16 (الحكاية)', story),
  'Countdown': ('مخيم الشتاء — ستوري العد التنازلي', countdown),
  'Video-Card': ('مخيم الشتاء — بطاقة الفيديو 16:9 (الحكاية)', endcard),
}

def local_urls():
    m = '../../../03-identity/motifs/'; ph = '../../../02-photos/graded/'; lg = '../../../03-identity/logos/'   # relative to _build/
    return {'brick-tile': m+'brick-tile.svg', 'brick-frieze': m+'brick-frieze.svg', 'stars': m+'stars.svg', 'palm-a': m+'palm-a.svg',
            'palm-b': m+'palm-b.svg', 'hero': ph+'hero-tent-sunset.jpg', 'night': ph+'night-lights.jpg', 'fire': ph+'fire-tents.jpg',
            'grain': m+'grain.png', 'logo-fawj': lg+'fawj-hiboun-seal.png', 'logo-scouts': lg+'unit-scouts-abdelmajid-attia.png',
            'logo-guides': lg+'unit-guides-bchira-ben-mrad.png'}

def local_html(name, U):
    t, fn = FORMATS[name]; W, H, body = fn(U)
    body = body.replace('{{days}}', '7').replace('{{unit}}', 'أيام')
    return W, H, f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{t}</title><style>{FONTS_LOCAL}body{{margin:0}}</style></head><body>{body}</body></html>'

def dc_html(name, U):
    t, fn = FORMATS[name]; W, H, body = fn(U)
    props = {"$preview": {"width": W, "height": H}}
    logic = "return {};"
    if name == 'Countdown':
        props.update({"days": {"editor": "int", "default": 7, "min": 1, "max": 30, "section": "العد التنازلي"}})
        logic = ("const d = this.props.days ?? 7;\n    // 1 and 2 days read better in hours: 24 / 48 ساعة\n"
                 "    if (d <= 2) return { days: String(d * 24), unit: 'ساعة' };\n"
                 "    return { days: String(d), unit: d <= 10 ? 'أيام' : 'يوما' };")
    return W, H, f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>{t}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS_LINK}
<style>
body{{margin:0}}
a{{color:{C['amber']}}}a:hover{{color:{C['cream']}}}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{json.dumps(props, ensure_ascii=False)}'>
class Component extends DCLogic {{
  renderVals() {{
    {logic}
  }}
}}
</script>
</body>
</html>'''

def close_svg_tags(s):
    # the canvas format wants every element closed explicitly
    return re.sub(r'<(rect|path|circle|ellipse|polyline|stop)([^<>]*?)\s*/>', r'<\1\2></\1>', s)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'local'
    BUILD.mkdir(exist_ok=True)
    if mode == 'local':
        U = local_urls()
        for n in FORMATS:
            W, H, h = local_html(n, U)
            (BUILD / f'prev_{n}.html').write_text(h, encoding='utf-8'); print(n, W, H)
    else:
        U = json.loads((HERE / 'canvas_blob_urls.json').read_text())
        out = BUILD / 'canvas' / 'project'; out.mkdir(parents=True, exist_ok=True)
        for n in FORMATS:
            W, H, h = dc_html(n, U)
            (out / f'{n}.dc.html').write_text(close_svg_tags(h), encoding='utf-8'); print(n, W, H)
