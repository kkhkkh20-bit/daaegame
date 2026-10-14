# Canonical source excerpts — d4342aea

All paths are inside preview/room13-source/ROOM13_SOURCE_HANDOFF.zip, not stale repository-root experiments.


## game/room13_revision.rpy

```text
13: label r13_object_mechanism(kind):
14:     if not r13_secret_route_available():
15:         return
16:     if kind=="passage_exit":
17:         call r13_observe([(None,"손잡이를 당기자 안쪽에서 걸쇠가 풀렸다. 책장 뒤판을 밀면 우리 객실로 나갈 수 있다.")],"puzzle:inside:release")
18:         menu:
19:             "2층 객실로 나간다":
20:                 $ r13_edit(location="room13")
21:             "통로를 더 살핀다":
22:                 pass
23:         return
24:     if kind=="kitchen_switch":
25:         if not r13_has("switch_found"):
26:             call r13_observe([(None,"선반 아래 덮개를 옆으로 밀었다. 작은 레버와 벽 안으로 이어지는 금속 줄. 전선은 없다.")],"puzzle:switch:find")
27:             $ r13_flag("switch_found")
28:         if r13_has("E04"):
29:             call r13_observe([(None,"도면에 덧그린 걸쇠 표시와 모양이 같다. 붉은 선의 다른 끝은 2층으로 올라간다.")],"puzzle:switch:plan")
30:         window hide
31:         call screen r13_lever_actions(room13["kitchen_switch"])
32:         if _return == "raise":
33:             $ r13_edit(kitchen_switch=True)
34:             $ source_fx("tap")
35:             call r13_observe([(None,"손을 떼어도 레버는 올라간 채다. 금속 줄이 팽팽해졌다.")],"puzzle:switch:on")
36:         elif _return == "lower":
37:             $ r13_edit(kitchen_switch=False,passage_open=False)
38:             $ source_fx("tap")
39:             call r13_observe([(None,"금속 줄이 느슨해졌다. 위층에서 작은 걸쇠 소리가 났다.")],"puzzle:switch:off")
40:         return
41:     if kind=="book_latch":
42:         if room13["passage_open"]:
43:             call r13_observe([(None,"책장 아래 판이 안쪽으로 밀린다. 틈 뒤에서 좁은 계단의 찬 공기가 올라온다.")],"puzzle:book:open")
44:             menu:
45:                 "통로로 들어간다":
46:                     $ r13_edit(location="passage")
47:                 "일단 방에 남는다":
48:                     pass
49:             return
50:         call r13_observe([(None,"책장 오른쪽 아래의 붉은 책. 등을 잡아당겼지만 속장이 넘어가지 않는다.")],"puzzle:book:look")
51:         menu:
52:             "책의 아래쪽을 누르고 옆으로 젖힌다":
53:                 if room13["kitchen_switch"]:
54:                     $ source_fx("door")
55:                     $ r13_edit(passage_open=True)
56:                     $ r13_flag("passage_known")
57:                     call r13_observe([(None,"책장 아래쪽 판이 벽 안으로 밀렸다. 어둠 속에 내려가는 계단이 있다. 안쪽 손잡이를 당기면 주방 쪽 걸쇠와 별개로 문을 밀 수 있다."),("dad","나오는 쪽에서는 갇히지 않게 했군."),(None,"손을 떼자 판이 다시 닫혔다. 풀린 걸쇠는 그대로라 다시 밀 수 있다.")],"puzzle:book:unlocked")
58:                     $ r13_grant(["E37"],"주방 레버와 2층 책장 손잡이의 실제 작동")
59:                     menu:
60:                         "통로로 들어간다":
61:                             $ r13_edit(location="passage")
62:                         "지금은 방에 남는다":
63:                             pass
64:                 else:
65:                     call r13_observe([(None,"책 모양 손잡이만 조금 움직였다. 뒤의 걸쇠가 버티고 있다." )],"puzzle:book:locked")
66:             "다른 곳을 살핀다":
67:                 pass
68:         return
69:     return
70: 
71: label r13_case_interview:
72:     call r13_scene("winter","초소 안 보호실 · 만남","quiet")
```


