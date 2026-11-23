"""Draws the identity motifs into 03-identity/motifs/:
brick-tile.svg, brick-frieze.svg (Djerid brick relief), palm-a.svg, palm-b.svg, palm-light.svg,
stars.svg, stars-tall.svg and grain.png. Seeds are fixed, so the output is identical on every run."""
import math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '03-identity' / 'motifs'
OUT.mkdir(parents=True, exist_ok=True)
import random
from PIL import Image
import numpy as np
random.seed(7)

MORTAR='#7A4A22'; B1='#C98E4E'; B2='#D39A58'; B3='#BD8142'; HI='#EBC07F'; SH='#8F5A2C'

def brick_tile(path):
    # seamless running-bond tile: 2 rows, brick 36x12, mortar 3
    bw,bh,m=36,12,3; W=bw+m; H=2*(bh+m)
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*4}" height="{H*2}" viewBox="0 0 {W*4} {H*2}">',f'<rect width="100%" height="100%" fill="{MORTAR}"/>']
    cols=[B1,B2,B3,B1,B2]
    for r in range(4):
        y=r*(bh+m)+m/2
        off=0 if r%2==0 else -W/2
        for c in range(-1,6):
            x=c*W+off+m/2
            s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{bh}" rx="1.5" fill="{cols[(c+r*2)%5]}"/>')
            s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="2" fill="{HI}" opacity=".45"/>')
    s.append('</svg>'); open(path,'w').write('\n'.join(s))

def frieze(path, cols=60, rows=7, motif='diamond'):
    # a band of bricks where some bricks are "raised" (light face + shadow) to draw Tozeur motifs
    bw,bh,m=30,10,3; W=bw+m; Hh=bh+m
    width=cols*W; height=rows*Hh+m
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',f'<rect width="100%" height="100%" fill="{MORTAR}"/>']
    mid=rows//2
    for r in range(rows):
        off=0 if r%2==0 else -W/2
        for c in range(-1,cols+1):
            x=c*W+off+m/2; y=r*Hh+m/2
            # motif: diamonds every 6 bricks
            period=6
            cc=(c + (0.5 if r%2 else 0))%period
            d=abs(cc-period/2)+abs(r-mid)*0.5
            raised = (motif=='diamond' and abs(d-1.5)<0.6) or (r in (0,rows-1))
            if raised:
                s.append(f'<rect x="{x+2:.1f}" y="{y+2:.1f}" width="{bw}" height="{bh}" fill="{SH}"/>')
                s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{bh}" rx="1" fill="{HI}"/>')
            else:
                s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{bh}" rx="1" fill="{random.choice([B1,B2,B3])}"/>')
    s.append('</svg>'); open(path,'w').write('\n'.join(s))



def palm(path, color='#3B4A8C', w=600, h=900, lean=0.12, n=13, seed=1):
    random.seed(seed)
    top=(w*0.5+w*lean, h*0.30)
    base=(w*0.5, h)
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><g fill="{color}">']
    segs=30; pts_l=[];pts_r=[]
    for i in range(segs+1):
        t=i/segs
        x=base[0]+(top[0]-base[0])*t + math.sin(t*math.pi)*w*0.05
        y=base[1]+(top[1]-base[1])*t
        hw=w*(0.04-0.018*t)+ (2.5 if i%2 else 0)
        pts_l.append((x-hw,y)); pts_r.append((x+hw,y))
    poly=pts_l+pts_r[::-1]
    s.append('<path d="M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in poly)+'Z"/>')
    # dates hanging under crown
    for dx in (-0.07,0.06):
        cx=top[0]+w*dx; cy=top[1]+h*0.035
        s.append(f'<path d="M{top[0]:.1f},{top[1]:.1f} Q{cx:.1f},{cy-10:.1f} {cx:.1f},{cy+6:.1f}" stroke="{color}" stroke-width="4" fill="none"/>')
        for j in range(14):
            s.append(f'<ellipse cx="{cx+random.uniform(-16,16):.1f}" cy="{cy+random.uniform(4,46):.1f}" rx="{random.uniform(4,6):.1f}" ry="{random.uniform(6,8.5):.1f}"/>')
    angs=[-math.pi*0.5 + (k-(n-1)/2)*(math.pi*1.18/(n-1)) + random.uniform(-.05,.05) for k in range(n)]
    for ang in angs:
        L=w*random.uniform(0.36,0.46)
        side=math.cos(ang)
        g=L*(0.18+0.55*abs(side)**1.3)
        sp=[]
        for i in range(25):
            t=i/24
            x=top[0]+math.cos(ang)*L*t
            y=top[1]+math.sin(ang)*L*t + g*t*t
            sp.append((x,y))
        d=[]
        for i in range(2,24):
            x,y=sp[i]; x2,y2=sp[i+1]
            dx,dy=x2-x,y2-y; ln=math.hypot(dx,dy) or 1
            nx,ny=-dy/ln,dx/ln
            lf=w*0.085*math.sin(math.pi*(i/24)**0.8)+3
            for sgn in (1,-1):
                tipx=x+nx*lf*sgn+dx*2.2; tipy=y+ny*lf*sgn+dy*2.2+lf*0.55
                d.append(f'M{x:.1f},{y:.1f} L{tipx:.1f},{tipy:.1f} L{x+dx*0.9:.1f},{y+dy*0.9:.1f}Z')
        s.append(f'<path d="{" ".join(d)}"/>')
        s.append('<polyline fill="none" stroke="'+color+'" stroke-width="5" stroke-linecap="round" points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in sp)+'"/>')
    s.append('</g></svg>')
    open(path,'w').write(chr(10).join(s))

def stars(path,w=1080,h=900,n=140,color='#F6EBD7'):
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    for i in range(n):
        x=random.uniform(0,w); y=random.uniform(0,h)**1.0
        y=h*(random.random()**1.6)
        r=random.choice([0.8,1,1.2,1.4,1.8,2.2])
        o=random.uniform(.35,.95)*(1-y/h*0.6)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" opacity="{o:.2f}"/>')
    # a few sparkle stars
    for i in range(7):
        x=random.uniform(40,w-40); y=random.uniform(20,h*0.6); r=random.uniform(6,11)
        s.append(f'<path d="M{x},{y-r} Q{x},{y} {x+r},{y} Q{x},{y} {x},{y+r} Q{x},{y} {x-r},{y} Q{x},{y} {x},{y-r}Z" fill="#F2B544" opacity=".9"/>')
    s.append('</svg>'); open(path,'w').write('\n'.join(s))


brick_tile(OUT / 'brick-tile.svg')
frieze(OUT / 'brick-frieze.svg')
random.seed(11)
palm(OUT / 'palm-a.svg', seed=3, lean=0.10)
palm(OUT / 'palm-light.svg', color='#F6EBD7', seed=5, lean=0.08)
palm(OUT / 'palm-b.svg', seed=8, lean=-0.12, n=12)
stars(OUT / 'stars.svg')
stars(OUT / 'stars-tall.svg', h=1300, n=200)
rng = np.random.default_rng(5)
Image.fromarray(rng.normal(128, 40, (256, 256)).clip(0, 255).astype(np.uint8), 'L').save(OUT / 'grain.png', optimize=True)
print('motifs written to', OUT)
