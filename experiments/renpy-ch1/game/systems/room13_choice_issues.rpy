# 2026-10-27 외부 리뷰(0.20.67) UI 지적 두 가지. 소유자 "체크하고 적용해줘".
#  ① 무게가 큰 선택창은 직전 대사 대신 「무엇을 정하는 자리인지」를 제목으로 둔다.
#     쉬었다 돌아온 사람은 직전 대사("그러네.")만으로는 무엇을 고르는지 모른다.
#     문장은 선택지에 이미 있는 말로만 짓고, 결과·생사·정답·숨은 조건은 암시하지 않는다.
#  ② 자료 제출 단계 안내와 되돌아갈 수 있는 범위 안내는 처음 한 번만 보인다.
# 대사·분기·조건·선택 결과는 바꾸지 않는다. 표에 없는 메뉴와 회의 선택지는 지금과 같다.
default persistent.r13_proof_guide_done = False
default persistent.r13_recovery_hint_retry = False
default persistent.r13_recovery_hint_morning = False

init 80 python:
    import bisect as _r13_issue_bisect
    import os as _r13_issue_os

    # 메뉴 id(메뉴를 품은 label) → (쟁점 한 줄, 그 메뉴의 선택지 전체).
    # 선택지 전체를 같이 적는 까닭: 같은 label 안에 다른 메뉴가 있거나 메뉴 글이 바뀌면 쟁점이 엉뚱한
    # 선택창에 붙는다. 보이는 선택지가 이 목록 안에 다 들어 있을 때만 쟁점을 쓰고, 아니면 예전처럼 둔다.
    # 회의 무대 안의 메뉴(3일 돌 반환·신병, 7일 아이들, 11일 가설 등)는 회의 선택지 화면으로 가므로 넣지 않는다.
    # 표와 실제 메뉴가 맞는지는 dev/test_choice_issues.py 가 확인한다.
    R13_CHOICE_ISSUES = {
        # 2026-10-27 D09: 7일 화재, 자료가 받아들여진 뒤 무엇부터 물을지(결과 분기 없음).
        "r13_v111_nubi_first_question7":("무엇부터 물을까",
            ("문 앞의 기름 흔적을 설명해 주십시오.","등잔은 뒷벽 물통 옆에 있었습니다. 뚜껑도 닫혀 있었고요.","창고 문 앞에 서 계신 걸 보리 씨가 봤습니다.")),
        "r13_v111_dry11":("지금 꺼내 덮을까, 짐 안에 둘까",
            ("두 장을 꺼내 덮는다","한 장을 함께 덮는다","짐 안에 둔다","외투 안쪽을 함께 덮는다")),
        "r13_v111_heat_seen11":("가족 자리·아랫길 대피·물자, 무엇부터 할까",
            ("가족 자리부터 본다","아랫길 대피 준비를 확인한다","준비된 물자를 학교로 옮긴다")),
        "r13_v111_blanket_choice11":("한 장을 가족 짐에 둘까, 토실에게 건넬까",
            ("가족 짐에 보관한다","토실에게 한 장을 건넨다")),
        "r13_v111_meal_choice12":("배식 전에 더 살필까, 장작을 받으러 갈까",
            ("배식 전에 더 살핀다","다람과 장작을 받으러 간다","다람은 나비 곁에 두고 다녀온다","아침에 부탁한 일들을 확인한다")),
        "r13_v111_aftermath_pre12":("신병을 돌목에게 맡길까, 너울에게 넘길까",
            ("돌목에게 감독을 맡긴다","너울에게 신병을 넘긴다")),
        "r13_v111_aftermath_late12":("신병을 돌목에게 맡길까, 너울에게 넘길까",
            ("돌목에게 감독을 맡긴다","너울에게 신병을 넘긴다")),
        "r13_v111_offer13":("가족 셋이 물러날까, 현장에 남을까",
            ("조건을 더 묻는다","가족 셋이 수락하고 물러난다","거절하고 현장에 남는다")),
        "r13_v111_family_position13":("엄마와 다람을 곁에 둘까, 학교로 보낼까",
            ("엄마와 다람이 곁에 남게 한다","엄마와 다람을 까로와 학교로 보낸다","엄마와 다람을 네로와 학교로 보낸다")),
        "r13_v111_handover_plan13":("인계를 앞두고 무엇부터 할까",
            ("학교 침상과 인수를 먼저 확인한다","하차한 사람부터 부축한다","보온·감독 아래 인계를 기다린다","검증한 기록을 공개한다")),
        "r13_v111_tosil_listen14":("안에서 직접 들을까, 밖에서 기다릴까",
            ("토실에게 함께 듣겠냐고 묻는다","밖에서 기다리고, 확인한 일을 나중에 말해 주겠다고 한다")),
        "r13_v111_name_board14":("토실이 쓰기를 기다릴까, 쓰지 않아도 된다고 할까",
            ("토실이 이름을 쓰겠다면 기다린다","지금 쓰지 않아도 된다고 말한다")),
    }

    def r13_choice_issue_label_index():
        # 새 세계 이야기 파일의 label 시작 줄. 메뉴 문은 이름이 없어서, 그 줄을 품은 label 을 메뉴 id 로 쓴다.
        # 함수 속성에 둬서 저장 파일에 실리지 않는다.
        cache=getattr(r13_choice_issue_label_index,"cache",None)
        if cache is None:
            cache={}
            for name in renpy.get_all_labels():
                try:node=renpy.game.script.lookup(name)
                except Exception:continue
                base=_r13_issue_os.path.basename(getattr(node,"filename","") or "").replace(".rpyc",".rpy")
                if base.startswith("room13_v111"):
                    cache.setdefault(base,[]).append((int(getattr(node,"linenumber",0) or 0),name))
            for rows in cache.values():rows.sort()
            r13_choice_issue_label_index.cache=cache
        return cache

    def r13_choice_issue_menu_id():
        try:filename,line=renpy.get_filename_line()
        except Exception:return None
        rows=r13_choice_issue_label_index().get(_r13_issue_os.path.basename(filename or "").replace(".rpyc",".rpy"))
        if not rows:return None
        i=_r13_issue_bisect.bisect_right(rows,(int(line or 0),"￿"))-1
        return rows[i][1] if i>=0 else None

    def r13_choice_issue_for(menu_id,captions):
        spec=R13_CHOICE_ISSUES.get(menu_id)
        captions=[c for c in captions if c]
        if not spec or not captions or not set(captions)<=set(spec[1]):return None
        return spec[0]

    def r13_choice_issue(entries):
        if getattr(store,"r13_meeting_active",False):return None
        return r13_choice_issue_for(r13_choice_issue_menu_id(),[entry[0] for entry in entries])

    def r13_choice_issue_subline(caption,context,limit=34):
        # 쟁점이 제목을 차지하면 직전 대사는 그 아래 작게 남긴다. 한 줄을 넘지 않게 잘라
        # 선택지가 쓸 높이를 빼앗지 않는다(인물 옆 좁은 판은 20자, 넓은 판은 34자).
        if caption:line=caption
        elif context and context[1]:line=(context[0]+" · "+context[1]) if context[0] else context[1]
        else:return None
        line=" ".join(str(line).split())
        return line if len(line)<=limit else line[:limit-1]+"…"

    # ② 자료 제출 단계 ------------------------------------------------
    R13_PROOF_STEPS=("자료 고르기","확인","선택한 근거 제출")

    def r13_proof_guide_active():
        return not persistent.r13_proof_guide_done

    def r13_proof_guide_step(chosen_count):
        return 0 if not chosen_count else 1

    def r13_proof_guide_steps(chosen_count,current=None,rest=None):
        # 타이포 V2: 지금 단계는 accent(테이프 빨강보다 한 단 어두운 글자용 빨강), 나머지는 muted. 끄면 이전 색.
        current=current or (r13_type_color("accent"))
        rest=rest or (r13_type_color("muted"))
        step=r13_proof_guide_step(chosen_count)
        return "  →  ".join("{color=%s}%d %s{/color}"%(current if i==step else rest,i+1,name) for i,name in enumerate(R13_PROOF_STEPS))

    # 2026-10-27 패널 정리: 단계는 한 글줄이 아니라 칩 셋으로 보인다. 칩에는 짧은 이름을 쓴다 — 긴 이름을 넣으면
    # 세 칩이 휴대폰 큰 글씨에서 한 줄을 넘는다. 긴 이름(R13_PROOF_STEPS)은 안내 문장이 그대로 쓴다.
    R13_PROOF_STEP_CHIPS=("고르기","확인","제출")

    def r13_proof_guide_chips(chosen_count):
        """[(칩 글자, 지금 단계인가)] — 화면은 지금 단계만 빨강으로 채운다."""
        step=r13_proof_guide_step(chosen_count)
        return [("%d %s"%(i+1,name),i==step) for i,name in enumerate(R13_PROOF_STEP_CHIPS)]

    def r13_proof_guide_help(chosen_count,chances=None):
        # 기존 안내(room13_proof_usability.rpy)를 단계형으로 고친 것. 첫 제출 성공 뒤에는 기존 문장으로 줄인다.
        if not chosen_count:
            return "「자료 고르기」로 자료를 담습니다. 담기·빼기는 기회를 쓰지 않습니다."
        if chances:
            return "위 목록이 맞으면 「선택한 근거 제출」. 잘못 내면 기회를 1회 씁니다."
        return "위 목록이 맞으면 「선택한 근거 제출」을 누릅니다."

    def r13_proof_guide_finish():
        if not persistent.r13_proof_guide_done:
            persistent.r13_proof_guide_done=True

    # ② 되돌아갈 수 있는 범위 ----------------------------------------
    # 실제로 있는 기능만 말한다: 회의 재시도 화면의 「회의를 처음부터 다시」, 더보기 판의
    # 「저장 · 불러오기」, 아침 저장이 있을 때만 보이는 「다시 시작할 아침」.
    def r13_recovery_retry_note():
        if persistent.r13_recovery_hint_retry:return None
        # 2026-10-27: 저장·불러오기는 「설정」의 「저장」 탭으로 갔고 「다시 시작할 아침」은 메뉴에서 뺐다.
        return "받아들여도 「설정」의 「저장」 탭에서 저장해 둔 곳에 돌아갈 수 있습니다."

    def r13_recovery_retry_seen():
        if not persistent.r13_recovery_hint_retry:
            persistent.r13_recovery_hint_retry=True

    def r13_recovery_morning_note(day):
        # 아침 저장이 실제로 남은 뒤, 첫날이 아닌 첫 아침에 한 번만 알린다(날짜가 처음 바뀐 때).
        if persistent.r13_recovery_hint_morning or day<2 or day not in r13_morning_days():return
        persistent.r13_recovery_hint_morning=True
        # 2026-10-27 14일 자동 플레이 2일: 「더보기」의 「다시 시작할 아침」은 메뉴에서 뺐는데 안내는 그 이름을 그대로 말했다.
        # 아침 저장은 이어 갈 수 없는 저장을 열었을 때 자동으로 쓰인다(systems/room13_return_recovery.rpy). 그 사실만 말한다.
        renpy.show_screen("r13_recovery_note","%d일 아침을 남겼습니다. 하던 장면을 이어 갈 수 없게 되면 이 아침부터 다시 시작합니다."%day)

screen r13_recovery_note(message):
    # 알림 자리(오른쪽 위, 날짜판 아래)를 쓰되 한 번만 나오는 안내라 조금 더 오래 둔다. 누르면 닫힌다.
    zorder 101
    button:
        id "r13_recovery_note"
        xanchor 1.0 xpos 1256 ypos 92 xmaximum 440 padding (22,16)
        background r13_sticker_button()
        hover_background r13_sticker_button(focused=True)
        action Hide("r13_recovery_note")
        alt message
        text message size (r13_type("small")) color (r13_type_color("ink")) font R13_UI_BOLD_FONT xmaximum 396 line_spacing 4
    timer 7.0 action Hide("r13_recovery_note")
