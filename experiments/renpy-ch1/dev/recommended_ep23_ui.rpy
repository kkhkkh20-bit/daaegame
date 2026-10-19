
# Shared card selector and scene/dialogue renderers are intentionally reused.
label r13_recommended_ep2_hearing:
    if not r13_rec_e2_ready(r13_recommended):
        call r13_lines([('dad','들은 말만으로 친구 잘못이 없다고 할 수도, 위험하다며 가둘 수도 없어. 수레를 보고, 담요와 손을 실제로 본 사람에게 물어보자.')], 'recommended:e2:missing')
        jump r13_recommended_hub
    call r13_scene('council', '5일 · 수레 앞에서 있었던 일', 'calm')
    $ r13_rec_stage_enter(2)
    if r13_recommended['episodes']['2']['privacy'] is None:
        call r13_lines([('guard','물린 팔이 여기 있습니다. 더 따질 게 있습니까?'),('bami','내가 말하면 그분 이름도 다 말해야 해?'),('dad','아니. 네가 왜 주저하는지 먼저 들었어. 이름과 거처를 공개하지 않고, 네가 겪은 행동만 이야기할 수 있어. 말하지 않아도 보호는 그대로야.')], 'recommended:e2:boundary')
        menu (screen="r13_rec_stage_choice"):
            '밤이가 말할 범위를 어떻게 지킬까?'
            '이름·거처 비공개를 회의 규칙으로 정하고, 밤이가 답할지 고르게 한다':
                call r13_lines([('resident_badook','기록에는 보호받는 주민이라고만 적겠습니다. 이름과 거처는 묻지 않겠습니다.'),('bami','그럼 말할게. 내가 돌목을 물었어. 손을 풀라고 했는데 계속 안으로 팔을 뻗었어.'),('daram','네가 물었다는 말은 그대로 들을게. 그 전에 무슨 일이 있었는지도 같이 말하자.')], 'recommended:e2:admission')
                $ r13_recommended = r13_rec_e2_privacy(r13_recommended, True)
            '오늘은 접촉 진술을 요구하지 않고, 다른 직접 목격만으로 심리한다':
                call r13_lines([('dad','말하지 않아도 돼. 이미 본 사람들이 아는 순서부터 확인하자.'),('bami','...옆에 있어 줘.'),('daram','응.')], 'recommended:e2:silence')
                $ r13_recommended = r13_rec_e2_privacy(r13_recommended, False)
    while r13_recommended['episodes']['2']['stage'] < 4:
        if r13_recommended['episodes']['2']['stage'] == 1:
            call r13_lines([('guard','팔을 뻗은 건 맞아요. 하지만 묶은 건 공격받은 뒤였습니다. 다시 다칠까 봐 보호한 겁니다.'),('dad','지금 말씀하신 순서는, 우리가 이미 들은 목격과 맞춰 보겠습니다.')], 'recommended:e2:new-order-claim')
        if r13_recommended['episodes']['2']['stage'] == 2:
            call r13_lines([('guard','바둑이가 본 건 담요를 고정한 끈이겠지요. 그때부터 손을 묶은 건 아니에요.'),('daram','그 사람이 말한 손 위치를 수레에 놓아 보면 어때?')], 'recommended:e2:blanket-rebuttal')
        $ r13_rec_stage_step = r13_rec_e2_steps[r13_recommended['episodes']['2']['stage']][1]
        $ r13_rec_stage_prompt(r13_rec_stage_step)
        call screen r13_recommended_cards(r13_rec_e2_steps[r13_recommended['episodes']['2']['stage']][0])
        if _return is None:
            jump r13_recommended_hub
        $ r13_recommended, r13_recommended_feedback, r13_recommended_correct = r13_rec_e2_present(r13_recommended, _return)
        $ r13_rec_stage_answer(r13_rec_stage_step,r13_recommended_correct)
        call r13_lines([('dad',r13_recommended_feedback)], 'recommended:e2:card-feedback')
    if r13_recommended['episodes']['2']['stage'] == 4:
        call r13_lines([('daram','그럼 친구를 믿는다는 건, 안 물었다고 우기는 게 아니네.'),('dad','응. 들은 것을 바꾸지 말고 순서를 맞춰 보자.')], 'recommended:e2:reconstruct-intro')
        $ r13_rec_stage_prompt('e2_order')
        menu (screen="r13_rec_stage_choice"):
            '직접 관찰과 실제로 답한 범위만 이어 보자.'
            '결박 → 풀라는 요구 → 수레 안으로 뻗은 팔 → 밤이의 물림' if r13_recommended['episodes']['2']['bite_admitted']:
                $ r13_recommended, r13_recommended_feedback, r13_recommended_correct = r13_rec_e2_reconstruct(r13_recommended, 'restraint_request_reach_bite')
            '물림 → 안전을 위한 결박 → 해제 요구':
                $ r13_recommended, r13_recommended_feedback, r13_recommended_correct = r13_rec_e2_reconstruct(r13_recommended, 'bite_then_restraint')
            '비명 전 결박 → 해제 요구 → 접촉은 아직 미확정' if not r13_recommended['episodes']['2']['bite_admitted']:
                $ r13_recommended, r13_recommended_feedback, r13_recommended_correct = r13_rec_e2_reconstruct(r13_recommended, 'restraint_request_cry_unconfirmed')
            '천이 걸렸으므로 밤이는 물지 않았다':
                $ r13_recommended, r13_recommended_feedback, r13_recommended_correct = r13_rec_e2_reconstruct(r13_recommended, 'deny_bite')
            '다시 현장을 살핀다':
                jump r13_recommended_hub
        $ r13_rec_stage_answer('e2_order',r13_recommended_correct)
        call r13_lines([('dad',r13_recommended_feedback)], 'recommended:e2:order-feedback')
        if not r13_recommended_correct:
            jump r13_recommended_ep2_hearing
    if r13_recommended['episodes']['2']['bite_admitted']:
        call r13_lines([('bami','문 건 미안해. 그래도 손을 묶어서 데려가면 안 되잖아.'),('guard','팔은 치료받겠습니다. 하지만 보호하려고 한 일입니다.'),('dad','그 말로 먼저 묶고 귀가를 막은 일이 없어지지는 않습니다. 밤이가 문 일과, 그 전에 억지로 데려가려 한 일은 따로 이야기해야 해요.')], 'recommended:e2:separate-responsibility')
    else:
        call r13_lines([('dad','그 순간을 다 알지는 못해요. 하지만 물린 뒤에 손을 묶었다는 말씀은 바둑이 씨가 본 순서와 맞지 않아요.')], 'recommended:e2:partial-result')
    if 'e2_care_complete' not in r13_recommended['done']:
        $ r13_rec_stage_exit()
        call r13_scene("winter", "입구 · 귀가 인계", "calm")
        call r13_lines(r13_rec_actions['e2_care']['lines'], 'recommended:e2:care-after-hearing')
        $ r13_recommended = r13_rec_apply(r13_recommended,'e2_care')
    call r13_lines([('resident_badook','밤이를 위험한 아이라며 따로 가두는 결정은 하지 않겠습니다. 수레로 데려가는 일도 중단합니다.'),(None,'바둑이가 빈 수레의 끈을 풀어 내려놓았다. 밤이는 다람 곁으로 돌아왔다.'),('daram','이제 혼자 있지 않아도 돼.')], 'recommended:e2:visible-consequence')
    call r13_lines([('resident_ppul','사람을 가두거나 구하려는 일을 막았는지는 여기서 함께 듣고 확인합시다. 그런 일이 확인되면 또 누군가를 해치지 못하게, 다른 사람이 지켜보는 곳에서 기다리도록 하겠소. 경비를 맡은 사람도 마찬가지요.'),('dad','의심스럽다는 말만으로 아이를 떼어 놓아서는 안 돼요. 그 사람이 하는 말도 듣고, 왜 기다려야 하는지 모두에게 설명해 주세요.'),('resident_ppul','그렇게 합시다. 보호자가 아이 곁에 있는 것도 막지 않겠습니다.')], 'recommended:e2:public-procedure')
    $ r13_recommended = copy.deepcopy(r13_recommended)
    $ r13_recommended['done'] = list(dict.fromkeys(r13_recommended['done']+['public_custody_procedure_heard']))
    jump r13_recommended_hub

