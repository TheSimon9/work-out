#!/usr/bin/env python3
"""
Genera le animazioni degli esercizi in anim/<chiave>.webp partendo da Free Exercise DB
(https://github.com/yuhonas/free-exercise-db, pubblico dominio).

Il DB ha due foto per esercizio (inizio/fine). Lo script genera i fotogrammi intermedi
con optical flow (OpenCV DIS) e crea un WebP animato: pausa 850 ms, transizione, pausa, ritorno.

Uso:
  pip install opencv-python-headless pillow numpy
  python tools/mkanim.py leg_press=Leg_Press seated_row=Leverage_Iso_Row
  python tools/mkanim.py --fade pallof=Pallof_Press   # dissolvenza al posto dell'optical flow

Usa --fade quando le due foto hanno inquadrature diverse (zoom, camera che si muove):
l'optical flow in quei casi produce artefatti.
L'ID esercizio è il nome della cartella in exercises/ del repo Free Exercise DB.
"""
import sys, os, urllib.request
import cv2, numpy as np
from PIL import Image

BASE = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/{}/{}.jpg"
OUT = os.path.join(os.path.dirname(__file__), "..", "anim")
W, N, HOLD, STEP, QUALITY = 560, 9, 850, 55, 62


def fetch(ex_id, i):
    data = urllib.request.urlopen(BASE.format(ex_id, i), timeout=30).read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    h = int(img.shape[0] * W / img.shape[1])
    return cv2.resize(img, (W, h), interpolation=cv2.INTER_AREA)


def flow(a, b):
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    return dis.calc(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), cv2.cvtColor(b, cv2.COLOR_BGR2GRAY), None)


def warp(img, fl, t):
    h, w = fl.shape[:2]
    gx, gy = np.meshgrid(np.arange(w), np.arange(h))
    return cv2.remap(img, (gx + fl[..., 0] * t).astype(np.float32), (gy + fl[..., 1] * t).astype(np.float32),
                     cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def build(key, ex_id, fade=False):
    a, b = fetch(ex_id, 0), fetch(ex_id, 1)
    if b.shape != a.shape:
        b = cv2.resize(b, (a.shape[1], a.shape[0]))
    fab, fba = (None, None) if fade else (flow(a, b), flow(b, a))
    mids = []
    for i in range(1, N):
        t = i / N
        t = t * t * (3 - 2 * t)  # smoothstep
        if fade:
            mids.append(cv2.addWeighted(a, 1 - t, b, t, 0))
        else:
            mids.append(cv2.addWeighted(warp(a, fba, t), 1 - t, warp(b, fab, 1 - t), t, 0))
    seq = [a] + mids + [b] + mids[::-1]
    dur = [HOLD] + [STEP] * len(mids) + [HOLD] + [STEP] * len(mids)
    frames = [Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)) for f in seq]
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{key}.webp")
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=dur, loop=0, quality=QUALITY, method=3)
    print(f"{path}  {os.path.getsize(path) // 1024} KB")


if __name__ == "__main__":
    args = sys.argv[1:]
    fade = "--fade" in args
    pairs = [a for a in args if "=" in a]
    if not pairs:
        print(__doc__)
        sys.exit(1)
    for p in pairs:
        k, v = p.split("=", 1)
        build(k, v, fade)
