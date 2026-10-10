# 2026-10-10 v2: 솜솜(바구니 속 손님) 발견은 조사 중 안 쓰는 방 침대 밑(o_under). 침대 밑을 본 뒤에야 같은 방 빵 바구니(C04)가 보인다.
# (옛 찻주전자 o_teapot 장면은 삭제. 저장 호환: 이미 C04를 가진 저장은 그대로 바구니가 보인다)
rep(' function avail(id){\n  if(id==="C11")return bt("inn_lock");',' function avail(id){\n  if(id==="C04"||id==="basket")return obsSeen("o_under")||has("C04");\n  if(id==="C11")return bt("inn_lock");')
# 월드 지점: 안 쓰는 방에 침대 밑 안쪽(o_under)·바구니(C04)·털(C05). 부엌엔 증거 지점 없음
rep("var anchors={bed13:{C01:[1219,338,96,96],","var anchors={bed13:{o_under:[840,650,130,64],C04:[360,732,150,80],C05:[360,732,150,80],C01:[1219,338,96,96],")
rep(",kitchen:{C04:[1245.5,457.5,185,91],C05:[1245.5,457.5,185,91]}};","};")
# 바구니 소품: 부엌 식탁 대신 안 쓰는 방 바닥(상자 앞). 원본 C04_basket_world.png, 배율·접지점은 부엌 배치와 같게(접지점 360,770)
rep("if(k==='kitchen'){body=image('BG03_kitchen_base.png',[0,0,1774,887]);if(st.basket)body+=prop(D.kitchen.placements[0])}",
    "if(k==='kitchen'){body=image('BG03_kitchen_base.png',[0,0,1774,887])}")
rep("D.storage.props.forEach(function(p){if(p.id==='chest_closed'&&st.box||p.id==='chest_open_with_C11'&&!st.box)return;body+=prop(p)})}",
    "D.storage.props.forEach(function(p){if(p.id==='chest_closed'&&st.box||p.id==='chest_open_with_C11'&&!st.box)return;body+=prop(p)});if(st.basket)body+=prop({id:'C04_world_basket_bed13',file:'C04_basket_world.png',worldDrawRect:{x:267.2,y:630.1,width:185.6,height:185.6}})}")
rep("return {sun:!!(window.__innSun&&__innSun()),box:!!b.inn_lock,basket:!!(b.inn_basket_transferred||b.inn_pro)}",
    "return {sun:!!(window.__innSun&&__innSun()),box:!!b.inn_lock,basket:(G.obsSeen||[]).indexOf('o_under')>=0||(G.found||[]).indexOf('C04')>=0}")
