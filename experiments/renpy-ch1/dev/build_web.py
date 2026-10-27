"""Build the Room13 web release from this project folder.

    python dev/build_web.py --sdk /path/renpy-8.5.3-sdk [--release ../../preview/room13-dev]

The project folder is the single source of truth: scripts, data and the final
web art live in game/. Nothing is taken from a previous release.

Release layout (preview/room13-dev):
  game.partNN             core zip: Ren'Py runtime (web/runtime.zip), scripts,
                          data, small UI images, sound effects, placeholders.
                          Unpacked at start, so it is kept small.
  game/assets/<file>      title/carriage/entrance dependencies are fetched before
                          start. Other images and audio use Ren'Py progressive
                          downloads at original quality. Every external request
                          uses a file hash so replaced art gets a fresh cache key.
  game-transport.json     what the loader fetches; renpy-pre.js reads it.

Art in game/assets is already web-ready (lossy WebP q95, alpha lossless). Add
new art with dev/import_art.py; the build never re-encodes.
"""
import ast, argparse, fnmatch, hashlib, io, json, os, re, shutil, subprocess, sys, time, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORED = (".png", ".webp", ".jpg", ".mp3", ".ogg", ".opus", ".woff2", ".ttf", ".otf")
MEDIA = (".png", ".webp", ".jpg", ".svg", ".mp3", ".ogg", ".opus", ".wav", ".ttf", ".otf", ".woff2")
# Files below this size ride in the core zip (cheaper than a request).
SMALL = 64 * 1024
# Never shipped (also mirrors build.classify(..., None) in options.rpy).
EXCLUDE = ("cache/*", "saves/*", "qa_tests/*", "*.rpyc", "*.rpymc", "*.bak",
           "assets/room13-painted-*.png", "assets/room13-painted-layouts.json",
           "assets/room13-hall.png", "assets/room13-passage.png")
# Ren'Py progressive download (placeholder first, real file when needed).
REMOTE_MUSIC = "assets/*.mp3"
# Legacy campaign art (archived chapters): only fetched when those open.
REMOTE_IMAGE = "assets/*.png"
# Click-to-open close-up backgrounds (0.18.22): fetched when a close-up first opens.
REMOTE_CLOSEUP = ("assets/room13-pixel-life-*.webp", "assets/r13-gimmick-*.webp")
# Not needed before the game starts (0.18.35): late-story cinematics and the day-14 altar.
# Fetched when first drawn and warmed in the background once the game runs (transport "prefetch").
# All non-opening expressions now use the existing progressive downloader.
REMOTE_LATER = ("assets/room13-aftermath-*.webp", "assets/room13-pixel-cinematic-*.webp", "assets/room13-pixel-altar-*.webp",
                "assets/room13-pixel-ready-altar*.webp")
# Art replaced by an NPC redesign (dev/apply_npc_redesign.py): kept so old saves
# that still hold the old picture can draw it, but never part of the first load.
REDESIGN_BACKUP = ROOT / "art/npc-redesign-20261015/original-entries.json"
# 0.18.89: the episode art (dev/apply_ep_art.py) replaced the teacher and Neoul the same way.
REDESIGN_BACKUPS = (REDESIGN_BACKUP, ROOT / "art/ep-art-20261016/original-entries.json")


# Only title + carriage and shared entrance scenery block the first interaction.
# Gate residents and notebook atlases load when used, not before the title. All other
# images use Ren'Py's existing progressive downloader, at original quality.
START_FILES = {"assets/room13-opening-coach-landscape.webp","assets/room13-title-winter020.webp", "assets/room13-pixel-carriage-empty-winter.webp",
               "assets/bgm-title.mp3", "assets/bgm-travel.mp3",
               "assets/type.wav", "assets/ms14-audio/cart-roll-light.mp3",
               "assets/room13-fx-shade-carriage.webp", "assets/room13-fx-glow-carriage-0.webp", "assets/room13-fx-carriage-window-mask.webp"}

