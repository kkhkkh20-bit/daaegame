"""Keep native logs and a bounded, explicitly inventoried screenshot sample."""
import hashlib
import json
import os
from pathlib import Path


def main():
    out = Path(os.environ["ROOM13_CI_OUT"])
    native = out / "native-qa"
    preferred = (
        "piko-nameplate-offer.png",
        "piko-actual-event-dialogue.png",
        "sofa-tosil-01-camera-zero.png",
        "sofa-nubi-01-camera-zero.png",
        "sofa-tosil-04-actual-topic-say.png",
        "sofa-nubi-04-actual-topic-say.png",
    )
    screenshots = sorted(native.rglob("*.png"))
    screenshots.sort(key=lambda p: (
        preferred.index(p.name) if p.name in preferred else len(preferred),
        p.relative_to(native).as_posix(),
    ))
    remaining = 8 * 1024 * 1024
    rows = []
    for path in screenshots:
        data = path.read_bytes()
        keep = len(data) <= remaining
        rows.append(dict(file=path.relative_to(out).as_posix(), bytes=len(data),
                         sha256=hashlib.sha256(data).hexdigest(), retained=keep))
        if keep:
            remaining -= len(data)
        else:
            path.unlink()
    report = dict(screenshot_budget_bytes=8 * 1024 * 1024,
                  retained_bytes=8 * 1024 * 1024 - remaining,
                  all_native_logs_retained=True, screenshots=rows)
    (out / "diagnostic-screenshot-inventory.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "screenshots"}))


if __name__ == "__main__":
    main()
