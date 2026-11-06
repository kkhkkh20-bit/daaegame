"""주민 별편을 분기별 읽기 HTML과 인쇄용 PDF·DOCX로 내보낸다."""
import asyncio
import base64
import html
import json
import os
import re
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Mm, Pt
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/design/resident-reactions-20261105'
OUT = Path(os.environ.get('ROOM13_BOOK_OUT', '/workspace/outputs/resident-reactions-20261105'))
NAME = os.environ.get('ROOM13_BOOK_NAME', '다람탐정_주민별편_3일의아침')
EDITION = os.environ.get('ROOM13_BOOK_EDITION', '2026년 11월 6일 · 행동·장면 개정본')


def clean(text):
    return text.replace('**', '').replace('`', '')


def export_plan():
    doc = Document()
    section = doc.sections[0]
    section.top_margin = section.bottom_margin = Mm(18)
    section.left_margin = section.right_margin = Mm(16)
    for name in ('Normal', 'Title', 'Heading 1', 'Heading 2', 'Heading 3'):
        style = doc.styles[name]
        style.font.name = '맑은 고딕'
        style._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), '맑은 고딕')
    doc.styles['Normal'].font.size = Pt(10)
    doc.add_heading('다람탐정 주민 반응 기획서', 0)
    doc.add_paragraph('14일 공통 시간표 · 피코 현장조사 · 사건 뒤 행동과 대사\n게임 미반영 기획 · ' + EDITION)
    for filename in ('README.md', '인물_개정기준.md', '피코_현장조사_기획.md', '사건후_주민행동시스템_기획.md', '공통시간표와_반응규칙.md'):
        doc.add_page_break()
        table = None
        for raw in (SOURCE / filename).read_text().splitlines():
            line = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', clean(raw)).strip()
            if not line:
                table = None
                continue
            if line.startswith('|'):
                cells = [c.strip() for c in line.strip('|').split('|')]
                if all(re.fullmatch(r':?-+:?', c) for c in cells):
                    continue
                if table is None:
                    table = doc.add_table(rows=0, cols=len(cells))
                    table.style = 'Table Grid'
                row = table.add_row().cells
                for index, cell in enumerate(cells):
                    target = min(index, len(row) - 1)
                    row[target].text += (' / ' if index >= len(row) else '') + cell
                continue
            table = None
            if line.startswith('#'):
                level = min(3, len(line) - len(line.lstrip('#')))
                doc.add_heading(line.lstrip('# ').strip(), level)
            else:
                doc.add_paragraph(line[2:] if line.startswith('- ') else line, style='List Bullet' if line.startswith('- ') else None)
    doc.core_properties.title = '다람탐정 주민 반응 기획서'
    doc.core_properties.author = '다람탐정'
    doc.save(OUT / '다람탐정_주민반응_기획서.docx')


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manuscript = (SOURCE / '주민_반응별편.md').read_text().split('## 작가·게임 매칭표')[0]
    scenes = json.loads((SOURCE / 'reaction-map.json').read_text())['scenes']
    chunks = re.split(r'^## (\d\d\..*)$', manuscript, flags=re.M)
    assert len(chunks) == 15 and len(scenes) == 7
    chapters = [(chunks[i].strip(), chunks[i + 1].strip(), scenes[(i - 1) // 2]) for i in range(1, len(chunks), 2)]
    labels = dict(dead_stolen='사망·등 도난', sheltered_stolen='보호 생존·등 도난', attempt='생존·절도 미수')

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
    doc.add_heading('다람탐정 주민 별편', 0)
    doc.add_paragraph('3일의 아침\n주민 네 명 · 일곱 장면\n' + EDITION)
    intro = '서로 다른 세 아침의 게임 미반영 원고입니다. 사망판은 01→05→07, 보호생존판은 04→02→05→07, 미수판은 03→06 순서입니다. 각 흐름만 이어 읽는 별도 PDF·Word도 함께 제공합니다.'
    doc.add_paragraph(intro)
    premise = '다돌과 딸 다람이 엄마를 만나러 찾아온 방은 비어 있었습니다. 두 사람은 엄마의 얼굴을 사람들에게 보여 주려고 화가 피코에게 초상을 부탁했습니다. 피코가 평소 잠을 자던 곳은 광장의 3번 등 아래였습니다. 안에 든 돌이 열을 내어 따뜻한 자리였습니다. 다음 날 아침은 전날 부녀가 한 일에 따라 달라집니다.'
    doc.add_paragraph(premise)

    font = base64.b64encode((ROOT / 'game/assets/Pretendard-Regular.otf').read_bytes()).decode()
    css = '''@font-face{font-family:Book;src:url(data:font/otf;base64,FONT)}
@page{size:A5;margin:18mm}*{box-sizing:border-box}body{font-family:Book,sans-serif;background:#f4efe4;color:#30271e;line-height:1.9;margin:0}main{max-width:760px;margin:auto;padding:36px 28px}h1,h2{line-height:1.5;word-break:keep-all}h1{font-size:32px}h2{font-size:24px;margin-top:40px}p{font-size:17px;word-break:keep-all;overflow-wrap:break-word}nav{position:sticky;top:0;background:#fffaf1;border-bottom:1px solid #d2c4ac;padding:12px;display:flex;gap:8px;flex-wrap:wrap}button{font:inherit;padding:10px 14px;border:1px solid #b4a389;border-radius:4px;background:#fff;color:#30271e;cursor:pointer}button[aria-pressed=true]{background:#26394a;color:white}.meta{color:#786957;font-size:14px}.chapter{border-top:1px solid #c8b899;padding-top:12px;margin-top:40px}.chapter[hidden]{display:none}footer{margin-top:40px;color:#786957;font-size:14px}
@media print{body{background:white;font-size:10.5pt}main{max-width:none;padding:0}nav{display:none}h1{font-size:24pt}h2{font-size:16pt;break-after:avoid}p{font-size:10.5pt;orphans:2;widows:2}.chapter,.chapter[hidden]{display:block!important;break-before:page;border:0;margin:0;padding:0}.meta{font-size:8pt}footer{display:none}}'''.replace('FONT', font)
    parts = ['<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>다람탐정 주민 별편 — 3일의 아침</title><style>' + css + '</style><nav aria-label="사건 흐름">']
    for key, label in list(labels.items()) + [('all', '전체 기획 원고')]:
        parts.append('<button type="button" data-branch="' + key + '">' + label + '</button>')
    parts.append('</nav><main><h1>다람탐정 주민 별편<br>3일의 아침</h1><p class="meta">' + html.escape(EDITION) + '</p><p>' + intro + '</p><p>' + premise + '</p>')
    for title, body, scene in chapters:
        doc.add_page_break()
        doc.add_heading(title, 1)
        paragraphs = [clean(p.strip()) for p in body.split('\n\n') if p.strip()]
        branches = ' '.join(scene['branches'])
        parts.append('<section class="chapter" data-scene="' + scene['id'] + '" data-flows="' + branches + '"><h2>' + html.escape(title) + '</h2>')
        for index, paragraph in enumerate(paragraphs):
            doc.add_paragraph(paragraph)
            parts.append('<p' + (' class="meta"' if index == 0 else '') + '>' + html.escape(paragraph).replace('\n', '<br>') + '</p>')
        parts.append('</section>')
    parts.append('<footer>' + html.escape(EDITION) + ' · 주민 반응 기획 원고 · 게임의 해당 분기에 맞춰 읽는 별편입니다.</footer></main>')
    reading_orders = json.loads((SOURCE / 'reaction-map.json').read_text())['reading_orders']
    parts.append('<script>const readingOrders=' + json.dumps(reading_orders) + ';\n')
    parts.append('''
function select(flow){const sections=Array.from(document.querySelectorAll('.chapter'));const order=readingOrders[flow]||sections.map(s=>s.dataset.scene).sort();sections.sort((a,b)=>{const ai=order.indexOf(a.dataset.scene),bi=order.indexOf(b.dataset.scene);return (ai<0?99:ai)-(bi<0?99:bi)});const footer=document.querySelector('footer');for(const section of sections){section.hidden=flow!=='all'&&!section.dataset.flows.split(' ').includes(flow);footer.before(section);}for(const button of document.querySelectorAll('[data-branch]'))button.setAttribute('aria-pressed',String(button.dataset.branch===flow));}
for(const button of document.querySelectorAll('[data-branch]'))button.addEventListener('click',()=>select(button.dataset.branch));select('dead_stolen');
</script></html>''')
    doc.core_properties.title = '다람탐정 주민 별편 — 3일의 아침'
    doc.core_properties.author = '다람탐정'
    doc.save(OUT / (NAME + '.docx'))
    branch_names = dict(dead_stolen='사망판', sheltered_stolen='보호생존판', attempt='미수판')
    chapter_by_id = {scene['id']: (title, body) for title, body, scene in chapters}
    for flow, suffix in branch_names.items():
        branch_doc = Document()
        section = branch_doc.sections[0]
        section.page_width, section.page_height = Mm(148), Mm(210)
        section.top_margin = section.bottom_margin = Mm(18)
        section.left_margin = section.right_margin = Mm(18)
        for style_name in ('Normal', 'Title', 'Heading 1'):
            style = branch_doc.styles[style_name]
            style.font.name = '맑은 고딕'
            style._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), '맑은 고딕')
        branch_doc.styles['Normal'].font.size = Pt(10.5)
        branch_doc.styles['Normal'].paragraph_format.line_spacing = 1.6
        branch_doc.add_heading('다람탐정 주민 별편', 0)
        branch_doc.add_paragraph('3일의 아침 · ' + labels[flow] + '\n' + EDITION)
        branch_doc.add_paragraph('이 사건 흐름의 장면만 시간순으로 묶었습니다. 게임 미반영 원고입니다.')
        branch_doc.add_paragraph(premise)
        for scene_id in reading_orders[flow]:
            title, body = chapter_by_id[scene_id]
            branch_doc.add_page_break()
            branch_doc.add_heading(title, 1)
            for paragraph in body.split('\n\n'):
                if paragraph.strip():
                    branch_doc.add_paragraph(clean(paragraph.strip()))
        branch_doc.core_properties.title = '다람탐정 주민 별편 — ' + suffix
        branch_doc.core_properties.author = '다람탐정'
        branch_doc.save(OUT / (NAME + '_' + suffix + '.docx'))
    export_plan()
    (OUT / (NAME + '.html')).write_text(''.join(parts))
    (OUT / (NAME + '.txt')).write_text(clean(manuscript))
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = await browser.new_page(viewport={'width': 1000, 'height': 900})
        await page.set_content(''.join(parts), wait_until='load')
        await page.evaluate('document.fonts.ready')
        for branch, count in [('dead_stolen', 3), ('sheltered_stolen', 4), ('attempt', 2), ('all', 7)]:
            await page.locator('[data-branch="' + branch + '"]').click()
            assert await page.locator('.chapter:visible').count() == count
            if branch != 'all':
                assert await page.locator('.chapter:visible').evaluate_all('(nodes)=>nodes.map(n=>n.dataset.scene)') == reading_orders[branch]
        await page.pdf(path=str(OUT / (NAME + '.pdf')), prefer_css_page_size=True, print_background=True)
        await page.add_style_tag(content='@media print{.chapter[hidden]{display:none!important}}')
        for flow, suffix in branch_names.items():
            await page.locator('[data-branch="' + flow + '"]').click()
            await page.locator('main > h1').evaluate('(node, label)=>{node.textContent="다람탐정 주민 별편 — "+label}', labels[flow])
            await page.locator('main > p').nth(1).evaluate('(node)=>{node.textContent="이 사건 흐름의 장면만 시간순으로 묶었습니다. 게임 미반영 원고입니다."}')
            await page.pdf(path=str(OUT / (NAME + '_' + suffix + '.pdf')), prefer_css_page_size=True, print_background=True)
        await page.locator('main > h1').evaluate('(node)=>{node.innerHTML="다람탐정 주민 별편<br>3일의 아침"}')
        await page.locator('main > p').nth(1).evaluate('(node, text)=>{node.textContent=text}', intro)
        await page.locator('[data-branch="dead_stolen"]').click()
        await page.screenshot(path=str(OUT / '별편_미리보기.png'), full_page=False)
        await browser.close()
    print(json.dumps(dict(chapters=7, viewpoints=4, html_branch_filter='통과', files=[NAME + ext for ext in ('.html', '.pdf', '.docx', '.txt')]), ensure_ascii=False))


if __name__ == '__main__':
    asyncio.run(main())