def startup_media(rel, startup_files):
    name = Path(rel).name
    # Intake poses are optional scene art. Only bravado occurs in the opening;
    # do not let the broad Daram compatibility whitelist preload every pose.
    if rel.startswith("assets/dialogue-context-master/daram/") and "/intake21_" in rel:
        return Path(rel).stem=="intake21_01_bravado"
    return (rel in startup_files or name in ICONS or Path(rel).suffix.lower() in (".ttf", ".otf", ".woff2"))

def startup_files(game):
    result = set(START_FILES)
    # Approved title/settings must be ready before the first interaction.
    for folder in ("ui-b-main", "ui-b-options", "ui-b-dialogue", "ui-b-question", "ui-b-choice", "ui-b-field", "ui-b-sticker", "ui-button-states", "ui-button-fit", "map-status"):
        result.update(p.relative_to(game).as_posix() for p in (game / "assets" / folder).glob("*.png"))
    result.update(p.relative_to(game).as_posix() for p in (game / "assets/diary-sounds").glob("*.*") if p.suffix in (".mp3", ".ogg"))
    # 도구함에서 다른 폴더의 에셋을 고르더라도 첫 UI에 필요한 실제 파일을 미리 받는다.
    toolbox = game / "asset-toolbox"
    if (toolbox / "bindings.json").exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("r13_build_assets", game / "python-packages/r13_assets.py")
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        registry = module.Registry(json.loads((toolbox / "catalog.json").read_text()), json.loads((toolbox / "bindings.json").read_text()))
        for role, rule in registry.bindings["bindings"].items():
            if role.startswith(("button.", "surface.", "font.", "main.", "file:assets/ui-b-", "file:assets/map-status/", "file:assets/diary-sounds/")):
                for state in rule.get("states", ["basic"]):
                    result.add(registry.resolve(role, state)["path"])
    # Small face stickers must be present when the first dialogue is drawn.
    result.update(p.relative_to(game).as_posix() for p in (game / "assets/dialogue-b-faces").glob("*.webp"))
    layout = json.loads((game / "assets/room13-world-layout.json").read_text())
    def files(value):
        if isinstance(value, str) and value.startswith("assets/"):result.add(value)
        elif isinstance(value, dict):
            for v in value.values():files(v)
        elif isinstance(value, list):
            for v in value:files(v)
    # Only the first gate period is needed near the opening; later daylight
    # and every obsolete Daram atlas remain compatible progressive assets.
    files(layout.get("gate", {}).get("files", {}).get("morning"))
    talking=json.loads((game / "assets/room13-dialogue-talk-art.json").read_text())
    files(talking["people"]["daram"])
    fx = json.loads((game / "assets/room13-dot-fx.json").read_text())
    files(fx.get("lights", {}).get("title", {}))
    files(fx.get("lights", {}).get("gate", {}))
    if (toolbox / "bindings.json").exists():
        for original in tuple(result):
            role="file:"+original
            if role in registry.bindings["bindings"]:
                result.add(registry.resolve(role)["path"])
    return result



def asset_files(value, profile=None):
    """Paths from character manifests; optionally select the runtime size only."""
    if isinstance(value, str):
        if value.startswith("assets/") and Path(value).suffix in (".png", ".webp", ".jpg"):
            yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            if key == "profiles" and profile is not None:
                yield from asset_files(child.get(str(profile), {}), profile)
            else:
                yield from asset_files(child, profile)
    elif isinstance(value, list):
        for child in value:
            yield from asset_files(child, profile)


def character_manifests(game):
    names = ("cast", "resident-art", "room13-avatars", "room13-portraits",
             "room13-fullbody-dialogue", "room13-dialogue-talk-art", "room13-dialogue-talk-art-extra",
             "room13-dialogue-context-art", "room13-dialogue-pose-source-art",
             "room13-meeting-seated", "room13-meeting-source-art", "room13-profile-source-art",
             "room13-pixel-acting", "room13-pixel-motion")
    manifests = [json.loads((game / "assets" / (name + ".json")).read_text())
                 for name in names if (game / "assets" / (name + ".json")).exists()]
    body = game / "assets/room13-dialogue-b-primary50.json"
    if body.exists():
        manifests.append({"people": {person: {"profiles": profiles}
            for person, profiles in json.loads(body.read_text()).items()}})
    faces = game / "assets/room13-dialogue-b-faces.json"
    if faces.exists():
        manifests.append(json.loads(faces.read_text()))
    return manifests


