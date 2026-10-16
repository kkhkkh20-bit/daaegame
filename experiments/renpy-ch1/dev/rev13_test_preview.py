"""TEST BRANCH ONLY: build the rev13 appearance-test preview (never the public preview).

    python3 dev/rev13_test_preview.py --sdk $RENPY_SDK

1. dev/build_web.py --release ../../preview/room13-rev13-test (seeded from preview/room13-dev
   on first use; the public folder is only read).
2. The page title and the service-worker cache name get a "rev13 시험" suffix, so the test
   page never shares or clears the public game's browser cache. (Saves are already separate:
   config.save_directory ends in -rev13test.)
"""
import argparse, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT.parents[1] / "preview/room13-dev"
TEST = ROOT.parents[1] / "preview/room13-rev13-test"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sdk", required=True)
    a = ap.parse_args()
    if not TEST.exists():
        shutil.copytree(PUBLIC, TEST)
    subprocess.run([sys.executable, str(ROOT / "dev/build_web.py"), "--sdk", a.sdk, "--release", str(TEST),
                    "--work", "/tmp/room13-build-rev13"], check=True)
    sw = TEST / "service-worker.js"
    text = sw.read_text(encoding="utf-8")
    text = text.replace("var cacheName = '다람탐정-눈에-갇힌-마을';", "var cacheName = '다람탐정-rev13-시험';", 1)
    sw.write_text(text, encoding="utf-8")
    index = TEST / "index.html"
    html = index.read_text(encoding="utf-8")
    if "(rev13 시험)" not in html:
        html = html.replace("<title>다람탐정 · 눈에 갇힌 마을", "<title>다람탐정 · 눈에 갇힌 마을 (rev13 시험)", 1)
    index.write_text(html, encoding="utf-8")
    assert "다람탐정-rev13-시험" in sw.read_text(encoding="utf-8")
    print("test preview:", TEST)


if __name__ == "__main__":
    main()
