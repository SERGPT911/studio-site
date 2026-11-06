"""Static build: copies src/ -> docs/ and fills {{PLACEHOLDERS}} from site.config.json.

Usage:  python build.py
GitHub Pages serves the docs/ folder of the main branch.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "docs"
TEXT_EXT = {".html", ".css", ".js", ".xml", ".txt", ".webmanifest", ".svg"}


def main() -> int:
    cfg = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
    cfg["SITE_URL"] = cfg["SITE_URL"].rstrip("/")
    cfg["TELEGRAM_URL"] = f"https://t.me/{cfg['TELEGRAM_HANDLE'].lstrip('@')}"
    cfg["DOMAIN"] = cfg["SITE_URL"].split("://", 1)[-1].split("/", 1)[0]

    OUT.mkdir(exist_ok=True)
    for child in OUT.iterdir():  # clear contents, keep the folder (may be open by a preview server)
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    for path in SRC.rglob("*"):
        if path.is_dir():
            continue
        dest = OUT / path.relative_to(SRC)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix in TEXT_EXT:
            text = path.read_text(encoding="utf-8")
            for key, val in cfg.items():
                text = text.replace("{{" + key + "}}", str(val))
            if "{{" in text and path.suffix == ".html":
                left = text[text.index("{{"):text.index("{{") + 40]
                print(f"warning: unfilled placeholder in {path.name}: {left!r}")
            dest.write_text(text, encoding="utf-8", newline="\n")
        else:
            shutil.copy2(path, dest)

    # Custom domain: write CNAME only when SITE_URL is not a github.io address.
    if not cfg["DOMAIN"].endswith("github.io"):
        (OUT / "CNAME").write_text(cfg["DOMAIN"] + "\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"built -> {OUT}  (site: {cfg['SITE_URL']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