def character_files(game):
    result = {f for manifest in character_manifests(game) for f in asset_files(manifest)}
    patterns = ("dialogue-source-master/*", "dialogue-source-master-v2/*", "dialogue-dot-v2/*", "dialogue-context-master/*", "dialogue-pose-source/*",
                "profile-source-master/*", "room13-fullbody-*", "room13-redesign-*",
                "room13-role-*", "room13-canonical-*", "room13-meeting-*",
                "room13-pixel-acting-*", "room13-pixel-dialogue-*")
    for path in (game / "assets").rglob("*"):
        if path.is_file() and any(fnmatch.fnmatch(path.relative_to(game / "assets").as_posix(), pat) for pat in patterns):
            result.add(path.relative_to(game).as_posix())
    return result


def character_prefetch(game):
    # r13_speaker / r13_question_list call r13_close_art(..., 840).
    # Never warm the alternate 560/760 profiles or the old fullbody atlases.
    people = ["daram", "dad", "karo"]
    speakers = ast.literal_eval(re.search(r"MS14_SPEAKERS\s*=\s*({.*?})", (game / "room13_v111_source_cast.rpy").read_text(), re.S).group(1))
    records = json.loads((game / "v111/records.json").read_text())["records"]
    for key, record in records.items():
        if key.startswith("MS14_D01_"):
            actor = speakers.get(record.get("direction", {}).get("actor"))
            if actor and actor not in people:
                people.append(actor)
    # Nabi is available in the first-day free exploration, outside the directed records.
    if "nabi" not in people:
        people.append("nabi")
    manifests = character_manifests(game)
    result = []
    for person in people:
        for manifest in manifests:
            # Source art, profile and field art only; old fullbody assets stay on demand.
            if "people" in manifest:
                entry = manifest["people"].get(person, {})
                if "images" in entry: continue
            elif "entries" in manifest:
                entry = {k: v for k, v in manifest["entries"].items() if v.get("person") == person}
            else:
                entry = manifest.get(person, {})
            result.extend(asset_files(entry, 840))
    return list(dict.fromkeys(result))

def superseded_art():
    """Files only the backed-up original entries used (empty if no redesign)."""
    backups = [p for p in REDESIGN_BACKUPS if p.exists()]
    if not backups:
        return set()
    files = set()

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                files.add(v) if k == "file" else walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    for backup in backups:
        walk(json.loads(backup.read_text(encoding="utf-8")))
    live = "".join(p.read_text(encoding="utf-8") for p in (ROOT / "game/assets").glob("*.json")
                   if p.name not in ("provenance.json", "room13-pixel-coverage.json"))
    live += "".join(p.read_text(encoding="utf-8") for p in (ROOT / "game").rglob("*.rpy"))
    return {f for f in files if f.split("/")[-1] not in live}
# Small UI icons that must never show a placeholder.
ICONS = {"evidence.png", "save.png", "menu.png", "back.png", "present.png", "investigate.png",
         "record.png", "move.png", "talk.png", "press.png", "sound-on.png", "sound-off.png",
         "lock.png", "notebook.png"}
MAIN_MENU_MUSIC = re.compile(r'config\.main_menu_music\s*=\s*"([^"]+)"')
PART = 60 * 1024 * 1024