# Actual reviewed night-v3 source, not the older abstract strip. Day/native remain pending.
init 916 python:
    R13_REC_E3_IMAGE = 'assets/recommended-story-icons/fire_lmw_night_geometry_v3.png'
    R13_REC_E3_CROP = (80,150,1500,650)
    R13_REC_E3_ANCHORS = dict(L=(245,430),M=(850,560),W=(1300,535),child=(245,348),teacher=(875,246),range4=(729,534),range6=(940,555))
    def r13_rec_e3_screen_point(point):
        return tuple(int(round(v/2.0))*2 for v in (70+(point[0]-80)*.76,116+(point[1]-150)*.76))
    def r13_rec_e3_point(key):return r13_rec_e3_screen_point(R13_REC_E3_ANCHORS[key])
    class R13RecE3Overlay(renpy.Displayable):
        def __init__(self,kind='path',**kwargs):
            super(R13RecE3Overlay,self).__init__(**kwargs);self.kind=kind
        def render(self,width,height,st,at):
            out=renpy.Render(1280,720);canvas=out.canvas()
            if self.kind=='overlap':
                canvas.polygon('#cbe58b66',[r13_rec_e3_screen_point(p) for p in ((721,502),(946,523),(948,586),(735,566))])
            else:
                canvas.lines('#f2ddbccc',False,[r13_rec_e3_point(k) for k in ('L','M','W')],4)
                canvas.lines('#ebbc71aa',False,[r13_rec_e3_point(k) for k in ('L','M','range6')],8)
                canvas.lines('#79c8e3aa',False,[r13_rec_e3_point(k) for k in ('range4','M','W')],5)
            return out