## game/room13_navigation.rpy

```text
3: # Spatial navigation: selecting a pin never travels or spends time.
4: init 60 python:
5:     R13_MAP_REGIONS = (("village", "마을"), ("inn", "여관 안"), ("mountain", "북쪽 산길"))
6:     R13_MAP_NODES = {
7:         "village": {"gate":(132,354), "square":(336,250), "inn":(715,299),
8:             "post":(466,172), "workshop":(585,425), "clinic":(407,370),
9:             "school":(95,143), "store":(553,292)},
10:         "inn": {"inn":(435,420), "dining":(434,307), "kitchen":(170,307),
11:             "hall":(340,120), "room13":(685,120), "passage":(685,40), "guestroom":(245,65)},
12:         "mountain": {"facility":(110,135), "greenhouse":(382,108), "altar":(644,100)},
13:     }
14:     R13_MAP_LABELS = {"gate":"마을 입구", "square":"광장", "inn":"여관 접수대",
15:         "post":"우체국", "workshop":"수리점", "clinic":"진료실", "school":"학교",
16:         "store":"공동 창고", "dining":"식당", "kitchen":"주방", "hall":"2층 복도",
17:         "room13":"13호실", "guestroom":"임시 객실", "passage":"숨은 통로", "facility":"보호시설",
18:         "greenhouse":"폐온실", "altar":"산속 제단"}
19: 
20:     R13_INN_LOCATIONS=("inn","dining","kitchen","hall","room13","passage","guestroom")
21:     R13_LOCAL_CONNECTIONS={
22:         "inn":(("dining","식당"),("kitchen","주방"),("hall","2층 복도"),("outside","여관 밖으로")),
23:         "dining":(("inn","접수대"),("kitchen","주방")),
24:         "kitchen":(("dining","식당"),("inn","접수대")),
25:         "hall":(("inn","1층 접수대"),("room13","13호실"),("guestroom","임시 객실")),
26:         "room13":(("hall","복도로"),("passage","숨은 통로")),
27:         "guestroom":(("hall","복도로"),),
28:         "passage":(("room13","13호실로"),),
29:     }
30: 
31:     def r13_local_connections():
32:         allowed=set(r13_places())
33:         return [(key,title) for key,title in R13_LOCAL_CONNECTIONS.get(store.room13["location"],())
34:             if key=="outside" or key in allowed]
35: 
36:     def r13_local_destination(key):
37:         # Validate again at dispatch, including after a saved interaction resumes.
38:         return key if key in dict(r13_local_connections()) else None
39: 
40:     def r13_map_region(location):
41:         if location in R13_INN_LOCATIONS:return "inn"
42:         if location in ("facility","greenhouse","altar"):return "mountain"
43:         return "village"
44: 
45:     def r13_map_nodes(region):
46:         allowed=set(r13_places())|{store.room13["location"]}
47:         return [(key,point) for key,point in R13_MAP_NODES[region].items()
48:             if key in allowed]
49: 
50:     def r13_map_selection(region,selected):
51:         keys=[key for key,point in r13_map_nodes(region)]
52:         if selected in keys:return selected
53:         current=store.room13["location"]
54:         if current in keys:return current
55:         return next((key for key in keys if key in r13_places()),keys[0] if keys else current)
56: 
```


## game/room13.rpy

