# 저장 호환(2026-10-10 dot 요청): 도입 장면 목록이 바뀌어(P4·P9 제외, 이전엔 P6·P8·P13도 있었음) 옛 도입 중간 저장의 장면 번호(inn_pi)가
# 다른 장면을 가리키던 것. 재현(f91cb14): 옛 P5→P10(열세 침대 장면 건너뜀), 옛 P9→P11(밤·종 건너뜀), 옛 P10→P12(사건 신고 건너뜀),
# 옛 P11·P12·P13→범위 밖이라 장면 번호가 지워져 P1부터 다시. 막힘·기록 손실은 없음.
# 보완: 앞으로는 장면 이름(inn_psid)도 저장. 이름이 없는 옛 저장은 번호·배경(inn_bg)·장소로 옛 장면을 알아내 같은 장면(빠진 장면이면 이야기 순서상 다음 장면)으로 옮긴다.
#   다른 저장 키·수집 기록(found·asked 등)은 건드리지 않는다. 알아낼 수 없는 저장은 예전과 같이 둔다.
rep('G.beats.inn_pi=i;var s=EP.PRO[i];G.beats.inn_bg=s.bg||null;',
    'G.beats.inn_pi=i;var s=EP.PRO[i];G.beats.inn_psid=s.sid||null;G.beats.inn_bg=s.bg||null;')
rep('  index("inn_pi",EP.PRO.length);index("inn_ei",EP.END.length);',
    '''  (function(){try{if(b.inn_pro||typeof b.inn_pi!=="number")return;var pi=b.inn_pi,sid=(typeof b.inn_psid==="string"&&/^P\\d+$/.test(b.inn_psid))?b.inn_psid:null;
    if(!sid){var lid=((EP.LOCS||[])[g.loc]||{}).id,bg=typeof b.inn_bg==="string"?b.inn_bg:null;
     /* 배경으로 먼저: 같은 배경이 두 번 나오는 현관(P3·P9)·복도(P5·P11)는 번호 앞뒤로 가른다(모든 옛 배열·f91cb14에서 성립) */
     if(bg==="carriage")sid="P1";else if(bg==="plaza")sid="P2";else if(bg==="reception_desk_wide")sid="P4";else if(bg==="room")sid="P10";
     else if(bg==="reception")sid=pi<=2?"P3":"P9";else if(bg==="corridor")sid=pi<=4?"P5":"P11";
     else if(!bg&&lid==="bed13")sid="P12";else if(!bg&&lid==="kitchen")sid="P13";else if(!bg&&lid==="dining")sid="P8";
     else if(!bg&&pi<=4)sid=["P1","P2","P3","P4","P5"][pi]}
    if(!sid)return;var n0=+sid.slice(1),k=-1;for(var i=0;i<EP.PRO.length;i++){var si=EP.PRO[i]&&EP.PRO[i].sid;if(si&&+si.slice(1)>=n0){k=i;break}}
    b.inn_pi=k<0?EP.PRO.length:k;   /* 지금 목록에 없으면 다음 장면, 뒤에 남은 장면이 없으면 도입 끝(조사 시작) */
    if(window.__innSaveMap)window.__innSaveMap.push(sid+"→"+b.inn_pi)}catch(e){}})();
  index("inn_pi",EP.PRO.length+1);index("inn_ei",EP.END.length);
  delete n.beats.inn_psid;if(typeof b.inn_psid==="string"&&/^P\\d+$/.test(b.inn_psid)&&n.beats.inn_pi!=null)n.beats.inn_psid=(EP.PRO[n.beats.inn_pi]||{}).sid||b.inn_psid;''')