screen r13_rec_e3_route_map():
    modal True
    add Solid('#142023')
    add Transform(Crop(R13_REC_E3_CROP,R13_REC_E3_IMAGE),xysize=(1140,494),nearest=True) xpos 70 ypos 116
    add R13RecE3Overlay()
    add R13RecE3Overlay('overlap')
    $ map_step=r13_recommended['episodes']['3']['map_step']
    text '통은 문앞에 남고, 사람은 돌아왔다' xpos 45 ypos 20 size 27
    text r13_rec_e3_map_questions[map_step][0] xpos 45 ypos 62 size 23
    text '밤 장면의 관찰 재구성 · 낮 원화/실행 검수 전 · 최종 지목 잠김' xpos 45 ypos 92 size 17 color '#f3ba83'
    for point in ('L','M','W'):
        $ px,py=r13_rec_e3_point(point)
        if map_step<=1:
            textbutton point xpos px-26 ypos py-26 xsize 52 ysize 52 background Solid('#172421dd') hover_background Solid('#a57835') action Return(point)
        else:
            text point xpos px ypos py size 25 color '#fff3c7'
    if map_step in (2,3):
        $ cx,cy=r13_rec_e3_point('child')
        $ tx,ty=r13_rec_e3_point('teacher')
        textbutton '큰아이 · L–M' xpos cx-60 ypos cy-48 xsize 180 ysize 48 background Solid('#573d29ee') action Return('L-M')
        textbutton '선생님 · M–W' xpos tx-65 ypos ty-30 xsize 190 ysize 48 background Solid('#254854ee') action Return('M-W')
        textbutton '한 사람이 L–W 전체를 봄' xpos 820 ypos 620 action Return('L-W')
    elif map_step==4:
        button:
            area (0,0,1280,610)
            background R13RecE3Overlay('overlap')
            hover_background R13RecE3Overlay('overlap')
            focus_mask True
            action Return('overlap')
            alt '두 관찰이 겹치는 담장 끝 M의 구간'
        text '겹치는 구간을 직접 짚는다' xpos 430 ypos 570 size 19
        textbutton '관찰 바깥' xpos 80 ypos 620 action Return('outside')
        textbutton '위치를 아직 모름' xpos 800 ypos 620 action Return('unknown')
    text '황토색: 아이가 따라 본 길 / 푸른색: 선생님이 따라 본 길' xpos 55 ypos 653 size 18
    text '학교 앞 갈림길은 실제 존재한다. 그 짧은 동안 다른 통행·인계가 없었다는 증언이다.' xpos 55 ypos 680 size 16
    textbutton '돌아가기' xpos 1080 ypos 18 action Return(None)
    key 'game_menu' action Return(None)

