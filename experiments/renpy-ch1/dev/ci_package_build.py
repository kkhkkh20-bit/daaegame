"""CI-only release verification and delta packaging. Never commits or deploys."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path.cwd()
RELEASE = ROOT / "preview/room13-dev"
OUT = Path(os.environ["ROOM13_CI_OUT"])
BASELINE = OUT / "release-baseline.json"

def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()

def inventory():
    return {p.relative_to(RELEASE).as_posix(): {"bytes": p.stat().st_size, "sha256": digest(p)}
            for p in sorted(RELEASE.rglob("*")) if p.is_file()}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if sys.argv[1] == "snapshot":
        BASELINE.write_text(json.dumps(inventory(), indent=2))
        return
    if sys.argv[1] != "package":
        raise SystemExit("Expected snapshot or package")
    before = json.loads(BASELINE.read_text())
    after = inventory()
    manifest = json.loads((RELEASE / "build-manifest.json").read_text())
    transport = json.loads((RELEASE / "game-transport.json").read_text())
    for name, expected in manifest["files"].items():
        assert after[name] == expected, ("manifest mismatch", name)
    expected_names = set(after) - {"build-manifest.json", "pwa_catalog.json"}
    assert set(manifest["files"]) == expected_names, "manifest coverage mismatch"
    assert manifest["total_bytes"] == sum(after[n]["bytes"] for n in expected_names)
    archive = hashlib.sha256()
    total = 0
    for part in transport["parts"]:
        assert after[part["file"]] == {k: part[k] for k in ("bytes", "sha256")}
        with (RELEASE / part["file"]).open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                archive.update(chunk)
                total += len(chunk)
    assert archive.hexdigest() == transport["archive_sha256"]
    assert total == transport["archive_bytes"]
    assert manifest["game_transport"]["archive_sha256"] == archive.hexdigest()
    for item in transport["preload"]:
        assert after[item["file"]] == {k: item[k] for k in ("bytes", "sha256")}
    report_path = Path(os.environ["RUNNER_TEMP"]) / "room13-build/build-report.json"
    assert json.loads(report_path.read_text())["archive_sha256"] == archive.hexdigest()
    changed = sorted(n for n in after if after[n] != before.get(n))
    deleted = sorted(set(before) - set(after))
    for name in changed:
        target = OUT / "release-delta" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(RELEASE / name, target)
    result = {
        "status": "verified_build_not_deployed",
        "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "archive_sha256": archive.hexdigest(),
        "changed": {name: after[name] for name in changed},
        "deleted": deleted,
        "delta_bytes": sum(after[name]["bytes"] for name in changed),
        "release_bytes": sum(spec["bytes"] for spec in after.values()),
        "warning": "Apply only to this exact source commit and baseline; browser QA and deployment remain separate."
    }
    (OUT / "verification.json").write_text(json.dumps(result, indent=2))
    (OUT / "release-final.json").write_text(json.dumps(after, indent=2))
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

