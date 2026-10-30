"""새 판(v2) 1일 시범 웹 빌드.

    python3 dev/build_web.py [--sdk ~/.cache/renpy/renpy-8.5.3-sdk] [--release ../../preview/room13-v2]

지금 판 dev/build_web.py 를 참고해 단순하게 줄였다. 지금 판의 폴더와 공개본은 읽기만 한다.
  - 웹 껍데기(renpy.js·renpy.wasm·renpy.data·renpy-pre.js·index.html·아이콘·글꼴)는 지금 판 공개본
    preview/room13-dev 에서 복사한다. SDK 에는 web 플랫폼이 없어서 지금 판도 공개본의 껍데기를 그대로 쓴다.
    renpy-pre.js 에는 지금 판 빌드가 넣은 내려받기 고리(game-transport.json 을 읽는다)가 이미 들어 있다.
  - Ren'Py 실행부(web/runtime.zip)는 지금 판 experiments/renpy-ch1/web/runtime.zip 을 읽는다.
  - 새 판은 28MB 쯤이라 단계가 셋뿐이다.
      core zip(game.partNN)  실행부·대본·작은 파일(64KB 미만)·줄인 글꼴. 시작할 때 푼다.
      preload                메인화면·대화판·수첩 판 그림과 메인화면 음악. 시작 전에 받는다.
      remote                 나머지(입구·여관·13호 그림, 지도, 나머지 음악). Ren'Py 가 쓸 때 받고,
                             게임이 뜬 뒤 뒤에서 차례로 미리 받는다(prefetch, 다음에 쓸 순서대로).
  - 로딩창은 메인화면과 같은 그림(메인화면의 세 층을 같은 좌표로 합친다). 배경음은 브라우저가 첫 터치
    뒤에만 허락하므로, 거부된 동안만 「화면을 한 번 누르면 음악이 켜집니다」 줄을 편다(지금 판과 같다).
"""
import argparse, hashlib, io, json, re, shutil, subprocess, time, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
OLD = REPO / "experiments/renpy-ch1"
SHELL_FILES = ("index.html", "renpy.js", "renpy.wasm", "renpy.data", "renpy-pre.js", "service-worker.js",
               "manifest.json", "Galmuri11.woff2", "Galmuri-OFL.txt")
STORED = (".png", ".webp", ".jpg", ".mp3", ".ogg", ".otf", ".ttf", ".woff2")
MEDIA = (".png", ".webp", ".jpg", ".mp3", ".ogg", ".wav", ".otf", ".ttf")
SMALL = 64 * 1024
PART = 60 * 1024 * 1024
EXCLUDE = ("cache/", "saves/", "qa/", "tests/")
# 시작 전에 받는 것: 메인화면·마차까지 쓰는 그림, 메인화면 음악, 글꼴.
PRELOAD_DIRS = ("assets/ui-b-main/", "assets/ui-b-options/", "assets/ui-b-dialogue/", "assets/ui-b-question/", "assets/ui-b-field/")
PRELOAD_FILES = ("assets/bgm-title.mp3", "assets/room13-pixel-carriage-empty-winter.webp", "assets/room13-fx-carriage-window-mask.webp")
# 뒤에서 미리 받는 순서(1일에 쓰는 차례). 목록에 없는 remote 파일은 그 뒤에 이름순.
PREFETCH_FIRST = ("assets/bgm-travel.mp3", "assets/room13-gate-wide-morning.webp", "assets/bgm-snow.mp3", "assets/amb-wind.mp3",
                  "assets/room13-pixel-panorama-inn-morning.webp", "assets/bgm-inn.mp3", "assets/amb-fire.mp3",
                  "assets/room13-pixel-wide-room13-before-morning.webp")
# 메인화면 세 층(screens/main_menu.rpy 의 add Transform 줄과 같은 값): (파일, 배율, x, y)
LOADING_LAYERS = (("assets/ui-b-main/b_main_background_postcard.png", 1280.0 / 1672, 0, 0),
                  ("assets/ui-b-main/b_logo.png", .85, -18, 10),
                  ("assets/ui-b-main/b_main_cast_poster_plain.png", 610.0 / 1402, 754, 80))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def font_charset(game):
    chars = set()
    for p in game.rglob("*"):
        if p.suffix in (".rpy", ".json", ".txt"):
            chars.update(p.read_text(errors="ignore"))
    for hi in range(0xB0, 0xC9):  # KS X 1001 한글 2,350자
        for lo in range(0xA1, 0xFF):
            try:
                chars.add(bytes((hi, lo)).decode("euc-kr"))
            except UnicodeDecodeError:
                pass
    for a, b in [(0x20, 0x7E), (0xA0, 0xFF), (0x2000, 0x206F), (0x2190, 0x21FF), (0x2460, 0x24FF), (0x25A0, 0x25FF),
                 (0x2600, 0x26FF), (0x3000, 0x303F), (0x3131, 0x318E), (0xFF01, 0xFF5E)]:
        chars.update(chr(c) for c in range(a, b + 1))
    return "".join(sorted(c for c in chars if ord(c) >= 0x20))


