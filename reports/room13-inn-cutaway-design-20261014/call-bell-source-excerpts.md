# 호출종 검토 추가 원문 · main505cf884


## game/room13.rpy

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
```
```text
615: label r13_prevention_hearing:
616:     call r13_lines([("seryeon","아이가 함께 들어왔다는 기록과, 따로 맡아 달라는 요청을 확인하겠습니다."),("resident_owlgp","아이는 나와 함께 있었소. 죽은 사람도, 아이가 저지른 살인도 없소. 없는 사건을 만들지는 맙시다."),("granny","낯선 아이를 따로 보호하자는 뜻이었어요."),("dad","보호자는 여기 있습니다. 입구에서 함께 등록한 원본도 있고요.")],"prevention:hearing")
617:     menu:
618:         "바로잡은 입장 기록 원본을 직접 보여 준다":
619:             call screen r13_book("resident_seori",present=True,hearing=True)
620:             if _return=="E02":
621:                 call r13_lines([("resident_seori","아빠와 딸이 함께 들어왔다는 기록은 그대로 인정됩니다. 따로 떼어 놓으라는 요청은 이유가 없다고 봅니다.")],"prevention:registered")
622:             else:
623:                 call r13_lines([("resident_owlgp","초소 원본을 여기서 직접 맞춰 봅시다. 아이를 떼어 놓고 볼 일이 아니오."),(None,"초소 담당자를 불러 원본을 확인했다. 그동안 부녀는 함께 기다렸다.")],"prevention:independent_check")
624:         "어르신과 함께 사람들 앞에서 맞춰 보자고 한다":
625:             call r13_lines([("resident_owlgp","내가 같이 있었소. 원본과 확인한 사람을 함께 부르시오."),("resident_seori","사람들 앞에서 맞춰 보기 전까지 가족을 떼어 놓지 마십시오.")],"prevention:witness")
626:     $ r13_edit(trial_result="prevention_hearing",trial_ended=True,daram_state="with_dad",period=3)
627:     jump r13_week2_opening
```

## game/room13_week2_rules.rpy

```text
238:         if all(r13_has(k) for k in ("maintenance_support","operators_ready","E28")):result.append("maintenance")
239:         return result
240: 
241:     def r13_true_ending_ready():
242:         s=store.room13
243:         first=s.get("observations",{}).get("first",{})
244:         second=s.get("observations",{}).get("second",{})
245:         return ("F4" in s["propositions"] and r13_has("mother_original_safe")
246:             and (r13_has("bami_protected") or r13_has("witness_protected"))
247:             and bool(first and second and first["time"]<second["time"] and first["load"]!=second["load"])
248:             and ("C4" in s["propositions"] or r13_has("premeditation_prevented_proven")))
249: 
250:     def r13_resolve_ending():
251:         s=store.room13
252:         if s["daram_state"]=="lost":return "E1"
253:         if "F2" not in s["propositions"]:return "E3"
254:         if not (r13_survival_ready() and "F1" in s["propositions"] and "F3" in s["propositions"]):return "E4"
255:         return "E6" if r13_true_ending_ready() else "E5"
256: 
257:     def r13_finish_ending(key):
```

## game/systems/room13_first_day_flow.rpy

```text
18:     _r13_firstday_places=r13_places
19:     def r13_places():
20:         if store.room13.get("life_poc") and store.room13.get("day")==1:
21:             if not r13_has("entry_corrected"):return ["gate"]
22:             return ["gate","square","inn","hall","room13"] if r13_has("lodging") else ["gate","square","inn"]
23:         return _r13_firstday_places()
24:     _r13_firstday_connections=r13_local_connections
25:     def r13_local_connections():
26:         if store.room13.get("life_poc") and store.room13.get("day")==1:
27:             if store.room13.get("location")=="gate":return [("square","광장으로"),("inn","여관으로")]
28:             if store.room13.get("location")=="square":return [("inn","여관으로"),("gate","마을 입구로")]
29:         return _r13_firstday_connections()
```
```text
91:     _r13_firstday_topic_lines=r13_conversation_topic_lines
92:     def r13_conversation_topic_lines(key):
93:         if store.room13.get("life_poc") and key=="granny_letter":
94:             return [("dad","소식이 끊겨서 저희에게 편지를 보내셨다고요?"),("granny","네. 물건도 두고 갔는데 돌아오지 않아서요."),("dad","마지막으로 누굴 만났는지 알아보겠습니다.")]
95:         if store.room13.get("life_poc") and key=="register":
96:             if store.room13.get("day",1)>1:
97:                 return [("granny","13호실 그대로 쓰세요. 숙식은 하루 열 냥이고, 모자라면 적어 둘게요.")]
98:             return [("dad","편지를 받고 왔습니다. 아내가 머물던 방을 볼 수 있습니까?"),("granny","13호실을 쓰세요. 두고 간 물건도 그대로예요."),("daram","엄마는 지금 어디 있어요?"),("granny","아직 돌아오지 않았어요. 그래서 가족께 소식을 전해야겠다고 생각했어요."),("dad","방부터 살펴보고, 마지막 소식도 여쭤보겠습니다."),("granny","오늘 식사와 방값은 받지 않을게요. 내일부터 두 분 숙식은 하루 열 냥이에요."),("daram","아빠, 엄마가 남긴 것도 찾아보자.")]
99:         return _r13_firstday_topic_lines(key)
100:     _r13_firstday_topics=r13_topics
101:     def r13_topics(person):
```