LOADER_BEGIN = "    // r13-loader-begin (dev/build_web.py)\n"
LOADER_END = "    // r13-loader-end\n"
LOADER = LOADER_BEGIN + r"""    // Core zip (runtime + scripts) is unpacked by Ren'Py; preloaded art is
    // written straight into /game so nothing large is unpacked or duplicated.
    let r13Prefetch = [];
    let r13AssetVersions = {};
    // Preserve engine paths while giving changed progressive assets fresh HTTP cache keys.
    if (typeof XMLHttpRequest !== "undefined" && !XMLHttpRequest.prototype.r13Versioned) {
        const open = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function(method, url, ...args) {
            const target = new URL(url, document.baseURI);
            const base = new URL(".", document.baseURI);
            const key = target.origin === base.origin && target.pathname.startsWith(base.pathname)
                ? target.pathname.slice(base.pathname.length) : "";
            if (r13AssetVersions[key]) target.searchParams.set("v", r13AssetVersions[key]);
            return open.call(this, method, target.href, ...args);
        };
        XMLHttpRequest.prototype.r13Versioned = true;
    }

    function r13Url(file, sha) {
        const url = new URL(file, document.baseURI);
        if (sha) url.searchParams.set("v", sha.slice(0, 12));
        return url;
    }

    async function r13FetchOnce(url, tick, expectedBytes, retry) {
        const response = await fetch(url, retry ? { cache: "reload" } : {});
        if (!response.ok) throw new Error(url + ": HTTP " + response.status);
        const reader = response.body.getReader();
        const chunks = [];
        let size = 0;
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
            size += value.length;
            tick(value.length);
        }
        const out = new Uint8Array(size);
        let at = 0;
        for (const chunk of chunks) { out.set(chunk, at); at += chunk.length; }
        if (expectedBytes != null && size !== expectedBytes) throw new Error(url + ": incomplete download " + size + "/" + expectedBytes);
        return out;
    }

    async function r13Fetch(url, tick, expectedBytes) {
        for (let attempt = 0; attempt < 3; attempt++) {
            let received = 0;
            try {
                return await r13FetchOnce(url, n => { received += n; tick(n); }, expectedBytes, attempt > 0);
            } catch (error) {
                tick(-received);
                if (attempt === 2) throw error;
                await new Promise(resolve => setTimeout(resolve, 300 * (attempt + 1)));
            }
        }
    }

    function r13MakeDirs(path) {
        let dir = "";
        for (const name of path.split("/").slice(1, -1)) {
            dir += "/" + name;
            try { FS.mkdir(dir); } catch (e) { /* exists */ }
        }
    }

    async function loadGameZip() {
        try {
            const response = await fetch(r13Url("game-transport.json"), { cache: "no-cache" });
            if (!response.ok) throw new Error("game-transport.json: HTTP " + response.status);
            const transport = await response.json();
            r13AssetVersions = transport.asset_versions || {};
            for (const file of Object.keys(r13AssetVersions)) r13MakeDirs("/" + file);
            const preload = transport.preload || [];
            gameZipSize = transport.archive_bytes + preload.reduce((n, f) => n + f.bytes, 0);
            const tick = (n) => { gameZipDownloaded += n; updateDownloadProgress(); };

            const core = (async () => {
                const parts = [];
                for (const part of transport.parts) parts.push(await r13Fetch(r13Url(part.file, part.sha256), tick, part.bytes));
                const f = FS.open("/game.zip", "w");
                for (const data of parts) FS.write(f, data, 0, data.length);
                FS.close(f);
            })();

            let next = 0;
            async function worker() {
                while (next < preload.length) {
                    const item = preload[next++];
                    const data = await r13Fetch(r13Url(item.file, item.sha256), tick, item.bytes);
                    const path = "/" + item.file;
                    r13MakeDirs(path);
                    FS.writeFile(path, data, { canOwn: true });
                }
            }
            const workers = [];
            for (let i = 0; i < 6; i++) workers.push(worker());
            await Promise.all([core].concat(workers));
            r13Prefetch = transport.prefetch || [];
        } catch (e) {
            reportError("게임 파일을 내려받지 못했습니다. 연결을 확인하고 다시 시도해 주세요.", e);
            throw e;
        }
    }

    // Warm first-day character art and nearby music once the game runs,
    // so Ren'Py's own download finds them immediately.
    async function r13PrefetchLater() {
        let next = 0;
        async function worker() {
            while (next < r13Prefetch.length) {
                const file = r13Prefetch[next++];
                try { await (await fetch(r13Url(file, r13AssetVersions[file]), { priority: "low" })).blob(); } catch (e) { /* retried by Ren'Py */ }
                await new Promise(resolve => setTimeout(resolve, 50));
            }
        }
        await Promise.all([worker(), worker()]);
    }

    // On failure the stock status line grows upward over the loading hint and
    // auto-scrolls to the English console notice (external QA 0.20.66). Hide both
    // and gather a Korean explanation plus the retry button in one panel; keep the
    // engine log, folded under "technical info", for support requests.
    const R13_LOAD_ERROR_CSS = [
        ".r13-load-failed #loading-brand,.r13-load-failed #statusDiv{display:none!important}",
        "#r13-load-error{position:fixed;z-index:2147483647;left:50%;top:50%;transform:translate(-50%,-50%);box-sizing:border-box;width:min(560px,calc(100vw - 32px));max-height:calc(100vh - 24px);overflow:auto;padding:clamp(12px,3vh,20px) clamp(14px,3vw,24px);background:#101b37f0;border:1px solid #777b9b;border-radius:8px;color:#edf0ff;font-family:Galmuri,sans-serif;text-shadow:none}",
        "#r13-load-error h2{margin:0 0 6px;font-size:clamp(16px,2.6vh,22px);color:#ffdc91}",
        "#r13-load-error .r13-load-error-message{margin:0 0 12px;font-size:clamp(13px,2.2vh,17px);line-height:1.5}",
        "#r13-load-error button{display:block;box-sizing:border-box;width:100%;min-height:48px;padding:10px 12px;border:0;border-radius:6px;background:#fff4df;color:#172a2a;font-family:inherit;font-size:clamp(15px,2.6vh,20px);cursor:pointer}",
        "#r13-load-error details{margin-top:8px;color:#d5d8ea}",
        "#r13-load-error summary{display:flex;align-items:center;min-height:44px;font-size:13px;cursor:pointer;list-style:none}",
        "#r13-load-error summary::-webkit-details-marker{display:none}",
        "#r13-load-error summary::before{content:\"\\25B8\";margin-right:6px}",
        "#r13-load-error details[open] summary::before{content:\"\\25BE\"}",
        "#r13-load-error #statusTextDiv{max-height:none;overflow:visible;font-size:12px;line-height:1.5;color:#d5d8ea;overflow-wrap:anywhere}"
    ].join("\n");

    function r13ShowLoadFailure(error) {
        const old = document.getElementById("r13-load-error");
        if (old) return old;
        const style = document.createElement("style");
        style.id = "r13-load-error-style";
        style.textContent = R13_LOAD_ERROR_CSS;
        (document.head || document.body).appendChild(style);
        document.documentElement.classList.add("r13-load-failed");

        const panel = document.createElement("div");
        panel.id = "r13-load-error";
        panel.setAttribute("role", "alert");
        const title = document.createElement("h2");
        title.textContent = "게임 파일을 받지 못했습니다";
        const message = document.createElement("p");
        message.className = "r13-load-error-message";
        message.textContent = "인터넷 연결을 확인한 뒤 다시 시도해 주세요. 저장 기록은 그대로 남아 있습니다.";
        const retry = document.createElement("button");
        retry.type = "button";
        retry.textContent = "게임 다시 불러오기 (저장 기록은 유지됩니다)";
        retry.onclick = () => location.reload();
        const details = document.createElement("details");
        const summary = document.createElement("summary");
        summary.textContent = "기술 정보 보기";
        details.appendChild(summary);
        // Move the live status line so later engine messages land in the same place.
        const log = document.getElementById("statusTextDiv");
        if (log) {
            details.appendChild(log);
        } else {
            const pre = document.createElement("pre");
            pre.textContent = String(error && error.message || error || "");
            details.appendChild(pre);
        }
        for (const child of [title, message, retry, details]) panel.appendChild(child);
        document.body.appendChild(panel);
        try { retry.focus({ preventScroll: true }); } catch (e) { /* focus is optional */ }
        return panel;
    }

    function runLoadGameZip() {
        Module.addRunDependency('loadGameZip');

        loadGameZip().then(() => {
            Module.removeRunDependency('loadGameZip');
            setTimeout(r13PrefetchLater, 1000);
        }).catch((error) => {
            // Do not start a partially populated filesystem and silently show legacy art.
            r13ShowLoadFailure(error);
        });

    }

    Module['preRun'].push(runLoadGameZip);
""" + LOADER_END


