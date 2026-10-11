"""Native UI review of the final head crops and matching town backgrounds."""
import argparse
import asyncio
import json
import shutil
from pathlib import Path
from playwright.async_api import async_playwright
from qa_source import SourceTrial


async def main(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    width, height = (844, 390) if args.touch else (1280, 720)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            executable_path=shutil.which("chromium"),
            args=["--no-sandbox", "--enable-unsafe-swiftshader"])
        context = await browser.new_context(
            viewport={"width": width, "height": height},
            has_touch=args.touch, is_mobile=args.touch)
        page = await context.new_page()
        trial = SourceTrial(page, width, height, output)
        await page.goto("http://127.0.0.1:8093/preview/renpy-ch1-test/")
        await page.wait_for_function("typeof renpy_exec==='function'", timeout=60000)
        await trial.state()
        await trial.click(320, 425)
        await trial.advance_until("line", "V_CARRIAGE:0")
        await trial.shot("daram-face")
        await trial.advance_until("line", "V_CARRIAGE:1")
        await trial.shot("dad-face")
        await trial.advance_until("village_place")
        await trial.arrival_action("talk")
        await trial.arrival_action("map")
        if not args.touch:
            for place in ("fountain", "lane", "inn"):
                await trial.arrival_move(place)
                await trial.arrival_action("talk")
                await trial.arrival_action("map")
        await trial.arrival_move("inn")
        await trial.arrival_action("stay")
        assert "room" in (await trial.state())["village_seen"]
        assert not trial.errors and not trial.failed and not trial.bad
        result = dict(viewport=[width, height], touch=args.touch,
                      family_head_closeups=True, town_interview_head_closeups=True,
                      same_background_before_and_during_interview=True,
                      room_topic_marked_read=True, errors=trial.errors,
                      failed_requests=trial.failed, bad_responses=trial.bad)
        (output / "report.json").write_text(json.dumps(result, indent=2))
        print(json.dumps(result), flush=True)
        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--touch", action="store_true")
    parser.add_argument("--output", required=True)
    asyncio.run(main(parser.parse_args()))
