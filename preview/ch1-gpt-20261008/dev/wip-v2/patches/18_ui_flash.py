# 2026-10-09 전환 플래시 정리
# 1) 장면 속 주민 전신: 처음부터 1장 새 그림 경로로 불러온다(옛 art/body 그림이 먼저 그려졌다가 바뀌던 문제). 경로표는 inn_ui9.js의 __innBody
_st='(G&&CASES[G.ci]&&CASES[G.ci].id==="inn"&&(k==="karo"';_en='"art/body/"+k+"-0.png"';_n=0;_pos=0
while True:
    _i=s.find(_st,_pos)
    if _i<0: break
    _j=s.find(_en,_i)
    if _j<0 or _j-_i>600: _pos=_i+1;continue
    _j+=len(_en);s=s[:_i]+'((window.__innBody&&window.__innBody(k))||('+s[_i:_j]+'))'+s[_j:];_n+=1;_pos=_j+40
if _n!=2: sys.exit('18_ui_flash: 주민 그림 경로 %d곳'%_n)
# 2) 작은 얼굴(대화 시작 컷인·기록 인물 칸): 할머니 v5·세련 앉은 v2·도토 v4도 새 그림에서 잘라 쓴다(옛 벡터 얼굴·옛 얼굴 PNG가 뜨던 문제). 그림 크기를 항목별로
rep('seryeon:["seryeon-normal-front-v1",52,4,96,96]}','innma:["innma-neutral-v5",12,0,92,92,146,182],seryeon:["seryeon-seated-paperwork-v2-talk",36,0,86,86,160,216],doto:["doto-v4-182",36,0,90,90,182,182]}')
rep('<image href="art/ch1/cast/\'+file+\'.png" width="192" height="192" style="image-rendering:pixelated"/>',
    '<image href="art/ch1/cast/\'+file+\'.png" width="\'+(f[5]||192)+\'" height="\'+(f[6]||192)+\'" style="image-rendering:pixelated"/>')
# 3) 작은 얼굴 잘라 보기: 항목에 그림 크기를 덧붙였으므로 viewBox에는 앞 네 값만
rep('viewBox="\'+f.slice(1).join(\' \')+\'" preserveAspectRatio="xMidYMid meet" overflow="hidden"><image href="art/ch1/cast/','viewBox="\'+f.slice(1,5).join(\' \')+\'" preserveAspectRatio="xMidYMid meet" overflow="hidden"><image href="art/ch1/cast/')
# 4) 살펴본 증거 지점의 체크 표시에 증거 번호를 달아, 1장 월드 장면(창고·부엌)에서도 실제 물건 자리에 놓을 수 있게(inn_ui9.js doneMarks)
rep('if(got)h+=\'<span class="hot done" style="\'+st+\'" aria-hidden="true">','if(got)h+=\'<span class="hot done" data-done="\'+s.ev.id+\'" style="\'+st+\'" aria-hidden="true">')
