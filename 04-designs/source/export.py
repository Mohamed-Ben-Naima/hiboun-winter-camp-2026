"""Renders the layouts from build.py into finished files with headless Chrome (Playwright):
04-designs/exports/  feed 4:5 and story 9:16 JPGs at 2x, the 16:9 video card, the A4 print PDF
                     and countdown/ stories for 7 → 1 days (1 and 2 days show 24 / 48 hours);
03-identity/campaign/ the seal and the title lockup as transparent PNGs.
Run `python build.py local` first."""
import asyncio, html, sys
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image
import build

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
B = HERE / '_build'
EXP = ROOT / '04-designs' / 'exports'
CAMP = ROOT / '03-identity' / 'campaign'
CHROME = None  # set to a Chrome path if Playwright's bundled Chromium is not installed

JPG = [('Main', 1080, 1350, 'WinterCamp-Degache-Feed-4x5.jpg'),
       ('Story', 1080, 1920, 'WinterCamp-Degache-Story-9x16.jpg'),
       ('Video-Card', 1920, 1080, 'WinterCamp-Degache-VideoCard-16x9.jpg')]

async def shot(b, url, w, h, out, scale=2, transparent=False):
    pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=scale)
    await pg.goto(url); await pg.wait_for_timeout(700); await pg.evaluate('document.fonts.ready')
    tmp = B / '_shot.png'
    await pg.screenshot(path=str(tmp), omit_background=transparent)
    await pg.close()
    im = Image.open(tmp)
    if transparent:
        im.crop(im.getbbox()).save(out)
    else:
        im.convert('RGB').save(out, quality=93, optimize=True, progressive=True)
    print(out.relative_to(ROOT))

async def main():
    (EXP / 'countdown').mkdir(parents=True, exist_ok=True); CAMP.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(**({'executable_path': CHROME} if CHROME else {}))
        for n, w, h, out in JPG:
            await shot(b, (B / f'prev_{n}.html').as_uri(), w, h, EXP / out)
        base = (B / 'prev_Countdown.html').read_text(encoding='utf-8')
        for d in range(7, 0, -1):
            num, unit = (str(d * 24), 'ساعة') if d <= 2 else (str(d), 'أيام')
            page = base.replace('>7</div>', f'>{num}</div>', 1).replace('>أيام</div>', f'>{unit}</div>', 1)
            f = B / f'countdown_{d}.html'; f.write_text(page, encoding='utf-8')
            await shot(b, f.as_uri(), 1080, 1920, EXP / 'countdown' / f'WinterCamp-Countdown-{d}.jpg', scale=1)
        pg = await b.new_page(viewport={'width': 794, 'height': 1123})
        await pg.goto((B / 'prev_Print-A4.html').as_uri()); await pg.wait_for_timeout(700); await pg.evaluate('document.fonts.ready')
        await pg.pdf(path=str(EXP / 'WinterCamp-Degache-Print-A4.pdf'), width='794px', height='1123px', print_background=True,
                     margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
        await pg.close(); print('04-designs/exports/WinterCamp-Degache-Print-A4.pdf')
        # campaign marks (transparent)
        C = build.C
        seal = f'<html><head><style>{build.FONTS_LOCAL}html,body{{margin:0;background:transparent}}</style></head><body>{build.seal(200, "P", style="display:block")}</body></html>'
        lock = (f'<html><head><style>{build.FONTS_LOCAL}html,body{{margin:0;background:transparent}}</style></head><body>'
                f'<div style="width:900px;padding:20px 0 30px;text-align:center;direction:rtl">'
                f'<div style="font-family:Lalezar;font-size:188px;line-height:1;color:{C["cream"]};text-shadow:0 6px 0 {C["ember"]}">مخيم الشتاء</div>'
                f'<div style="margin-top:26px;font-family:\'Aref Ruqaa\';font-weight:700;font-size:60px;line-height:1.2;color:{C["amber"]}">بين النخيل والنجوم</div></div></body></html>')
        (B / 'seal.html').write_text(seal, encoding='utf-8'); (B / 'lockup.html').write_text(lock, encoding='utf-8')
        await shot(b, (B / 'seal.html').as_uri(), 200, 200, CAMP / 'WinterCamp-Seal-transparent.png', scale=8, transparent=True)
        await shot(b, (B / 'lockup.html').as_uri(), 900, 340, CAMP / 'WinterCamp-Title-transparent.png', scale=3, transparent=True)
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