```text
263:         $ r13_mark("empty:%d:%d"%(r13_choice[1][0]//70,r13_choice[1][1]//70),*r13_choice[1])
264:         call r13_lines([(None,"발밑과 벽을 살폈다. 이 자리에는 따로 눈에 띄는 흔적이 없다.")],"field:empty:"+room13["location"])
265:         jump r13_field
266:     if r13_choice[0]=="person":
267:         $ r13_target=r13_choice[1]
268:         call r13_talk
269:         jump r13_roam
270:     if r13_choice[0]=="travel":
271:         $ r13_destination=r13_local_destination(r13_choice[1])
272:         if r13_destination=="outside":
273:             call screen r13_map(initial_region="village")
274:             if _return and _return in r13_places() and _return!=room13["location"]:
275:                 $ r13_edit(location=_return)
276:                 jump r13_roam
277:         elif r13_destination:
278:             $ r13_edit(location=r13_destination)
279:             jump r13_roam
280:         jump r13_field
281:     if r13_choice[1] in ("doorway","room_inside"):
282:         $ r13_destination="hall" if r13_choice[1]=="doorway" else "room13"
283:         if r13_destination in r13_places():
284:             $ r13_edit(location=r13_destination)
285:             jump r13_roam
286:         jump r13_field
287:     if r13_choice[1]=="people":
288:         call screen r13_nearby
289:         if _return:
290:             $ r13_target=_return
291:             call r13_talk
292:         jump r13_roam
293:     if r13_choice[1]=="map":
294:         call screen r13_map
295:         if _return and _return in r13_places() and _return!=room13["location"]:
296:             $ r13_edit(location=_return)
297:             jump r13_roam
298:         jump r13_field
299:     jump r13_field
300: 
```