def subset_font(path, text):
    # 글꼴은 첫 화면부터 필요해 크기가 그대로 첫 로딩이 된다. 게임 글자 + 흔한 한글만 남긴다(원본은 그대로).
    from fontTools import subset
    before = path.stat().st_size
    opts = subset.Options(); opts.layout_features = ["*"]; opts.name_IDs = ["*"]; opts.notdef_outline = True
    font = subset.load_font(str(path), opts)
    sub = subset.Subsetter(opts); sub.populate(text=text); sub.subset(font)
    subset.save_font(font, str(path), opts)
    print("글꼴 줄임 %s %.2fMB -> %.2fMB" % (path.name, before / 1e6, path.stat().st_size / 1e6))


def has_transparency(data):
    from PIL import Image
    im = Image.open(io.BytesIO(data))
    if im.mode not in ("RGBA", "LA", "P") and "transparency" not in im.info:
        return False
    return im.convert("RGBA").getchannel("A").getextrema()[0] < 255


def placeholder(data):
    # 받기 전 잠깐 보일 자리 그림. 투명한 그림(인물·물건)은 모자이크 대신 빈 그림(지금 판 0.20.4 소유자 결정).
    from PIL import Image
    im = Image.open(io.BytesIO(data))
    w, h = im.size
    if has_transparency(data):
        im = Image.new("P", (w, h), 0); im.putpalette([0, 0, 0, 0, 0, 0]); im.info["transparency"] = 0
        buf = io.BytesIO(); im.save(buf, "PNG", optimize=True, bits=1)
    else:
        im = im.convert("RGBA").resize((max(1, w // 32), max(1, h // 32)), Image.BOX)
        buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return (w, h), buf.getvalue()


def loading_scene(game, out):
    from PIL import Image
    scene = Image.new("RGBA", (1280, 720), (0, 0, 0, 255))
    for rel, zoom, x, y in LOADING_LAYERS:
        layer = Image.open(game / rel).convert("RGBA")
        layer = layer.resize((round(layer.width * zoom), round(layer.height * zoom)), Image.LANCZOS)
        scene.alpha_composite(layer, (x, y))
    scene.convert("RGB").save(out, "WEBP", quality=88, method=6)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sdk", type=Path, default=Path.home() / ".cache/renpy/renpy-8.5.3-sdk")
    ap.add_argument("--release", type=Path, default=REPO / "preview/room13-v2")
    ap.add_argument("--runtime", type=Path, default=OLD / "web/runtime.zip")
    ap.add_argument("--shell", type=Path, default=REPO / "preview/room13-dev")
    ap.add_argument("--work", type=Path, default=Path("/tmp/room13-v2-build"))
    a = ap.parse_args()
    release, work = a.release.resolve(), a.work.resolve()
    if release == a.shell.resolve():
        raise SystemExit("공개 폴더가 지금 판 공개본과 같다. 지금 판은 건드리지 않는다.")
    stage = work / "stage"
    shutil.rmtree(stage, ignore_errors=True); stage.mkdir(parents=True)

    # 1. 실행부 + game/(시험·캐시·저장·컴파일 결과 제외)
    with zipfile.ZipFile(a.runtime) as z:
        z.extractall(stage)
    src = ROOT / "game"
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src).as_posix()
        if not path.is_file() or rel.startswith(EXCLUDE) or path.suffix in (".rpyc", ".rpymc", ".bak") or "__pycache__" in rel:
            continue
        dest = stage / "game" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
    game = stage / "game"

    # 2. 같은 SDK 로 컴파일하고 lint 를 본다.
    renpy = a.sdk / "renpy.sh"
    subprocess.run([str(renpy), str(stage), "compile"], check=True)
    lint = subprocess.run([str(renpy), str(stage), "lint"], capture_output=True, text=True)
    (work / "lint.txt").write_text(lint.stdout)
    if any(re.search(r"\.rpy:\d+ ", line) for line in lint.stdout.splitlines()):
        raise SystemExit("lint 문제가 있다: " + str(work / "lint.txt"))
    shutil.rmtree(game / "cache", ignore_errors=True)
    shutil.rmtree(game / "saves", ignore_errors=True)
    for junk in ("log.txt", "errors.txt", "traceback.txt", "lint.txt"):
        (stage / junk).unlink(missing_ok=True)
    subset_font(game / "assets/Pretendard-Regular.otf", font_charset(game))

    # 3. 나누기: core zip / preload / remote
    preload, remote, remote_lines = [], [], []
    for path in sorted((game / "assets").rglob("*")):
        rel = path.relative_to(game).as_posix()
        suffix = path.suffix.lower()
        if not path.is_file() or suffix not in MEDIA:
            continue
        size = path.stat().st_size
        if suffix == ".wav" or (size < SMALL and suffix != ".mp3"):
            continue  # core zip 에 들어간다(효과음은 자리 소리로 대신할 수 없다)
        if rel.startswith(PRELOAD_DIRS) or rel in PRELOAD_FILES or suffix in (".otf", ".ttf"):
            preload.append(rel)
        elif suffix == ".mp3":
            remote.append(rel); remote_lines += [rel, "music -"]
        else:
            (w, h), thumb = placeholder(path.read_bytes())
            ph = stage / "_placeholders" / rel
            ph.parent.mkdir(parents=True, exist_ok=True); ph.write_bytes(thumb)
            remote.append(rel); remote_lines += [rel, "image %d,%d" % (w, h)]
    (game / "renpyweb_remote_files.txt").write_text("".join(line + "\n" for line in remote_lines))

    archive = work / "game.zip"
    separate = {"game/" + r for r in preload + remote}
    with zipfile.ZipFile(archive, "w") as z:
        for path in sorted(stage.rglob("*")):
            rel = path.relative_to(stage).as_posix()
            if not path.is_file() or rel in separate:
                continue
            info = zipfile.ZipInfo(rel, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED if rel.endswith(STORED) else zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, path.read_bytes())
    data = archive.read_bytes()

    # 4. 공개 폴더: 지난 빌드 결과를 지우고 새로 쓴다(이 폴더는 빌드로만 만든다).
    shutil.rmtree(release, ignore_errors=True); release.mkdir(parents=True)
    parts = []
    for index, at in enumerate(range(0, len(data), PART), 1):
        chunk = data[at:at + PART]; name = "game.part%02d" % index
        (release / name).write_bytes(chunk)
        parts.append({"file": name, "bytes": len(chunk), "sha256": sha(chunk)})
    preload_entries = []
    for rel in preload + remote:
        blob = (game / rel).read_bytes()
        dest = release / "game" / rel
        dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(blob)
        if rel in preload:
            preload_entries.append({"file": "game/" + rel, "bytes": len(blob), "sha256": sha(blob)})
    # 메인화면 음악을 맨 먼저(로딩창 음악과 같은 주소라 한 번만 받는다).
    preload_entries.sort(key=lambda e: e["file"] != "game/assets/bgm-title.mp3")
    order = [r for r in PREFETCH_FIRST if r in remote] + sorted(r for r in remote if r not in PREFETCH_FIRST)
    transport = {"multipart": True, "archive_bytes": len(data), "archive_sha256": sha(data), "parts": parts,
                 "preload": preload_entries,
                 "asset_versions": {"game/" + r: sha((game / r).read_bytes())[:12] for r in remote},
                 "prefetch": ["game/" + r for r in order], "by_day": {}}
    (release / "game-transport.json").write_text(json.dumps(transport, indent=1))

    # 5. 웹 껍데기(지금 판 공개본에서 복사만 한다)와 새 판 이름·로딩 그림·음악 안내
    for name in SHELL_FILES:
        shutil.copy2(a.shell / name, release / name)
    shutil.copytree(a.shell / "icons", release / "icons")
    loading_scene(game, release / "loading-scene.webp")
    music_hash = sha((game / "assets/bgm-title.mp3").read_bytes())[:12]
    index = release / "index.html"
    s = index.read_text()
    s, n = re.subn(r"<title>.*?</title>", "<title>다람탐정 v2 · 1일 시범</title>", s, count=1); assert n == 1
    s, n = re.subn(r"bgm-title\.mp3\?v=[0-9a-f]+", "bgm-title.mp3?v=" + music_hash, s); assert n == 1
    assert 'src="loading-scene.webp"' in s and 'class="loading-audio-hint" hidden' in s
    index.write_text(s)
    # 같은 사이트의 지금 판과 저장 캐시가 섞이지 않게 서비스 워커 캐시 이름을 바꾼다.
    sw = release / "service-worker.js"
    s = sw.read_text(); s, n = re.subn(r"var cacheName = '[^']*';", "var cacheName = '다람탐정-v2-시범';", s); assert n == 1
    sw.write_text(s)
    man = json.loads((release / "manifest.json").read_text())
    man["name"] = "다람탐정 v2 · 1일 시범"
    (release / "manifest.json").write_text(json.dumps(man, ensure_ascii=False))

    files = sorted(p.relative_to(release).as_posix() for p in release.rglob("*") if p.is_file())
    manifest = {"files": {f: {"bytes": (release / f).stat().st_size, "sha256": sha((release / f).read_bytes())} for f in files},
                "built": time.strftime("%Y-%m-%d %H:%M:%S")}
    manifest["total_bytes"] = sum(v["bytes"] for v in manifest["files"].values())
    (release / "build-manifest.json").write_text(json.dumps(manifest, indent=1))

    shell_first = sum((release / f).stat().st_size for f in ("index.html", "renpy.js", "renpy.wasm", "renpy.data", "renpy-pre.js", "loading-scene.webp"))
    first = len(data) + sum(e["bytes"] for e in preload_entries)
    summary = dict(core_zip_bytes=len(data), preload_files=len(preload_entries), preload_bytes=first - len(data),
                   first_load_game_bytes=first, first_load_with_engine_bytes=first + shell_first,
                   remote_files=len(remote), remote_bytes=sum((game / r).stat().st_size for r in remote),
                   release_total_bytes=manifest["total_bytes"])
    (work / "build-report.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
