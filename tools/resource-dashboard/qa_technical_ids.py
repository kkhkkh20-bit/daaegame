"""Regression: reader-facing surfaces hide code; explicit details and ID search retain it."""
import json, os, re
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(os.environ.get('DASHBOARD_QA_OUT',ROOT/'reports/dashboard-technical-ids-20261018'))
OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('DASHBOARD_ORIGIN','http://127.0.0.1:8765')+'/preview/resource-dashboard/'
TECH=re.compile(r'\b(?:resident_\w+|r13_\w+|map\d+_\w+|assets/\S+|[a-z]+_[a-z_]+)\b')
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM','/usr/bin/chromium'),args=['--no-sandbox'])
    errors=[];counts={}
    for width in (1365,390):
        page=browser.new_page(viewport={'width':width,'height':900},is_mobile=width==390,has_touch=width==390)
        page.on('pageerror',lambda error:errors.append(str(error)))
        requests=[];page.on('request',lambda request:requests.append(request.url))
        page.goto(URL);page.locator('.character').first.wait_for()
        assert any('/app.js?v=' in url for url in requests)
        assert not TECH.search(page.locator('#content').inner_text())
        characters=page.evaluate('data.characters');counts[str(width)]=len(characters)
        for character in characters:
            # Case-insensitive exact technical ID search still finds the same person.
            page.locator('#query').fill(character['id'].upper())
            card=page.locator(f'.character[data-person="{character["id"]}"]')
            assert card.count()==1
            assert character['name'] in card.inner_text()
            assert character['id'] not in card.inner_text()
            card.click();page.locator('#detail[open]').wait_for()
            assert not TECH.search(page.locator('#detail').inner_text()),character['id']
            if character['id']=='resident_piko':
                page.wait_for_function('document.querySelector("#detail img").naturalWidth>0')
                page.screenshot(path=str(OUT/f'piko-popup-{width}.png'))
            evidence=page.locator('#detail .technical').last
            evidence.locator('summary').click()
            assert character['id'] in evidence.inner_text()
            page.locator('#close').click();page.wait_for_function('!document.querySelector("#detail").open')
            page.wait_for_function('!location.hash')
        page.locator('#query').fill('resident_piko');assert page.locator('.character').count()==1
        page.locator('#query').fill('피코');assert page.locator('.character[data-person="resident_piko"]').count()==1
        page.locator('.character img').scroll_into_view_if_needed()
        page.wait_for_function('document.querySelector(".character img").naturalWidth>0')
        page.screenshot(path=str(OUT/f'piko-card-{width}.png'))
        page.locator('#query').fill('')
        for tab in ('places','audio','audit'):
            page.locator(f'[data-tab={tab}]').click()
            assert not TECH.search(page.locator('#content').inner_text()),tab
            if tab=='places':
                action=page.evaluate('data.characters.flatMap(c=>c.placements).find(p=>p.activity)?.activity')
                assert action
                page.locator('#query').fill(action);assert page.locator('.placement-card').count()>0
                page.locator('#query').fill('')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.close()
    assert not errors,errors
    report={'status':'passed','scope':'local checkout; public read blocked by proxy CONNECT 403','characters_checked_per_width':counts,'checks':['versioned renderer request','all IDs searchable case-insensitively','names remain readable','all default character popups hide code','IDs remain in expanded evidence','place/audio/audit default views hide code','action search preserved','mobile layout'],'page_errors':errors}
    (OUT/'browser-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False));browser.close()