```text
459: label r13_case_choice:
460:     call r13_scene("hall","목요일 저녁 · 여관 2층 복도","night")
461:     call r13_lines([("karo","되돌아온 짐이 마을 바깥 초소에 도착했어요. 확인하러 가실 거죠?"),("daram","할아버지 물건은 내가 받아둘게. 방에서 같이 기다릴게."),(None,"계단 아래에서 할머니가 고개를 끄덕였다. 아이는 자기가 봐 주겠다는 얼굴이었다."),("dad","(짐을 받으러 갈까, 아이 곁에 남을까.)",{"thought":True})],"case:appointment:v4")
462:     menu:
463:         "되돌아온 짐은 미루고 방에서 함께 기다린다":
464:             $ r13_flag("father_accompanied")
465:             jump r13_prevented
466:         "통로에 사람을 세우고 나비에게 동행을 부탁한다" if r13_has("E05") and r13_has("E18"):
467:             $ r13_flag("route_watched")
468:             jump r13_prevented
469:         "까로와 되돌아온 짐을 확인하러 간다":
470:             call r13_lines([("dad","할머니하고 있어. 돌아와서 함께 보자."),("daram","금방 와?"),("dad","받는 대로 올게.")],"case:separate:v4")
471:     call r13_scene("winter","바깥 초소 · 되돌아온 짐","night")
472:     call r13_lines([("karo","봉투 위 날짜를 봐요. 이건 부인이 여기 오기 전에 보냈던 물건 같네요."),(None,"오래된 우체국 날짜 도장이 젖어 있었다. 안에는 우리가 보냈던 장갑과 맡김표가 있었다."),("dad","이걸 받으러 오라고 한 사람은요?"),("karo","전달은 여관에서 했죠. 지금 연락인 줄 알았는데…….")],"case:father:parcel:v3")
473:     $ r13_grant(["E34"],"까로와 바깥 초소에서 되돌아온 짐을 직접 확인")
474:     call r13_scene("hall","여관 2층 · 연기가 새는 문","quiet")
475:     call r13_cinematic("return")
476:     $ source_fx("knock")
477:     call r13_lines([(None,"계단 위에서 나무를 두드리는 소리가 들렸다. 우리 방 문 아래로 연기가 샜다."),("nabi","다람아, 거기 있어. 문에서 떨어져!"),("dad","무슨 일이에요?"),("doto","안의 빗장이 안 풀립니다. 비명 듣고 바로 왔는데."),("dad","다람아!"),("daram","아빠…… 나 여기."),("granny","비켜요. 공구 가져왔어."),(None,"도토가 지렛대를 받아 문틀 틈에 밀어 넣었다. 너울과 함께 문을 받쳤다.")],"case:father:return:v3")
478:     $ source_fx("impact")
479:     $ r13_edit(case_state="occurred",victim_state="dead",location="room13",kitchen_switch=False,passage_open=False)
480:     call r13_scene("room","여관 2층 · 13호 구조 직후","quiet")
481:     call r13_cinematic("rescue")
482:     call r13_lines([(None,"빗장 고정부가 뜯겨 나갔다. 너울이 작은 깔개 위로 젖은 천을 덮었다. 침대는 타지 않았다."),("dad","다람아. 나와도 돼. 아빠가 잡아 줄게."),(None,"침대 아래에서 다람이가 손을 뻗었다. 그 옆 바닥에 어르신이 쓰러져 있었다."),("daram","내가 때렸어."),("dad","어디 다쳤어?"),("daram","아빠, 내가 때렸다고."),(None,"아이의 손목에 눌린 자국이 보였다. 촛대는 바닥에서 두 부분으로 갈라져 있었다.")],"case:discovery:v3")
483:     menu:
484:         "아이를 안고 너울에게 바닥 모습과 물건을 거둔 순서를 남겨 달라고 한다":
485:             call r13_lines([("dad","아이는 제가 데리고 나가겠습니다. 사람부터 살피되 물건을 옮긴 자리는 남겨 주세요."),("neoul","문 앞을 막겠습니다. 도토 씨, 지금 보이는 자국부터 그려 주십시오.")],"case:preserve:v3")
486:             $ r13_flag("floor_preserved")
487:             $ r13_grant(["E33"],"구한 직후 너울·도토가 남긴 방 그림과 봉해 둔 물건")
488:         "아이를 데리고 나와 진료할 사람을 부른다":
489:             call r13_lines([("buri","할아버지! 비켜요!"),("neoul","발밑에 물건이 있습니다."),(None,"사람들이 어르신 곁으로 모였다. 너울이 촛대를 거둬 갔지만 바닥의 자국은 이미 여러 발에 겹쳐졌다.")],"case:unpreserved:v3")
490:     call r13_lines([("resident_seori","숨이 없습니다. 아이 팔도 보겠습니다."),(None,"촛대의 휘어진 장식 고리에 금속 조각이 걸려 있었다. 너울이 그대로 싸서 봉해 두었다."),("daram","내가 놓으라고 했어. 그런데 안 놔서……."),("granny","아이를 잡아당기지 말아요. 얘도 떨잖아."),("neoul","확인할 때까지 초소 보호실에 둡니다."),("dad","아이만요?"),("neoul","아버님은 까로 씨와 밖에 있던 게 확인됐습니다."),("dad","아이를 만나겠습니다. 아이 말은 고치지 말고 그대로 남겨 주세요.")],"case:sealing:v3")
491:     $ r13_grant(["E07","E08","E14"],"구한 직후 봉해 둔 범행 도구와 처음 살핀 진료 기록")
492:     $ r13_flag("family_room_unusable")
493:     $ r13_edit(daram_state="held",period=3,location="inn")
494:     call r13_lines([("nabi","짐은 옆방으로 옮겨둘게요. 오늘부터는 거기서 쉬세요."),(None,"13호 열쇠를 내려놓았다. 다람이가 가져오겠다고 했던 가방만 손에 남았다.")],"case:displaced:v3")
495:     jump r13_roam
496: 
497: label r13_prevented:
498:     call r13_scene("room","13호실","night")
499:     if r13_has("route_watched"):
500:         call r13_lines([(None,"나비에게 아이 곁을 부탁하고, 어르신에게 통로를 알고 있다고 전했다. 문은 열린 채였다."),("resident_owlgp","그럼 여기서 기다리지 맙시다. 아래로 내려가요.")],"case:prevented:watch")
501:     else:
502:         call r13_lines([("resident_owlgp","되돌아온 짐 찾으러 간 줄 알았소."),("dad","그건 내일도 확인할 수 있습니다."),("daram","같이 왔어요. 보여 준다는 거, 이제 봐도 돼요?"),(None,"어르신의 손이 잠깐 떨렸다. 옆에 앉아 기다리자 쥐고 있던 봉투를 놓았다."),("resident_owlgp","아래에서 이야기합시다. 이 방은 답답해.")],"case:prevented:accompany")
503:     call r13_lines([("granny","다 같이 계셨네. 아이하고 있으려고 왔어요. 차라도 내올까요?"),("dad","식당에서 함께 마시겠습니다."),(None,"그날 13호에서는 아무도 죽지 않았다. 누군가의 범행을 막았다는 증거까지 얻은 것은 아니다.")],"case:prevented:result")
504:     $ r13_edit(case_state="prevented",victim_state="protected",daram_state="with_dad",period=3,location="inn")
505:     $ r13_flag("victim_protected")
506:     $ r13_grant(["E17"],"살아 있는 어르신이 간직해 온 베낀 기록")
507:     jump r13_roam
508: 
509: label r13_trial:
510:     if room13["trial_ended"]:
```