def prefetch_order(rel):
    """Background warm-up order once the game runs; 9 = never warmed (legacy/close-up art)."""
    if rel.endswith(".mp3"):
        return 0
    if any(fnmatch.fnmatch(rel, p) for p in REMOTE_LATER):
        return 1
    return 9


def sha(data):
    return hashlib.sha256(data).hexdigest()


def excluded(rel):
    return any(fnmatch.fnmatch(rel, pattern) for pattern in EXCLUDE)


def install_loader(path):
    s = path.read_text()
    if LOADER_BEGIN in s:
        a = s.index(LOADER_BEGIN); b = s.index(LOADER_END) + len(LOADER_END)
    else:
        # First run: replace the stock/multipart loader up to its preRun hook.
        a = s.index("    async function r13FetchGameZip()")
        hook = "    Module['preRun'].push(runLoadGameZip);\n"
        b = s.index(hook, a) + len(hook)
    s = s[:a] + LOADER + s[b:]
    # Import can leave newest_slot(None) cached when the menu had no saves.
    # Rescan disk, invalidate all slot metadata, and let clear_cache redraw UI.
    old_import = "renpy_exec('renpy.loadsave.location.scan()')"
    new_import = "renpy_exec('renpy.loadsave.location.scan(); renpy.loadsave.clear_cache()')"
    s = s.replace(old_import, new_import)
    if new_import not in s:
        raise RuntimeError("Save import refresh hook not found in web runtime")
    path.write_text(s)


