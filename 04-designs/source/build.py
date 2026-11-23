"""Builds the Winter Camp layouts (feed 4:5, A4, story 9:16, countdown, 16:9 video card).

  python build.py local   -> _build/prev_<Name>.html, rendered by export.py (local fonts and files)
  python build.py dc      -> _build/canvas/project/<Name>.dc.html, the artboards of the Design canvas
                             (Google Fonts + the canvas's /_blob urls from canvas_blob_urls.json)
All copy is Arabic; every layout shares one anatomy: header, arch + seal, title, info row, call pill + prices, frieze."""
import json, sys, os, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BUILD = HERE / '_build'

C = dict(night='#141833', night2='#1A2150', sky='#2A3470', cream='#F6EBD7', sand='#D9CBB0',
         amber='#F2B544', ember='#E2552D', brick='#C98E4E', brickhi='#E9C48A', ink='#141833', muted='#5A4A3A')

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

def moon(size):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 74 74" aria-hidden="true"><path d="M52 8a30 30 0 1 0 14 52A26 26 0 1 1 52 8z" fill="{C["amber"]}"></path></svg>'

def header(s, top, side, align='space-between', moon_on=True):
    p = lambda v: round(v*s)
    return f'''<div style="position:absolute;top:{p(top)}px;right:{p(side)}px;left:{p(side)}px;display:flex;justify-content:{align};align-items:flex-start">
<div style="display:flex;flex-direction:column;gap:{p(6)}px">
<div style="font-family:'Reem Kufi',sans-serif;font-weight:600;font-size:{max(13,p(22))}px;letter-spacing:.5px;color:{C['brickhi']}">الكشافة التونسية · جهة المهدية</div>
<div style="font-weight:800;font-size:{p(30)}px;color:{C['cream']}">فرقة كشافة ومرشدات فوج هيبون</div>
</div>
{moon(p(74)) if moon_on else ''}
</div>'''

def arch(s, U, top, w, h, left=None, img='hero', pos='50% 58%', alt='خيمة تحت النخيل في واحة دقاش عند الغروب'):
    p = lambda v: round(v*s)
    frame = p(20)
    pos_css = f'left:{p(left)}px' if left is not None else f'left:{(round(1080*s)-p(w))//2}px'
    return f'''<div style="position:absolute;top:{p(top)}px;{pos_css};width:{p(w)}px;height:{p(h)}px;border-radius:{p(w)//2}px {p(w)//2}px 0 0;background-image:url({U['brick-tile']});background-size:{p(148)}px auto;padding:{frame}px;box-sizing:border-box;box-shadow:0 {p(30)}px {p(60)}px rgba(5,7,20,.55)">
<div style="position:relative;width:100%;height:100%;border-radius:{p(w)//2-frame}px {p(w)//2-frame}px 0 0;overflow:hidden;box-shadow:inset 0 0 0 {max(2,p(3))}px {C['cream']}">
<img src="{U[img]}" alt="{alt}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos}">
<div style="position:absolute;left:0;right:0;bottom:0;height:46%;background:linear-gradient(to top,rgba(17,21,47,.95),rgba(17,21,47,0))"></div>
</div></div>'''

def title(s, top, size=188, left=0, right=0, align='center', tag=56):
    p = lambda v: round(v*s)
    return f'''<div style="position:absolute;top:{p(top)}px;left:{p(left)}px;right:{p(right)}px;text-align:{align}">
<h1 style="margin:0;font-family:Lalezar,sans-serif;font-weight:400;font-size:{p(size)}px;line-height:1;color:{C['cream']};text-shadow:0 {p(6)}px 0 {C['ember']},0 {p(18)}px {p(40)}px rgba(0,0,0,.45)">مخيم الشتاء</h1>
<p style="margin:{p(6)}px 0 0;font-family:'Aref Ruqaa',serif;font-weight:700;font-size:{p(tag)}px;line-height:1.2;color:{C['amber']}">بين النخيل والنجوم</p>
</div>'''

def info_items(s, fsmin=12):
    p = lambda v: round(v*s)
    sub = max(fsmin, p(21))
    return [
     ('cal', '12 · 13 · 14 ديسمبر', '2026 · من السبت إلى الإثنين'),
     ('pin', 'دقاش، توزر', 'واحة الجريد · الجنوب التونسي'),
     ('people', 'فتية وفتيات', 'من 12 إلى 17 سنة'),
    ], sub