## game/room13_route_knowledge.rpy

```text
1: # Knowledge eligibility is captured at NEW GAME, never unlocked mid-run.
2: init 90 python:
3:     def r13_secret_route_available():
4:         return bool((store.room13 or {}).get("secret_route_unlocked", False))
5: 
6:     for _key in ("map", "passage_measure"):
7:         ROOM13["activities"][_key]["secret_route_only"] = True
8:     ROOM13["topics"]["mystery:door"]["secret_route_only"] = True
9:     for _place, _key in (("room13", "books"), ("kitchen", "shelf"), ("workshop", "plans")):
10:         ROOM13["objects"][_place][_key]["secret_route_only"] = True
11:     for _spec in ROOM13["objects"].get("passage", {}).values():
12:         _spec["secret_route_only"] = True
13: 
14:     _r13_route_available = r13_available
15:     def r13_available(spec):
16:         if spec.get("secret_route_only") and not r13_secret_route_available():
17:             return False
18:         return _r13_route_available(spec)
19: 
20:     _r13_route_object_visible = r13_object_visible
21:     def r13_object_visible(spec):
22:         if spec.get("secret_route_only") and not r13_secret_route_available():
23:             return False
24:         return _r13_route_object_visible(spec)
25: 
26:     _r13_route_places = r13_places
27:     def r13_places():
28:         return [p for p in _r13_route_places() if p != "passage" or r13_secret_route_available()]
```


## game/room13_first_mystery.rpy

```text
45:         def __init__(self,stage=0,selected=None,lens=False,**kwargs):
46:             super(R13PlanDrawing,self).__init__(**kwargs)
47:             self.stage=stage;self.selected=selected;self.lens=lens
48:         def render(self,width,height,st,at):
49:             r=renpy.Render(700,360);c=r.canvas()
50:             c.rect("#ede3ca",(0,0,700,360))
51:             for x in range(20,700,20):c.line("#dcd0b7",(x,0),(x,360),1)
52:             for y in range(20,360,20):c.line("#dcd0b7",(0,y),(700,y),1)
53:             if self.stage==0:
54:                 c.rect("#7f735b",(70,95,560,65),4)
55:                 c.rect("#7f735b",(70,215,425,65),4)
56:                 c.line("#8b7661",(70,80),(70,308),3)
57:                 c.line("#8b7661",(630,80),(630,308),3)
58:                 c.line("#8b7661",(495,200),(495,308),3)
59:                 if self.selected=="books":c.rect("#b4853b",(498,218,129,59),4)
60:                 elif self.selected=="window":c.rect("#b4853b",(74,218,100,59),4)
61:                 elif self.selected=="center":c.rect("#b4853b",(240,218,120,59),4)
62:             else:
63:                 # Two floor bands, service void on the right, independent flue.
64:                 c.rect("#7f735b",(45,40,600,265),4)
65:                 c.line("#7f735b",(45,175),(645,175),4)
66:                 c.line("#7f735b",(530,40),(530,305),3)
67:                 c.lines("#777e78",False,[(455,278),(455,68),(300,68)],9)
68:                 c.lines("#a44f3e",False,[(200,272),(579,272),(579,108),(220,108)],5)
69:                 for x,y in ((200,272),(220,108)):
70:                     c.rect("#a44f3e",(x-10,y-10,20,20),3)
71:                     if self.lens:
72:                         c.lines("#563d2b",False,[(x-16,y+18),(x+16,y+18),(x+16,y-18)],4)
73:                 if self.lens:c.rect("#b4853b",(552,84,53,210),3)
74:             return r
75: 
```

