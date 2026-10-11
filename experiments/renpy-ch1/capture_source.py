"""Capture shipped v2 data read-only from a locally served public build."""
import argparse
import asyncio
import hashlib
import json
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
SOURCE=Path('preview/ch1-gpt-20261008/play_v2.html')

async def main(url):
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        page=await browser.new_page()
        await page.goto(url)
        await page.wait_for_function('!!window.EP1INN')
        data=await page.evaluate('({episode: JSON.parse(JSON.stringify(window.EP1INN)), music: window.__INN_MUSIC})')
        await browser.close()
    data.update(source=str(SOURCE),sha256=hashlib.sha256((REPO/SOURCE).read_bytes()).hexdigest())
    (ROOT/'game/chapter-source.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--url',default='http://127.0.0.1:8093/preview/ch1-gpt-20261008/play_v2.html')
    asyncio.run(main(parser.parse_args().url))
