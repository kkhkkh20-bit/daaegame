"""Reproducible SDK build with a small, game-themed HTML loading shell."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]

def theme(destination):
    index = destination / "index.html"
    html = index.read_text()
    html = html.replace('lang="en-us"', 'lang="ko"')
    html = html.replace('src="web-presplash.jpg"', 'src="loading-scene.webp"')
    html = html.replace('<meta name="theme-color" content="#000" />', '<meta name="theme-color" content="#211a16" />')
    css = """
    <style>
    @font-face{font-family:Galmuri;src:url('Galmuri11.woff2') format('woff2');font-display:swap}
    html,body{margin:0;background:#17120f;font-family:Galmuri,sans-serif;overflow:hidden}
    #presplash{object-fit:cover;filter:brightness(.55)}
    #loading-brand{position:fixed;left:7vw;top:30vh;color:#f3e7ce;pointer-events:none;z-index:2}
    #loading-brand h1{font-size:clamp(26px,5vw,52px);color:#ffdc91;margin:0 0 16px}
    #loading-brand p{font-size:clamp(14px,2vw,22px);line-height:1.7}
    #statusDiv{top:auto;bottom:5vh;max-width:560px;min-width:0;width:80%;background:#211a16ed;border:1px solid #806446;border-radius:8px;padding:16px;z-index:3}
    #statusTextDiv{color:#f3e7ce;font-family:Galmuri,sans-serif;max-height:25vh}
    #statusProgress{accent-color:#d8b568;height:12px}
    #ContextContainer{left:auto;right:8px;top:4px;z-index:100}
    #ContextButton{font-size:15px;opacity:.4}
    #ContextMenu a{color:#f3e7ce;background:#30261f;border-color:#806446;font-size:14px;width:190px}
    #portrait-note{display:none}
    @media(orientation:portrait){#portrait-note{display:block;position:fixed;bottom:15px;left:5%;width:90%;box-sizing:border-box;padding:12px;text-align:center;color:#f3e7ce;background:#30261fe8;border:1px solid #806446;border-radius:8px;font-size:14px;pointer-events:none;z-index:90}}
    </style>
    """
    html = html.replace("</head>", css + "\n</head>")
    html = html.replace('<div id="ContextContainer">', '''<div id="loading-brand"><h1>다람탐정</h1><p>마을로 들어가는 중…<br>처음 접속할 때 실행 파일을 내려받습니다.</p></div>
    <div id="portrait-note">휴대폰을 가로로 돌리면 글씨와 조사 지점이 더 잘 보입니다.</div>
    <div id="ContextContainer">''')
    html = html.replace("Import Saves", "저장 파일 가져오기").replace("Export Saves", "저장 파일 내보내기").replace("Download Log", "실행 기록 다운로드")
    html = html.replace("</body>", """<script>
    const brand=document.getElementById('loading-brand');
    const observer=new MutationObserver(()=>{if(!document.getElementById('presplash')){brand.remove();observer.disconnect();}});
    observer.observe(document.body,{childList:true});
    </script></body>""")
    index.write_text("\n".join(line.rstrip() for line in html.splitlines()) + "\n")
    shutil.copyfile(ROOT / "game/assets/winter-gate.webp", destination / "loading-scene.webp")
    shutil.copyfile(REPO / "preview/ch1-gpt-20261008/art/ui/galmuri11.woff2", destination / "Galmuri11.woff2")
    shutil.copyfile(ROOT / "game/assets/font-license.txt", destination / "Galmuri-OFL.txt")
    (destination / "web-presplash.jpg").unlink(missing_ok=True)
    (destination / "index.html.symbols").unlink(missing_ok=True)
    loader = destination / "renpy-pre.js"
    loader.write_text(loader.read_text().replace("Downloading engine...", "게임을 실행할 준비를 하고 있습니다…").replace("Downloading game data...", "마을의 그림과 음악을 준비하고 있습니다…"))
    manifest_path = destination / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest.update(lang="ko", background_color="#17120f", theme_color="#211a16")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False))
    catalog_path = destination / "pwa_catalog.json"
    catalog = json.loads(catalog_path.read_text())
    catalog["files"] = [f for f in catalog["files"] if (destination / f).exists()]
    catalog["files"] += ["loading-scene.webp", "Galmuri11.woff2", "Galmuri-OFL.txt"]
    catalog_path.write_text(json.dumps(catalog))
    report = {"engine": "Ren'Py 8.5.3", "files": {}}
    for file in sorted(destination.rglob("*")):
        if file.is_file():
            report["files"][str(file.relative_to(destination))] = {
                "bytes": file.stat().st_size,
                "sha256": hashlib.sha256(file.read_bytes()).hexdigest()}
    report["total_bytes"] = sum(v["bytes"] for v in report["files"].values())
    (destination / "build-manifest.json").write_text(json.dumps(report, indent=2))
    print(f"Web build: {destination}; total {report['total_bytes'] / 1024 / 1024:.1f} MiB")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk", required=True, type=Path, help="Ren'Py SDK containing renpy.sh and web/")
    parser.add_argument("--destination", type=Path, default=REPO / "preview/renpy-ch1-test")
    args = parser.parse_args()
    sdk, destination = args.sdk.resolve(), args.destination.resolve()
    if sdk == destination or sdk in destination.parents:
        raise SystemExit("Build destination must be outside the SDK.")
    if destination == ROOT or destination in ROOT.parents or destination == REPO:
        raise SystemExit("Build destination must be separate from project/repository sources.")
    if destination.exists() and any(destination.iterdir()) and not (destination / "renpy.js").exists():
        raise SystemExit("Refusing to replace a directory that is not a Ren'Py web build.")
    subprocess.run(["python3", str(ROOT / "prepare_assets.py")], check=True)
    env = dict(os.environ, SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy")
    lint = subprocess.run([str(sdk / "renpy.sh"), str(ROOT), "lint"], env=env, check=True, capture_output=True, text=True)
    print(lint.stdout)
    # Ren'Py reports some script failures with process status 0; require statistics.
    if "Statistics:" not in lint.stdout:
        raise SystemExit("Ren'Py lint did not complete successfully.")
    build = subprocess.run([str(sdk / "renpy.sh"), str(sdk / "launcher"), "web_build", str(ROOT),
                          "--destination", str(destination)], env=env, capture_output=True, text=True)
    if build.returncode or not (destination / "game.zip").exists():
        print(build.stdout[-3000:]); print(build.stderr[-3000:])
        raise SystemExit("Ren'Py web build failed.")
    theme(destination)

if __name__ == "__main__":
    main()