```text
103:         if person=="buri" and key=="E04" and bool({"first_plan_read","first_plan_compared"}&old_flags):
104:             if "plan_reviewed_with_buri" in old_flags:return [("buri","표시한 두 끝을 보세요. 한쪽을 풀어도 다른 쪽 문은 직접 밀어야 해요.")]
105:             r13_flag("plan_reviewed_with_buri")
106:             return [("dad","도면에 붉게 덧그린 선은 무엇입니까?"),
107:                 ("buri","배관은 회색이에요. 붉은 건 금속 줄이고요.",{"expression":"neutral"}),
108:                 ("dad","왜 두 층 사이에 금속 줄이 필요합니까?"),
109:                 ("buri","멀리 있는 걸쇠를 당길 때 쓰죠. 실제 장치가 남아 있는지는 직접 봐야 해요.")]
110:         if person=="granny" and key=="E04" and "inn_front_door_claim" in old_flags:
111:             return [("granny","옛 도면까지 구하셨네.",{"expression":"thinking"}),
112:                 ("dad","책장 뒤에 공간이 있습니다. 문은 하나뿐이라고 하셨지요."),
113:                 ("granny","낡은 집은 고친 데가 많아요. 종이하고 지금하고 같겠어요?",{"expression":"neutral"})]
114:         if person=="granny" and key in ("E37","E05") and "inn_front_door_claim" in old_flags:
115:             if "inn_claim_retracted" in old_flags:return [("granny","세탁물을 나르던 문이에요. 아까 말씀드린 대로예요.")]
116:             r13_flag("inn_claim_retracted")
117:             return [("dad","주방 레버를 올리고 책장 손잡이를 움직였습니다. 뒤에 문이 열리더군요."),
118:                 ("granny","……그걸 여셨어요?",{"expression":"distressed"}),
119:                 ("dad","복도 쪽 문밖에 없다고 하셨는데요."),
120:                 ("granny","손님이 쓰는 문 말이에요. 예전에는 세탁물을 그리로 날랐지요.",{"expression":"neutral"}),
121:                 ("dad","아내도 그 길을 썼습니까?"),("granny","그건 못 봤어요."),
122:                 ("dad","그럼 직접 확인하겠습니다.")]
123:         return response
```


## game/systems/room13_debate.rpy

