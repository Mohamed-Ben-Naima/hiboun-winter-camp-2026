"""Film the teaser page into Reels.

  python render.py check [t1 t2 ...]   key frames -> _build/check/
  python render.py                     both variants -> ../../exports/teaser/
  python render.py teaser|reveal       one variant

One encoded file per scene (same size, rate and encoder), joined with the concat demuxer,
then the sound from sound.py is added with -c:v copy. A silent copy is kept for adding
music inside Instagram.
"""
import os, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
BUILD = HERE / '_build'
OUT = HERE.parents[1] / 'exports' / 'teaser'
CHROME = os.environ.get('CHROME', '/usr/bin/google-chrome')
FPS = 30
ENC = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS)]

SCENES = {
    'teaser': [('s1-hook', 0, 2.1), ('s2-journey', 2.1, 4.75), ('s3-clues', 4.75, 11.15), ('s7-ask', 11.15, 13.1), ('s8-end', 13.1, 15.5)],
    'reveal': [('s1-hook', 0, 2.1), ('s2-journey', 2.1, 4.75), ('s3-clues', 4.75, 11.15), ('r7-stamp', 11.15, 13.6), ('r8-end', 13.6, 17.0)],
}
NAMES = {'teaser': 'Teaser-Reel', 'reveal': 'Reveal-Reel'}

def open_page(p):
    b = p.chromium.launch(executable_path=CHROME, args=['--force-color-profile=srgb', '--disable-lcd-text'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
    pg.goto((BUILD / 'teaser.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(400)
    return b, pg

def shot(pg, t, variant, **kw):
    pg.evaluate(f'seek({t:.5f}, "{variant}")')
    return pg.locator('#stage').screenshot(**kw)

def check(times):
    (BUILD / 'check').mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b, pg = open_page(p)
        for spec in times:
            variant, t = ('reveal', float(spec[1:])) if spec.startswith('r') else ('teaser', float(spec))
            out = BUILD / 'check' / f'{variant}-{t:05.2f}.jpg'
            shot(pg, t, variant, path=str(out), type='jpeg', quality=88)
            print(out.name)
        b.close()

def render(variant):
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = BUILD / 'scenes' / variant; tmp.mkdir(parents=True, exist_ok=True)
    files = []
    with sync_playwright() as p:
        b, pg = open_page(p)
        for name, t0, t1 in SCENES[variant]:
            final = tmp / f'{name}.mp4'; part = tmp / f'{name}.part.mp4'
            ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-', *ENC, str(part)],
                                  stdin=subprocess.PIPE)
            f0, f1 = round(t0 * FPS), round(t1 * FPS)
            for f in range(f0, f1):
                ff.stdin.write(shot(pg, f / FPS, variant, type='jpeg', quality=92))
            ff.stdin.close()
            if ff.wait() != 0: raise SystemExit(f'ffmpeg failed on {name}')
            part.rename(final); files.append(final)
            print(variant, name, f1 - f0, 'frames')
        b.close()
    lst = tmp / 'list.txt'
    lst.write_text(''.join(f"file '{f.name}'\n" for f in files))
    silent = OUT / f'WinterCamp-{NAMES[variant]}-9x16-silent.mp4'
    part = silent.with_suffix('.part.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', '-movflags', '+faststart', str(part)], check=True)
    part.rename(silent)
    mux(variant)

def mux(variant):
    silent = OUT / f'WinterCamp-{NAMES[variant]}-9x16-silent.mp4'
    wav = BUILD / f'sound-{variant}.wav'
    if not wav.exists():
        subprocess.run([sys.executable, str(HERE / 'sound.py'), variant], check=True)
    final = OUT / f'WinterCamp-{NAMES[variant]}-9x16.mp4'
    part = final.with_suffix('.part.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(silent), '-i', str(wav), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(part)], check=True)
    part.rename(final)
    print('wrote', final.name)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'check':
        check(a[1:] or ['0', '0.62', '0.9', '1.6', '2.6', '3.3', '3.9', '4.45', '4.65', '5.4', '7.0', '8.6', '10.4', '11.9', '12.6', '14.6', '15.3',
                        'r11.4', 'r12.0', 'r13.3', 'r15.4'])
    elif a and a[0] == 'mux':
        for v in a[1:] or ['teaser', 'reveal']: mux(v)
    else:
        for v in a or ['teaser', 'reveal']: render(v)
