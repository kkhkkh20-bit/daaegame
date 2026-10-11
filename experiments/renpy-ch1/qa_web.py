"""Exercise the real Ren'Py WASM game through pointer input, not state injection."""
import argparse
import asyncio
import json
import shutil
import time
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent

class Trial:
    def __init__(self, page, width, height, output):
        self.page, self.width, self.height, self.output = page, width, height, output
        self.errors, self.failed, self.responses = [], [], []
        page.on("pageerror", lambda e: self.errors.append(str(e)))
        page.on("console", self.console)
        page.on("requestfailed", lambda r: self.failed.append({"url": r.url, "error": r.failure}))
        page.on("response", lambda r: self.responses.append({"url": r.url, "status": r.status}))

    def console(self, message):
        if message.type == "error" and "favicon" not in message.text:
            self.errors.append(message.text)
        if "Traceback" in message.text or "Exception:" in message.text:
            self.errors.append(message.text)

    async def state(self):
        return await self.page.evaluate('renpy_exec("import renpy; result=renpy.store.trial_state()")')

    async def click(self, x, y):
        scale = min(self.width / 1280, self.height / 720)
        px = (self.width - 1280 * scale) / 2 + x * scale
        py = (self.height - 720 * scale) / 2 + y * scale
        if await self.page.evaluate("navigator.maxTouchPoints > 0"):
            await self.page.touchscreen.tap(px, py)
        else:
            await self.page.mouse.click(px, py)
        await self.page.wait_for_timeout(160)

    async def advance_until(self, field, value=True, limit=100):
        for _ in range(limit):
            st = await self.state()
            if st.get(field) == value:
                await self.page.wait_for_timeout(400)
                return st
            await self.click(830, 646)
        await self.screenshot("failure")
        raise AssertionError(f"Did not reach {field}={value}: {await self.state()}")

    async def wait_state(self, field, value=True):
        for _ in range(35):
            st = await self.state()
            if st.get(field) == value:
                # The authored after-load fade is 0.44s; logical screen presence
                # precedes the point where the engine accepts pointer input.
                await self.page.wait_for_timeout(650)
                return st
            await self.page.wait_for_timeout(150)
        raise AssertionError(f"Missing {field}={value}: {await self.state()}")

    async def screenshot(self, name):
        await self.page.screenshot(path=str(self.output / f"{name}.png"))

    async def save(self):
        await self.click(1090, 47)
        await self.wait_state("saving")
        await self.screenshot("save")
        await self.click(770, 240)
        await self.page.wait_for_timeout(500)
        assert (await self.state())["saved_slots"], "Save button did not create a slot"
        await self.click(250, 563)
        await self.wait_state("saving", False)

    async def load(self):
        await self.click(1156, 47)
        await self.wait_state("menu")
        await self.click(530, 391)
        await self.wait_state("loading")
        await self.click(770, 240)
        await self.page.wait_for_timeout(700)
        await self.wait_state("loading", False)

