# QA 전용 저장칸(2026-10-10 GPT 요청: 원본 저장 17기록을 건드리지 않고 새 게임 QA): 주소에 ?qa=1(또는 ?slot=이름)을 붙이면 다른 접두어에만 읽고 쓴다.
# 기본 주소의 저장은 읽지도 쓰지도 않는다. 화면 왼쪽 아래에 'QA 저장칸' 표시
rep(' var P="daae-preview-ch1-gpt-20261008:";window.__EP1INN=true;',
    ' var P="daae-preview-ch1-gpt-20261008:";window.__EP1INN=true;\n try{var _q=new URLSearchParams(location.search),_s=_q.get("slot")||(_q.has("qa")?"qa":"");_s=String(_s).replace(/[^a-z0-9_-]/gi,"").slice(0,16);if(_s){P="daae-preview-ch1-gpt-20261008-"+_s+":";window.__QASLOT=_s}}catch(e){}')
