# 에피소드 ⑤ 「긴 밤과 겨울 수프」 (11~12일). 대본: docs/EPISODE5_SCRIPT.md
#   다 죽을 것 같아서, 사랑하는 아이들을 먼저 재웠다. 구원은 몇 시간 늦게 왔다.
#   대본의 10~12일을 게임의 11~12일(둘째 주 첫 이틀)에 맞춰 줄였다.
#   11일: 숲 뿌리 밑(여기는 들켰다 + 초록 유리 조각) → 폐온실 길의 토실 → 폐온실에서 엄마와 재회.
#         아랫길의 네로(식어 가는 돌을 보여 준다) + 사자 선생님(네로의 이름표를 보여 준다) → 천막 사람들이 학교로.
#   11일 밤: 긴 밤. 아랫길 천막에서 사람들이 언다(앞에서 한 일만큼 덜 죽는다).
#   12일: 엄마와 옛 시설(데워지는 조각, 실험 기록, 벽의 옛 편지, 죽은 사람 명단 원본).
#         서리가 약장을 잠근다(①에서 서리를 믿었다면). 사자 선생님을 설득한다(작은 회의 Q5A).
#   12일 저녁: 수프. 12일 밤: 대피소 회의 Q5(아이가 죽었다면) → 결정 → 선생님이 남은 수프를 마시려 한다.
#   기존 둘째 주 장치와의 관계: 재회는 이 파일이 맡는다(mom_reunited, E30). 옛 '연락 신호를 따라 만난다'는 그 뒤 열리지 않는다.
#   깃발 접두사 ws_, 장면 r13_ws_*.
init 156 python:
    for _key,_name,_est,_not in (
        ("Y02","「여기는 들켰다」 쪽지","숲 뿌리 밑 은신처에 남은 엄마 글씨. 그래서 무슨 뜻? 누가 이 굴을 찾아냈고, 엄마는 더 깊은 데로 옮겼다.",""),
        ("Y03","초록 유리 조각","숲 뿌리 밑 재 옆의 초록 유리. 숲에서 이런 유리를 쓰는 곳은 무너진 폐온실뿐이다. 그래서 무슨 뜻? 엄마는 폐온실로 갔다.",""),
        ("Y04","토실의 말","토실: \"할머니가 아저씨 따라가 보라고 했어. ……할머니가 우리 엄마도 보호소에 보냈어.\" 그래서 무슨 뜻? 할머니가 아직 엄마를 쫓고 있다.",""),
        ("Y05","죽은 사람 명단 원본","옛 시설 돌 선반의 할머니 글씨 장부. 겉장은 '보호소', 안은 죽은 사람 칸. 아직 살아 있는 사람 이름 옆에도 '이송'. 그래서 무슨 뜻? 보호소에 간 사람은 죽는다.",""),
        ("Y06","데워지는 조각","조각 셋을 손바닥에 모으자 점점 따뜻해졌다. 그래서 무슨 뜻? 나눠 둔 온기를 모으면 돌이 다시 데워진다.",""),
        ("Y07","옛 시설 실험 기록","엄마와 굴돌 할아버지가 밤새 지켜본 종이. 한밤에도 새벽에도 따뜻함, 줄어들지 않음. 그래서 무슨 뜻? 엄마의 방법은 진짜로 된다.",""),
        ("Y08","벽의 옛 편지","옛 시설 벽의 글자. \"돌은 하나가 아니었다. 나눠서 데웠다.\" 그래서 무슨 뜻? 옛날엔 사람을 바치지 않았다.",""),
        ("Y09","네로의 이름표 꾸러미","아랫길 천막 사람들 이름이 하나씩 삐뚤하게 바느질된 천 조각들. 그래서 무슨 뜻? 이름 없이 죽은 사람은 없다.",""),
        ("Y10","대피 명단","학교 게시판. 표 없는 아이 셋 이름에 줄이 그어지고 옆에 너울 글씨로 '수레'. 그래서 무슨 뜻? 선생님이 겁낸 이유다.",""),
        ("Y11","아이 그릇만","어른 냄비 수프를 먹은 사람은 다 멀쩡하다. 그래서 무슨 뜻? 아이 냄비에만 무언가 들었다.",""),
        ("Y12","약장의 빈 자리","진료소 약장에서 '잠드는 약 — 한 방울만' 병이 사라졌다. 출입 명단에 '사자 — 아이 기침약'. 그래서 무슨 뜻? 선생님이 그날 약장 앞에 있었다.",""),
        ("Y13","새미의 말","새미: \"쓴맛이 나서 남겼어. 선생님은 안 먹고 젓기만 했어.\" 선생님만 빨간 그릇, 안에는 큰 냄비 건더기. 그래서 무슨 뜻? 선생님은 아이 냄비를 먹지 않았다.",""),
        ("Y14","밝아진 등","12일 밤, 광장 등이 전부 밝아졌다. 그래서 무슨 뜻? '어차피 다 죽었을 것'은 틀렸다.",""),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind="기록",establishes=_est,does_not_establish=_not or "이것만으로 다른 사실까지 정할 수는 없다.",scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(Y02="여기는 들켰다",Y03="초록 유리",Y04="토실의 말",Y05="죽은 사람 명단",Y06="데워지는 조각",Y07="실험 기록",Y08="벽의 옛 편지",
        Y09="이름표 꾸러미",Y10="대피 명단",Y11="아이 그릇만",Y12="약장의 빈 자리",Y13="새미의 말",Y14="밝아진 등")
    for _k,_n in (("kid_dodam","도담"),("kid_saemi","새미")):
        R13_NAMES[_k]=_n
        R13_CHARS[_k]=Character(_n)

    # 숲 뿌리 밑: 기존 은신처 장면 뒤에 초록 유리 조각을 더한다.
    ROOM13["objects"]["forest"]["forest_roots"]["call_label"]="r13_ws_roots"
    # 폐온실은 엄마의 신호(E19)나 초록 유리 조각으로 찾는다.
    _r13_ws_places=r13_places
    def r13_places():
        result=_r13_ws_places()
        if store.room13["day"]>=R13_WEEK2_DAY and r13_has("Y03") and "greenhouse" not in result:
            result.append("greenhouse")
        return result

    def r13_ws_daram():
        return (store.room13 or {}).get("daram_state") in ("with_dad","rescued")

    def r13_ws_victims():
        names=["kid_kkam","kid_mong","kid_bang","kid_dodam"]
        if r13_has("wf_kkomi_alive"):names=["kid_kkomi"]+names
        return names

    # ---- 작은 회의 Q5A: 사자 선생님 설득 (12일 오후, 학교) ----
    R13_DEBATE_SEATS["ep5a"]=["resident_teacher","mom","resident_seori"]
    R13_DEBATE_STANCE["ep5a"]=("다 죽는다고 믿는다","모르겠다","기다려 본다")
    R13_EP_MEETING_PLACE["ep5a"]="r13_school"
    R13_EP_MEETING_HEADER["ep5a"]="학교 교실 · 12일째"
    R13_DEBATE["Q5A"]=dict(title="오늘 밤, 아이들은 버틸 수 있나",session="ep5a",chair="mom",
        statements=[
            dict(id="s1",who="resident_teacher",text="돌은 식고 있어요. 【오늘 밤도, 내일 밤도】 그럴 겁니다. 아이들은 못 버팁니다.",
                accept=["Y06"],
                broken_by={"Y06":[(None,"엄마가 조각 셋을 선생님 손바닥에 모아 올렸다."),("mom","가만히 계셔 보세요."),(None,"숨 몇 번 사이에 초록빛이 짙어졌다."),("resident_teacher","……따뜻해지네요. 이게, 왜…….")]},
                hint="모으면 따뜻해지는 것.",
                wrong=("resident_teacher","다 알고 있어요. 그래서 그러는 거예요.")),
            dict(id="s2",who="resident_teacher",text="한 번 따뜻해졌다가 【다시 식겠지요】. 그런 방법이 있었다면 왜 지금까지 아무도 몰랐습니까.",
                accept=["Y07","Y08"],
                broken_by={"Y07":[("dad","밤새 지켜봤습니다. 한밤에도, 새벽에도 식지 않았어요."),("resident_teacher","…….")],
                    "Y08":[("dad","옛 시설 벽에 이렇게 적혀 있었습니다. '나눠서 데웠다.' 옛날엔 사람을 바치지 않았답니다."),("resident_teacher","…….")]},
                hint="밤새 지켜본 것, 또는 옛사람들이 남긴 말.",
                wrong=("resident_teacher","다 알고 있어요. 그래서 그러는 거예요.")),
        ],
        conclusion=dict(prompt="선생님께 무엇을 부탁할까?",
            options=[("correct","오늘 밤 돌이 데워진다. 하루만 기다려 달라"),
                ("over","선생님이 아이들을 해치려 한다"),
                ("weak","아이들을 잘 돌봐 달라")],
            correct=[("resident_teacher","……오늘 밤, 정말로 데워집니까."),("mom","저녁 먹을 때쯤이면 광장 등이 밝아질 거예요. 제가 약속해요."),
                ("resident_teacher","약속…… 저도 아이들에게 약속을 했었는데."),("dad","수레는 제가 막겠습니다. 명단에서 줄 그은 이름, 다시 살려 놓겠습니다."),
                ("resident_teacher","(눈을 감는다) ……하루만. 하루만 기다려 보지요.")],
            over=("resident_teacher","제가요? ……저는 이 아이들 이름을 틀린 적이 없어요."),
            weak=("resident_teacher","고맙습니다. 걱정 마세요.")),
        sway=["resident_teacher"])

    # ---- 회의 Q5: 대피소의 수프 (12일 밤, 학교) ----
    R13_DEBATE_SEATS["ep5"]=["resident_bori","resident_madam","resident_seori","resident_teacher","neoul","mom"]
    R13_DEBATE_STANCE["ep5"]=("감자 탓","모르겠다","냄비를 의심")
    R13_EP_MEETING_PLACE["ep5"]="r13_school"
    R13_EP_MEETING_HEADER["ep5"]="학교 대피소 회의 · 12일째"
    R13_DEBATE["Q5"]=dict(title="아이 냄비에 약을 넣은 사람",session="ep5",chair="neoul",
        statements=[
            dict(id="s1",who="resident_bori",text="백 부인이 댄 감자가 【상했던 거요】. 싸구려를 넘겼겠지.",
                accept=["Y11"],
                broken_by={"Y11":[("dad","어른들도 같은 감자를 먹었습니다. 큰 냄비에서요. 여기 있는 누구도 아프지 않습니다. 아이들 냄비만입니다."),("resident_madam","……거봐요. 저는 아니에요.")]},
                hint="어른 냄비와 아이 냄비.",
                wrong=("resident_bori","그게 뭐.")),
            dict(id="s2",who="resident_madam",text="그럼 약을 다루는 【서리 선생】이죠. 진료소 약이 아니면 뭐겠어요.",
                accept=["Y12"],
                broken_by={"Y12":[("resident_seori","약장에서 잠드는 약이 한 병 없어졌습니다. 오늘 낮 진료소에 온 사람은 넷. 그중 한 분이 '아이 기침약'을 찾으셨습니다."),
                    (None,"서리가 출입 명단을 폈다. 사자 선생님의 이름. 사람들이 웅성거렸다.")]},
                hint="그날 진료소 약장 앞에 있던 사람.",
                wrong=("resident_madam","그게 서리 선생이 아니라는 증거예요?")),
            dict(id="s3",who="resident_teacher",text="기침약을 가지러 간 건 맞습니다. 하지만 저는 【아이들과 같은 냄비에서】 먹었어요.",
                accept=["Y13"],
                broken_by={"Y13":[("kid_saemi","쓴맛이 나서 반만 먹고 남겼어요. 배고픈 날 먹으려고. ……선생님은 안 먹었어요. 젓기만 했어요."),
                    ("dad","아이들은 다 하얀 그릇입니다. 선생님만 빨간 그릇. 안에 남은 건 큰 냄비의 건더기입니다.")]},
                hint="수프를 남긴 아이.",
                wrong=("resident_teacher","……")),
            dict(id="s4",who="resident_teacher",text="……설령 제가 그랬다 해도, 【어차피 다 죽었을 거요】.",
                accept=["Y14"],
                broken_by={"Y14":[("resident_teacher","어젯밤 보셨잖아요. 아랫길 사람들이 서로 기대 앉은 채로 얼었어요."),
                    ("resident_teacher","대피 명단에서 이 아이들 이름에 줄이 그어졌어요. 옆에 '수레'라고. 보호소에 간 사람은 돌아오지 않아요."),
                    ("resident_teacher","추운 수레에 묶여서, 무서워하면서 가게 할 수는 없었어요. 내 반 아이들을."),
                    ("resident_teacher","그래서 따뜻할 때. 배부를 때. 노래 부를 때. 아프지 않게."),
                    (None,"다람이 창가로 가서 까치발을 하고 창문을 열었다."),
                    ("daram","(작게) ……선생님. 저거 봐."),
                    (None,"광장의 등이 전부 밝아져 있었다. 대피소 창으로 초록빛 온기가 들어왔다. 교실이 처음으로 따뜻했다."),
                    ("mom","오늘 밤부터 데워져요. 아이들은…… 안 죽어도 됐어요."),
                    (None,"선생님이 아이들 머리맡에 주저앉았다. 출석부를 품에 안았다."),
                    ("resident_teacher","……하나도, 안 틀렸는데."),
                    ("resident_bori","몇 시간이야. 몇 시간만 기다렸으면.")]},
                hint="창밖.",
                wrong=("resident_teacher","어차피, 다 죽었을 거요.")),
        ],
        conclusion=dict(prompt="이 일을 어떻게 정리할까?",
            options=[("correct","약을 넣은 건 선생님이다. 아이들이 얼거나 수레에 실려 갈 거라 믿었다"),
                ("over","선생님이 아이들을 미워했다"),
                ("weak","약을 잘못 둔 서리 탓이다")],
            correct=[("neoul","선생은 내가 데려가오. 수레 명단에 올리면 그만이오."),("mom","(아빠를 본다) ……여기 사람들이 수레가 어디로 가는지 알아야 해.")],
            over=("kid_saemi","아니야! 선생님은 우리 이름 다 알아!"),
            weak=("resident_seori","약장 문을 연 손은 제 손이 아닙니다.")),
        sway=["resident_bori","resident_seori","resident_madam"])

    R13_EVENT_OFFERS.update({
        "r13_ws_lowroad":("아랫길 천막 사이에 작은 불 하나. 네로가 불을 지킨다",[],""),
        "r13_ws_teacher_talk":("교실에서 사자 선생님이 출석부의 이름을 하나씩 짚고 있다",[],""),
    })
    R13_OFFER_ACTORS.update({"r13_ws_lowroad":("resident_nero",None),"r13_ws_teacher_talk":("resident_teacher",None)})

# =========================================================
# 장면
# =========================================================
label r13_ws_events:
    $ _wsd,_wsp,_wsloc=room13["day"],room13["period"],room13["location"]
    if _wsd<R13_WEEK2_DAY:
        return
    if _wsd==R13_WEEK2_DAY and _wsloc=="greenhouse" and r13_has("Y03") and not r13_has("mom_reunited"):
        call r13_ws_greenhouse
    if _wsd==R13_WEEK2_DAY and _wsp<=1 and _wsloc=="river" and not r13_has("ws_lowroad"):
        $ r13_offer("r13_ws_lowroad")
    if _wsd==R13_WEEK2_DAY+1 and not r13_has("ws_long_night"):
        call r13_ws_long_night
        return
    if _wsd==R13_WEEK2_DAY+1 and not r13_has("ws_lab") and r13_has("mom_reunited"):
        call r13_ws_lab
    if _wsd==R13_WEEK2_DAY+1 and r13_has("seori_trust") and not r13_has("ws_cabinet_locked"):
        $ r13_flag("ws_cabinet_locked")
        call r13_lines([("resident_seori","긴 밤 뒤라 진료소가 어수선합니다. 약장에 새 자물쇠를 달았습니다. 열쇠는 제 목에만 있습니다."),
            ("resident_seori","요즘 사람들이 '편하게 보내는 법'을 묻습니다. 저는 대답하지 않았습니다.")],"ws:seori:lock")
    if _wsd==R13_WEEK2_DAY+1 and _wsp<=1 and _wsloc=="school" and not r13_has("ws_teacher_talked"):
        $ r13_offer("r13_ws_teacher_talk")
    if _wsd==R13_WEEK2_DAY+1 and _wsp>=2 and not r13_has("ws_soup"):
        call r13_ws_soup
    return

label r13_ws_roots:
    call r13_mom_hideout
    if room13["day"]>=R13_WEEK2_DAY and r13_has("mom_hideout_found") and not r13_has("Y03"):
        $ r13_grant(["Y02"],"숲 뿌리 밑에 남은 엄마의 쪽지")
        call r13_lines([(None,"재 옆에 초록빛 유리 조각. 손가락 마디만 하다. 한쪽 면에 오래된 흙이 말라붙어 있다."),
            ("dad","(숲에서 이런 유리를 쓰는 곳은 하나다. 무너진 폐온실.)",{"thought":True})],"ws:roots:glass")
        $ r13_grant(["Y03"],"숲 뿌리 밑 재 옆에서 주운 초록 유리")
        if r13_ws_daram():
            call r13_lines([(None,"담요 안쪽에 크레용 그림이 접혀 있었다. 삐뚤빼뚤한 다람쥐 셋."),
                ("daram","이거 내가 그린 거야! 엄마 가방에 넣어 줬던 거!"),
                ("daram","……엄마가 이거 가지고 있었구나. 버린 게 아니구나.")],"ws:roots:drawing")
    return

label r13_ws_greenhouse:
    call r13_scene("r13_forest","폐온실 가는 숲길","quiet")
    if not r13_has("ws_tosil_met"):
        $ r13_flag("ws_tosil_met")
        call r13_lines([(None,"폐온실로 가는 숲길. 눈 밟는 소리가 하나 더 있었다. 멈추면 그것도 멈췄다."),
            ("dad","거기 누구야. 나와."),
            (None,"나무 뒤에서 작은 아이가 나왔다. 털모자를 눈썹까지 눌러쓴 토실이었다."),
            ("resident_tosil","……미안해. 할머니가…… 아저씨 따라가 보라고 했어. 어디 가는지만 보고 오라고."),
            ("resident_tosil","할머니가 무서워. 할머니 눈이 요즘 이상해."),
            ("resident_tosil","……근데, 그거 알아? 할머니가 우리 엄마도 보호소에 보냈어. 나 문 뒤에서 들었어."),
            ("resident_tosil","우리 엄마는 안 돌아왔어.")],"ws:tosil")
        $ r13_grant(["Y04"],"폐온실 길에서 토실에게 들은 말")
        menu:
            "“우리랑 같이 가자.”":
                call r13_lines([(None,"토실이 내 소매를 잡았다.")],"ws:tosil:keep")
                $ r13_flag("ws_tosil_kept")
            "여관으로 돌려보낸다":
                call r13_lines([("resident_tosil","……응.")],"ws:tosil:send")
                $ r13_flag("ws_tosil_sent","granny_knows_greenhouse")
    call r13_scene("r13_greenhouse","폐온실","quiet")
    call r13_lines([(None,"유리 지붕이 반쯤 내려앉은 온실. 마른 덩굴 사이로 빛이 초록색으로 새었다."),
        (None,"바닥 판자 하나가 들려 있었다. 누군가 사다리를 올라왔다. 목도리에 반쯤 가린 얼굴. 코를 찡그렸다. 눈부셔서.")],"ws:reunion:open")
    if r13_ws_daram():
        call r13_lines([("daram","……엄마."),
            (None,"다람이 달렸다. 눈 위에서 한 번 미끄러지고, 그대로 엄마 품으로."),
            ("mom","다람아…… 다람아. 많이 컸네. 이렇게 컸어."),
            ("daram","엄마 왜 안 왔어! 왜 편지만 썼어! 나 엄청, 엄청 기다렸어!"),
            ("mom","응. 미안해. 엄마가 미안해. 엄마가 오면 너희가 위험할까 봐……."),
            ("daram","그래도 왔어야지!"),
            ("mom","……응. 그래도 왔어야 했어.")]+
            ([("daram","엄마, 나 탐정단 단장이야. 진짜야. 도토리도 나눠 줬어."),("mom","우리 다람이가?")] if r13_has("kids_club") else []),"ws:reunion:daram")
    else:
        call r13_lines([("mom","다람은?"),("dad","아직 보호실에. 내가 못 꺼냈어."),("mom","……그럼 오늘 밤 창문으로 가자. 얼굴만이라도.")],"ws:reunion:held")
    call r13_lines([(None,"……"),
        ("mom","당신도. 미안해. 그 편지, 내가 쓴 게 아니야."),
        ("dad","알아. 할머니였어.")]+
        ([("mom","네가 토실이구나. ……아줌마가 네 엄마 이름, 꼭 찾아 줄게.")] if r13_has("ws_tosil_kept") else [])+
        [("mom","연구 원본은 여기 있어. 내일 옛 시설에 같이 가. 사람을 바치지 않아도 되는 길이 있어.")],"ws:reunion:close")
    $ r13_flag("mom_reunited","ws_reunited")
    $ r13_edit(mom_state="reunited",reply_due=None)
    $ r13_grant(["E30"],"엄마가 보관한 연구 원본 직접 확인")
    $ r13_tick()
    return

label r13_ws_lowroad:
    $ r13_flag("ws_lowroad")
    call r13_scene("r13_river","아랫길 · 천막들","quiet")
    call r13_lines([(None,"아랫길. 등록 안 된 사람들의 천막 여섯 채. 천막 사이에 작은 불 하나."),
        ("resident_nero","오늘 밤이 춥다고? 매일 춥다. 우리는 늘 여기서 버텼다."),
        ("resident_nero","학교는 표 있는 사람 데다. 우리 같은 건 문 앞에서 돌려보낸다.")]+
        ([("resident_nero","……탐정단 꼬마구나. 이름표는 아직 있냐."),("daram","응. 안 잃어버렸어.")] if r13_has("K08") and r13_ws_daram() else []),"ws:nero")
    menu:
        "식어 가는 돌을 보여 준다" if r13_has("W4"):
            call r13_lines([("dad","진료소에서 잰 숫자입니다. 돌이 밤마다 더 식고 있어요. 오늘 밤이 제일 낮습니다."),
                ("resident_nero","…… 어젯밤에 영감 하나가 손가락을 못 폈다. 그게 그거였군."),
                ("resident_nero","알았다. 근데 걷지 못하는 사람도 있다. 그리고 문이 안 열리면 끝이다.")],"ws:nero:moved")
            $ r13_flag("ws_nero_moved")
        "말로 설득한다":
            call r13_lines([("resident_nero","말은 공짜다.")],"ws:nero:no")
    if r13_has("ws_nero_moved"):
        call r13_scene("r13_school","학교 교실","quiet")
        call r13_lines([("resident_teacher","아랫길 분들을요? ……명단에 없는 분들은 촌장님 허락이 있어야 합니다.")],"ws:teacher:nero")
        menu:
            "네로의 이름표를 보여 준다" if r13_has("K08"):
                call r13_lines([("dad","아랫길 사람들은 서로 이름표를 만들어 줍니다. 이름 없는 사람은 없어요."),
                    ("resident_teacher","(천 조각을 오래 들여다본다) ……이름이 있으면, 우리 반이지요."),
                    ("resident_teacher","들어오세요. 뒷문으로. 아이들 교실 옆이 비어 있어요.")],"ws:teacher:open")
                $ r13_flag("ws_tents_school")
            "부탁만 한다":
                call r13_lines([("resident_teacher","죄송합니다. 오늘 밤은 아이들 자리도 모자라요.")],"ws:teacher:closed")
    $ r13_tick()
    return

label r13_ws_long_night:
    $ r13_flag("ws_long_night")
    call r13_scene("r13_school","11일 밤 · 긴 밤","night")
    call r13_lines([(None,"해가 지자마자 추위가 내려앉았다. 광장 등이 하나, 또 하나 흐려졌다."),
        (None,"불 꺼진 집에서 사람들이 담요를 둘러쓰고 나왔다. 모두 학교 쪽으로 걸었다."),
        ("neoul","줄 서시오! 명단에 있는 사람만 들어가오!"),
        ("resident_teacher","깜이, 몽이, 방울, 도담."+(" 꼬미." if r13_has("wf_kkomi_alive") else "")+" ……그리고 새미구나. 새미는 오늘 처음 왔지요. 여기 따뜻한 자리."),
        ("kid_saemi","우리 집 불이 꺼졌어요. 엄마는 옆 교실에 있어요."),
        ("resident_teacher","그럼 오늘부터 새미도 우리 반이에요."),
        (None,"복도 게시판에 너울의 대피 명단. 깜이, 몽이, 방울. 세 이름에 줄이 그어져 있다. 옆에 '수레'."),
        (None,"그 앞에 사자 선생님이 서 있었다. 손에 든 분필이 부러져 있었다."),
        ("resident_teacher","……표가 없으면 이름도 없는 거라더군요. 보호소에 간 사람이 돌아오는 걸, 저는 한 번도 못 봤습니다.")],"ws:night")
    $ r13_grant(["Y10"],"학교 복도 게시판의 대피 명단")
    # 아랫길에서 죽는 수(대본 「긴 밤 — 아랫길」 표).
    $ _ws_dead=6
    if r13_has("ws_nero_moved") and r13_has("ws_tents_school"):
        $ _ws_dead=3
    if r13_has("madam_store_opened"):
        $ _ws_dead=max(2,_ws_dead-2)
    if r13_has("bori_ally") or r13_has("wf_bori_freed"):
        $ _ws_dead=max(2,_ws_dead-1)
    $ r13_edit(ws_tent_dead=_ws_dead)
    call r13_scene("r13_river","12일 아침 · 아랫길","quiet")
    call r13_lines([(None,"눈이 그쳐 있었다. 아랫길은 소리가 없었다."),
        (None,"천막 안. 사람들이 서로 어깨를 기댄 채 앉아 있었다. 담요 하나를 셋이 나눠 덮고."),
        (None,"모두 같은 쪽을 보고 있었다. 천막 벽 너머, 광장의 돌이 있는 쪽."),
        (None,"……")]+([("daram","……왜 다 저쪽 봐?"),("dad","…….")] if r13_ws_daram() else []),"ws:morning:tents")
    if _ws_dead<=2:
        call r13_lines([(None,"노부부 둘이 서로 기댄 채였다. 그 곁에서 네로가 숨을 붙이고 있었다."),
            ("resident_nero","……내가 다 못 데려왔다. 이름이라도 데려가라.")],"ws:morning:nero_alive")
        $ r13_flag("nero_alive")
    else:
        call r13_lines([(None,"맨 앞에 앉은 흰 늑대의 품에 천 꾸러미 하나. 이름표들이다. 이름마다 삐뚤한 바느질."),
            ("dad","(이름은 잃어버리면 안 된다.)",{"thought":True})],"ws:morning:nero_dead")
        $ r13_flag("nero_dead")
    $ r13_grant(["Y09"],"아랫길 천막에서 거둔 이름표 꾸러미")
    call r13_scene("winter_square","12일 아침 · 광장 이름 판","quiet")
    call r13_lines([(None,"광장의 이름 판. 오늘 아침, 이름이 한꺼번에 늘었다.")]+
        ([(None,"다람이 판 앞에 섰다. 늘 하던 대로, 위에서부터 손가락으로 짚었다."),
          (None,"손가락이 새 이름들 위에서 멈췄다."),
          ("daram","아빠. ……못 읽겠어."),
          ("dad","그래. 아빠가 읽을게.")] if r13_ws_daram() else [])+
        ([(None,"판 맨 아래, 너울의 글씨로 '아랫길 사람들 (이름 모름)'."),
          ("daram","이거 틀렸어. 이름 있어."),
          (None,"다람이 크레용을 꺼냈다. 이름표를 하나씩 펴서, 판에 옮겨 적었다. 삐뚤빼뚤."),
          ("daram","네로 아저씨가 잃어버리면 안 된다고 했어. 그러니까 내가 적어 둘 거야.")] if r13_ws_daram() else []),"ws:morning:board")
    $ r13_flag("ws_names_written")
    return

label r13_ws_lab:
    $ r13_flag("ws_lab","ancient_found")
    $ r13_edit(passage_open=True)
    call r13_scene("wide_ancient","돌을 만들던 옛 시설","quiet")
    call r13_lines([(None,"엄마는 13호 뒤 통로로 내려갔다. 갈라진 벽 너머 돌계단. 아래에서 따뜻한 바람이 올라왔다."),
        ("mom","여관 아래에 옛사람들이 돌을 만들던 곳이 있어. 할머니가 예전에 나를 여기 데려왔어."),
        (None,"돌기둥 사이에 유리관이 줄지어 있다. 유리관 안에서 초록빛 조각들이 숨 쉬듯 깜빡였다.")]+
        ([("daram","……사람 손 같아. 엄마 손 같아.")] if r13_ws_daram() else [])+
        [(None,"유리관 줄 끝 돌 선반에 두꺼운 장부. 할머니 글씨로 겉장에 '보호소'. 안은 죽은 사람 칸이었다."),
        (None,"지난겨울 칸에 '모과'. 세 해 전 칸에 '보미 — 여관'. 올겨울 칸은 벌써 차 있었다. '판돌 — 이송'."),
        ("dad","(보호소에 간 사람은 죽은 사람 칸에 있다. 아직 떠나지도 않은 사람까지.)",{"thought":True}),
        ("resident_guldol","(벽의 글자를 손가락으로 짚으며) \"돌은…… 하나가 아니었다. 나눠서…… 데웠다.\""),
        ("mom","조각이 하나씩 식으니까, 마을은 남은 큰 돌 하나만 붙잡았어요. 그리고 그 돌에…… 사람을 바쳤어요."),
        ("mom","이 조각 셋을 한데 모아 볼게. 잘 봐."),
        (None,"처음엔 미지근했다. 숨 몇 번 사이에, 초록빛이 짙어졌다."),
        ("mom","따로 두면 식어. 모으면 서로 데워. 사람을 바치지 않아도 돼."),
        ("resident_guldol","밤새 지켜봅시다. 정말 안 식는지."),
        ("mom","다만 시간이 걸려. 꼬박 하루. 오늘 밤, 저녁 먹을 무렵이면.")],"ws:lab")
    $ r13_grant(["Y05","Y06","Y07","Y08"],"옛 시설에서 엄마·굴돌 할아버지와 본 것")
    if r13_has("kd_farewell_seen"):
        call r13_lines([(None,"솜이가 유리관 앞에 쪼그려 앉아 있었다."),
            ("resident_somi","……다람아. 방금 누가 내 이름 불렀어. 할아버지 목소리였어. \"솜이야.\" 그렇게."),
            (None,"관 속 조각 하나가 한 번, 크게 깜빡였다. 아무도 그 이유를 말하지 않았다.")],"ws:lab:somi")
    $ r13_tick()
    return

label r13_ws_teacher_talk:
    $ r13_flag("ws_teacher_talked")
    call r13_scene("r13_school","학교 교실 · 이름을 세는 선생님","quiet")
    call r13_lines([("resident_teacher","깜이, 몽이, 방울, 도담, 새미."+(" 꼬미." if r13_has("wf_kkomi_alive") else "")+" 하나도 안 틀렸지요."),
        ("resident_teacher","오늘 저녁은 수프를 끓이려고요. 아이들이 좋아하는 노래도 부르고. 따뜻하게."),
        ("resident_teacher","(아이들을 보며, 아주 작게) ……이제 아무도 추운 데로 안 보낼 겁니다. 제가 약속했어요.")],"ws:teacher:count")
    if r13_has("mom_reunited") and r13_has("Y06"):
        call r13_lines([("mom","선생님. 잠깐 이야기 좀 할 수 있을까요. 아이들 일이에요.")],"ws:teacher:mom")
        call r13_debate_run("Q5A")
        if _return:
            $ r13_flag("ws_teacher_persuaded")
    else:
        call r13_lines([("resident_teacher","고맙습니다. 걱정 마세요."),
            ("dad","(다정한 말인데, 등이 서늘하다.)",{"thought":True})],"ws:teacher:alone")
    $ r13_tick()
    return

label r13_ws_soup:
    $ r13_flag("ws_soup")
    $ r13_edit(location="school")
    call r13_scene("r13_school","12일 저녁 · 대피소, 수프와 노래","quiet")
    if r13_has("ws_teacher_persuaded") and r13_has("ws_cabinet_locked"):
        call r13_lines([(None,"교실 난로 위에 냄비 둘. 아이들이 국자를 같이 쥐고 노래했다."),
            ("kid_dodam","(노래) 휘휘 저어라 겨울 수프, 감자 하나 당근 하나."),
            (None,"선생님은 낮에 진료소에 갔다가 잠긴 약장 앞에서 돌아섰다고 했다. 주머니는 비어 있었다."),
            (None,"창밖이 환해졌다. 광장 등이 하나, 둘, 셋."),
            ("resident_teacher","……아."),
            ("resident_teacher","다 같이 먹어요. 내일도 같이 먹어요.")],"ws:soup:perfect")
        $ r13_flag("ws_kids_alive","ws_perfect")
        call r13_ws_after
        return
    call r13_lines([(None,"교실 난로 위에 냄비 둘. 큰 냄비는 어른들 몫, 작은 냄비는 아이들 몫."),
        ("kid_kkam","(노래) 휘휘 저어라 겨울 수프, 감자 하나 당근 하나."),
        ("kid_dodam","(노래) 다 같이 먹으면 따뜻해, 내일도 같이 먹자."),
        (None,"아이들이 다시 노래하는 동안, 선생님이 주머니에서 작은 병을 꺼냈다. 아무도 보지 않았다."),
        ("resident_teacher","(작게) 아프지 않게. ……따뜻할 때.")],"ws:soup:song")
    if r13_has("ws_teacher_persuaded"):
        call r13_lines([(None,"선생님이 병을 냄비 위로 기울였다. 그때 창밖이 환해졌다. 광장 등이 하나, 둘, 셋."),
            ("resident_teacher","……아."),
            (None,"선생님이 냄비를 엎었다. 수프가 바닥으로 쏟아졌다."),
            ("resident_teacher","미안해요. 선생님이 손이 미끄러졌어요. ……새로 끓일게요. 처음부터.")],"ws:soup:spilled")
        $ r13_flag("ws_kids_alive","dodam_sick")
        call r13_ws_after
        return
    call r13_lines([(None,"하얀 그릇에 수프가 담겼다. 선생님 앞에는 빨간 그릇 하나. 선생님은 큰 냄비에서 떴다."),
        ("kid_dodam","선생님, 오늘 수프 진짜 맛있다."),
        ("kid_saemi","……"),
        (None,"새미가 반만 먹고 그릇을 무릎에 감췄다."),
        (None,"아이들이 하나둘 하품을 했다. 선생님이 한 명씩 안아 담요에 눕혔다. 이마를 쓸어 주며, 이름을 불렀다."),
        ("resident_teacher","깜이. 몽이. 방울. 도담. ……잘 자요."),
        (None,"밤이 깊었다. 대피소는 조용했다. 너무 조용했다."),
        (None,"창밖에서 빛이 일었다. 광장의 등이 하나, 둘, 셋, 차례로 밝아졌다."),
        (None,"땡그랑. 숟가락이 바닥에 떨어졌다."),
        ("resident_teacher","…… 몇 시간만.")],"ws:soup:tragedy")
    if r13_has("mom_reunited"):
        call r13_lines([("mom","(빈 그릇 냄새를 맡고) 이건…… 잠드는 약이야. 옛 기록에 있던 거야."),
            ("mom","아직 숨이 있어. 조각 가져와! 아이들 가슴에 올려!"),
            (None,"엄마가 데워진 조각을 아이들 가슴에 하나씩 올렸다. 오래, 아주 오래."),
            (None,"깜이가 기침을 했다. 몽이가 눈을 떴다. 방울이 울음을 터뜨렸다."),
            (None,"제일 작은 도담만, 끝내 눈을 뜨지 않았다.")],"ws:soup:revive")
        $ r13_flag("dodam_dead","ws_some_alive")
    else:
        call r13_lines([("kid_saemi","일어나. 일어나, 도담아. 불 켜졌어. 따뜻해졌어."),
            ("kid_saemi","……안 일어나."),
            (None,"담요 여럿. 숟가락이 가지런히 놓여 있었다. 아이들은 웃는 얼굴로 자고 있었다.")]+
            ([("daram","아빠, 얘들 왜 안 일어나? ……그림책처럼 자는 거야? 왕자 오면 일어나?")] if r13_ws_daram() else []),"ws:soup:all")
        $ r13_flag("dodam_dead","soup_kids_dead")
        if r13_has("wf_kkomi_alive"):
            $ r13_flag("kkomi_dead_soup")
    $ r13_grant(["Y11","Y12","Y13","Y14"],"대피소와 진료소에서 직접 확인한 것")
    call r13_ws_meeting
    call r13_ws_after
    return

label r13_ws_meeting:
    call r13_scene("r13_school","학교 대피소 · 회의","hearing")
    call r13_lines([(None,"담요 덮인 자리 앞. 보리가 무릎을 꿇고 도담의 작은 손을 쥐고 있었다. 화상 자국이 있는 손으로."),
        ("neoul","대피소에서 아이가 죽었소. 오늘 밤 안에 끝냅시다."),
        ("resident_bori","(고개를 들지 않고) 누구야. 누가 내 애한테.")],"ws:meeting:open")
    call r13_debate_run("Q5")
    if not _return:
        call r13_lines([("neoul","감자 탓이든 약 탓이든, 선생은 내가 데려가오."),(None,"사자 선생님은 아무 말도 하지 않았다.")],"ws:meeting:fail")
        $ r13_flag("teacher_on_cart","ws_meeting_lost")
        return
    $ _ws_pick=renpy.display_menu([("선생님을 어떻게 할까?",None),("선생님을 너울에게 넘긴다","hand"),("수레의 진실을 밝힌다","truth")])
    if _ws_pick=="hand":
        call r13_lines([(None,"너울이 선생님의 팔을 잡았다. 사람들은 수레를 벌로만 알았다.")],"ws:decision:hand")
        $ r13_flag("teacher_on_cart")
        return
    call r13_lines([("dad","보호소는 없습니다. 수레는 산속 제단으로 갑니다."),
        (None,"웅성거림이 분노로 바뀌었다. 사람들이 너울을 둘러쌌다."),
        (None,"그 사이, 선생님이 작은 냄비를 끌어당겼다. 바닥에 조금 남은 수프."),
        ("resident_teacher","아이들만 보낼 수는 없지요. 선생이 같이 가야지요.")],"ws:decision:truth")
    $ r13_flag("ws_cart_truth","village_knows_cart")
    menu:
        "냄비를 쳐낸다":
            call r13_lines([(None,"냄비를 쳐냈다. 수프가 눈처럼 바닥에 번졌다."),
                ("dad","아직 이름을 불러 줄 아이가 하나 남았습니다."),
                ("kid_saemi","선생님. 나 아직 글자 다 못 배웠어요."),
                ("resident_teacher","(무너지듯 울며) ……그래요. 그래요, 새미야.")],"ws:decision:saved")
            $ r13_flag("teacher_alive")
        "막지 않는다":
            call r13_lines([(None,"선생님이 냄비를 비웠다. 아이들 옆에 눕고, 담요를 끌어 덮었다."),
                ("resident_teacher","깜이, 몽이, 방울, 도담. 선생님 왔어요."),
                (None,"……"),
                (None,"머리맡에 출석부가 남았다. 새미의 이름에만 동그라미가 없었다.")],"ws:decision:gone")
            $ r13_flag("teacher_dead")
    return

label r13_ws_after:
    if r13_has("portrait_finished_by_daram") and r13_has("mom_reunited") and r13_ws_daram():
        call r13_lines([(None,"다람이 판자 하나를 엄마 앞에 내밀었다. 엄마 얼굴. 코만 크레용으로 삐뚤빼뚤."),
            ("daram","그림쟁이 아저씨가 그린 거야. 코는 내가 그렸어. 약속했거든."),
            ("mom","……코를, 찡그렸네."),
            (None,"엄마가 판자를 끌어안고 울었다. 웃으면서. 코를 찡그리며.")],"ws:after:portrait")
    if r13_has("ws_some_alive") or (r13_has("bori_adopts") and not r13_has("soup_kids_dead")):
        call r13_lines([(None,"보리가 대피소 구석에 앉아 있었다. 무릎에 깜이, 양옆에 몽이와 방울이 잠들어 있었다."),
            ("resident_bori","내 애 하나 잃고…… 셋 얻었다."),
            ("resident_bori","이번엔 안 놓친다.")],"ws:after:bori")
    elif r13_has("soup_kids_dead"):
        call r13_lines([(None,"보리는 아무 말도 하지 않았다. 도담의 작은 신발 한 짝을 손에 쥐고, 밤새 난로 옆에 앉아 있었다.")],"ws:after:bori_silent")
        $ r13_flag("bori_mute")
    call r13_lines([(None,"모두 잠든 밤. 교실 구석에서 작은 목소리."),
        ("kid_saemi","(노래) 휘휘 저어라 겨울 수프, 감자 하나 당근 하나."),
        ("kid_saemi","(노래) 다 같이 먹으면 따뜻해……"),
        (None,"노래가 거기서 멈췄다. 한참 뒤에, 아주 작게."),
        ("kid_saemi","(노래) ……내일도 같이 먹자."),
        (None,"(그림책) 공주는 물레 바늘에 찔려 깊은 잠에 빠졌어요."),
        (None,"(그림책) 성 안의 사람들도 모두 함께 잠들었어요.")]+
        ([(None,"(그림책) 왕자가 오기 전에, 누군가 성의 창문을 열었어요.")] if r13_has("ws_kids_alive") else [(None,"(그림책) 왕자는 몇 시간 늦게 왔어요.")])+
        ([("daram","……아빠. 왕자가 늦게 오면, 공주는 안 일어나?"),("daram","그럼 다음엔 우리가 먼저 가자. 왕자보다 먼저.")] if r13_ws_daram() else []),"ws:after:night")
    $ r13_flag("ws_done")
    return