def info_row(s, top, side, fsmin=12, big=36):
    p = lambda v: round(v*s)
    items, sub = info_items(s, fsmin)
    line = f'{max(1,p(2))}px solid rgba(246,235,215,.22)'
    cells = []
    for i,(ic,a,b) in enumerate(items):
        border = f'border-right:{line};border-left:{line};' if i==1 else ''
        cells.append(f'''<div style="display:flex;flex-direction:column;align-items:center;gap:{p(6)}px;text-align:center;{border}">
{icon(ic, p(34), C['amber'])}
<div style="font-weight:800;font-size:{p(big)}px;line-height:1.1;white-space:nowrap;color:{C['cream']}">{a}</div>
<div style="font-size:{sub}px;color:{C['sand']}">{b}</div></div>''')
    return f'''<div style="position:absolute;top:{p(top)}px;right:{p(side)}px;left:{p(side)}px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:{line};border-bottom:{line};padding:{p(22)}px 0">
{''.join(cells)}</div>'''

def info_stack(s, top, right, width, fsmin=12, big=40):
    p = lambda v: round(v*s)
    items, sub = info_items(s, fsmin)
    rows = []
    for ic,a,b in items:
        rows.append(f'''<div style="display:flex;align-items:center;gap:{p(20)}px">
<div style="width:{p(64)}px;height:{p(64)}px;border-radius:50%;border:{max(2,p(2))}px solid {C['amber']};display:flex;align-items:center;justify-content:center;flex:none">{icon(ic, p(32), C['amber'])}</div>
<div style="display:flex;flex-direction:column"><div style="font-weight:800;font-size:{p(big)}px;line-height:1.15;color:{C['cream']}">{a}</div>
<div style="font-size:{sub}px;color:{C['sand']}">{b}</div></div></div>''')
    return f'''<div style="position:absolute;top:{p(top)}px;right:{p(right)}px;width:{p(width)}px;display:flex;flex-direction:column;gap:{p(22)}px">{''.join(rows)}</div>'''

def cta(s, num_size=46):
    p = lambda v: round(v*s)
    return f'''<div style="display:flex;align-items:center;gap:{p(18)}px;background:{C['cream']};color:{C['ink']};border-radius:999px;padding:{p(14)}px {p(34)}px {p(14)}px {p(18)}px">
<div style="width:{p(64)}px;height:{p(64)}px;border-radius:50%;background:{C['ember']};display:flex;align-items:center;justify-content:center;flex:none">{icon('phone', p(32), C['cream'], 2.2)}</div>
<div style="display:flex;flex-direction:column">
<div style="font-size:{max(13,p(20))}px;font-weight:600;color:{C['muted']}">للتسجيل والاستفسار</div>
<div dir="ltr" style="font-weight:900;font-size:{p(num_size)}px;line-height:1.05;letter-spacing:1px;text-align:right">22 882 867</div>
</div></div>'''

def prices(s, d=140):
    p = lambda v: round(v*s)
    def one(amount, label, fill):
        bg = f'background:{C["amber"]};color:{C["ink"]};' if fill else f'border:{max(2,p(3))}px solid {C["amber"]};color:{C["cream"]};'
        rot = '-6deg' if fill else '5deg'
        return f'''<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;width:{p(d)}px;height:{p(d)}px;border-radius:50%;{bg}transform:rotate({rot});box-sizing:border-box">
<div style="font-weight:900;font-size:{p(48)}px;line-height:1">{amount}<span style="font-size:{p(20)}px;font-weight:700"> د</span></div>
<div style="font-size:{max(12,p(16))}px;font-weight:700;margin-top:{p(2)}px">{label}</div></div>'''
    return f'''<div style="display:flex;gap:{p(14)}px">{one('100','للمنخرطين',True)}{one('120','لغير المنخرطين',False)}</div>'''

def bg(s, W, H, U, palms=True, stars_h=900):
    p = lambda v: round(v*s)
    out = [f'<img src="{U["stars"]}" alt="" style="position:absolute;top:0;left:0;width:{p(1080)}px;height:{p(stars_h)}px;opacity:.9">']
    if W > 1500:  # landscape: second star field
        out.append(f'<img src="{U["stars"]}" alt="" style="position:absolute;top:0;left:{p(1080)}px;width:{p(1080)}px;height:{p(stars_h)}px;opacity:.9">')
    return out

def frieze(s, U, h=46):
    p = lambda v: round(v*s)
    return f'<div style="position:absolute;bottom:0;left:0;right:0;height:{p(h)}px;background-image:url({U["brick-frieze"]});background-size:auto {p(h)}px;background-repeat:repeat-x;border-top:{max(2,p(3))}px solid {C["amber"]}"></div>'

def grain(U):
    return f'<div style="position:absolute;inset:0;background-image:url({U["grain"]});background-size:256px;opacity:.07;mix-blend-mode:overlay;pointer-events:none"></div>'

def root(W, H, inner, bgcss=None):
    bgcss = bgcss or f'radial-gradient(120% 70% at 50% 18%,{C["sky"]} 0%,{C["night2"]} 42%,#11152F 100%)'
    return f'''<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{bgcss};font-family:Alexandria,sans-serif;color:{C['cream']};direction:rtl">
{inner}
</div>'''