label r13_recommended_ep3_hearing:
    if not r13_rec_e3_ready(r13_recommended):
        call r13_lines([('dad','문과 벽, 현장에 남은 통을 먼저 살펴보자. 보리와 선생님에게 직접 본 순서를 듣고, 통 주인에게 인계를 물어야 한다.')], 'recommended:e3:missing')
        jump r13_recommended_hub
    call r13_scene('r13_school', '6일 · 창고 문밖의 불', 'calm')
    $ r13_rec_stage_enter(3)
    if r13_recommended['episodes']['3']['privacy'] is None:
        if 'e3_child_support_ready' in r13_recommended['done']:
            call r13_lines([('resident_teacher','아이의 자리와 돌봄은 마련돼 있습니다. 이야기하지 않아도 그대로입니다.'),('dad','관찰을 공개하면 엄마의 대여 주장을 판단하는 데 쓰일 수 있어. 이름과 거처는 공개하지 않을 거야. 그래도 말하지 않을 수 있어.')], 'recommended:e3:privacy-choice')
            menu (screen="r13_rec_stage_choice"):
                '큰아이가 정한 범위에서 들을까?'
                '보호자 동석·이름 비공개로, 아이가 동의한 관찰만 듣는다':
                    $ r13_recommended = r13_rec_e3_privacy(r13_recommended, True)
                    call r13_lines([('kid_nubi1','그 범위라면 말할게요. 빨래터 문에서 엄마 얼굴과 통을 봤어요. 담장 끝까지 가는 걸 계속 봤고 기다렸어요.'),('kid_nubi1','불빛이 보인 뒤 돌아올 때도 계속 봤어요. 문앞에서 다시 얼굴을 봤는데 빈손이었어요. 그동안 다른 사람이나 통을 주고받는 모습은 없었어요.'),('dad','창고 문앞에서 불붙이는 모습도 봤니?'),('kid_nubi1','아니요. 불을 붙이는 순간은 못 봤어요. 내가 계속 따라 본 건 담장 끝 근처까지예요.')], 'recommended:e3:child-testimony')
                '더 묻지 않고 이미 확보한 자료로만 판단한다':
                    $ r13_recommended = r13_rec_e3_privacy(r13_recommended, False)
        else:
            menu (screen="r13_rec_stage_choice"):
                '지금 큰아이의 세부 진술은 없다. 보호와 공개 범위를 먼저 마련할 수 있다.'
                '학교의 실제 돌봄과 비공개 면담을 준비하러 돌아간다':
                    jump r13_recommended_hub
                '아이 진술 없이 확인한 범위까지만 심리한다':
                    $ r13_recommended = r13_rec_e3_privacy(r13_recommended, False)
    while r13_recommended['episodes']['3']['stage'] < 3:
        if r13_recommended['episodes']['3']['stage'] == 0:
            call r13_lines([('resident_nubi','벽을 뜯었잖아요. 장작을 가져가려고 들었다가 불을 낸 것 아닌가요?'),('resident_bori','문이 타서 벽으로 갔어요.'),('dad','말만 맞서지 말고, 먼저 실제 벽을 보겠습니다.')], 'recommended:e3:wall-claim')
        if r13_recommended['episodes']['3']['stage'] == 1:
            call r13_lines([('resident_nubi','나중에 사람을 도왔다고 먼저 불을 안 냈다는 건 아니잖아요.'),('dad','맞습니다. 그러니 먼저 점화하고 돌아간 행동을 본 사람과 대조하겠습니다.')], 'recommended:e3:legitimate-resistance')
        if r13_recommended['episodes']['3']['stage'] == 2:
            call r13_lines([('resident_nubi','내 통이라고 내가 썼다는 뜻은 아니죠. 보리에게 빌려줬어요.'),('dad','소유와 사용은 다릅니다. 현장 물체부터 확인하죠.')], 'recommended:e3:can-rebuttal')
        $ r13_rec_stage_step = r13_rec_e3_steps[r13_recommended['episodes']['3']['stage']][1]
        $ r13_rec_stage_prompt(r13_rec_stage_step)
        call screen r13_recommended_cards(r13_rec_e3_steps[r13_recommended['episodes']['3']['stage']][0])
        if _return is None:
            jump r13_recommended_hub
        $ r13_recommended, r13_recommended_feedback, r13_recommended_correct = r13_rec_e3_present(r13_recommended, _return)
        $ r13_rec_stage_answer(r13_rec_stage_step,r13_recommended_correct)
        call r13_lines([('dad',r13_recommended_feedback)], 'recommended:e3:card-feedback')
    if r13_recommended['episodes']['3']['privacy']:
        call r13_lines([('dad','통을 어디서 건넸습니까?'),('resident_nubi','낮은 담장 끝 M에서요. 보리가 통을 들고 갔고, 나는 빈손으로 돌아왔어요.'),('daram','그럼 거기서 두 사람이 만나야겠네. 통이 가는 길과 사람이 돌아오는 길을 따로 놓아 보자.')], 'recommended:e3:new-handoff-path')
        while r13_recommended['episodes']['3']['map_step'] < 5:
            $ r13_rec_stage_step = "e3_map_%d" % r13_recommended["episodes"]["3"]["map_step"]
            $ r13_rec_stage_prompt(r13_rec_stage_step)
            call screen r13_rec_e3_route_map
            if _return is None:
                jump r13_recommended_hub
            $ r13_recommended, r13_recommended_feedback, r13_recommended_correct = r13_rec_e3_map_answer(r13_recommended, _return)
            $ r13_rec_stage_answer(r13_rec_stage_step,r13_recommended_correct)
            call r13_lines([('dad',r13_recommended_feedback)], 'recommended:e3:map-feedback')
        $ r13_rec_stage_prompt('e3_finish')
        call screen r13_recommended_cards('통을 이 길로 빌려줬다고 말한 사람은 누구였지? 그 설명을 다시 보자.')
        if _return is None:
            jump r13_recommended_hub
        $ r13_recommended, r13_recommended_feedback, r13_recommended_correct = r13_rec_e3_finish(r13_recommended, _return)
        if not r13_recommended_correct:
            $ r13_rec_stage_answer('e3_finish',False)
            call r13_lines([('dad',r13_recommended_feedback)], 'recommended:e3:person-feedback')
            jump r13_recommended_ep3_hearing
    else:
        $ r13_recommended, r13_recommended_feedback, r13_recommended_correct = r13_rec_e3_finish(r13_recommended)
    $ r13_rec_stage_answer('e3_finish',r13_recommended_correct)
    call r13_lines([('dad',r13_recommended_feedback)], 'recommended:e3:conclusion')
    if r13_recommended['episodes']['3']['verdict'] != 'nubi_ignition_bori_afterward':
        call r13_lines([('resident_teacher','보리 혼자 불을 냈다는 이유로 붙잡아 두는 일은 중단하겠습니다. 남은 확인은 아이들에게 증언을 강요하지 않고 하겠습니다.')], 'recommended:e3:partial-consequence')
    else:
        call r13_lines([('resident_teacher','문밖 점화와 그 뒤 구조 행동을 나눠 기록하겠습니다. 누비의 아이들 돌봄은 처분과 관계없이 이어갑니다.')], 'recommended:e3:full-consequence')
    if r13_recommended['e3_school_handoff']:
        call r13_lines([('kid_kkomi','다람아, 어제 가져간 도토리야. 오늘도 같이 밥 먹자.'),(None,'네 아이가 학교 식탁에 앉았다. 불난 창고로 돌아가 자지 않아도 됐다.')], 'recommended:e3:survival-consequence')
    else:
        call r13_lines([('kid_kkam','꼬미 것도 여기 둘래요.'),(None,'남은 세 아이 곁에 어른이 앉았다. 더 많은 대답을 요구하지 않고 저녁을 놓았다.')], 'recommended:e3:loss-consequence')
    jump r13_recommended_hub

# Direct-entry QA labels initialize an isolated recommended state, not legacy story flags.
label r13_recommended_ep2_admin:
    call r13_recommended_ep23_admin_boot
    $ r13_recommended = r13_rec_e2_start(r13_recommended)
    jump r13_recommended_hub

label r13_recommended_ep3_admin:
    call r13_recommended_ep23_admin_boot
    $ r13_recommended = r13_rec_e3_start(r13_recommended)
    jump r13_recommended_hub

label r13_recommended_ep23_admin_boot:
    $ room13_mode = True
    $ winter_mode = True
    $ winter = winter_new()
    $ source_mode = False
    $ room13 = r13_new()
    $ r13_recommended = r13_rec_new_state()
    $ room13['campaign_id'] = 'room13_recommended_v1'
    $ room13['day'] = 4
    $ r13_recommended['mother'] = 'M2'
    $ r13_recommended['piko'] = 'safe'
    $ r13_recommended['nabi'] = 'supervised_relief'
    $ r13_scene_key = None
    $ r13_world_cameras = {}
    $ r13_inspection_location = None
    $ room13['learning_archive'] = r13_learning_archive_seed()
    $ typing_allowed = True
    hide screen r13_hud
    hide screen winter_hud
    hide screen hud
    return