```text
81:             chair="resident_seori",
82:             statements=[
83:                 dict(id="s1",who="granny",text="비명이 들릴 때 나는 【식당에】 있었어요. 다들 봤잖아요.",
84:                     truth=True,
85:                     press=[("granny","나비가 바로 옆에 있었어요. 물어봐요."),("nabi","네. 첫 비명 때는 같이 있었어요.")],
86:                     hint="이 말은 사실이다. 따질 것은 '첫 비명 다음'이다.",
87:                     wrong=("nabi","제가 같이 있던 것까지 없던 일로 만들지는 마세요.")),
88:                 dict(id="s2",who="granny",text="그 뒤로도 나는 【계속 사람들 곁에】 있었어요.",
89:                     accept=["E12","E11"],
90:                     hint="공구를 가지러 주방에 간 뒤로는 아무도 할머니를 보지 못했다.",
91:                     broken=[("nabi","공구를 가지러 주방에 가신 뒤로는…… 저도 못 봤어요."),
92:                         ("granny","잠깐 안 보였다는 게 전부잖아요.")],
93:                     wrong=("granny","그게 내가 혼자 있었다는 증거예요?")),
94:                 dict(id="s3",who="granny",text="주방에서 그 방까지는 【한참 걸려요】. 그 잠깐에 다녀올 수는 없어요.",
95:                     accept=["E05","E37"],
96:                     hint="주방과 13호 책장은 통로로 바로 이어져 있다.",
97:                     broken=[("dad","주방에서 레버를 올리면 13호 책장 뒤로 바로 이어집니다. 복도를 돌아갈 필요가 없습니다."),
98:                         ("granny","……그 길은 세탁물을 나르던 길이에요.")],
99:                     wrong=("granny","그게 주방에서 그 방까지 가까웠다는 거예요?")),
100:             ],
101:             conclusion=dict(prompt="할머니의 그날 움직임을 어떻게 정리할까?",
102:                 options=[
103:                     ("correct","첫 비명 때 식당에 있었던 건 맞다. 하지만 주방에 간 뒤로는 아무도 못 봤고, 주방에서 그 방까지 바로 가는 길이 있다."),
104:                     ("over","그 시간에 할머니가 13호실에 가서 어르신을 죽였다."),
105:                     ("weak","나비는 할머니 편이니 그 말은 믿을 수 없다."),
106:                 ],
107:                 correct=[("resident_seori","첫 비명 때 식당에 있었다는 건 사실입니다. 하지만 그 뒤 시간까지 설명해 주지는 않습니다."),
108:                     ("resident_seori","할머니가 그 방에 실제로 들어갔는지는 이어서 보겠습니다.")],
109:                 over=("resident_seori","갈 수 있었다는 것과 갔다는 것은 다릅니다. 그건 아직 보여 주지 않았습니다."),
110:                 weak=("nabi","저는 본 것만 말했어요. 편을 든 게 아니에요.")),
```

```text
113:         "C4":dict(title="들어갔다 해도 도우려 했을 뿐이다",
114:             chair="resident_seori",
115:             statements=[
116:                 dict(id="s1",who="granny",text="그 핀은 【오후에 그분을 도울 때】 떨어졌을 수도 있잖아요.",
117:                     accept=["E15"],
118:                     soft={"E13":("resident_seori","그날 새 핀으로 바꿨다는 건 알겠습니다. 언제까지 할머니 옷에 있었는지가 궁금합니다.")},
119:                     hint="첫 비명 직후, 나비가 그 핀을 할머니 목도리에 직접 여며 주었다.",
120:                     broken=[("nabi","첫 비명 바로 뒤에 제가 그 핀을 여며 드렸어요. 그때는 목도리에 있었어요."),
121:                         ("granny","……그래서요?")],
122:                     wrong=("granny","그게 오후에 떨어진 게 아니라는 증거예요?")),
123:                 dict(id="s2",who="granny",text="구하려고 들어갔다가 【촛대를 주웠을 뿐】이에요.",
124:                     accept=["E14","E35"],
125:                     soft={"E33":("resident_seori","구한 직후 누가 촛대를 거뒀는지는 확인됩니다. 그 전에 무슨 일이 있었는지가 문제입니다.")},
126:                     hint="핀은 촛대 장식 고리 안에, 내려친 방향으로 눌려 끼어 있었다.",
127:                     broken=[("dad","핀은 촛대 장식 고리 안에 끼어 있었습니다. 고리는 내려친 방향으로 찌그러졌고, 핀도 같이 휘었습니다."),
128:                         ("dad","주워 들다가 들어간 게 아닙니다. 내려친 순간에 끼어 들어간 겁니다.")],
129:                     wrong=("granny","그걸로 내가 촛대를 휘둘렀다는 거예요?")),
130:                 dict(id="s3",who="granny",text="그분이 그렇게 위험한 줄은 【몰랐어요】.",
131:                     accept=["E36"],
132:                     hint="전날 저녁, 할머니가 직접 쓴 진료 요청이 있다.",
133:                     broken=[("resident_seori","전날 저녁 할머니가 직접 적어 보낸 쪽지입니다. 발작이 심하다고, 그리고 제가 '혼자 두지 마라'고 답했습니다."),
134:                         ("granny","……….")],
135:                     wrong=("granny","그게 내가 알았다는 증거예요?")),
136:             ],
137:             conclusion=dict(prompt="핀과 촛대로 무엇을 말할까?",
138:                 options=[
139:                     ("correct","첫 비명 뒤에도 핀은 할머니 옷에 있었다. 그 핀이 내려친 방향으로 눌린 고리에 끼었다. 구하다 주운 게 아니라 내려친 것이다."),
140:                     ("over","할머니는 처음부터 우리 가족을 노리고 이 모든 걸 꾸몄다."),
141:                     ("weak","할머니가 그 방에 들어간 적이 있다는 것까지만 말할 수 있다."),
142:                 ],
143:                 correct=[("resident_seori","위험을 알면서 둘만 남겼고, 촛대에 할머니의 핀이 내려친 방향으로 끼어 있습니다. 구하려다 생긴 흔적이라는 말은 받아들일 수 없습니다."),
144:                     ("resident_seori","대답하지 않으셔도, 내놓은 자료로 판단하겠습니다.")],
145:                 over=("resident_seori","오늘은 그날 그 방에서 있었던 일만 따집니다. 가족을 부른 이유는 따로 보여 주셔야 합니다."),
146:                 weak=("dad","(아니다. 거기서 멈추면 '도우려 했다'는 말이 그대로 남는다.)")),
147:             sway=["buri","resident_bori","resident_kongi"]),
148: 
149:         "F1":dict(title="저 사람들은 돌아올 수 없다",
150:             chair="resident_seori",
151:             statements=[
```