# ---------- formats ----------
def feed(U):
    s=1; W,H=1080,1350
    parts = bg(s,W,H,U) + [
      f'<img src="{U["palm-a"]}" alt="" style="position:absolute;right:-170px;top:300px;width:540px;height:810px;opacity:.55">',
      f'<img src="{U["palm-b"]}" alt="" style="position:absolute;left:-190px;top:230px;width:580px;height:870px;opacity:.55">',
      header(s,44,64),
      arch(s,U,168,600,640),
      seal(196,'F',style='position:absolute;top:190px;left:142px;transform:rotate(-10deg)'),
      title(s,652),
      info_row(s,956,64),
      f'<div style="position:absolute;top:1128px;right:64px;left:64px;display:flex;justify-content:space-between;align-items:center;gap:24px">{cta(s)}{prices(s)}</div>',
      frieze(s,U), grain(U)]
    return W,H,root(W,H,'\n'.join(parts))

def a4(U):
    s=794/1080; W,H=794,1123  # design units 1080 x 1528
    p=lambda v: round(v*s)
    parts = bg(s,W,H,U,stars_h=1000) + [
      f'<img src="{U["palm-a"]}" alt="" style="position:absolute;right:{p(-170)}px;top:{p(380)}px;width:{p(560)}px;height:{p(840)}px;opacity:.55">',
      f'<img src="{U["palm-b"]}" alt="" style="position:absolute;left:{p(-190)}px;top:{p(300)}px;width:{p(600)}px;height:{p(900)}px;opacity:.55">',
      header(s,64,72),
      arch(s,U,200,640,760),
      seal(p(200),'A',style=f'position:absolute;top:{p(224)}px;left:{p(120)}px;transform:rotate(-10deg)'),
      title(s,808,size=196,tag=60),
      info_row(s,1118,72,fsmin=13,big=34),
      f'<div style="position:absolute;top:{p(1300)}px;right:{p(72)}px;left:{p(72)}px;display:flex;justify-content:space-between;align-items:center;gap:{p(24)}px">{cta(s,48)}{prices(s,148)}</div>',
      frieze(s,U,56), grain(U)]
    return W,H,root(W,H,'\n'.join(parts))

def story(U):
    s=1; W,H=1080,1920
    parts = bg(s,W,H,U,stars_h=1300) + [
      f'<img src="{U["palm-a"]}" alt="" style="position:absolute;right:-190px;top:520px;width:600px;height:900px;opacity:.55">',
      f'<img src="{U["palm-b"]}" alt="" style="position:absolute;left:-210px;top:420px;width:640px;height:960px;opacity:.55">',
      header(s,150,72),
      arch(s,U,320,720,900),
      seal(220,'S',style='position:absolute;top:330px;left:96px;transform:rotate(-10deg)'),
      title(s,1060,size=208,tag=64),
      info_row(s,1400,64,big=36),
      f'<div style="position:absolute;top:1572px;right:64px;left:64px;display:flex;justify-content:space-between;align-items:center;gap:24px">{cta(s,48)}{prices(s,146)}</div>',
      frieze(s,U,56), grain(U)]
    return W,H,root(W,H,'\n'.join(parts))

def endcard(U):
    s=1; W,H=1920,1080
    parts = bg(s,W,H,U,stars_h=900) + [
      f'<img src="{U["palm-b"]}" alt="" style="position:absolute;left:-220px;top:140px;width:620px;height:930px;opacity:.55">',
      arch(s,U,110,600,850,left=150),
      seal(200,'E',style='position:absolute;top:110px;left:620px;transform:rotate(-10deg)'),
      header(s,90,120,align='flex-start',moon_on=False).replace('left:120px','left:900px'),
      f'''<div style="position:absolute;top:250px;right:120px;left:900px;text-align:right">
<h1 style="margin:0;font-family:Lalezar,sans-serif;font-weight:400;font-size:176px;line-height:1;color:{C['cream']};text-shadow:0 6px 0 {C['ember']},0 18px 40px rgba(0,0,0,.45)">مخيم الشتاء</h1>
<p style="margin:26px 0 0;font-family:'Aref Ruqaa',serif;font-weight:700;font-size:58px;line-height:1.2;color:{C['amber']}">بين النخيل والنجوم</p></div>''',
      info_stack(s,548,120,640,big=38),
      f'<div style="position:absolute;top:826px;right:120px;left:900px;display:flex;justify-content:space-between;align-items:center;gap:20px">{cta(s,46)}{prices(s,132)}</div>',
      frieze(s,U,46), grain(U)]
    return W,H,root(W,H,'\n'.join(parts))

