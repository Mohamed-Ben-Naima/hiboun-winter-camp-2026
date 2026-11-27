"""Still images that go with the teaser Reel.

  python make_stills.py     -> ../../exports/teaser/  (rendered at 2x)

  Carousel-1..6 (4:5)  the same story as a swipeable post: hook, the four clues, the question.
                       Slide 1 also works on its own as a single teaser post.
  Story-Quiz (9:16)    «وين مخيمنا هالشتاء؟» with an empty band for Instagram's Quiz sticker.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
import make_teaser as T

HERE = Path(__file__).resolve().parent
BUILD = HERE / '_build'
OUT = HERE.parents[1] / 'exports' / 'teaser'
CHROME = os.environ.get('CHROME', '/usr/bin/google-chrome')
C, x3d = T.C, T.x3d
L = '../../../../03-identity/logos/'

def card(i, art, x=0, y=0, r=0, s=1.0, dark=0.0):
    cap, kind, tape = T.CLUES[i]
    f = f'filter:brightness({1-dark});' if dark else ''
    return f'''<div class="card" style="opacity:1;{f}transform:translate({x}px,{y}px) rotate({r}deg) scale({s})">
  <div class="tape" style="opacity:1;background:{tape};transform:rotate({5 if i % 2 else -4}deg)"></div>
  <div class="ph">{art[kind]}</div>
  <div class="cap"><span>{cap}</span></div>
  <div class="num" style="opacity:1;transform:rotate({-8 if i % 2 else 10}deg)">{i+1}</div>
</div>'''

def pile(art, n, ox=0, oy=0, scale=1.0):
    """The logbook pile after n clues have landed (same offsets as the Reel)."""
    out = []
    for i in range(n):
        bx, by, br = T_BASE[i]; dark = 0
        for k in range(i+1, n):
            bx += T_PUSH[i][0]; by += T_PUSH[i][1]; br += T_PUSH[i][2]; dark += .05
        out.append(card(i, art, bx, by, br, 1, dark))
    return f'<div style="position:absolute;inset:0;transform-origin:540px 990px;transform:translate({ox}px,{oy}px) scale({scale})">{"".join(out)}</div>'

T_BASE = [[-26, 10, -5.5], [28, -14, 4.2], [-14, 18, -2.6], [20, -8, 3.4]]
T_PUSH = [[10, -6, .8], [-12, 8, -.9], [8, 6, .6], [0, 0, 0]]

def sea_scene(offset):
    """The opening night scene (moon, lighthouse, the boat), cropped from the Reel's world."""
    return f'''<div style="position:absolute;left:0;top:{-offset}px;width:1080px;height:5120px">{T.world_svg()}</div>
<script>document.getElementById('beam').setAttribute('transform','rotate(-12 975 860)');
document.getElementById('boat').setAttribute('transform','translate(330 1430) rotate(-2)');
document.querySelectorAll('.wave').forEach((e,i)=>e.setAttribute('transform',`translate(${{-(i*37)%+e.dataset.P}} 0)`));
document.querySelectorAll('.tw').forEach((e,i)=>e.setAttribute('opacity',(.45+.55*Math.abs(Math.sin(i*1.7))).toFixed(2)));</script>'''

def doc(W, H, inner, title):
    css = (HERE / 'teaser.css').read_text(encoding='utf-8').replace('{F}', '../../../../03-identity/fonts/')
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{title}</title>
<style>{css}
#stage{{width:{W}px;height:{H}px}}</style></head><body><div id="stage">{inner}
<div id="grain"></div><div id="vig"></div></div></body></html>'''

def logbook(art, n, H):
    head = f'''<div class="paper" style="clip-path:none"></div>
<img src="{L}fawj-hiboun-seal.png" style="position:absolute;top:44px;left:490px;width:100px;height:100px;border-radius:50%" alt="فوج هيبون">
<div style="position:absolute;top:172px;right:96px;font-family:'Reem Kufi';font-weight:700;font-size:40px;color:#7A4A22">كرّاس الرحلة</div>
<div style="position:absolute;top:160px;left:76px;font-family:Lalezar;font-size:54px;color:#E2552D;border:5px dashed #E2552D;border-radius:20px;padding:0 24px;line-height:1.35;background:rgba(255,250,238,.55);transform:rotate(-4deg)">تلميح {n} / 4</div>
<div class="ruqaa" style="top:{H-150}px;font-size:62px;color:#7A4A22">{'ركّزوا مليح… وخمّنوا وين!' if n < 4 else 'آخر تلميح… اسحبوا!'}</div>'''
    return head + pile(art, n, 0, -290, .88)

def build():
    BUILD.mkdir(exist_ok=True)
    art = {'photo': T.photo_palms(), 'dates': T.clue_dates(), 'bricks': T.clue_bricks(), 'chott': T.clue_chott()}
    pages = {}
    # 1: hook
    pages['Carousel-1'] = (1080, 1350, sea_scene(250) + f'''