## game/room13_life.rpy

```text
97:             return Transform(r13_art_path("altar"),size=(1280,720),nearest=True)
98:         if key=="hall":
99:             after=store.room13 and store.room13["case_state"]=="occurred"
100:             return Transform(r13_art_path("hall-after" if after else "hall-before"),size=(1280,720),nearest=True)
101:         if key in ("front","kitchen","winter_passage","council"):
102:             index={"front":0,"kitchen":1,"winter_passage":2,"council":3}[key]
103:             return r13_atlas(r13_art_path("inn"),index,2,2)
104:         if key in ("winter_square","winter_post","winter_workshop"):
105:             index=("winter_square","winter_post","winter_workshop").index(key)
106:             return r13_atlas(r13_art_path("village"),index,2,2)
107:         if key=="guestroom":
108:             return Transform(r13_art_path("room-before"),size=(1280,720),nearest=True)
109:         if key=="room":
110:             after=store.room13 and store.room13["case_state"]=="occurred"
111:             return Transform(r13_art_path("room-after" if after else "room-before"),size=(1280,720),nearest=True)
112:         if key.startswith("r13_"):
113:             index=("clinic","school","store","greenhouse","facility","altar").index(key[4:])
```


## game/room13_rules.rpy

```text
65: 
66:     def r13_new():
67:         return dict(campaign_id="room13_v1",version=3,story_revision=ROOM13["story_revision"],day=1,period=0,location="gate",
68:             kitchen_switch=False,passage_open=False,secret_route_unlocked=bool(persistent.room13_endings),
69:             case_state="pending",victim_state="alive",daram_state="with_dad",
70:             granny_state="trusted",trial_result="pending",evidence=[],records={},
71:             flags=[],read_topics=[],done=[],checks={},encounters=[],resident_knowledge={},
72:             propositions=[],arguments={},log=[],trial_ended=False)
```

```text
200:     def r13_places():
201:         result=["gate","square","post","inn","workshop"]
202:         if r13_has("lodging"):result += ["dining","kitchen","hall","room13","clinic","school","store"]
203:         if r13_has("lodging") and (r13_has("family_room_unusable") or store.room13["case_state"]=="occurred"):result.append("guestroom")
204:         if store.room13.get("passage_open"):result.append("passage")
205:         if store.room13["day"]>=8:
206:             result += ["facility"]
207:             if r13_has("E19"):result.append("greenhouse")
208:         return result
209: 
210:     def r13_where(person):
```