async def run_one(browser, url, width, height, reverse, output):
    ctx = await browser.new_context(viewport={"width": width, "height": height},
                                    has_touch=width < 1000, is_mobile=width < 1000)
    page = await ctx.new_page()
    trial = Trial(page, width, height, output)
    start = time.monotonic()
    await page.goto(url)
    await page.wait_for_function("typeof renpy_exec==='function'", timeout=60000)
    ready = await asyncio.wait_for(trial.state(), timeout=60)
    startup = time.monotonic() - start
    await trial.screenshot("title")
    await trial.click(280, 378)
    # Early clicks on the pillow must only advance dialogue, never acquire evidence.
    for _ in range(3):
        await trial.click(800, 280)
    assert not (await trial.state())["inventory"]
    await trial.advance_until("investigation_open")
    assert (await trial.state())["music"] == "assets/search.mp3"
    await trial.screenshot("investigation")
    # Gate the meeting before the two relevant pieces of evidence are found.
    await trial.click(1110, 640)
    assert (await trial.state())["investigation_open"]

    spots = [("fur", 650, 525), ("pouch", 800, 275), ("flour", 610, 365)] if reverse else [
        ("pouch", 800, 275), ("fur", 650, 525), ("flour", 610, 365)]
    for key, x, y in spots:
        await trial.click(x, y)
        await trial.advance_until("investigation_open", False, limit=6)
        await trial.advance_until("investigation_open")
        assert key in (await trial.state())["inventory"], key
        # Revisiting must not add a duplicate card.
        await trial.click(x, y)
        await trial.advance_until("investigation_open", False, limit=6)
        await trial.advance_until("investigation_open")
        assert (await trial.state())["inventory"].count(key) == 1

    await trial.click(1020, 47)
    await trial.wait_state("evidence_open")
    await trial.screenshot("evidence")
    await trial.click(227, 553)
    await trial.wait_state("evidence_open", False)
    saved = await trial.state()
    await trial.save()
    await trial.click(1110, 640)
    await trial.advance_until("testimony_open")
    assert (await trial.state())["music"] == "assets/meeting.mp3"
    await trial.load()
    restored = await trial.wait_state("investigation_open")
    assert restored["inventory"] == saved["inventory"]
    assert restored["stage"] == "investigation"
    await trial.screenshot("restored")

    # A reload of the browser must retain the real engine save in IndexedDB.
    await page.reload()
    await page.wait_for_function("typeof renpy_exec==='function'", timeout=60000)
    await asyncio.wait_for(trial.state(), timeout=60)
    await trial.click(270, 456)
    await trial.wait_state("loading")
    await trial.click(770, 240)
    await trial.wait_state("investigation_open")
    assert (await trial.state())["inventory"] == saved["inventory"]

    await trial.click(1110, 640)
    await trial.advance_until("testimony_open")
    await trial.screenshot("meeting")
    state = await trial.state()
    order = state["inventory"]
    def card(key):
        return (40 + order.index(key) * 403 + 190, 595)
    # Wrong card elicits a response without advancing the proof.
    await trial.click(*card("flour"))
    await trial.advance_until("testimony_open")
    assert (await trial.state())["wrong"] == 1
    assert (await trial.state())["first"] is None
    await trial.click(135, 325)
    await trial.advance_until("testimony_open")
    first, second = ("fur", "pouch") if reverse else ("pouch", "fur")
    await trial.click(*card(first))
    await trial.advance_until("testimony_open")
    assert (await trial.state())["first"] == first
    await trial.save()
    await trial.click(*card(second))
    await trial.advance_until("choice_open")
    await trial.load()
    await trial.wait_state("testimony_open")
    state = await trial.state()
    assert state["first"] == first and not state["proved"]
    await trial.click(*card(second))
    await trial.advance_until("choice_open")
    await trial.screenshot("conclusion")
    await trial.click(580, 269)  # Overclaim guilt: the game must reject that inference.
    await trial.advance_until("choice_open")
    assert (await trial.state())["conclusion_attempts"] == 1
    await trial.click(570, 360)
    await trial.advance_until("completed_open")
    await trial.screenshot("complete")
    final = await trial.state()
    assert final["complete"] and final["proved"]
    bad = [x for x in trial.responses if x["status"] >= 400 and "favicon" not in x["url"]]
    assert not trial.errors, trial.errors
    assert not bad, bad
    result = {"viewport": [width, height], "reverse_evidence": reverse,
              "startup_seconds_local": round(startup, 2), "final": final,
              "errors": trial.errors, "failed_requests": trial.failed,
              "bad_responses": bad}
    await ctx.close()
    return result

async def main(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=shutil.which("chromium"),
                    args=["--no-sandbox", "--enable-unsafe-swiftshader"])
        results = []
        for width, height, reverse in [(1280, 720, False), (844, 390, True)]:
            folder = output / f"{width}x{height}"
            folder.mkdir(exist_ok=True)
            results.append(await run_one(browser, args.url, width, height, reverse, folder))
        await browser.close()
    (output / "report.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8093/preview/renpy-ch1-test/")
    parser.add_argument("--output", default=str(ROOT / "qa-output"))
    asyncio.run(main(parser.parse_args()))
