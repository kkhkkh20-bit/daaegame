"""Verify real typing output with BGM muted, audio controls, and revised evidence."""
import argparse
import asyncio
import json
import shutil
from pathlib import Path

from playwright.async_api import async_playwright
from qa_web import AUDIO_PROBE
from qa_source import SourceTrial
from qa_ui import check_volume_sliders


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
        trial = SourceTrial(page, 1280, 720, output)
        await page.goto(args.url)
        await page.wait_for_function("typeof renpy_exec==='function'", timeout=60000)
        await trial.state()
        await trial.click(320, 425)
        # Skip the silent-typing cold hook; probe a normal carriage line.
        await trial.advance_until("scene","V_CARRIAGE")
        # Advance through short replies to a longer normally typed line.
        for _ in range(12):
            if (await trial.state())["typing"]:break
            await trial.click(830,665)
        # Open settings while a line is still typing.
        for _ in range(90):
            if (await trial.state())["typing"]:
                break
            await page.wait_for_timeout(50)
        assert (await trial.state())["typing"]
        await trial.click(1174, 45)
        await trial.wait("menu")
        await check_volume_sliders(trial)
        assert (await trial.state())["typing"] is None
        baseline = (await trial.state())["music_volume"]
        await trial.click(850, 350)
        assert (await trial.state())["music_volume"] > baseline
        await trial.shot("volume")
        await trial.click(630, 400)
        await page.wait_for_timeout(700)
        assert (await trial.state())["music_mute"]
        signals = await page.evaluate("__probeAudio()")
        await trial.shot("muted")
        assert (await trial.state())["fx"] is None, "One-shot effect did not finish"
        assert signals and all(s["rms"] < 1e-7 for s in signals)
        # Keep music muted while returning to dialogue; isolate the typing channel.
        await trial.click(450,190)
        await trial.wait("menu",False)
        typing_signal = False
        for _ in range(12):
            await trial.click(830,665)
            for sample in range(4):
                state = await trial.state()
                if state["typing"] and not state["fx"]:
                    assert state["music_mute"]
                    typing_signal |= any(s["rms"]>1e-5 for s in await page.evaluate("__probeAudio()"))
                await page.wait_for_timeout(60)
            if typing_signal:break
        assert typing_signal, "Typing channel has no audible output with BGM muted"
        await trial.click(1174,45)
        await trial.wait("menu")
        await page.wait_for_timeout(400)
        assert (await trial.state())["typing"] is None
        assert all(s["rms"]<1e-7 for s in await page.evaluate("__probeAudio()"))
        await trial.click(630, 400)
        await page.wait_for_timeout(900)
        assert not (await trial.state())["music_mute"]
        assert any(s["rms"] > 1e-5 for s in await page.evaluate("__probeAudio()"))
        await trial.click(450, 190)
        await trial.wait("menu", False)
        await trial.arrival_route(rich=False)
        assert (await trial.state())["stage"] == "investigation"
        await trial.click(842, 635)
        await trial.wait("map")
        await trial.shot("map")
        await trial.click(1089, 361)
        await trial.wait("roam")
        assert (await trial.state())["location"] == "bed13"
        await trial.interact(900,280)
        await trial.click(1038, 45)
        await trial.wait("evidence")
        await trial.shot("notebook")
        assert not trial.errors and not trial.failed and not trial.bad
        result = dict(volume_slider=True, volume_tracks_and_handles_visible=True, mute_silences_output=True,
                      unmute_restores_output=True, active_typing_stops_in_menu=True,
                      one_shot_effect_finishes=True, typing_outputs_with_bgm_muted=typing_signal,
                      seven_location_map_room_selection=True, errors=trial.errors,
                      failed_requests=trial.failed, bad_responses=trial.bad)
        (output / "report.json").write_text(json.dumps(result, indent=2))
        print(json.dumps(result), flush=True)
        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8093/preview/renpy-ch1-test/")
    parser.add_argument("--output", default="/tmp/daram-audio-qa")
    asyncio.run(main(parser.parse_args()))
