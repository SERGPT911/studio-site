"""Render the OpenGraph image (src/img/og.png, 1200x630) with headless Chrome.

Run after changing STUDIO_NAME in site.config.json:  python tools/make_og.py
Set CHROME env var if Chrome is not in the default Windows location.
"""
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")

cfg = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
html = (ROOT / "tools" / "og.html").read_text(encoding="utf-8").replace("{{STUDIO_NAME}}", cfg["STUDIO_NAME"])
tmp = ROOT / "tools" / "_og_render.html"
tmp.write_text(html, encoding="utf-8")
out = ROOT / "src" / "img" / "og.png"
try:
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1200,630",
                    "--virtual-time-budget=3000", f"--screenshot={out}", tmp.as_uri()],
                   check=True, capture_output=True)
finally:
    tmp.unlink(missing_ok=True)
# Social networks handle JPEG best; keep it small.
from PIL import Image  # noqa: E402
jpg = out.with_suffix(".jpg")
Image.open(out).convert("RGB").save(jpg, "JPEG", quality=84, optimize=True, progressive=True)
out.unlink()
print("wrote", jpg, jpg.stat().st_size // 1024, "KB")