def countdown(U):
    s=1; W,H=1080,1920
    inner = f'''<img src="{U['night']}" alt="خيام مضاءة تحت النخيل ليلا" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 40%">
<div style="position:absolute;inset:0;background:linear-gradient(to bottom,rgba(20,24,51,.55) 0%,rgba(20,24,51,.12) 26%,rgba(20,24,51,.55) 44%,rgba(20,24,51,.92) 66%,{C['night']} 100%)"></div>
{header(s,150,72)}
{seal(230,'C',style='position:absolute;top:420px;left:425px;transform:rotate(-8deg)')}
<div style="position:absolute;top:760px;left:0;right:0;text-align:center">
<p style="margin:0;font-family:'Aref Ruqaa',serif;font-weight:700;font-size:74px;line-height:1.2;color:{C['amber']}">بقي على مخيم الشتاء</p>
<div style="display:flex;justify-content:center;align-items:baseline;gap:28px;margin-top:6px">
<div style="font-family:Lalezar,sans-serif;font-size:440px;line-height:.95;color:{C['cream']};text-shadow:0 10px 0 {C['ember']}">{{{{days}}}}</div>
<div style="font-family:Lalezar,sans-serif;font-size:130px;line-height:1;color:{C['cream']}">{{{{unit}}}}</div>
</div>
<p style="margin:30px 0 0;font-weight:800;font-size:44px;color:{C['cream']}">12 · 13 · 14 ديسمبر 2026</p>
<p style="margin:8px 0 0;font-weight:600;font-size:34px;color:{C['sand']}">دقاش، توزر · فتية وفتيات من 12 إلى 17 سنة</p>
</div>
<div style="position:absolute;top:1500px;left:0;right:0;display:flex;justify-content:center">{cta(s,52)}</div>
{frieze(s,U,56)}{grain(U)}'''
    return W,H,root(W,H,inner, bgcss=C['night'])

FORMATS = {
  'Main': ('مخيم الشتاء — منشور فيسبوك/إنستغرام 4:5', feed),
  'Print-A4': ('مخيم الشتاء — ملصق A4 للطباعة', a4),
  'Story': ('مخيم الشتاء — ستوري / حالة واتساب 9:16', story),
  'Countdown': ('مخيم الشتاء — ستوري العد التنازلي', countdown),
  'Video-Card': ('مخيم الشتاء — بطاقة الفيديو 16:9', endcard),
}

def local_urls():
    m='../../../03-identity/motifs/'; p='../../../02-photos/graded/'   # relative to _build/
    return {'brick-tile':m+'brick-tile.svg','brick-frieze':m+'brick-frieze.svg','stars':m+'stars.svg','palm-a':m+'palm-a.svg',
            'palm-b':m+'palm-b.svg','hero':p+'hero-tent-sunset.jpg','night':p+'night-lights.jpg','fire':p+'fire-tents.jpg','grain':m+'grain.png'}

def local_html(name, U):
    t, fn = FORMATS[name]; W,H,body = fn(U)
    body = body.replace('{{days}}','7').replace('{{unit}}','أيام')
    return W,H,f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{t}</title><style>{FONTS_LOCAL}body{{margin:0}}</style></head><body>{body}</body></html>'

def dc_html(name, U):
    t, fn = FORMATS[name]; W,H,body = fn(U)
    props = {"$preview":{"width":W,"height":H}}
    logic = "return {};"
    if name=='Countdown':
        props.update({"days":{"editor":"int","default":7,"min":1,"max":30,"section":"العد التنازلي"}})
        logic = ("const d = this.props.days ?? 7;\n    // 1 and 2 days read better in hours: 24 / 48 ساعة\n"
                 "    if (d <= 2) return { days: String(d * 24), unit: 'ساعة' };\n"
                 "    return { days: String(d), unit: d <= 10 ? 'أيام' : 'يوما' };")
    return W,H,f'''<!doctype html>
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
    return re.sub(r'<(rect|path|circle|ellipse|polyline)([^<>]*?)\s*/>', r'<\1\2></\1>', s)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'local'
    BUILD.mkdir(exist_ok=True)
    if mode == 'local':
        U = local_urls()
        for n in FORMATS:
            W,H,h = local_html(n,U)
            (BUILD / f'prev_{n}.html').write_text(h, encoding='utf-8'); print(n,W,H)
    else:
        U = json.loads((HERE / 'canvas_blob_urls.json').read_text())
        out = BUILD / 'canvas' / 'project'; out.mkdir(parents=True, exist_ok=True)
        for n in FORMATS:
            W,H,h = dc_html(n,U)
            (out / f'{n}.dc.html').write_text(close_svg_tags(h), encoding='utf-8'); print(n,W,H)
