#!/usr/bin/env python3
"""Renderizador de Reels (motion design) do Intercâmbio Summit 2026.

O template HTML define UMA timeline de animações CSS pausadas; este script
posiciona o currentTime de todas as animações frame a frame, captura JPEGs
via Chromium e monta o MP4 (H.264, 30fps, yuv420p) com o ffmpeg estático
do imageio-ffmpeg. Saída pronta para Reels/Stories: 1080x1920, sem áudio
(a trilha entra no app, com áudio em alta da plataforma).

Uso:
    python3 criativos/render_reel.py reel-abertura.html \
        out=criativos/out/reels/reel-abertura.mp4 [dur=12] [fps=30]

Dependências: pip install playwright imageio-ffmpeg
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, "templates")


def _chromium_path():
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    if os.path.exists(os.path.join(base, "chromium")):
        return os.path.join(base, "chromium")
    hits = glob.glob(os.path.join(base, "chromium-*", "chrome-linux*", "chrome"))
    return hits[0] if hits else None


def render(template, out_mp4, dur=12.0, fps=30, size=(1080, 1920)):
    frames_dir = tempfile.mkdtemp(prefix="reel-frames-")
    total = int(dur * fps)
    w, h = size
    with sync_playwright() as p:
        exe = _chromium_path()
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        page.goto("file://" + os.path.join(TPL, template))
        page.evaluate("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(300)
        for i in range(total):
            t_ms = i * 1000.0 / fps
            page.evaluate(
                "t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; })",
                t_ms,
            )
            page.screenshot(path=os.path.join(frames_dir, f"f{i:05d}.jpg"),
                            type="jpeg", quality=92,
                            clip={"x": 0, "y": 0, "width": w, "height": h})
            if i % (fps * 2) == 0:
                print(f"  frame {i}/{total}")
        browser.close()

    os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([
        ff, "-y", "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "f%05d.jpg"),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        out_mp4,
    ], check=True, capture_output=True)
    shutil.rmtree(frames_dir)
    mb = os.path.getsize(out_mp4) / 1e6
    print(f"ok {out_mp4} ({dur:.0f}s @ {fps}fps, {mb:.1f} MB)")


def main():
    if len(sys.argv) < 2 or not sys.argv[1].endswith(".html"):
        print(__doc__)
        return
    kw = dict(a.split("=", 1) for a in sys.argv[2:] if "=" in a)
    render(sys.argv[1],
           kw.get("out", "/tmp/reel.mp4"),
           dur=float(kw.get("dur", 12)),
           fps=int(kw.get("fps", 30)))


if __name__ == "__main__":
    main()
