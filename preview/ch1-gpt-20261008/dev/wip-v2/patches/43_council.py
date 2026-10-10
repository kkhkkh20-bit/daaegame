# 2026-10-10 회귀 복구(사용자 QC 메모 6): 242bf8d에서 원탁회의 배경에 식당 월드 그림을 넣으면서 '#rtg:has(svg[data-inn-world])' 규칙이 원탁 전경(.tbl)을 숨기고
#   무대를 화면 전체로 늘려, 원탁 없이 전신이 일렬로 서 보이던 것 → 원탁 방 배경·원탁 전경(art/council/*-v1.png)으로 되돌린다(전체 롤백 아님)
rep('((G&&CASES[G.ci]&&CASES[G.ci].id==="inn"&&window.__innWorldSvg)?window.__innWorldSvg("dining"):"")','""')
# 너울: 승인된 원탁 착석 그림이 없다(missing). 옛 주황 조끼 앉은 그림(art/seat/wanggu-*)·전신 자동 대체 대신, 승인 프로필(neoul-v2 profile)을 둥근 자리표로만 둔다(착석 아트 완료 아님)
rep('["det1","karo","nabi","geokkuri","seryeon"].indexOf(k)>=0)return null;var L=window.__RTG_SEAT[k];','["det1","karo","nabi","geokkuri","seryeon","wanggu"].indexOf(k)>=0)return null;var L=window.__RTG_SEAT[k];')
rep('function figHtml(k,m){if(G&&CASES[G.ci]&&CASES[G.ci].id==="inn"&&["det1","karo","nabi","geokkuri","seryeon"].indexOf(k)>=0){',
    'function figHtml(k,m){if(G&&CASES[G.ci]&&CASES[G.ci].id==="inn"&&k==="wanggu"){var nv=/fluster|rebuttal/.test(exprOf(m,"0"))?"neoul-admonish-profile":"neoul-default-profile";return \'<img alt="" class="sf innpixel neoul9" draggable="false" src="art/ch1/neoul-v2/\'+nv+\'.png">\'}if(G&&CASES[G.ci]&&CASES[G.ci].id==="inn"&&["det1","karo","nabi","geokkuri","seryeon"].indexOf(k)>=0){')
