# 2026-10-10 찻주전자 발견을 조사 중 부엌으로: 찻주전자(o_teapot)를 본 뒤에야 바구니 속 손님(C04)이 보인다. 부엌 지점 위치(월드 좌표)
rep(' function avail(id){\n  if(id==="C11")return bt("inn_lock");',' function avail(id){\n  if(id==="C04"||id==="basket")return obsSeen("o_teapot")||has("C04");\n  if(id==="o_teapot")return !has("C04");\n  if(id==="C11")return bt("inn_lock");')
rep('kitchen:{C04:[1245.5,457.5,185,91],','kitchen:{o_teapot:[895,150,170,110],C04:[1245.5,457.5,185,91],')