def seed_previous_rpyc(release, game):
    parts = sorted(release.glob("game.part[0-9][0-9]"))
    if not parts:
        return 0
    data = b"".join(p.read_bytes() for p in parts)
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        return 0
    n = 0
    for name in z.namelist():
        if not (name.startswith("game/") and name.endswith(".rpyc")):
            continue
        source = game / (name[len("game/"):-1])
        if source.exists():  # orphan .rpyc would load a removed script
            (game / name[len("game/"):]).write_bytes(z.read(name)); n += 1
    return n


def has_transparency(path):
    from PIL import Image
    im = Image.open(path)
    if im.mode not in ("RGBA", "LA", "P") and "transparency" not in im.info:
        return False
    return im.convert("RGBA").getchannel("A").getextrema()[0] < 255


def placeholder(data, transparent=False):
    from PIL import Image
    im = Image.open(io.BytesIO(data))
    w, h = im.size
    if transparent:
        im = Image.new("P", (w, h), 0)
        im.putpalette([0, 0, 0, 0, 0, 0])
        im.info["transparency"] = 0
    elif w > 32 and h > 32:
        im = im.convert("RGBA").resize((max(1, w // 32), max(1, h // 32)), Image.BOX)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True, **({"bits": 1} if transparent else {}))
    return (w, h), buf.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sdk", type=Path, required=True)
    ap.add_argument("--release", type=Path, default=ROOT.parents[1] / "preview/room13-dev")
    ap.add_argument("--work", type=Path, default=Path("/tmp/room13-build"))
    ap.add_argument("--skip-lint", action="store_true")
    ap.add_argument("--part-mb", type=int, choices=range(1,61), default=PART//(1024*1024), help="Core archive transport chunk size; archive bytes stay identical.")
    a = ap.parse_args()
    release, work = a.release.resolve(), a.work.resolve()
    stage = work / "stage"
    shutil.rmtree(stage, ignore_errors=True); stage.mkdir(parents=True)

    # 1. stage = web runtime + game/
    with zipfile.ZipFile(ROOT / "web/runtime.zip") as z:
        z.extractall(stage)
    game_src = ROOT / "game"
    for path in sorted(game_src.rglob("*")):
        rel = path.relative_to(game_src).as_posix()
        if path.is_file() and not excluded(rel) and "__pycache__" not in rel:
            dest = stage / "game" / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
    game = stage / "game"

    # 1b. 0.19.8: seed the previous release's .rpyc so Ren'Py keeps the generated return-site names of
    # unchanged call statements. A fresh compile renamed every one, and saves made inside a call failed
    # to load after each release ("Could not find return label").
    seeded = seed_previous_rpyc(release, game)
    print("seeded %d .rpyc from the previous release" % seeded)
    if not seeded and list(release.glob("game.part[0-9][0-9]")):
        raise SystemExit("previous release parts exist but no .rpyc could be seeded; saves would break")

    # 2. every referenced pixel asset exists
    texts = [p for p in game.rglob("*") if p.suffix in (".rpy", ".json")]
    missing = sorted({m for p in texts for m in re.findall(r"assets/room13-pixel-[\w\-]+\.(?:png|webp)", p.read_text(errors="ignore"))
                      if not (game / m).exists()})
    assert not missing, "unresolved art references: %s" % missing[:10]

    # 3. compile + lint with the matching SDK
    renpy = a.sdk / "renpy.sh"
    subprocess.run([str(renpy), str(stage), "compile"], check=True)
    if not a.skip_lint:
        lint = subprocess.run([str(renpy), str(stage), "lint"], capture_output=True, text=True)
        (work / "lint.txt").write_text(lint.stdout)
        if any(re.search(r"\.rpy:\d+ ", l) for l in lint.stdout.splitlines() if "is not loadable" not in l):
            raise SystemExit("lint reported problems; see " + str(work / "lint.txt"))
    shutil.rmtree(game / "cache", ignore_errors=True)
    shutil.rmtree(game / "saves", ignore_errors=True)  # compile may create persistent; never publish it
    for junk in ("log.txt", "errors.txt", "traceback.txt", "lint.txt"):
        (stage / junk).unlink(missing_ok=True)

    # 4. classify media
    menu_music = MAIN_MENU_MUSIC.search((game / "options.rpy").read_text())
    menu_music = menu_music.group(1) if menu_music else None
    preload, remote, remote_lines = [], [], []
    startup = startup_files(game)
    characters = character_files(game)
    for path in sorted((game / "assets").rglob("*")):
        rel = path.relative_to(game).as_posix()
        suffix = path.suffix.lower()
        if not path.is_file() or suffix not in MEDIA:
            continue
        # One-shot interface sounds cannot rely on a remote silent placeholder.
        # Keep the small shared root WAV set compressed in the core archive.
        if suffix == ".wav" and path.parent == game / "assets":
            continue
        if startup_media(rel, startup):
            if path.stat().st_size >= SMALL:preload.append(rel)
        elif suffix in (".mp3", ".ogg", ".opus", ".wav"):
            remote.append(rel); remote_lines += [rel, "music -"]
        elif suffix in (".webp", ".png", ".jpg"):
            # 0.20.4 (owner: "캐릭터가 자꾸 모자이크 처리됨이 뜨네 ... 이런게 뜨면 안됨"): any picture
            # with transparent pixels (characters, action poses, props) waits invisibly instead of a mosaic.
            (w, h), thumb = placeholder(path.read_bytes(), rel in characters or has_transparency(path))
            ph = stage / "_placeholders" / rel
            ph.parent.mkdir(parents=True, exist_ok=True); ph.write_bytes(thumb)
            remote.append(rel); remote_lines += [rel, "image %d,%d" % (w, h)]
        elif path.stat().st_size >= SMALL:
            preload.append(rel)
    (game / "renpyweb_remote_files.txt").write_text("".join(l + "\n" for l in remote_lines))

    # 5. core zip
    archive = work / "game.zip"
    separate = {"game/" + r for r in preload + remote}
    with zipfile.ZipFile(archive, "w") as z:
        for path in sorted(stage.rglob("*")):
            rel = path.relative_to(stage).as_posix()
            if not path.is_file():
                continue
            if rel in separate:
                continue
            info = zipfile.ZipInfo(rel, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED if rel.endswith(STORED) else zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, path.read_bytes())
    data = archive.read_bytes()
    digest, size = sha(data), len(data)

    # 6. release files
    for stale in release.glob("game.part[0-9][0-9]"):
        stale.unlink()
    parts = []
    part_size = a.part_mb*1024*1024
    for index, at in enumerate(range(0, size, part_size), 1):
        chunk = data[at:at + part_size]; name = "game.part%02d" % index
        (release / name).write_bytes(chunk)
        parts.append({"file": name, "bytes": len(chunk), "sha256": sha(chunk)})
    shipped = set()
    preload_entries = []
    # Retain stable URLs for older open tabs while new clients read these from core.
    shared_sfx = [p.relative_to(game).as_posix() for p in (game / "assets").glob("*.wav")]
    for rel in dict.fromkeys(preload + remote + shared_sfx):
        src = game / rel; dest = release / "game" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        blob = src.read_bytes()
        if not dest.exists() or dest.read_bytes() != blob:
            dest.write_bytes(blob)
        shipped.add(dest)
        if rel in preload:
            preload_entries.append({"file": "game/" + rel, "bytes": len(blob), "sha256": sha(blob)})
    removed = []
    for old in sorted((release / "game").rglob("*")):
        if old.is_file() and old not in shipped:
            removed.append(old.relative_to(release).as_posix()); old.unlink()
    preload_entries.sort(key=lambda item: item["file"] != "game/" + menu_music)
    warm = character_prefetch(game) + ["assets/bgm-snow.mp3", "assets/amb-wind.mp3", "assets/bgm-inn.mp3", "assets/amb-fire.mp3"]
    transport = {"multipart": True, "archive_bytes": size, "archive_sha256": digest, "parts": parts,
                 "preload": preload_entries, "asset_versions": {"game/"+r: sha((game/r).read_bytes())[:12] for r in remote},
                 "prefetch": ["game/"+r for r in dict.fromkeys(warm) if r in remote]}
    (release / "game-transport.json").write_text(json.dumps(transport, indent=1))

    install_loader(release / "renpy-pre.js")
    index = release / "index.html"; s = index.read_text()
    loader_digest = sha((release / "renpy-pre.js").read_bytes())
    s, n = re.subn(r"renpy-pre\.js\?v=[0-9a-f]+", "renpy-pre.js?v=" + loader_digest[:12], s)
    assert n == 1; index.write_text(s)

    sys.path.insert(0, str(ROOT / "dev"))
    from update_title_loader import update_title_loader
    update_title_loader(release, game)

    # Service worker / PWA catalog and the integrity manifest cover every file.
    files = sorted(p.relative_to(release).as_posix() for p in release.rglob("*") if p.is_file()
                   and p.name not in ("build-manifest.json", "pwa_catalog.json"))
    (release / "pwa_catalog.json").write_text(json.dumps({"files": files, "version": int(time.time())}))
    manifest_path = release / "build-manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    manifest["files"] = {f: {"bytes": (release / f).stat().st_size, "sha256": sha((release / f).read_bytes())} for f in files}
    manifest["game_transport"] = {k: v for k, v in transport.items() if k in ("archive_bytes", "archive_sha256", "parts")}
    manifest["total_bytes"] = sum(v["bytes"] for v in manifest["files"].values())
    manifest_path.write_text(json.dumps(manifest, indent=1))

    first_load = size + sum(e["bytes"] for e in preload_entries)
    summary = dict(core_zip_bytes=size, archive_sha256=digest, parts=len(parts), preload_files=len(preload_entries),
                   first_load_bytes=first_load, prefetch_files=len(transport["prefetch"]), transparent_placeholders=len(characters.intersection(remote)), remote_files=len(remote), removed_from_release=removed)
    (work / "build-report.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
