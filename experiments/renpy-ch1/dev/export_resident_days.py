"""날짜·분기 매칭표에 맞춘 주민 별편의 읽기 파일과 인쇄본을 만든다."""
import argparse
import asyncio
import base64
import html
import json
import re
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Mm, Pt
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]


def word(path, title, subtitle, premise, chapters):
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Mm(148), Mm(210)
    section.top_margin = section.bottom_margin = Mm(18)
    section.left_margin = section.right_margin = Mm(18)
    for name in ('Normal', 'Title', 'Heading 1'):
        style = doc.styles[name]
        style.font.name = '맑은 고딕'
        style._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), '맑은 고딕')
    doc.styles['Normal'].font.size = Pt(10.5)
    doc.styles['Normal'].paragraph_format.line_spacing = 1.6
    doc.add_heading(title, 0)
    doc.add_paragraph(subtitle)
    doc.add_paragraph(premise)
    for heading, paragraphs in chapters:
        doc.add_page_break()
        doc.add_heading(heading, 1)
        for paragraph in paragraphs:
            doc.add_paragraph(paragraph)
    doc.core_properties.title = title + ' — ' + subtitle
    doc.core_properties.author = '다람탐정'
    doc.save(path)


async def export(source, out):
    out.mkdir(parents=True, exist_ok=True)
    spec = json.loads((source / 'reaction-map.json').read_text())
    basename = spec.get('basename', 'resident-days456')
    edition = spec.get('edition', '2026년 11월 6일 · 4~6일차')
    renumber = spec.get('renumber_chapters', False)
    raw = (source / '주민_반응별편.md').read_text().split('## 작가·게임 매칭표')[0]
    chunks = re.split(r'^## (\d\d\..*)$', raw, flags=re.M)
    assert len(chunks) == 1 + len(spec['scenes']) * 2
    chapters = {}
    for index, scene in enumerate(spec['scenes']):
        heading, body = chunks[1 + index * 2:3 + index * 2]
        chapters[scene['id']] = (heading.strip(), [p.strip() for p in body.split('\n\n') if p.strip()])
    profiles = dict(spec['reading_profiles'])
    profiles['all'] = dict(label='전체 분기 비교', order=list(chapters))
    font = base64.b64encode((ROOT / 'game/assets/Pretendard-Regular.otf').read_bytes()).decode()
    css = '''@font-face{font-family:Book;src:url(data:font/otf;base64,FONT)}
@page{size:A5;margin:18mm}*{box-sizing:border-box}body{font-family:Book,sans-serif;background:#f4efe4;color:#30271e;line-height:1.9;margin:0}main{max-width:760px;margin:auto;padding:36px 28px}h1,h2{line-height:1.5;word-break:keep-all}h1{font-size:30px}h2{font-size:23px;margin-top:40px}p{font-size:17px;word-break:keep-all;overflow-wrap:break-word}nav{position:sticky;top:0;background:#fffaf1;border-bottom:1px solid #d2c4ac;padding:12px;display:flex;gap:8px;flex-wrap:wrap}button{font:inherit;padding:10px 14px;border:1px solid #b4a389;border-radius:4px;background:white;color:#30271e;cursor:pointer}button[aria-pressed=true]{background:#26394a;color:white}.meta{color:#786957;font-size:14px}.chapter{border-top:1px solid #c8b899;padding-top:12px;margin-top:40px}.chapter[hidden]{display:none}footer{margin-top:40px;color:#786957;font-size:14px}
@media print{body{background:white;font-size:10.5pt}main{max-width:none;padding:0}nav{display:none}h1{font-size:24pt}h2{font-size:16pt;break-after:avoid}p{font-size:10.5pt;orphans:2;widows:2}.chapter{break-before:page;border:0;margin:0;padding:0}.meta{font-size:8pt}footer{display:none}.chapter[hidden]{display:none!important}}'''.replace('FONT', font)
    esc = html.escape
    parts = ['<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + esc(spec['title']) + '</title><style>' + css + '</style><nav aria-label="이야기 경로">']
    for key, profile in profiles.items():
        parts.append('<button type="button" data-flow="' + esc(key) + '">' + esc(profile['label']) + '</button>')
    parts.append('</nav><main><h1>' + esc(spec['title']) + '</h1><p class="meta">' + esc(edition) + '</p><p id="intro">' + esc(spec['introduction']) + '</p><p>' + esc(spec['premise']) + '</p>')
    for scene_id, (heading, paragraphs) in chapters.items():
        parts.append('<section class="chapter" data-id="' + scene_id + '"><h2>' + esc(heading) + '</h2>')
        parts.extend('<p>' + esc(p).replace('\n', '<br>') + '</p>' for p in paragraphs)
        parts.append('</section>')
    parts.append('<footer>별편 전문은 읽기 문서입니다. 본편에는 해당 경로의 짧은 행동·대사만 연결했습니다.</footer></main><script>const profiles=' + json.dumps(profiles, ensure_ascii=False) + ';const introduction=' + json.dumps(spec['introduction'], ensure_ascii=False) + ';')
    parts.append('const renumber=' + json.dumps(renumber) + ';')
    parts.append('''for(const s of document.querySelectorAll('.chapter'))s.dataset.title=s.querySelector('h2').textContent.replace(/^\\d+\\.\\s*/, '');function select(flow){const order=profiles[flow].order;const sections=Array.from(document.querySelectorAll('.chapter'));const footer=document.querySelector('footer');for(const [i,id] of order.entries()){const node=sections.find(n=>n.dataset.id===id);node.hidden=false;if(renumber)node.querySelector('h2').textContent=String(i+1).padStart(2,'0')+'. '+node.dataset.title;footer.before(node);}for(const node of sections)if(!order.includes(node.dataset.id)){node.hidden=true;footer.before(node);}for(const b of document.querySelectorAll('[data-flow]'))b.setAttribute('aria-pressed',String(b.dataset.flow===flow));document.querySelector('#intro').textContent=flow==='all'?introduction:profiles[flow].label+' · 같은 판에서 이어지는 장면만 시간순으로 읽습니다.';}for(const b of document.querySelectorAll('[data-flow]'))b.addEventListener('click',()=>select(b.dataset.flow));select(Object.keys(profiles)[0]);</script></html>''')
    content = ''.join(parts)
    (out / (basename + '.html')).write_text(content)
    (out / (basename + '.txt')).write_text(raw)
    result = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = await browser.new_page(viewport={'width': 1000, 'height': 900})
        await page.set_content(content, wait_until='load')
        await page.evaluate('document.fonts.ready')
        for flow, profile in profiles.items():
            await page.locator('[data-flow="' + flow + '"]').click()
            visible = await page.locator('.chapter:visible').evaluate_all('(nodes)=>nodes.map(n=>n.dataset.id)')
            assert visible == profile['order'], (flow, visible)
            if flow == 'all':
                await page.locator('#intro').evaluate('(node,text)=>node.textContent=text', spec['introduction'])
            selected = [chapters[k] for k in profile['order']]
            if renumber:
                selected = [(re.sub(r'^\d+\.', '%02d.' % i, title), paragraphs) for i, (title, paragraphs) in enumerate(selected, 1)]
                headings = await page.locator('.chapter:visible h2').all_text_contents()
                assert headings == [title for title, paragraphs in selected]
            subtitle = profile['label'] + ' · ' + edition
            word(out / (basename + '-' + flow + '.docx'), spec['title'], subtitle, spec['premise'], selected)
            await page.pdf(path=str(out / (basename + '-' + flow + '.pdf')), prefer_css_page_size=True, print_background=True)
            result[flow] = len(visible)
        await page.locator('[data-flow="' + next(iter(spec['reading_profiles'])) + '"]').click()
        await page.screenshot(path=str(out / 'book-preview.png'))
        await browser.close()
    (out / 'export-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=ROOT / 'docs/design/resident-reactions-day456-20261106')
    parser.add_argument('--out', type=Path, default=Path('/workspace/outputs/resident-days456-20261106'))
    args = parser.parse_args()
    asyncio.run(export(args.source, args.out))
