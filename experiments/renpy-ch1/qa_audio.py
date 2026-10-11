"""Verify actual WebAudio controls and review the six-location map with real UI input."""
import argparse
import asyncio
import json
import shutil
from pathlib import Path

from playwright.async_api import async_playwright
from qa_web import AUDIO_PROBE, Trial


async def main(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=shutil.which("chromium"),
            args=["--no-sandbox", "--enable-unsafe-swiftshader"],
        )
        context = await browser.new_context(viewport={"width": 1280, "height": 720})
        await context.add_init_script(AUDIO_PROBE)
        page = await context.new_page()
        trial = Trial(page, 1280, 720, output)
        await page.goto(args.url)
        await page.wait_for_function("typeof renpy_exec==='function'", timeout=60000)
        await trial.state()
        await trial.click(320, 425)
        # Open settings while the first line is still typing.
        for _ in range(40):
            if (await trial.state())["typing"]:
                break
            await page.wait_for_timeout(50)
        assert (await trial.state())["typing"]
        await trial.click(1174, 45)
        await trial.wait("menu")
        assert (await trial.state())["typing"] is None
        baseline = (await trial.state())["music_volume"]
        await trial.click(850, 350)
        assert (await trial.state())["music_volume"] > baseline
        await trial.shot("volume")
        await trial.click(630, 400)
        await page.wait_for_timeout(700)
        assert (await trial.state())["music_mute"]
        signals = await page.evaluate("__probeAudio()")
        assert signals and all(s["rms"] == 0 for s in signals)
        await trial.click(630, 400)
        await page.wait_for_timeout(900)
        assert not (await trial.state())["music_mute"]
        assert any(s["rms"] > 1e-5 for s in await page.evaluate("__probeAudio()"))
        await trial.click(450, 190)
        await trial.wait("menu", False)
        await trial.advance_until("explore")
        await trial.talk()
        await trial.click(1090, 637)
        await trial.advance_until("explore")
        assert (await trial.state())["stage"] == "investigation"
        await trial.click(882, 640)
        await trial.wait("map")
        await trial.shot("map")
        await trial.click(1072, 455)
        await trial.wait("explore")
        assert (await trial.state())["location"] == "room"
        await trial.click(1038, 45)
        await trial.wait("evidence")
        await trial.shot("notebook")
        assert not trial.errors and not trial.failed and not trial.bad
        result = dict(volume_slider=True, mute_silences_output=True,
                      unmute_restores_output=True, active_typing_stops_in_menu=True,
                      six_location_map_room_selection=True, errors=trial.errors,
                      failed_requests=trial.failed, bad_responses=trial.bad)
        (output / "report.json").write_text(json.dumps(result, indent=2))
        print(json.dumps(result), flush=True)
        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8093/preview/renpy-ch1-test/")
    parser.add_argument("--output", default="/tmp/daram-audio-qa")
    asyncio.run(main(parser.parse_args()))
