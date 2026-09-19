"""Generate the PWA icons: sea gradient, a ring and two wave lines."""
import math

from PIL import Image, ImageDraw

TOP = (10, 77, 140)
BOTTOM = (3, 26, 51)
FOAM = (191, 233, 255)
ACCENT = (95, 212, 244)


def make(size, path, inset):
    """inset: fraction of the canvas kept clear around the artwork (maskable needs more)."""
    scale = 4
    s = size * scale
    img = Image.new("RGB", (s, s), TOP)
    px = img.load()
    for y in range(s):
        t = y / (s - 1)
        row = tuple(round(TOP[i] + (BOTTOM[i] - TOP[i]) * t) for i in range(3))
        for x in range(s):
            px[x, y] = row
    d = ImageDraw.Draw(img)
    pad = s * inset
    box = (pad, pad, s - pad, s - pad)
    d.ellipse(box, outline=ACCENT, width=round(s * 0.045))
    inner = s - 2 * pad
    for k, (yf, amp) in enumerate(((0.52, 0.035), (0.64, 0.028))):
        pts = []
        x0, x1 = pad + inner * 0.2, pad + inner * 0.8
        steps = 120
        for i in range(steps + 1):
            x = x0 + (x1 - x0) * i / steps
            y = pad + inner * yf + math.sin(i / steps * math.pi * 3 + k) * inner * amp
            pts.append((x, y))
        d.line(pts, fill=FOAM, width=round(s * 0.035), joint="curve")
    img.resize((size, size), Image.LANCZOS).save(path)


make(192, "icon-192.png", 0.14)
make(512, "icon-512.png", 0.14)
make(512, "icon-maskable-512.png", 0.24)
