"""Package original generator PNGs without changing pixels. PIL is read-only."""
import argparse, hashlib, html, json, math, shutil, zipfile
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
URL = 'https://kkhkkh20-bit.github.io/daaegame/'

def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def measure(item):
    target = ROOT / item['path']
    source = Path(item['source'])
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or target.read_bytes() != source.read_bytes():
        shutil.copyfile(source, target)
    with Image.open(target) as original:
        original.load()
        rgba = original.convert('RGBA')
        alpha = rgba.getchannel('A')
        hist = alpha.histogram()
        total = rgba.width * rgba.height
        bounds = alpha.point(lambda value: 255 if value > 64 else 0).getbbox()
        out = dict(item, size=list(rgba.size), mode=original.mode,
            bytes=target.stat().st_size,
            sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
            alphaRange=list(alpha.getextrema()),
            transparentPercent=round(hist[0] / total * 100, 3),
            partialAlphaPercent=round(sum(hist[1:255]) / total * 100, 3),
            visibleBoundsAlphaOver64=list(bounds) if bounds else None,
            crop=[0, 0, rgba.width, rgba.height],
            strictRasterCompliant=False, userApproved=False, runtimeReviewed=False)
        if item['transparent']:
            assert hist[0] > total * .05 and bounds, item['id'] + ': transparency missing'
        assert target.read_bytes() == source.read_bytes(), item['id'] + ': source changed'
        if item['batch'].startswith('I'):
            left, top, right, bottom = bounds
            side = math.ceil(max(right-left, bottom-top) * 1.18)
            out['crop'] = [(left+right-side)//2, (top+bottom-side)//2, side, side]
            out['logicalDisplaySizes'] = [22, 32, 36]
            out['requestedDeliverySize'] = [128, 128]
        elif item['batch'] in ['D02', 'F01', 'C02-F']:
            assert rgba.width == rgba.height, item['id'] + ': portrait must be square'
            out['logicalDisplaySizes'] = [96]
            out['alignmentRule'] = 'Use whole common canvas for every expression; never independently crop visible bounds.'
        elif item['batch'] == 'H01':
            width = min(rgba.width, rgba.height * 9 / 5)
            height = min(rgba.height, rgba.width * 5 / 9)
            out['crop'] = [(rgba.width-width)/2, (rgba.height-height)/2, width, height]
            out['logicalSize'] = [360, 200]
            out['evidence'] = [
                {'spotId':'s2f_stone','evidenceId':'f2_fakestone','name':'등불 속 돌','point':[180,61]},
                {'spotId':'s2f_feather','evidenceId':'f2_feather','name':'기둥 아래 깃털','point':[157,154]},
                {'spotId':'f2_order','evidenceId':'f2_order','name':'바위 위 의뢰서','point':[281,131]}]
        elif item['batch'] == 'U01':
            out['logicalSize'] = [192, 96]
            out['requestedDeliverySize'] = [768, 384]
            tile_review = HERE / 'wood-validation.json'
            review = json.loads(tile_review.read_text()).get(item['id'], {}) if tile_review.exists() else {}
            out['tileabilityReviewed'] = review.get('visualRepeatReviewed', False)
            out['tileBoundaryValidation'] = review
            out['tileabilityRule'] = 'Preview actual repeat in both axes; do not claim edge pixels match without measurement.'
        else:
            out['targetAspect'] = '9:19.5' if item['id']=='title-bg' else '16:9'
            out['overlaySafeRegions'] = {'title':[0,.30], 'importantContent':[.35,.65], 'buttons':[.65,1]}
            out['strictSafeBandGuaranteed'] = False
            out['layoutReview'] = 'Title/menu overlay visually reviewed in preview. Curtain rod and feet slightly extend past nominal importantContent band; preserve aspect ratio and use preview placement.'
        return out

def make_archive(batch, assets):
    path = HERE / (batch + '-assets.zip')
    manifest = {'batchId':batch,'coordinateConvention':'x,y,width,height',
                'strictRasterCompliant':False,'runtimeReviewed':False,'assets':assets}
    cards = ''.join('<figure><img src="'+html.escape(Path(a['path']).name)+'" alt="'+html.escape(a['id'])+'"><figcaption>'+html.escape(a['id'])+'</figcaption></figure>' for a in assets)
    page = '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+batch+' 그림 원본</title><style>body{background:#1a1c2c;color:#f4e4c1;font-family:system-ui;margin:24px}main{display:flex;flex-wrap:wrap;gap:12px}figure{margin:0;padding:12px;background:#2b2d4a}img{width:192px;max-height:420px;object-fit:contain;image-rendering:pixelated}figcaption{max-width:192px;overflow-wrap:anywhere}</style><h1>'+batch+'</h1><p>변형하지 않은 PNG 원본. 실제 표시 좌표·크기는 manifest.json을 참고하세요.</p><main>'+cards+'</main>'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as archive:
        for asset in assets:
            archive.write(ROOT / asset['path'], Path(asset['path']).name)
        archive.writestr('manifest.json', json.dumps(manifest,ensure_ascii=False,indent=2))
        archive.writestr('HANDOFF.txt', (HERE / ('HANDOFF-'+batch+'.txt')).read_text())
        archive.writestr('index.html', page)
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        for asset in assets:
            assert archive.read(Path(asset['path']).name)==(ROOT/asset['path']).read_bytes()
    return {'path':path.relative_to(ROOT).as_posix(),'bytes':path.stat().st_size}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--partial',action='store_true');args=parser.parse_args()
    requests=json.loads((HERE/'requests.json').read_text())
    by_id={}
    for path in sorted(HERE.glob('provenance-*.json')):
        for asset in json.loads(path.read_text()):by_id[asset['id']]=asset
    assets=[measure(item) for item in by_id.values()]
    if not args.partial:
        expected={p for a in requests['assignments'].values() for p in a['files']}
        assert {a['path'] for a in assets}==expected, 'Registered requests incomplete'
        assert len(assets)==requests['expectedNewImages']
    lookup={a['id']:a for a in assets}
    for base,variant in [('sound-on','sound-off'),('trust-full','trust-empty'),('star-full','star-empty'),('lamp-life-on','lamp-life-off')]:
        pair=[lookup.get('icon-'+base),lookup.get('icon-'+variant)]
        if all(pair):
            boxes=[a['visibleBoundsAlphaOver64'] for a in pair]
            left=min(b[0] for b in boxes);top=min(b[1] for b in boxes);right=max(b[2] for b in boxes);bottom=max(b[3] for b in boxes)
            side=math.ceil(max(right-left,bottom-top)*1.18)
            for a in pair:a['crop']=[(left+right-side)//2,(top+bottom-side)//2,side,side]
    groups={batch:[a for a in assets if a['batch']==batch] for batch in requests['assignments']}
    archives={}
    for batch,items in groups.items():
        completed=len(items)==len(requests['assignments'][batch]['files'])
        if not completed:continue
        instructions=['다람 탐정 · '+batch+' 그림 인계','',
            '원본 PNG는 생성 도구 출력 그대로 복사했습니다. 원본 게임과 art/는 변경하지 않았습니다.',
            '이미지 생성은 완료, 사용자 승인 및 실제 게임 적용 검토는 별도입니다.',
            '미리보기: '+URL+'design/retro/production/',
            'manifest.json에 실제 크기·SHA256·투명도·x,y,width,height 좌표·프롬프트가 있습니다.',
            '엄격한 32픽셀 격자/128픽셀 납품 또는 26색 제한 충족으로 표시하지 마세요.',
            '화면 크기에 맞춘 축소·색상 정리·반투명 가장자리 정리는 게임 담당자가 사본에서 수행합니다.','']
        if batch in ['D02','F01','C02-F']:
            instructions+=['얼굴은 머리와 어깨의 공통 전체 캔버스를 96×96으로 최근접 축소합니다.',
                '표정별 불투명 경계를 각각 잘라 확대하면 얼굴 위치가 흔들립니다. 같은 인물은 같은 crop을 유지하세요.',
                'D02는 기존 D01 neutral/happy/think/smug와 함께 총 8표정입니다.',
                'C01/C02 전신 시트는 다른 채팅 원본을 chars/에 그대로 보관했습니다. 이 얼굴들은 별도 추가 납품입니다.','']
        elif batch.startswith('I'):
            instructions+=['각 아이콘은 투명 PNG 한 파일입니다. 기본 표시 32px, 작은 버튼 22px, 큰 버튼 36px.',
                '아이콘 crop에 투명 여백을 조금 남겨 같은 시각 크기로 표시합니다. 원본 PNG 자체는 잘라내지 않았습니다.',
                'on/off 및 full/empty 쌍은 두 파일의 공통 crop을 유지하세요.','']
        elif batch=='H01':
            instructions+=['배경은 가운데 9:5로 crop하고 360×200 좌표를 사용합니다.',
                '증거 점: s2f_stone/f2_fakestone=(180,61), s2f_feather/f2_feather=(157,154), f2_order=(281,131).',
                '노란 줄은 4개 말뚝 사이 장식이며 새 증거가 아닙니다. 벤치/표지판/도토리/꽃/돌도 장식입니다.',
                '장면의 다람은 별도 전신 스프라이트로 겹칩니다. 기존 승인 언덕 파일은 보존합니다.','']
        elif batch=='U01':
            instructions+=['UI 바탕 호두나무 타일 기본/어두운 두 버전입니다. 곧은 가로 판자 4줄, 낮은 대비로 요청했습니다.',
                '원본을 CSS background-repeat로 양 방향 반복해 확인하세요. 실제 native 크기는 manifest 기준입니다.',
                '192×96 반복 미리보기에서 두 버전의 연결을 시각 확인했습니다. 원본 경계 픽셀은 완전히 같지 않으며 수치는 wood-validation.json에 있습니다.',
                '어두운 버전은 기본 버전에서 같은 무늬를 유지하도록 편집 생성했습니다.','']
        else:
            instructions+=['세로용 title-bg와 가로용 title-bg-wide는 서로 다른 구도입니다. 세로 그림을 가로로 억지로 자르지 마세요.',
                '이미지에는 글자/버튼이 없습니다. 제목 위쪽 30%, 중요 내용 가운데 35~65%, 버튼 아래쪽 35%에 겹칩니다.',
                '가로 구도는 실제 이미지와 미리보기 안전 영역을 보고 제목 위치를 맞추세요.','']
            instructions+=['35~65%는 목표 영역입니다. 커튼봉과 의자 발이 가이드 밖으로 조금 나가므로 미리보기의 실제 제목·버튼 배치를 참고하세요.',
                '세로와 가로 모두 제목·버튼이 주요 그림을 가리지 않는 배치로 확인했습니다.','']
        for a in items:
            instructions.append(a['path']+' | 크기 '+str(a['size'])+' | crop '+str(a['crop'])+' | SHA256 '+a['sha256'])
        (HERE/('HANDOFF-'+batch+'.txt')).write_text('\n'.join(instructions)+'\n')
        dump(HERE/(batch+'-manifest.json'),{'batchId':batch,'assets':items,'strictRasterCompliant':False,'runtimeReviewed':False})
        archives[batch]=make_archive(batch,items)
        state_path=ROOT/'design/retro/coordination/parallel'/(batch+'.json')
        state=json.loads(state_path.read_text())
        state.update(status='ready_for_review',generationStarted=True,generationCompleted=True,
            deliveredFiles=[a['path'] for a in items],manifest='design/retro/production/'+batch+'-manifest.json',
            handoff='design/retro/production/HANDOFF-'+batch+'.txt',preview='design/retro/production/index.html',
            archive=archives[batch]['path'],runtimeReviewed=False,userApproved=False,gameIntegration='not_applied',
            note='사용자가 확인한 등록 미완료 요청 전체 제작. PNG 원본 보존, 공통 crop·투명도·ZIP 확인. 실제 게임 적용 검토 대기.')
        dump(state_path,state)
    result={'sourceRequestCommit':requests['sourceRequestCommit'],'scope':requests['scope'],
        'generatedImageCount':len(assets),'expectedImageCount':requests['expectedNewImages'],
        'generationCompleted':len(assets)==requests['expectedNewImages'],'runtimeReviewed':False,'userApproved':False,
        'strictRasterCompliant':False,'protectedGameFilesChanged':False,
        'held':requests['held'],'archives':archives,'assets':assets,
        'archivedPeerBodies':{'sourceBranch':'art/c01-papa-rei-karo-20261007','commit':'a231920742212ec05db3854c10ff229c956497fa','characters':['papa','rei','karo','buri','wanggu','doto'],'pngPixelsChanged':False}}
    dump(HERE/'manifest.json',result)
    (HERE/'data.js').write_text('window.ART_PRODUCTION = '+json.dumps(result,ensure_ascii=False)+';\n')
    dump(HERE/'completion.json',{k:v for k,v in result.items() if k not in ['assets']})
    (HERE/'HANDOFF-ALL.txt').write_text('등록된 미완료 요청 전체 · '+str(len(assets))+'/'+str(requests['expectedNewImages'])+'장 제작\n\n'+
        '미리보기: '+URL+'design/retro/production/\n'+
        '제작 묶음: D02, H01, F01, C02-F, T01, I01, I02, I03, I04, U01\n'+
        '각 묶음의 HANDOFF와 manifest, ZIP은 이 폴더에 있습니다. 게임 담당자는 파일을 개별 전달받지 않아도 이 폴더에서 전부 가져갈 수 있습니다.\n'+
        '요청 문서의 묶음별 중단 규칙은 사용자의 등록 미완료 요청 전체 진행 지시로 이번 범위에서 연속 수행했습니다.\n'+
        'R-005는 사용자 확인 전 보류 상태를 유지합니다. 첨부 문서의 미등록 전체 제작 목록은 이번 범위에 포함하지 않습니다.\n'+
        '원본 game.html/index.html/dot.html/sw.js와 art/ 및 승인 PNG는 수정하지 않았습니다.\n'+
        'C01/C02 전신 원본은 다른 채팅 브랜치에서 내용 그대로 보관했습니다. 새 정면 얼굴은 이 작업의 추가 납품입니다.\n'+
        '생성 완료는 사용자 승인 또는 실제 게임 적용 완료를 뜻하지 않습니다. 화면 검토는 이 폴더 미리보기 기준입니다.\n'+
        '생성 결과는 엄격한 26색/정수 논리 픽셀/128×128 납품이 아니며, 실제 native 크기와 crop을 manifest에 기록했습니다.\n')
    print(json.dumps({'images':len(assets),'completedBatches':list(archives),'archiveBytes':sum(a['bytes'] for a in archives.values())}))

if __name__=='__main__':main()