<img src="{L}fawj-hiboun-seal.png" style="position:absolute;top:40px;left:484px;width:112px;height:112px;border-radius:50%;box-shadow:0 0 0 5px rgba(246,235,215,.16)" alt="فوج هيبون">
<div class="big" style="top:150px;font-size:220px;padding-left:40px;{x3d(C['cream'], C['seadeep'], 14)}">من البحر...</div>
<div class="big" style="top:380px;font-size:290px;padding-left:80px;{x3d(C['amber'], C['emberdeep'], 18)}">لوين؟</div>
<div class="ruqaa" style="top:742px;font-size:60px;color:{C['amber']};padding-left:80px">كان يا مكان… في شتاء 2026</div>
<div style="position:absolute;top:1150px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:16px;background:{C['cream']};color:{C['night']};font-weight:800;font-size:46px;padding:14px 40px 18px;border-radius:999px;white-space:nowrap;box-shadow:0 12px 26px rgba(0,0,0,.35)">
  4 تلميحات · اسحبوا <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="{C['ember']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></div>''')
    # 2-5: the clues
    for n in range(1, 5):
        pages[f'Carousel-{n+1}'] = (1080, 1350, logbook(art, n, 1350))
    # 6: the question
    pages['Carousel-6'] = (1080, 1350, T.end_sky('q') + f'''
{pile(art, 4, 0, -560, .5)}
<div class="big" style="top:690px;font-size:250px;{x3d(C['amber'], C['emberdeep'], 18)}">عرفتوها؟</div>
<div style="position:absolute;top:1000px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:16px;background:{C['cream']};color:{C['night']};font-weight:800;font-size:50px;padding:16px 44px 20px;border-radius:999px;white-space:nowrap;box-shadow:0 12px 26px rgba(0,0,0,.35)">
  <svg width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="{C['night']}" stroke-width="2.2" stroke-linejoin="round"><path d="M20 12a8 8 0 0 1-11.6 7.1L4 20l1-4.2A8 8 0 1 1 20 12z"/></svg>
  اكتبوها في الكومنتار</div>
<div style="position:absolute;top:1150px;left:0;right:0;text-align:center;font-family:'Reem Kufi';font-weight:700;font-size:40px;color:{C['sand']}">مخيم الشتاء · 12 · 13 · 14 ديسمبر 2026 · فوج هيبون</div>
<div class="frieze" style="height:56px;background-size:auto 56px"></div>''')
    # story with room for the quiz sticker
    pages['Story-Quiz'] = (1080, 1920, T.end_sky('s') + f'''
<img src="{L}fawj-hiboun-seal.png" style="position:absolute;top:150px;left:478px;width:124px;height:124px;border-radius:50%;box-shadow:0 0 0 5px rgba(246,235,215,.16)" alt="فوج هيبون">
<div class="big" style="top:300px;font-size:200px;{x3d(C['cream'], C['seadeep'], 14)}">وين مخيمنا</div>
<div class="big" style="top:520px;font-size:220px;{x3d(C['amber'], C['emberdeep'], 18)}">هالشتاء؟</div>
{pile(art, 4, 0, 100, .6)}
<div class="ruqaa" style="top:1400px;font-size:58px;color:{C['sand']}">4 تلميحات… والجواب عندكم</div>
<div class="frieze"></div>''')
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=['--force-color-profile=srgb'])
        for name, (W, H, inner) in pages.items():
            f = BUILD / f'still-{name}.html'
            f.write_text(doc(W, H, inner, name), encoding='utf-8')
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
            pg.goto(f.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
            ratio = '4x5' if H == 1350 else '9x16'
            out = OUT / f'WinterCamp-Teaser-{name}-{ratio}.jpg'
            pg.locator('#stage').screenshot(path=str(out), type='jpeg', quality=92)
            pg.close(); print(out.name)
        b.close()

if __name__ == '__main__':
    build()
