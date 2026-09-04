# -*- coding: utf-8 -*-
"""논문 테트리스 브랜드 에셋 생성 — Klim 문법 (black/ivory/red, Batang serif)
favicon.png(64/32 내장) · apple-touch-icon.png(180) · og.png(1200x630)
이탤릭은 전단(shear)으로 근사."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)

BLACK=(10,10,10); PAPER=(244,240,230); RED=(211,60,3); DIM=(244,240,230,110)
BATANG_BOLD = r"C:\Windows\Fonts\HANBatangB.ttf"
BATANG_MED  = r"C:\Windows\Fonts\KoPubBatangMedium.ttf"
BATANG_LIGHT= r"C:\Windows\Fonts\HANBatang.ttf"
MONO = r"C:\Windows\Fonts\consola.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def shear(img, k=0.18, bg=BLACK):
    """오른쪽으로 기울이기(이탤릭 근사). k=세로 대비 가로 이동 비율"""
    w,h = img.size
    pad = int(h*k)+2
    canvas = Image.new("RGBA",(w+pad,h), bg+(0,))
    canvas.paste(img,(pad,0),img)
    return canvas.transform((w+pad,h), Image.AFFINE, (1,k,-k*h,0,1,0), resample=Image.BICUBIC)

def glyph(ch, size, color, fpath=BATANG_BOLD):
    """글자 하나를 캔버스 없이 RGBA로 잘라 반환(이탤릭 옵션)"""
    f = font(fpath, size)
    tmp = Image.new("RGBA",(size*2,size*2),(0,0,0,0))
    d = ImageDraw.Draw(tmp)
    d.text((size//2,size//4), ch, font=f, fill=color)
    bbox = tmp.getbbox()
    return tmp.crop(bbox) if bbox else tmp

# ── 파비콘: 검은 사각 + 붉은 이탤릭 '논' + 아이보리 밑줄 ──
def make_icon(size):
    img = Image.new("RGBA",(size,size), BLACK+(255,))
    d = ImageDraw.Draw(img)
    g = shear(glyph("논", int(size*.72), RED+(255,)), k=0.14)
    gw,gh = g.size
    scale = min(size*.62/gw, size*.62/gh, 1.6)
    g = g.resize((int(gw*scale), int(gh*scale)), Image.LANCZOS)
    gx = (size-g.width)//2 + int(size*.02)
    gy = (size-g.height)//2 - int(size*.04)
    img.alpha_composite(g,(gx,gy))
    uy = int(size*.80)
    d.rectangle([int(size*.22), uy, int(size*.78), uy+max(2,size//22)], fill=PAPER)
    return img

make_icon(512).save(os.path.join(OUT,"favicon-512.png"))
make_icon(64).save(os.path.join(OUT,"favicon.png"))
make_icon(180).save(os.path.join(OUT,"apple-touch-icon.png"))

# ── OG 이미지 1200x630 ──
W,H = 1200,630
img = Image.new("RGB",(W,H), BLACK)
d = ImageDraw.Draw(img)

# 배경 떨어지는 글리프들 (희미한 적층 + 우측 붉은 낙하)
ghost_chars = "본연구는읽지않은논문을".replace(" ","")
faint = font(BATANG_MED, 88)
x = 40
import random
random.seed(7)
for i,ch in enumerate(ghost_chars):
    if x > W-120: break
    a = 26 + (i%3)*10
    d.text((x, H-170-(i%4)*46), ch, font=faint, fill=(244,240,230,a))
    x += 96 + (i%2)*18
# 우측 붉은 이탤릭 낙하 조각
fall = [shear(glyph(c, 120, RED),k=0.18) for c in "테트리스"]
fy = 60
for g in fall:
    img.paste(g,(W-320,fy),g); fy += 118
# 낙하 조각 아래 가는 밑줄
d.rectangle([W-316, fy+6, W-176, fy+10], fill=RED)

# 킥커
d.text((64,72), "read or reject  ·  2026.09  ·  no.1", font=font(MONO,26), fill=(244,240,230,150))
d.rectangle([64,120,148,122], fill=RED)

# 헤드라인 (Batang, 혼합 웨이트)
h1a = font(BATANG_LIGHT, 104)
d.text((58,168), "읽지 않는", font=h1a, fill=(244,240,230,235))
g_it = shear(glyph("쌓아서", 118, PAPER), k=0.16, bg=BLACK)
img.paste(g_it,(60,292),g_it)
d.rectangle([60,430,60+g_it.width,436], fill=RED)
g_rd = glyph("지운다", 122, RED)
img.paste(g_rd,(78+g_it.width,290),g_rd)

# 하단: 도메인 + 슬로건
d.text((64,530), "stack.saju.blog", font=font(MONO,34), fill=(244,240,230,200))
d.text((64,578), "논문은 쌓아서 지우는 것이다 — 완독 100% = Accept", font=font(BATANG_MED,26), fill=(244,240,230,120))

img.save(os.path.join(OUT,"og.png"), quality=95)

# 루트에도 복사(로컬 서버·문서루트 패리티 — index.html이 /favicon.png 루트 경로를 참조)
import shutil
ROOT = os.path.dirname(__file__)
for f in ["favicon.png","favicon-512.png","apple-touch-icon.png","og.png"]:
    shutil.copy2(os.path.join(OUT,f), os.path.join(ROOT,f))
print("saved:", os.listdir(OUT), "+ copied to project root")
