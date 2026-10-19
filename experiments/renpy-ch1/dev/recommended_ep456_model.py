"""Recommended 4A/5B/6C. Pure copy-on-write plugin, independent of legacy story.
The new R/P/G/K layout is explicitly a recommended-route reconstruction, not old art.
No poison recipes, medical timing thresholds or universal winter solution are modeled.
"""
import copy

r13_rec_e456_version = '2026-10-18-review-v2'
r13_rec_e456_art_status = '신규 R/P/G/K 도식과 냄비 도식 적용. 기존 배경 공간·원화 결합 검수 및 변경 사인의 의료·서사 감수 미완료.'


def r13_rec_e456_state(s, episode):
    n = copy.deepcopy(s)
    n['episode'] = episode
    n['period'] = 0
    n['location'] = {4:'hall',5:'school',6:'school'}[episode]
    n['day'] = {4: 7, 5: 11, 6: 13}[episode]
    n.setdefault('episodes', {})[str(episode)] = dict(hearing=0, verdict=None, selected=[])
    if episode == 4:
        n['episodes']['4'].update(victim='trapped_alive', ttadak='not_started', day9='pending')
    elif episode == 5:
        n['episodes']['5'].update(event='pending', children='well', lids='original', contents='unchanged')
    else:
        n['episodes']['6'].update(transport='scheduled', protection='unprepared', today_sacrifice_stopped=False,
                                  resources=dict(heat=False, beds=0, meals=0, carers=0, route=False), passengers=3)
    return n


def r13_rec_e456_flag(s, *flags):
    n = copy.deepcopy(s)
    n['done'] = list(dict.fromkeys(n['done'] + list(flags)))
    return n


def r13_rec_e456_effect(s, key):
    n = copy.deepcopy(s)
    e = n['episodes'][str(n['episode'])]
    if key == 'e4_alone_tool': n['daram'] = 'protected_wait'
    if key == 'e4_rescue': e['victim'] = 'recovering'
    if key == 'e4_block_lever': n['e4_lever_blocked'] = True
    if key == 'e4_work':
        if n['e4_lever_blocked']:
            e.update(day9='prevented', ttadak='safe')
            n = r13_rec_e456_flag(n, 'e4_day9_prevented')
        elif 'e4_wedge_set' in n['done']:
            e.update(day9='attempt', ttadak='safe')
            n = r13_rec_e456_flag(n, 'e4_day9_attempt')
        else:
            e.update(day9='locked', ttadak='injured_rescued')
            n = r13_rec_e456_flag(n, 'e4_day9_locked')
    if key == 'e5_lock': n['e5_poison_blocked'] = True
    if key == 'e5_serve_safe':
        e.update(event='prevented', children='well', lids='original', contents='unchanged')
    if key == 'e5_serve_accident':
        e.update(event='contaminated', children='under_care', lids='swapped', contents='adult_body_contaminated')
    if key == 'e6_hold':
        n['location'] = 'altar' if e['transport']=='at_altar_waiting' else 'school'
        e['transport'] = 'paused'
        e['protection'] = 'supervised_wait'
    if key == 'e6_heat': e['resources']['heat'] = True
    if key == 'e6_beds': e['resources']['beds'] = 3
    if key == 'e6_meals': e['resources']['meals'] = 3
    if key == 'e6_care': e['resources']['carers'] = 2
    if key == 'e6_route': e['resources']['route'] = True
    if key == 'e6_cancel':
        e['transport'] = 'cancelled'
        e['today_sacrifice_stopped'] = True
    if key == 'e6_handoff': e['protection'] = 'housed_fed_cared'
    if key == 'e6_night':
        n['period'] = 2
        e['verdict'] = 'complete_today'
        e['family'] = ('together_departure_unverified' if e.get('future_choice')=='departure_pending' else 'together_staying') if n['mother'] == 'M2' else 'mother_reunion_unfinished'
    return n


def r13_rec_e456_advance(s):
    reason = r13_rec_e456_block(s)
    if reason: raise ValueError(reason)
    n = copy.deepcopy(s)
    n['period'] = 0
    ep = n['episode']; e = n['episodes'][str(ep)]
    if ep == 4:
        if n['day'] == 7:
            if e['victim'] == 'trapped_alive':
                e['victim'] = 'dead_after_delayed_rescue'
                n = r13_rec_e456_flag(n, 'e4_victim_dead')
            else: n = r13_rec_e456_flag(n, 'e4_victim_alive')
        n['day'] = min(10, n['day'] + 1)
    elif ep == 5: n['day'] = min(13, n['day'] + 1)
    elif ep == 6:
        n['day'] = 14
        if e['transport'] == 'scheduled': e['transport'] = 'at_altar_waiting'
    return n


def r13_rec_e456_block(s):
    done = set(s['done']); ep = s['episode']; day = s['day']
    if ep == 4 and day == 7 and 'e4_discovery' not in done:
        return '식기를 돌려놓던 복도에서 들은 구조 요청부터 확인하자.'
    if ep == 4 and day == 8 and not {'e4_nabi7_heard','e4_care_checked','e4_mechanism_checked','e4_work_announced'} <= done:
        return '나비의 7일 관찰, 진료 경과, 문 구조와 내일 작업 예고를 확인하자.'
    if ep == 4 and day == 9 and 'e4_work' not in done:
        return '실측의 실제 결과를 확인하자. 따닥이 일을 마쳤는지 확인하고 돌아가자.'
    if ep == 5 and day == 12 and not {'e5_serve_safe','e5_serve_accident'} & done:
        return '정상 배식 또는 사고 뒤 돌봄의 실제 결과를 확인하자.'
    if ep == 6 and day == 13 and 'e6_pandol_seen' not in done:
        return '출발 전에 판돌이 지금 어디에서 보호받고 있는지 직접 확인하자.'
    return None


r13_rec_cards.update({
'e4_card_daram': ('다람 · 7일 객실 R에서의 구조 요청', '7일 R에서 직접 듣고 봄. 열린 객실 문 A로 R에 왔다. 판자문 G 너머 P에 사람이 살아서 도움을 청했다. 다람은 P 안에 들어가지 않았다. 너울에게 사람이 남았다고 알리자 밖에서는 열 수 없다는 답을 들었다. 이전 수색은 못 봤다.'),
'e4_card_tool': ('벌림 도구 · 객실 쪽 자국', '7일 사용 현물. 끝과 맞는 자국은 R 쪽에서 G를 벌리려 한 자리다. 흉기로 쓴 증거가 아니며, 이것만으로 다람이 오기 전 일을 증명하지 않는다.'),
'e4_card_parent': ('아빠 · 동행 또는 기다림 확인', '7일 다람이 객실 R에 머물며 도움을 청하고 P에 들어가지 않은 구간을 직접 확인했다. 당시 다람은 도구를 쓰지 않았다.'),
'e4_card_seori': ('서리 · 발견과 진료 경과', '7일 구조·진료 및 8일 설명. 넘어짐 손상은 치명적 흉기 상처가 아니다. 발견 때 살아 있던 구조 요청과 이후 추위 속 감금·구조 지연 경과를 대조했다. 정확한 사망 시각이나 구할 수 있었던 초는 계산하지 않는다.'),
'e4_card_lever': ('13호 개폐 장치 · R / G / P / K', '8일 부리와 빈 칸에서 안전하게 직접 시험. G는 R과 막다른 작업칸 P 사이. K의 L을 끝까지 내리면 걸쇠가 걸리고 올리면 열린다. K 유일 출입은 B. 내부 조작·자연 낙하·끈·예약 장치는 없음.'),
'e4_card_nabi7': ('나비 · 7일의 두 짧은 개폐 관찰', '7일 업무 인계에서 직접 관찰, 8일 공개 면담에서 들음. 처음 B에서 너울이 L로 G를 여는 것을 보고 너울·피해자가 R→P로 들어갔다. 수색 중엔 배식 일로 떠났다. 종료 인계로 B에 돌아왔을 때 혼자 나온 너울이 L을 내려 G를 닫는 것을 봤다. 내부 넘어짐은 보지 못했다.'),
'e4_card_ttadak': ('따닥 · 8일 작업 예고', '8일 R에서 아빠·다람·너울이 함께 듣는 자리. 9일 P 안에서 실측하겠다고 설명했다. 9일 생존 여부와 독립인 전날 관찰이다.'),
'e4_card_nabi9': ('나비 · 9일 한 차례 연속 출입 관찰', '9일 작업 시작 직전 K가 비었고 G가 열렸음을 확인. B 밖에서 짧은 업무 인계 동안 한 번도 떠나지 않았고, 들어갔다 나온 것은 너울뿐. L의 손동작 자체는 못 봤다. 7일 개폐 관찰과 다른 카드다.'),
'e4_card_neoul': ('너울 · 7일 책임을 묻는 대상', '7일 다람의 구조 요청에 밖에서는 못 연다고 답한 경비. 다람이 발견하기 전 내부 수색에 관해서는 아직 직접 말하지 않았다.'),
'e5_card_pots': ('두 냄비 · 고정 몸체와 이동 뚜껑', '12일 오전 직접 관찰. 왼쪽 A는 깨진 귀, 원래 순찰대 몫. 오른쪽 C는 천 감은 손잡이, 원래 아이들 몫. 아이 그림 뚜껑은 원래 C. 두 뚜껑 크기는 같다. 이후 음식 이동 여부는 계속 지켜본 사람에게 별도로 확인해야 한다.'),
'e5_card_bottle': ('반출 약통 · 동일 용기의 인계', '12일 서리가 보관하던 용기가 선생님 손으로 학교까지 인계된 구간을 서리·보리가 이어 확인했다. 학교 조리대의 같은 목테 흠집과 실제 인계를 대조했다. 상표나 빈 통만으로 혼입자를 맞히지 않는다.'),
'e5_card_cabinet': ('서리 · 약장 안의 보관약', '12일 배식 전 진료실. 서리는 선생님에게서 보관약 사용 요청을 받았고 용기는 아직 약장 안에 있다고 확인했다. 학교 반출이나 혼입을 본 것은 아니다.'),
'e5_card_seori': ('서리 · 반출 용기와 내용물', '12일 진료실에서 꺼낸 용기가 선생님 손으로 학교에 인계된 구간을 확인했다. 보관 내용은 알지만 학교에서 붓는 행동은 못 봤다.'),
'e5_card_bori': ('보리 · 원래 요청·혼입 위치·배식', '12일 학교에서 직접 관찰. 선생님은 깨진 귀 A를 순찰대 몫으로 남겨 달라고 했다. 같은 용기를 A에 비우는 것을 봤지만 당시 위험약인 줄은 몰랐다. 뚜껑을 덮을 때 보리는 앞문 F에서 물을 주고 있었다. 이후 아이 그림을 따라 A에서 아이들에게 배식했다. 치료 중 면담과 돌봄 인계 후 회의의 내용은 같다.'),
'e5_card_saemi': ('새미 · 두 뚜껑과 앞문', '12일 F 안쪽에서 두 냄비를 여는 때부터 첫 배식까지 자리를 떠나지 않고 조리대를 직접 관찰. 몸체는 고정되어 있었고 수프를 서로 옮겨 붓지 않았다. 선생님이 열어 둔 두 뚜껑을 순찰대 도착 때 다시 덮었다. 아이 그림이 깨진 귀 A 위에 갔다. 보리는 자기 앞에서 물을 주었고 뚜껑을 만지지 않았다. 약 성분·속마음은 모른다.'),
'e5_card_teacher': ('선생님 · 요청과 행동의 책임', '12일 학교에서 깨진 귀 A 냄비를 순찰대 몫으로 남겨 달라고 직접 요청했다. 그 말을 안다고 이후 모든 행동이나 의도까지 아는 것은 아니다.'),
'e5_card_notice': ('학교 점검 · 실제 계속 쓸 자리', '11~12일 학교 직접 확인. 한 난로의 점검이지 학교 전체 폐쇄가 아니다. 현재 쓸 난로와 교실, 물품을 확인했다. 약을 써서 순찰대를 막아야만 아이들이 머문다는 전제를 바꾼다.'),
'e6_card_board': ('학교 배분판 · 7일 결정 / 12일 적용', '원본의 판돌 칸: 외부 보호 완료, 학교 몫 제외, 비축 분류. 결정은 7일, 적용은 12일. 선생님처럼 나중에 추가된 사람을 7일 대상이라고 읽지 않는다.'),
'e6_card_manifest': ('출발 명단 · 판돌 13일 저녁 / 제단 인계', '현재 명단의 판돌 예정 출발은 13일 저녁. 목적지는 제단이며 마을 식사·숙소 재배정은 없다. 날짜와 실제 인계를 서로 다른 질문으로 읽는다. 과거 모든 운행의 사망을 증명하지 않는다.'),
'e6_card_pandol': ('판돌 · 13일에도 학교에 있는 사람', '13일 학교에서 직접 대화. 7일에도 예정 대상이었지만 13일 저녁 출발 전까지 학교에 남아 있다. 아직 밖에서 보호받지 않았다.'),
'e6_card_nabi': ('나비 · 7일 요청 / 12일 실제 수령', '7일 인계에서 할머니에게 판돌이 13일 저녁까지 남으니 12~13일 몫도 필요하다고 직접 말했다. 12일 실제 배달에는 몫이 없었고 배분 담당자가 현재 배분판의 제외 칸을 보여 줬다.'),
'e6_card_munchi': ('뭉치 · 직접 지시와 실제 적용', '7일 같은 인계 자리에서 나비의 요청을 들었다. 이어 할머니가 판돌 몫을 12일부터 학교 배달에서 빼고 비축 쪽으로 분류하라고 직접 지시했다. 자신이 그 기준대로 포장·배달했고 나비에게 같은 판을 보여 줬다.'),
'e6_card_granny': ('할머니 · 7일 식사 요청을 들은 사람', '나비에게 들은 7일 인계: 판돌이 13일 저녁까지 학교에 남으며 식사 몫이 필요하다는 말을 직접 들었다. 누가 제외를 지시했는지는 이 요청만으로 알 수 없다. 직접 지시와 배달 적용은 뭉치에게 따로 확인해야 한다.'),
'e6_card_siluk': ('실룩 · 이번 운행의 끝', '현재 명단대로 제단까지 운행하라는 지시를 확인했다. 하차 뒤 의료·생활 보호를 직접 본 적은 없다. 보지 못한 곳에 아무도 없다고 단정하지 않는다.'),
'e6_card_badook': ('바둑이 · 제단의 실제 인계 확인', '가족·촌장과 현재 제단 현장을 확인. 사람을 돌 앞에 두는 인계였고, 확인한 장소에는 돌봄 담당·식사·잠자리 인계가 없었다. 의식 장소를 생활 보호소로 부르는 설명과 맞지 않는다. 미확인 숨은 건물·귀환로까지 없다고 말하지 않는다.'),
'e6_card_school': ('학교 · 오늘 보호할 실제 준비', '실행한 항목만 상태로 표시한다. 검증 난로, 3자리, 3인분, 두 담당자의 교대, 환자 이동길이 각각 필요하다. 진료소 비축을 전부 가져오거나 겨울 전체를 해결하지 않는다.'),
})


def r13_rec_e456_add(key, title, place, lines, need=(), forbid=(), give=(), flags=(), day=None, label=None):
    ep = int(key[1])
    r13_rec_actions[key] = r13_rec_action(title, place, lines, need=need, forbid=forbid,
        give=give, flags=flags, day=day, episode=ep, label=label)
    r13_rec_effects[key] = lambda s, key=key: r13_rec_e456_effect(s, key)


r13_rec_e456_add('e4_escort', '식기를 돌려놓으며 아빠와 함께 복도를 지난다', 'hall', [
('dad','저녁 식기를 갖다 놓고 같이 올라가자.'),('resident_owlgp','밖에 누구 없소? 문을 열어 주시오.'),('daram','부엉이 할아버지 목소리야!'),
(None,'공개 복도 A는 열려 있었다. 두 사람은 객실 R까지만 들어갔다. 판자문 G 아래 틈 너머 작업칸 P에서 사람이 손을 움직였다.'),
('dad','사람이 살아 있습니다. 너울 씨, 문을 열어 주세요.'),('neoul','밖에서는 못 엽니다. 다른 길을 찾으십시오.'),
('dad','내가 다람이와 여기에 있었습니다. 다람이는 잠긴 칸에 들어가지 않았어요.')], forbid=('e4_discovery',), give=('e4_card_daram','e4_card_parent','e4_card_neoul'), flags=('e4_discovery','e4_parent_seen'), day=7)
r13_rec_e456_add('e4_alone_tool', '혼자 식기를 반납하다 어른을 부르고 문을 벌려 본다', 'room13', [
('resident_owlgp','거기 누구요? 여기 문을 열어 주시오.'),('daram','부엉이 할아버지예요! 어른들, 도와주세요!'),(None,'다람은 공개 입구 A로 객실 R에 들어왔을 뿐, 판자문 G 너머 작업칸 P에는 들어가지 않았다. 기다리며 객실 쪽에서 수리 도구로 G를 벌리려 했다.'),
('neoul','그 도구를 내려놓아라.'),('daram','안에서 살아서 말을 해요. 열어 주세요.'),('neoul','밖에서는 못 연다.'),
(None,'아빠가 와서 다람 옆에 섰다. 경비는 다람에게 아빠와 함께 기다려 달라고 했다. 아빠는 다람 옆 의자를 당겨 앉았다.')], forbid=('e4_discovery',), give=('e4_card_daram','e4_card_tool','e4_card_neoul'), flags=('e4_discovery','e4_tool_used'), day=7)
r13_rec_e456_add('e4_wait', '구조 요청을 듣고 도구에 손대지 않은 채 어른을 기다린다', 'room13', [
('resident_owlgp','문을 열어 주시오.'),('daram','부엉이 할아버지가 살아 있어요!'),(None,'다람은 객실 R에서 어른을 기다렸다. G 너머 P의 사람에게 계속 말을 걸었다. 아빠가 와서 다람과 문 너머를 확인했다.'),
('dad','문을 열어 주세요.'),('neoul','밖에서는 못 엽니다.'),('dad','도구에는 손대지 않았습니다. 먼저 안의 사람을 구합시다.')], forbid=('e4_discovery',), give=('e4_card_daram','e4_card_parent','e4_card_neoul'), flags=('e4_discovery','e4_parent_seen'), day=7)
r13_rec_e456_add('e4_rescue', '나비에게 여는 방법을 물어 부리와 즉시 구조한다', 'kitchen', [
('dad','너울은 못 연다지만, 오늘 이 문을 연 사람을 보셨습니까?'),('nabi','업무 인계 때 너울이 이 레버로 열고 닫는 걸 봤어요. 사람이 아직 안에 있었군요.'),
('buri','아이들은 객실 쪽에서 기다려요. 내가 관리 칸 레버를 올릴게요.'),
(None,'부리가 G를 올렸다. 서리가 작업칸에서 피해자를 옮겨 보온과 진료를 시작했다. 부리가 할아버지의 손을 잡았다. 할아버지가 약하게 손가락을 움직였다.')], need=('e4_discovery',), flags=('e4_fast_rescue',), day=7)
r13_rec_e456_add('e4_nabi7', '나비에게 7일의 열기와 닫기를 따로 묻는다', 'kitchen', [
('dad','수색 내내 지켜보았다는 뜻입니까?'),('nabi','아니에요. 처음 안내할 때 B에서 너울이 L을 올려 G를 여는 걸 봤어요. 둘이 R을 지나 P에 들어갔죠.'),
('nabi','수색 중에는 배식을 했어요. 끝날 때 물품을 받으러 B로 돌아왔고, 혼자 나온 너울이 L을 내려 닫는 걸 봤어요. 그때는 피해자가 이미 따로 나간 줄 알았어요.'),
('dad','내부의 넘어짐은 못 봤고, 두 번의 업무 인계에서 개폐 동작을 직접 본 거군요. 9일 일과 섞지 않겠습니다.')], need=('e4_discovery',), give=('e4_card_nabi7',), flags=('e4_nabi7_heard',), day=8)
r13_rec_e456_add('e4_clinic_alive', '서리에게 구조된 피해자의 회복과 손상을 확인한다', 'clinic', [
('resident_seori','넘어진 손상은 있었지만 치명적인 흉기 상처는 아닙니다. 구조 뒤 보온과 진료를 받았고 회복 중입니다.'),
('dad','살아 있는 사람을 잠그고 구조를 막은 책임을 묻겠습니다. 사망하지 않은 사건을 살인이라고 하지는 않겠습니다.')], need=('e4_victim_alive',), give=('e4_card_seori',), flags=('e4_care_checked',), day=8)
r13_rec_e456_add('e4_clinic_dead', '서리에게 발견부터 늦은 구조까지의 경과를 확인한다', 'clinic', [
(None,'다른 길을 찾는 동안 구조가 지연됐다. 문이 열린 뒤 서리가 옮겼지만 피해자는 회복하지 못했다.'),
('resident_seori','넘어진 손상만으로 이미 끝난 사건이 아닙니다. 다람이 들은 살아 있는 구조 요청과 이후 경과를 함께 보아야 합니다. 추위 속 감금과 구조 지연이 사망 경과에 이어집니다.'),
('resident_seori','정확히 몇 시, 몇 초였으면 살았다고 말할 수는 없습니다. 그래도 발견 전에 이미 숨진 사람이라고 할 수는 없어요.')], need=('e4_victim_dead',), give=('e4_card_seori',), flags=('e4_care_checked',), day=8)
r13_rec_e456_add('e4_mechanism', '부리와 빈 작업칸의 문·레버를 안전하게 시험한다', 'room13', [
('buri','아무도 작업칸에 들어가지 않은 상태에서 확인합시다. 다람이는 객실 쪽에서 나와 같이 봐요.'),
('dad','복도 문과 안쪽 판자문이 같지 않군요. 어느 쪽에 사람이 있었는지부터 짚어 보자.')], need=('e4_discovery',), give=('e4_card_lever',), flags=('e4_mechanism_checked',), day=8, label='r13_rec_e4_inspect_layout')
r13_rec_e456_add('e4_plan', '따닥이 너울 앞에서 설명하는 내일 실측을 듣는다', 'room13', [
('resident_ttadak','내일 9일, G 안쪽 작업칸 P의 벽을 실측하겠습니다. 저는 이 안에 있게 됩니다.'),('neoul','들었습니다.'),
('dad','작업 위치와 시간을 모두 들었군요. 아이는 R에서 기다리고, 문에는 안전 조치를 합시다.'),('resident_seori','10일 식당에서 개폐와 구조 경과를 공개로 확인하겠습니다. 7일과 9일의 일을 나눠 가져와 주세요.')], need=('e4_mechanism_checked',), give=('e4_card_ttadak',), flags=('e4_work_announced',), day=8)
r13_rec_e456_add('e4_wedge', '따닥과 판자문에 버팀목을 설치한다', 'room13', [
('buri','통로 G가 내려오지 못하게 버팀목을 받칩니다. 관리 칸 물품 출입까지 막은 것은 아니에요.'),
(None,'빈 작업칸에서 버팀 상태를 시험했다. 버팀목 설치와 레버 출입 완전 봉쇄는 다른 조치다.')], need=('e4_work_announced',), forbid=('e4_work',), flags=('e4_wedge_set',), day=9)
r13_rec_e456_add('e4_block_lever', '레버를 고정하고 공개 동행·출입 감시까지 배치한다', 'kitchen', [
('buri','레버를 움직일 수 없게 고정했어요. 업무 물품은 제가 문 밖으로 가져다주죠.'),
('nabi','B에 서서 출입을 받지 않겠어요. 따닥의 실측이 끝날 때까지 여기 있습니다.'),
(None,'부리가 고정쇠를 다시 당겨 확인했다. 나비는 출입구 옆에 의자를 가져와 앉았다.')], need=('e4_work_announced',), forbid=('e4_work',), flags=('e4_lever_guarded',), day=9)
r13_rec_e456_add('e4_watch', '나비와 작업 시작의 빈 칸·열린 문·출입선을 확인한다', 'kitchen', [
(None,'K 안은 비어 있고 G는 열려 있었다. B 밖의 업무 탁자에서 나비가 짧은 인계 구간을 맡았다.'),
('nabi','끝날 때까지 이 문을 떠나지 않습니다. 다른 배식은 지금 맡지 않았어요.'),('dad','손동작을 못 보면 못 봤다고 말하고, 실제로 드나든 사람만 구별합시다.')], need=('e4_work_announced',), forbid=('e4_work',), flags=('e4_watch_ready',), day=9)
r13_rec_e456_add('e4_work', '따닥의 실제 실측과 안전 결과를 확인한다', 'room13', [], need=('e4_work_announced',), flags=('e4_work_done',), day=9, label='r13_rec_e4_work_scene')
r13_rec_e456_add('e4_nabi9', '나비에게 9일의 짧은 출입 구간만 확인한다', 'kitchen', [
('nabi','그 짧은 구간엔 너울만 들어갔다 나왔어요. 나는 B를 떠나지 않았습니다. 레버에 닿는 손은 안 보였어요.'),
('dad','7일의 직접 개폐와 9일의 독점 출입은 서로 다른 관찰입니다.')], need=('e4_work_done','e4_watch_ready'), forbid=('e4_day9_prevented',), give=('e4_card_nabi9',), flags=('e4_nabi9_heard',), day=9)

r13_rec_e456_add('e5_school', '학교의 점검 공지와 실제 남는 난방 공간을 확인한다', 'school', [
('resident_teacher','난로 점검을 핑계로 학교를 비우게 하면 아이들은 어디로 가죠?'),('buri','공지에는 한 대의 점검만 있습니다. 이 교실의 난로는 가동 중이고 사용을 계속할 수 있어요.'),
(None,'가족은 불이 들어온 난로와 현재 쓸 교실, 남아 있는 이불을 직접 확인했다. 학교 전체 폐쇄 공지는 아니었다.')], give=('e5_card_notice',), flags=('e5_notice_checked',), forbid=('e5_event_done',))
r13_rec_e456_add('e5_pots', '배식 전 두 냄비의 몸체·뚜껑·원래 몫을 살펴본다', 'school', [
('resident_teacher','깨진 귀가 있는 왼쪽 냄비는 순찰 분들 몫으로 남겨 주세요.'),('resident_bori','아이들은 천 손잡이 냄비에 아이 그림 뚜껑을 써요. 배식할 때는 그 그림을 보고 뜹니다.'),
(None,'같은 크기의 뚜껑 두 개를 나란히 내려 수프를 식혔다. 몸체와 음식은 서로 옮기지 않는다.')], give=('e5_card_pots','e5_card_teacher'), flags=('e5_pots_seen',), day=12, label='r13_rec_e5_inspect_pots')
r13_rec_e456_add('e5_pharmacy', '서리에게 보관약과 선생님의 요청을 묻는다', 'clinic', [
('resident_seori','선생님이 순찰 식사 전에 이 보관약을 쓰고 싶다고 했습니다. 음식에 넣을 물건이 아니에요. 아직 약장 안에 있습니다.'),
('dad','용기가 아직 여기에 있군요. 음식에 넣지 못하게 우선 보관을 지키고, 선생님이 무엇을 걱정하는지도 직접 물어보겠습니다.')], need=('e5_pots_seen',), forbid=('e5_event_done',), give=('e5_card_cabinet',), flags=('e5_drug_in_cabinet',), day=12)
r13_rec_e456_add('e5_lock', '서리와 약장을 잠그고 선생님에게 실제 학교 자리를 보여 준다', 'clinic', [
(None,'서리는 용기가 약장 안에 그대로 있는지 확인한 뒤 잠갔다. 아빠와 함께 선생님을 현재 사용 가능한 교실로 데려갔다.'),
('resident_teacher','아이들을 여기서 지킬 수 있군요. 그 약을 가져가지 않겠습니다.'),('dad','위험한 계획을 막은 겁니다. 일어나지 않은 혼입을 했다고 말하지는 않겠습니다.')], need=('e5_drug_in_cabinet','e5_notice_checked'), forbid=('e5_event_done',), flags=('e5_prevented',), day=12)
r13_rec_e456_add('e5_serve_safe', '정상 냄비를 확인하고 아이들과 저녁을 먹는다', 'school', [
(None,'서리가 잠금 확인을 마치고 학교로 왔다. 선생님과 보리가 몸체 표식에 맞는 뚜껑을 차분히 덮었다.'),
('resident_bori','깨진 귀는 순찰 몫, 천 손잡이와 아이 그림은 아이들 몫. 그대로예요.'),
('kid_saemi','오늘은 같이 먹어요.'),('daram','응. 내일도 따뜻한 데서 먹자.'),('resident_seori','내일 학교 회의에서 위험한 요청과 실제로 막은 일을 구별해 확인합시다.')], need=('e5_prevented','e5_pots_seen'), flags=('e5_event_done',), day=12)
r13_rec_e456_add('e5_serve_accident', '배식 자리로 돌아가 이상을 확인하고 즉시 돌봄을 인계한다', 'school', [
(None,'아빠와 다람이 돌아왔을 때 순찰대가 앞문으로 들어오고 있었다. 조리대에는 두 냄비가 같은 자리에 있었지만, 아이 그림 뚜껑은 왼쪽에 놓여 있었다.'),
('daram','아침엔 그림이 저쪽 아니었나?'),
('resident_bori','아이 그림이 이쪽이네. 여기서 나눠 줄게.'),
(None,'몸체와 수프는 움직이지 않았지만 아이들이 A에서 배식받았다. 이상이 발견되자 즉시 배식을 멈추고 서리에게 돌봄을 요청했다. 보리는 국자를 내려놓고 아이 곁에 무릎을 꿇었다.')], need=('e5_pots_seen',), forbid=('e5_prevented',), flags=('e5_event_done','e5_accident'), day=12)
r13_rec_e456_add('e5_interview', '치료실에서 보리에게 순서와 위치를 묻는다', 'clinic', [
('resident_bori','왼쪽 깨진 귀 냄비를 순찰대 몫으로 남겨 달랬어요. 선생님이 그 통을 비운 것도 그쪽입니다. 그땐 약이라고 몰랐어요.'),
('resident_bori','덮는 순간에는 앞문에서 새미에게 물을 줬어요. 배식할 때 아이 그림이 보이는 냄비에서 떴고요.'),
('dad','아이부터 돌보세요. 저는 여기서 도울 테니, 보신 순서를 천천히 말씀해 주세요.')], need=('e5_accident',), give=('e5_card_bori',), flags=('e5_bori_heard',))
r13_rec_e456_add('e5_saemi', '새미에게 약이 아니라 두 뚜껑을 덮은 사람을 묻는다', 'school', [
('kid_saemi','선생님이 둘 다 덮었어요. 아이 그림이 왼쪽 깨진 귀 위에 갔어요. 보리는 내 앞에서 물을 줬고요.'),
('dad','그 전에 냄비나 수프가 다른 쪽으로 옮겨지지는 않았니?'),('kid_saemi','아니요. 두 뚜껑을 열 때부터 여기서 보리를 기다렸어요. 처음 수프를 나눌 때까지 냄비는 그대로였어요. 다른 냄비에 붓지도 않았어요.'),
('dad','통 안에 무엇이 있었는지까지 본 건 아니지?'),('kid_saemi','그건 몰라요.')], need=('e5_accident',), give=('e5_card_saemi',), flags=('e5_saemi_heard',))
r13_rec_e456_add('e5_bottle', '서리·보리와 실제 반출 용기와 인계 구간을 대조한다', 'clinic', [
('resident_seori','내가 맡던 그 용기입니다. 이 목테 흠집을 확인했어요. 진료실 앞에서 선생님이 보리와 함께 학교 쪽으로 가져갔죠.'),
('resident_bori','진료실 앞에서부터 같이 왔어요. 선생님이 들고 온 통을 조리대에 놓았고, 다시 들어 왼쪽 A에 비웠어요. 통을 바꿔 쥔 적은 없어요.'),
('dad','상표만 같은 다른 병이라고 가정한 게 아니라 실제 인계와 같은 현물을 대조했습니다.')], need=('e5_bori_heard',), give=('e5_card_bottle','e5_card_seori'), flags=('e5_bottle_checked',))
r13_rec_e456_add('e5_care_handoff', '서리에게 아이 돌봄을 인계하고 보리와 회의에 간다', 'clinic', [
('resident_seori','제가 아이들을 계속 돌보겠습니다. 보리 씨는 회의 뒤 교대 시간에 돌아오세요.'),
('resident_bori','여기서 말한 바로 그 순서를, 냄비를 보면서 설명할게요.'),('resident_seori','공개 회의는 학교에서 열립니다. 돌봄은 제가 맡겠습니다.')], need=('e5_bottle_checked','e5_saemi_heard'), flags=('e5_care_handed',), day=13)

r13_rec_e456_add('e6_board', '현재 학교 배분판의 판돌 제외 칸과 적용일을 읽는다', 'school', [
('nabi','판돌 몫이 12일부터 실제 배달에서 빠졌어요. 이 판의 외부 보호 완료 칸을 근거로 들었죠.'),
('dad','부족한 수량표인지, 아직 남은 사람을 이미 떠난 사람으로 적은 것인지 구별해 봅시다.')], give=('e6_card_board',), flags=('e6_board_read',))
r13_rec_e456_add('e6_manifest', '현재 출발 명단의 날짜와 다음 인계 항목을 읽는다', 'gate', [
('resident_siluk','판돌 씨는 13일 저녁 제단으로 모시라고 되어 있소. 그 뒤 치료를 본 적은 없소.'),
('dad','제단 인계, 마을 식사와 숙소 재배정 없음. 날짜뿐 아니라 다음 보호자가 누군지도 확인하겠습니다.')], give=('e6_card_manifest','e6_card_siluk'), flags=('e6_manifest_read',))
r13_rec_e456_add('e6_pandol', '학교에 남은 판돌에게 현재 보호와 실제 출발을 묻는다', 'school', [
('npc_pandol','나는 7일에도 명단에 있었소. 그래도 실제 출발은 13일 저녁이오. 아직 여기서 자고 먹고 있는데 내 몫이 없더군.'),
('dad','떠나기도 전에 오늘 몫이 없어진 거군요. 언제부터 그렇게 적혔는지 함께 확인하죠.')], day=13, give=('e6_card_pandol',), flags=('e6_pandol_seen',))
r13_rec_e456_add('e6_nabi', '나비에게 7일 요청과 12일 수령을 구분해 묻는다', 'school', [
('nabi','7일 오전 인계에서 할머니에게 직접 말했어요. 판돌은 13일 저녁까지 학교에 남으니 12~13일 몫이 필요하다고요.'),
('nabi','12일 받은 배달에는 빠져 있었어요. 그때도 판돌이 학교에 있는 걸 확인했고요. 오후 여관에서 본 13호 사건과는 다른 시간입니다.')], need=('e6_board_read',), give=('e6_card_nabi','e6_card_granny'), flags=('e6_nabi_heard',))
r13_rec_e456_add('e6_munchi', '뭉치에게 같은 자리의 지시와 실제 포장을 묻는다', 'store', [
('resident_mungchi','나비의 요청을 함께 들었어요. 그다음 할머니가 판돌 몫을 12일부터 학교 배달에서 빼고 비축으로 분류하라고 했어요.'),
('resident_mungchi','나는 그 기준대로 포장했고, 나비가 물어서 이 판을 보여 줬어요.'),
('dad','알고 있었다는 사실뿐 아니라 직접 지시와 실제 적용을 따로 확인하겠습니다.')], need=('e6_nabi_heard',), give=('e6_card_munchi',), flags=('e6_munchi_heard','e6_granny_order_heard'))
r13_rec_e456_add('e6_hold', '촌장·바둑이·실룩과 현재 승객을 보호하며 출발을 멈춘다', 'school', [],
    need=('e6_manifest_read',), flags=('e6_transport_paused',), label='r13_rec_e6_hold_scene')
r13_rec_e456_add('e6_altar', '바둑이·촌장과 제단의 실제 돌봄 인계를 확인한다', 'altar', [
('resident_badook','받은 인계는 사람을 돌 앞에 두라는 것이었어요. 여기 확인한 곳엔 식사와 잠자리도, 치료를 맡아 넘겨받는 사람도 없습니다.'),
('dad','실룩이 그 뒤를 못 봤다는 말만 믿지 않고 직접 확인한 겁니다. 이 장소의 실제 인계와 보호소라는 설명이 맞지 않습니다.'),
('resident_ppul','그동안 보호소로 가는 일이라 여겼소. 지금 이 장소와 인계를 확인한 책임은 내가 지겠소.')], need=('e6_transport_paused',), give=('e6_card_badook',), flags=('e6_altar_checked',))
r13_rec_e456_add('e6_research', '엄마 연구 원본을 실제 조각·공동 난로·공간과 대조한다', 'school', [
('mom','원본에 적었다고 믿지 말고 함께 확인하자. 남은 힘을 한곳에 모아, 이 공간이 버티는 범위만 보는 거야.'),
(None,'새 희생이 없는 동안, 가족과 부리는 기존 조각·공동 난로와 같은 사용 공간을 대조했다. 확인한 관찰 시간과 방의 범위를 연구 원본에 적었다.'),
('mom','이 공간에서 확인한 시간의 결과야. 온 마을이 겨울 내내 산다는 약속은 아니야.'),('dad','오늘 보낼 사람에게 실제로 쓸 방과 식사, 교대도 따로 준비하겠습니다.')], need=('reunited',), flags=('e6_research_verified',))
r13_rec_e456_add('e6_heat', '검증한 난로를 점검하고 오늘의 공동 공간을 가동한다', 'school', [
('buri','비어 있는 방까지 데우는 대신 확인한 이 교실을 씁니다. 난로 가동을 직접 확인했어요.'),
(None,'부리가 난로 옆과 맞은편 벽 가까이의 온기를 차례로 확인했다. 열은 열린 복도 끝까지 닿지 않았다. 가족은 따뜻해진 교실 안으로 이불 자리를 모았다.')], need=('e6_research_verified',), give=('e6_card_school',), flags=('e6_heat_ready',))
r13_rec_e456_add('e6_beds', '학교 책상을 옮기고 승객 세 사람의 실제 자리를 편다', 'school', [
(None,'기존 수용자의 자리를 빼앗지 않는 빈 구역을 확인하고 책상을 옮겼다. 준비되어 있던 이불 세 채를 실제로 폈다.'),
('daram','판돌 씨와 이번 승객 두 분 자리는 여기야. 문 앞은 비워 뒀어.')], need=('e6_transport_paused',), give=('e6_card_school',), flags=('e6_beds_ready',))
r13_rec_e456_add('e6_meals', '나비·뭉치와 실제 남은 재료로 세 사람의 식사를 준비한다', 'school', [
('resident_ppul','진료소의 다음 폭설 비축을 전부 풀 수는 없소.'),('dad','비축이 있다는 사실만으로 모든 부족이 해결된다는 주장은 하지 않겠습니다.'),
(None,'나비와 뭉치가 학교에서 지금 쓸 수 있는 재료를 확인하고 세 그릇을 실제로 준비했다. 뭉치가 마지막 재료 상자를 주방에 내려놓고 빈 운반 상자를 가져갔다.'),
('nabi','오늘 이 세 사람에게 낼 몫입니다. 다른 곳의 비축을 전부 끌어오지 않았어요.')], need=('e6_transport_paused',), give=('e6_card_school',), flags=('e6_meals_ready',))
r13_rec_e456_add('e6_care', '서리와 나비의 실제 돌봄 교대와 연락을 맞춘다', 'school', [
('resident_seori','먼저 도착할 때 진료를 맡겠습니다. 이후 나비가 밤 첫 교대를 하고, 저는 다음 교대에 돌아오겠습니다.'),
('nabi','여관 배식은 인계하고 왔어요. 여기 첫 교대가 끝날 때까지 제가 곁에 있을게요.'),
(None,'두 사람이 교대 장소와 시간을 서로 확인했다. 서리가 진료 가방을 열어 첫 자리 옆에 놓았다.')], need=('e6_transport_paused',), give=('e6_card_school',), flags=('e6_care_ready',))
r13_rec_e456_add('e6_route', '실룩·바둑이와 환자가 탈 실제 이동길을 점검한다', 'gate', [
('resident_siluk','제단 아래 길부터 학교 문 앞까지 수레를 끌고 확인했소. 눈이 쌓인 좁은 곳은 치웠고, 한 번에 무리하지 않고 두 차례로 나눠 옮기겠소.'),
('resident_badook','학교 문턱과 복도를 비웠어요. 묶어 데려가지 않고 보호자와 함께 이동합니다.'),
(None,'성인들이 길의 눈과 문턱을 정리하고 수레가 학교 입구까지 지나가는 것을 확인했다. 다람은 아빠 손을 잡고 문 옆에서 수레가 지나가는 것을 지켜봤다.')], need=('e6_transport_paused',), give=('e6_card_school',), flags=('e6_route_ready',))
r13_rec_e456_add('e6_cancel', '촌장의 철회와 바둑이의 강행 준비 해제를 직접 확인한다', 'gate', [
('resident_ppul','이번 강제 제단 이송은 철회하겠소. 남아 보호받을 사람으로 처리하시오.'),
('resident_badook','묶는 끈과 강행 준비를 치웠습니다. 보호 이동으로 바꾸겠습니다.'),
('resident_siluk','수레도 학교로 가는 보호 이동에 쓰겠소.'),
(None,'바둑이가 수레 앞의 끈을 접어 치웠다. 촌장은 실룩에게 학교 문 쪽으로 수레를 돌려 달라고 말했다.')], need=('e6_case_proven',), flags=('e6_order_cancelled',))
r13_rec_e456_add('e6_handoff', '배분판을 바로잡고 실제 식사·잠자리·돌봄을 인계한다', 'school', [
(None,'같은 배분판의 외부 보호 완료를 현재 학교 수용으로 정정했다. 실룩과 바둑이가 세 사람을 준비한 교실 안까지 안내했다.'),
('nabi','판돌 씨, 준비한 식사 여기 있어요. 이불 자리도 바로 옆입니다.'),('resident_seori','제가 먼저 상태를 보겠습니다. 다음 교대도 기다리고 있습니다.'),
(None,'판돌이 따뜻한 그릇을 두 손으로 받았다. 서리가 옆자리에 앉아 이름과 몸 상태를 물었다.')], need=('e6_order_cancelled','e6_heat_ready','e6_beds_ready','e6_meals_ready','e6_care_ready','e6_route_ready'), flags=('e6_actual_handoff',))
r13_rec_e456_add('e6_split_duties', '다음 보호 인계 전 지원을 끊지 못하도록 업무를 나눠 맡긴다', 'school', [
('nabi','나는 실제 수용자를 확인합니다.'),('resident_mungchi','나는 실제 배달과 수령을 맞춥니다.'),('resident_badook','다음 장소의 실제 보호 인계를 확인하기 전엔 여기 지원을 끊지 않겠습니다.'),
('dad','한 사람이 떠나기 전부터 보호 완료라고 써서 몫을 없애는 경로를 닫는 겁니다. 다음 인계 때도 오늘처럼 서로 얼굴을 보고 확인합시다.')], need=('e6_actual_handoff',), flags=('e6_shared_checks',))
r13_rec_e456_add('e6_night', '가족의 현재 상태를 확인하고 학교의 첫 밤을 함께 보낸다', 'school', [], need=('e6_shared_checks',), flags=('e6_first_night',), label='r13_rec_e6_night_scene')


def r13_rec_e456_step(key, question, card, details, right_detail, claims, right_claim, answer):
    """Semantic answer IDs survive option reordering and source wording changes."""
    return dict(id=key, question=question, card=card, details=tuple(details), right_detail=right_detail,
                claims=tuple(claims), right_claim=right_claim, answer=answer)


def r13_rec_e456_hearing(s):
    q = r13_rec_e456_step
    ep=s['episode']; d=set(s['done'])
    if ep == 4:
        if 'e4_tool_used' in d:
            first=q('e4_tool_use','다람 손에 있던 도구로 무엇을 했는지 어디서 알 수 있을까?','e4_card_tool',
            [('held','경비가 왔을 때 도구를 쥔 손','손에 있었다는 것만으로 어디에 썼는지는 알 수 없어요.'),('pry','도구 끝과 객실 쪽 벌림 자국',''),('found','피해자 가까이 놓였던 위치','두 사람은 판자문 양쪽에 있었습니다. 방 이름만 같다고 같은 자리는 아니에요.')],'pry',
            [('before','문을 잠그기 전에 공격하고 나중에 벌렸다','그 앞의 일은 아직 못 봤습니다. 지금 자국이 어떤 사용과 맞는지부터 봐야 해요.'),('rescue','객실 쪽에서 문을 벌리려 한 자국이다','')],'rescue',
            '이 끝이 들어간 곳은 객실 쪽 문틈이에요. 다람이가 문을 벌리려 했다는 말과 맞습니다. 그 전에 무슨 일이 있었는지는 더 들어 봐야죠.')
        else:
            first=q('e4_daram_side','다람이 안쪽 칸에 있었다는 말과 맞지 않는 것은?','e4_card_parent',
            [('together','아빠가 객실 쪽에서 다람과 함께 있던 때',''),('door','공개 복도로 난 문이 열려 있던 상태','복도 문은 객실로 통합니다. 그 안쪽 판자문까지 열렸다는 뜻은 아니에요.')],'together',
            [('same_room','13호 안이니 피해자와 같은 칸에 있었다','객실과 작업칸 사이에 판자문이 있었어요. 어느 쪽인지 나눠 봐야 합니다.'),('outside','다람은 판자문 바깥 객실에서 도움을 청했다','')],'outside',
            '제가 다람이 옆에 있었어요. 할아버지는 판자문 너머였고요. 다람이가 그 안에 있었다고 하진 마세요.')
        steps=[first,
        q('e4_alive','처음 발견했을 때 이미 숨진 뒤였다는 말에 무엇이 걸릴까?','e4_card_daram',
        [('sound9','따닥이 다음 실측 때 낸 작업 소리','따닥의 실측은 9일 일이에요. 지금은 7일 처음 발견했을 때를 묻고 있어요.'),('voice7','7일 판자문 너머에서 들은 문을 열어 달라는 말','')],'voice7',
        [('alive','다람이 왔을 때 할아버지는 살아 있었다',''),('knock','기계 소리를 사람 목소리로 잘못 들었을 수 있다','다람이는 단순한 소리가 아니라 문을 열어 달라는 말과 할아버지 목소리를 들었어요.')],'alive',
        '다람이는 문을 열어 달라는 할아버지 말을 들었어요. 처음 발견했을 때 이미 끝난 일이라고 할 수는 없죠.'),
        q('e4_course','넘어진 손상만으로 설명할 수 없는 부분은?','e4_card_seori',
        [('injury','몸에 남아 있던 넘어짐 손상','넘어진 것은 맞아요. 하지만 그 손상이 곧 숨진 까닭인지는 이후 경과를 같이 봐야 합니다.'),('course','살아 있던 구조 요청부터 늦게 문을 연 뒤까지','')],'course',
        [('fatal_fall','넘어진 순간 이미 돌이킬 수 없는 치명상을 입었다','서리가 본 손상은 그런 치명상이 아니었어요. 살아서 도움을 청한 뒤에도 문이 열리지 않았죠.'),('delay','다친 채 추운 칸에 갇혀 구조가 늦어졌다','')],'delay',
        '넘어진 것은 맞지만 그 자리에서 이미 끝난 건 아니었어요. 살아서 도움을 청한 뒤에도 추운 칸에서 나오지 못했습니다.'),
        q('e4_external_open','밖에서는 못 연다는 말과 직접 대조할 부분은?','e4_card_lever',
        [('lever','관리 칸 레버를 올리자 판자문이 열린 연결',''),('entry','복도에서 객실로 들어가는 열린 문','그 문은 다람이가 들어온 문이에요. 할아버지를 가둔 안쪽 판자문은 따로 있습니다.'),('weight','무거운 판자문 자체의 무게','무거우면 떨어질 수 있다는 말과, 걸쇠가 걸려 못 나오는 것은 다릅니다.')],'lever',
        [('inside','안쪽 사람이 당겨야만 걸쇠가 풀린다','빈 작업칸에 아무도 없을 때 부리가 바깥 레버로 열었어요.'),('outside','관리 칸에서 안쪽 문을 열고 잠글 수 있다','')],'outside',
        '빈 칸에서 함께 해 봤잖아요. 부리가 관리 칸 레버를 올리자 문이 열렸습니다. 밖에서 할 수 없는 일이 아니었어요.'),
        q('e4_knowledge7','너울이 그 여는 법을 이미 알았다는 것은 언제 보았을까?','e4_card_nabi7',
        [('visit','7일 너울과 할아버지가 함께 들어간 때','함께 들어간 사실만으로 누가 문을 열었는지는 정할 수 없어요.'),('open_close','7일 업무 인계 때 너울이 직접 열고 닫은 때',''),('later','나비가 9일 출입구를 지킨 때','9일 문 앞에서 지킨 일은 따로 있어요. 7일에 무엇을 알았는지 먼저 봅시다.')],'open_close',
        [('knew','너울은 그날 직접 레버로 문을 열었다',''),('borrowed','나비가 문을 열어 주고 너울은 닫기만 했다','나비는 처음에도 너울 손으로 여는 것을 봤다고 했어요. 닫는 장면만 본 게 아닙니다.')],'knew',
        '나비 씨는 수색하는 동안엔 다른 일을 했어요. 그래도 처음 문을 연 손과 나중에 닫은 손은 보았다고 했습니다. 둘 다 너울 씨였어요.'),
        q('e4_refusal','너울의 설명에서 서로 맞지 않는 일을 이으려면?','e4_card_neoul',
        [('alone','너울이 혼자 나온 뒤 문이 닫혀 있었다','혼자 나온 사실만으로 안에 사람이 남았음을 알았는지는 더 물어야 해요.'),('report','직접 문을 연 일과 살아 있다는 보고 뒤 못 연다고 한 답','')],'report',
        [('mistake','여는 법을 몰라서 다른 길을 찾게 했다','그날 처음에 스스로 열었어요. 모른다는 말은 그 행동과 맞지 않습니다.'),('blocked','열 줄 알면서 살아 있는 사람의 구조를 막았다','')],'blocked',
        '너울 씨, 그날 직접 문을 열었잖아요. 다람이가 안에 사람이 살아 있다고 했는데, 왜 우리한테는 못 연다고 했어요?')]
        if 'e4_card_nabi9' in s['facts'] and 'e4_day9_prevented' not in d:
            steps += [
            q('e4_access9','9일에는 어느 짧은 구간을 맞춰 봐야 할까?','e4_card_nabi9',
            [('interval','빈 관리 칸과 열린 문을 확인한 뒤 너울이 나올 때까지',''),('whole_day','아침부터 저녁까지 주방에 왔던 사람 전체','나비가 그 하루를 전부 지킨 것은 아닙니다. 일 시작의 짧은 인계 시간은 떠나지 않았고요.')],'interval',
            [('earlier','누군가 미리 관리 칸 안에 남아 있었을 수 있다','일 시작 전에 칸이 비어 있는 것을 함께 확인했어요.'),('sole','그 구간 관리 칸에 들어간 사람은 너울뿐이다',''),('automatic','너울이 지나가자 문이 저절로 잠겼다','부리와 해 본 걸쇠는 사람이 레버를 끝까지 내려야 걸렸어요.')],'sole',
            '하루 종일 누가 왔는지를 묻는 게 아닙니다. 빈 칸을 확인한 뒤 문이 움직일 때까지, 너울 씨만 들어갔다 나왔어요.'),
            q('e4_work_warning','따닥이 안에 있을 줄 몰랐다는 답에는?','e4_card_ttadak',
            [('after','구조 뒤 따닥에게 들은 다친 경위','지금 묻는 건 너울이 그 전에 작업을 알았느냐는 거예요.'),('before','8일 너울 앞에서 말한 9일 작업 위치와 시간','')],'before',
            [('heard','너울은 따닥이 안쪽 칸에서 일할 것을 들었다',''),('room_only','너울은 객실 바깥만 잰다고 들었다','따닥은 안쪽 칸의 벽을 잰다고 위치까지 짚었어요. 저희도 그 자리에 있었습니다.')],'heard',
            '따닥 씨가 전날 그 안에서 실측한다고 말했어요. 너울 씨도 바로 앞에서 들었고요. 아무도 없는 줄 알았다는 말은 맞지 않습니다.')]
        return steps
    if ep == 5:
        if s['e5_poison_blocked']:
            return [
            q('e5_cabinet_kept','선생님이 약을 음식에 넣었다고 말할 수 있을까?','e5_card_cabinet',
            [('request','식사 전에 약을 쓰고 싶다고 한 요청','위험한 생각을 한 것은 맞지만, 요청과 실제로 가져다 넣은 것은 달라요.'),('locked','안의 용기를 확인한 뒤 잠근 약장','')],'locked',
            [('mixed','요청한 뒤라면 잠그기 전에 조금 덜어 갔을 것이다','서리와 용기가 그대로 있는지 확인한 뒤 잠갔어요. 덜어 간 모습을 본 사람은 없습니다.'),('stopped','약이 나가기 전에 계획을 멈췄다','')],'stopped',
            '서리와 함께 안의 용기를 확인하고 잠갔어요. 위험한 요청은 했지만, 그 약이 학교로 나간 것은 아닙니다.'),
            q('e5_room_kept','아이들이 쫓겨날 것이라는 걱정과 맞춰 볼 것은?','e5_card_notice',
            [('one_stove','난로 한 대 점검과 지금 쓸 수 있는 교실',''),('order','학교를 비워야 할지 모른다는 선생님의 걱정','그 걱정 때문에 직접 공지를 보러 갔어요. 실제로 어디를 비우라는지는 공지와 현재 방을 같이 봐야 합니다.')],'one_stove',
            [('waiting','점검하는 동안 아이들을 모두 밖에서 기다리게 해야 한다','점검하지 않는 난로와 사용 가능한 교실을 함께 봤습니다. 아이들이 머물 자리는 남아 있어요.'),('room','현재 쓰는 교실에서 계속 아이들을 돌볼 수 있다','')],'room',
            '점검은 한 대였고, 이 교실은 계속 쓸 수 있었어요. 약 없이도 아이들이 여기서 저녁을 먹었습니다.')]
        return [
        q('e5_body','아이 그림이 얹힌 냄비, 아침에도 아이들 몫이었을까?','e5_card_pots',
        [('drawing','지금 얹혀 있는 아이 그림 뚜껑','그 그림은 보리가 어디서 뜰지 정하는 표식이었어요. 떼어 옮길 수 있는 뚜껑이지요.'),('fixed_ear','뚜껑을 내려도 남는 깨진 귀','')],'fixed_ear',
        [('adult','아침에 순찰대에게 남겨 달랬던 몸체다',''),('children','아이 그림이 있으니 아침의 아이 냄비다','아침에 아이 그림은 천 손잡이 냄비 위에 있었어요. 지금 깨진 귀 위에 놓인 그림만 따라가면 몸체를 놓칩니다.')],'adult',
        '그림은 아이들 것이 맞아요. 그런데 그 밑의 깨진 귀는 아침에 순찰대 몫으로 남기라던 냄비에 있었어요.'),
        q('e5_original_target','약을 넣은 곳과 원래 남겨 달라는 요청을 어떻게 이을까?','e5_card_bori',
        [('served','나중에 보리가 아이들에게 떠 준 냄비','누가 먹었는지는 알 수 있어요. 하지만 넣을 때 누구에게 주려 했는지는 앞선 요청과 함께 봐야 해요.'),('pour_request','같은 깨진 귀 냄비에 붓는 모습과 앞선 순찰대 몫 요청','')],'pour_request',
        [('child_intent','아이들이 먹었으니 처음부터 아이들에게 넣은 것이다','보리가 들은 앞선 요청은 순찰대 몫이었어요. 뒤에 바뀐 뚜껑 때문에 먹은 사람과 처음 남겨 둔 대상이 달라졌습니다.'),('adult_pot','선생님이 약을 넣은 몸체는 원래 순찰대 몫이었다','')],'adult_pot',
        '아이들을 겨냥했다고 처음 생각한 건 거두겠어요. 보리가 본 건 순찰대 몫으로 남겨 둔 그 냄비에 붓는 모습입니다.'),
        q('e5_label_path','같은 냄비의 음식이 아이들에게 간 길을 되짚으려면?','e5_card_pots',
        [('soup','두 냄비의 수프를 서로 바꿔 놓는다','새미는 열 때부터 배식까지 보았고, 수프를 옮기지는 않았다고 했어요.'),('bodies','깨진 귀와 천 손잡이 냄비 위치를 바꾼다','두 몸체는 같은 자리에 있었어요. 움직인 것은 위에 덮은 물건입니다.'),('lids','몸체는 두고 두 뚜껑만 아침 자리로 돌린다','')],'lids',
        [('label','바뀐 그림을 따라 원래 순찰대 냄비에서 아이들에게 떴다',''),('choice','보리가 순찰대 몫인 줄 알고 아이들 몫을 빼앗아 줬다','보리는 지금 보이는 아이 그림을 따라 떴다고 했어요. 그 그림을 누가 바꾸었는지 확인해야 합니다.')],'label',
        '음식은 그 냄비 안에 그대로예요. 아이 그림이 옮겨가자 보리는 그쪽에서 떴습니다. 뚜껑만 바뀌어도 먹는 사람이 달라진 거죠.'),
        q('e5_lid_actor','보리가 배식 전에 뚜껑을 바꿨다는 말에 무엇을 맞춰 볼까?','e5_card_saemi',
        [('hands','선생님이 두 뚜껑을 덮을 때 앞문에서 물을 주던 보리',''),('ladle','나중에 보리가 국자를 들고 있던 모습','국자를 든 것은 배식 때예요. 뚜껑을 덮을 때 누구 손이 어디에 있었는지와는 다릅니다.')],'hands',
        [('bori','보리가 물을 나눠 준 뒤 돌아와 두 뚜껑을 바꿨다','새미는 첫 배식까지 기다리며 조리대를 봤어요. 그 사이 다시 뚜껑을 바꾸는 사람은 없었습니다.'),('teacher','마지막으로 두 뚜껑을 덮은 사람은 선생님이다','')],'teacher',
        '선생님이 덮을 때 보리는 새미 앞에서 물을 주고 있었어요. 새미는 첫 배식까지 그 두 냄비를 보고 있었습니다.'),
        q('e5_same_bottle','학교의 통이 서리가 보관하던 바로 그 통인지는?','e5_card_bottle',
        [('label','같은 표기가 붙은 용기라는 점','표기만 같으면 다른 통일 수도 있죠. 이번에는 가지고 오는 길까지 함께 확인했어요.'),('chain','목테 흠집과 진료실 앞부터 학교까지 함께 온 인계','')],'chain',
        [('other','학교 조리대에서 비슷한 조미료 통으로 바꿔 들었을 수 있다','보리는 함께 온 통을 내려놓았다 다시 드는 것을 봤고, 바꿔 쥔 적은 없다고 했어요.'),('linked','서리가 알던 내용물과 보리가 본 붓는 행동이 같은 통으로 이어진다','')],'linked',
        '서리는 그 통에 무엇이 들었는지 압니다. 보리는 진료실 앞에서 함께 와, 같은 통을 냄비에 비우는 것을 봤어요. 둘의 말을 그 길로 잇는 겁니다.'),
        q('e5_responsibility','아이들을 노린 게 아니었다는 말 뒤에도 남는 일은?','e5_card_teacher',
        [('motive','아이들이 쫓겨날까 두려웠다는 설명','그 두려움은 들었어요. 그래도 누가 약을 넣고 누구 손으로 뚜껑을 덮었는지는 바뀌지 않습니다.'),('acts','순찰대 몫에 넣은 약과 마지막으로 덮은 두 뚜껑','')],'acts',
        [('teacher_acts','선생님의 약 넣기와 뚜껑 바꾸기가 아이들 배식으로 이어졌다',''),('bori_only','아이들에게 뜬 보리의 잘못만 남는다','보리가 따른 아이 그림은 선생님이 다른 몸체 위에 덮은 것입니다. 그 앞의 행동을 지울 수는 없어요.')],'teacher_acts',
        '아이들을 노렸다고 몰아가지는 않겠어요. 그래도 약을 넣고 뚜껑을 바꾼 일까지 보리에게 떠넘기진 마세요.')]
    return [
    q('e6_false_status','판돌의 몫이 줄었다는 것과 다른 문제는 어디에 있을까?','e6_card_board',
    [('reserve','비축 쪽에 남겨 둔 전체 물자','비축도 필요하다는 말은 맞아요. 남아 있는 사람을 어떤 상태로 적었는지부터 봅시다.'),('complete','판돌의 외부 보호 완료 칸과 12일 적용일','')],'complete',
    [('less','다른 주민처럼 식사 양을 조금 줄인 기록이다','양을 줄였다고 적힌 게 아니라 밖에서 보호가 끝났다고 적혀 있어요. 그래서 학교 몫 전체가 빠졌습니다.'),('excluded','이미 다른 곳에서 보호받는 사람처럼 학교 몫에서 빠졌다','')],'excluded',
    '이건 적게 나눠 주자는 표가 아니에요. 판돌 씨는 이미 다른 데서 보호받는다며 학교에서 먹을 사람에서 빠져 있습니다.'),
    q('e6_dates','떠날 사람을 미리 적었을 뿐이라는 말과 어느 날짜를 맞춰 볼까?','e6_card_manifest',
    [('issued','명단을 처음 만든 7일','명단을 적은 날과 실제로 떠나는 날은 달라요. 그 사이에도 학교에서 먹고 있었죠.'),('departure','13일 저녁 출발과 12일부터 빠진 학교 몫','')],'departure',
    [('early','학교에 남아 먹어야 할 동안 몫이 먼저 끊겼다',''),('simultaneous','떠나는 날과 같은 날부터 빠졌으니 빈틈이 없다','학교 몫은 12일부터 빠졌고 출발은 13일 저녁입니다. 그동안 먹을 곳을 어디에도 넘기지 않았어요.')],'early',
    '출발은 13일 저녁인데 몫은 12일부터 빠졌어요. 떠나기 전까지 여기서 먹어야 했던 겁니다.'),
    q('e6_prior_notice','할머니는 판돌이 남아 있다는 말을 언제 들었을까?','e6_card_nabi',
    [('receipt','12일 나비가 배달을 받아 몫이 없음을 안 때','그날 빠진 것을 알게 된 사람은 나비예요. 할머니에게 미리 무엇을 말했는지가 필요합니다.'),('request7','7일 인계 자리에서 13일 저녁까지의 식사를 부탁한 때','')],'request7',
    [('notice','제외가 적용되기 전에 남을 기간과 식사 필요를 들었다',''),('late','배달이 끝난 뒤에야 판돌이 남았다는 소식을 들었다','나비가 부탁한 것은 7일, 빠진 배달은 12일이에요. 부탁이 먼저였습니다.')],'notice',
    '나비 씨는 배달이 빠진 뒤 처음 말한 게 아니에요. 7일에, 13일 저녁까지 먹을 몫이 필요하다고 직접 부탁했습니다.'),
    q('e6_order','그 부탁을 들은 것과 빼라고 시킨 것은 다르다. 빠진 연결은?','e6_card_munchi',
    [('direct','같은 자리에서 받은 제외 지시와 그 기준대로 한 포장',''),('handwriting','배분판에 적힌 글씨 모양','글씨를 쓴 사람과 빼라고 시킨 사람이 다를 수도 있죠. 뭉치가 직접 들은 말을 물어야 합니다.')],'direct',
    [('mistake','뭉치가 날짜를 잘못 읽어 혼자 빼 버렸다','뭉치는 12일부터 빼라는 말을 직접 들었고 그 날짜대로 포장했다고 했어요.'),('order_applied','할머니가 빼라고 했고 뭉치가 그 말대로 포장했다','')],'order_applied',
    '뭉치가 날짜를 잘못 읽은 게 아닙니다. 할머니가 12일부터 빼라고 했고, 뭉치는 그 말대로 학교 배달을 꾸렸어요.'),
    q('e6_next_carer','그쪽에서 맡을 거라는 말은 명단 어디로 확인할까?','e6_card_manifest',
    [('destination','제단 목적지와 식사·숙소를 다시 맡기는 항목',''),('passenger','판돌의 이름과 출발 시간','누가 언제 가는지는 알 수 있어요. 그 뒤 누가 밥과 잠자리를 맡는지는 다른 항목입니다.')],'destination',
    [('handover','제단이라는 이름만으로 생활 보호가 이어졌다고 할 수 없다',''),('assume','목적지가 적혔으니 도착 뒤 누군가 돌볼 것이다','목적지를 아는 것과 다음 보호자를 확인한 것은 달라요. 그다음 돌볼 사람이 있는지는 직접 봐야 알 수 있어요.')],'handover',
    '수레가 어디까지 가는지는 적혔어요. 그다음 누가 식사와 잠자리를 맡는지는 없습니다. 그래서 그곳에서 누가 맞아 주는지까지 확인해야 해요.'),
    q('e6_altar_care','직접 가 본 제단에서는 어떤 인계가 기다리고 있었을까?','e6_card_badook',
    [('outside','실룩이 문 안쪽을 못 보았다는 말','못 보았다는 말만으로 안에 아무도 없다고 할 수 없어요. 바둑이와 함께 직접 본 것을 봅시다.'),('actual','돌 앞에 사람을 두는 자리와 돌봄·식사·잠자리 인계의 부재','')],'actual',
    [('temporary','돌 앞에서 기다리면 준비된 의료진에게 곧 넘겨질 것이다','받은 지시는 돌 앞에 두라는 것이었어요. 현장에서도 그다음 돌봄을 맡을 사람이나 준비는 없었습니다.'),('not_shelter','확인한 인계는 사람을 먹이고 재우는 보호소 인계가 아니다','')],'not_shelter',
    '바둑이가 받은 일은 사람을 돌 앞에 두는 것이었어요. 우리가 본 자리에는 그분들이 먹고 잘 준비도, 이어서 돌볼 사람도 없었습니다.'),
    q('e6_today_heat','영원히 버틸 수 없다는 말은 맞다. 그래도 오늘에 관해 확인한 것은?','research',
    [('old_day','예전에 낮 동안 따뜻했던 기록','그 좋은 낮 기록만으로 오늘 밤의 방을 고를 수는 없어요. 지금 함께 해 본 결과가 필요합니다.'),('tested','새 희생 없이 현재 난로와 교실에서 확인한 시간','')],'tested',
    [('today','확인하고 준비한 이 공간에서는 오늘을 버틸 다른 길이 있다',''),('wait','겨울 전체가 해결되지 않았으니 오늘도 반드시 보내야 한다','앞으로의 모든 답을 모른다는 것과 오늘 방법이 없다는 것은 달라요. 오늘 쓸 공간은 함께 확인했습니다.')],'today',
    '엄마 말대로 영원히는 못 버팁니다. 그래도 새로 사람을 보내지 않은 동안 이 교실이 따뜻해지는 건 함께 봤어요. 오늘 이분들을 돌 앞에 두어야만 하는 건 아니에요.'),
    q('e6_real_preparation','난로 외에 지금 이분들 곁에 놓을 수 있는 것은?','e6_card_school',
    [('promise','도와주겠다고 한 주민들의 약속','고마운 말이지만 아직 음식과 자리가 놓이지 않았다면 그대로 데려올 수는 없어요.'),('prepared','펴 놓은 세 자리·준비한 세 식사·두 담당자·확인한 이동길','')],'prepared',
    [('heat_only','난로가 켜졌으니 식사와 교대는 나중에 구하면 된다','따뜻해도 먹고 돌볼 사람이 필요해요. 나비와 서리가 준비한 것을 지금 함께 맞춰 봅시다.'),('care_now','확인한 세 사람의 식사와 잠자리와 돌봄을 오늘 넘길 수 있다','')],'care_now',
    '이불은 폈고 세 그릇도 준비했어요. 서리와 나비가 교대를 맞췄고 수레가 지날 길도 확인했습니다. 이제 그분들을 여기로 모셔야죠.'),
    q('e6_granny_choice','남아 있을 방법이 없었다는 말 앞에서 할머니에게 물을 것은?','e6_card_granny',
    [('known_order','판돌이 남는다는 부탁 뒤에도 몫을 빼라는 지시',''),('transport_order','너울이 운행을 맡았다는 사실만','너울의 운행과는 별도로, 누가 남아 먹을 몫을 빼라고 했는지 확인했어요.')],'known_order',
    [('copy','이미 떠난 사람이라고 믿고 명단만 옮겨 적었다','나비는 남을 날짜를 직접 말했고, 뭉치는 그 뒤 빼라는 지시를 받았어요. 이미 떠난 줄 알았다는 말과 맞지 않습니다.'),('restore','남아 있는 줄 알면서 끊은 몫을 돌려놓아야 한다','')],'restore',
    '할머니, 판돌 씨가 아직 학교에 있다는 걸 들으셨잖아요. 그런데도 그분 몫을 빼라고 하셨어요. 남아 있는 사람의 밥과 잠자리는 돌려놔야죠.')]


def r13_rec_e456_ready(s):
    ep=s['episode']; d=set(s['done']); e=s['episodes'][str(ep)]
    if s['day'] != {4:10,5:13,6:14}[ep]: return '회의 날짜가 아니다. 오늘의 현장을 먼저 확인하자.'
    if e['verdict'] in ('complete_today','prevented','contamination_responsibility','confinement_responsibility'): return '그 이야기는 함께 확인했어. 이제 남은 사람들을 돌보러 가자.'
    if ep==4 and not {'e4_nabi7_heard','e4_care_checked','e4_mechanism_checked','e4_work_done'} <= d:
        return '7일의 직접 개폐, 구조·진료 경과, 안전한 장치 확인과 9일의 실제 결과가 필요하다.'
    if ep==5 and 'e5_event_done' not in d: return '실제로 배식과 돌봄이 어떻게 됐는지 먼저 확인하자.'
    if ep==5 and not s['e5_poison_blocked'] and 'e5_care_handed' not in d: return '조사에서 보리·새미·용기 인계를 듣고 아이 돌봄을 인계한 뒤 회의하자.'
    if ep==6:
        if not {'e6_board_read','e6_manifest_read','e6_nabi_heard','e6_munchi_heard'} <= d: return '현재 배분과 출발 명단, 인지·지시·실제 적용을 확인하자.'
        h=e['hearing']
        if h>=4 and 'e6_transport_paused' not in d: return '배제 책임은 확인했다. 우선 현재 승객을 보호하며 운행을 멈추자.'
        if h>=5 and 'e6_altar_checked' not in d: return '배제 책임만으로 끝내지 말고 제단의 실제 인계를 확인하자. 승객들을 기다리게 해 둔 동안 우리가 가서 보고 오자.'
        if h>=6 and 'e6_research_verified' not in d:
            if s['mother']=='M2' and 'research' in s['facts']:
                return '엄마에게 받은 원본을 현재 난로와 교실에 대조해 보자. 승객들은 계속 보호하고 있어.'
            if s['mother']=='M1':
                return '엄마와 약속한 지금의 만남을 확인하자. 만나서 받은 원본도 난로와 교실에 직접 대조해야 해. 승객들은 계속 보호하자.'
            return '엄마에게 지금 연락할 길을 따라가자. 함께 만나서 원본을 받은 뒤 난로와 교실을 살펴보자. 승객들은 계속 보호하자.'
        if h>=7 and not r13_rec_e6_resources_ready(s): return '난로·세 자리·세 식사·두 교대·환자 이동길의 빠진 준비를 실제로 채우자.'
    return None


def r13_rec_e6_resources_ready(s):
    r=s['episodes']['6']['resources']
    return r['heat'] and r['beds']>=3 and r['meals']>=3 and r['carers']>=2 and r['route']


def r13_rec_e456_present(s, card, detail, claim):
    reason=r13_rec_e456_ready(s)
    if reason: return copy.deepcopy(s), reason, False
    if card not in s['facts']: raise ValueError('Unearned presentation')
    n=copy.deepcopy(s); e=n['episodes'][str(n['episode'])]; steps=r13_rec_e456_hearing(n)
    if e['hearing']>=len(steps): return n, '말만 끝내고 갈 수는 없어. 기다리는 분들을 학교로 모셔야 해.',False
    step=steps[e['hearing']]
    if card!=step['card']:
        return n, '이 이야기는 다른 사람이 본 장면이에요. 지금 누구의 어느 말을 묻고 있는지 다시 보죠.',False
    detail_options={item[0]:item for item in step['details']}
    claim_options={item[0]:item for item in step['claims']}
    if detail not in detail_options or claim not in claim_options:
        return n, '고른 답을 다시 확인하자. 이름이 없는 선택을 자료와 연결할 수는 없어.',False
    if detail!=step['right_detail']:
        return n, detail_options[detail][2],False
    if claim!=step['right_claim']:
        return n, claim_options[claim][2],False
    e['selected'].append(dict(step=step['id'],card=card,detail=detail,claim=claim));e['hearing']+=1
    if n['episode']==6 and e['hearing']==4:
        n=r13_rec_e456_flag(n,'e6_exclusion_proven')
        n['episodes']['6']['verdict']='exclusion_proven_relief_pending'
    e=n['episodes'][str(n['episode'])]
    if e['hearing']==len(steps):
        if n['episode']==4:
            e['verdict']='confinement_responsibility'; n['neoul']='detained';n['daram']='with_parent'
        elif n['episode']==5: e['verdict']='prevented' if n['e5_poison_blocked'] else 'contamination_responsibility'
        else:
            e['verdict']='case_proven_execution_pending'
            n=r13_rec_e456_flag(n,'e6_case_proven')
    return n,step['answer'],True


def r13_rec_e456_done(s):
    e=s['episodes'].get(str(s['episode']),{})
    return e.get('verdict') in ('confinement_responsibility','prevented','contamination_responsibility','complete_today')


for _ep,_title,_start,_end in ((4,'13호 A · 감금과 구조 방해',7,10),(5,'수프 B · 몸체와 이동 표식',11,13),(6,'최종 C · 오늘의 강제 희생 중단',13,14)):
    r13_rec_episodes[_ep]=dict(title=_title,start_day=_start,end_day=_end,hearing_label='r13_recommended_ep%d_hearing'%_ep,next_label=None)
    r13_rec_episode_start[_ep]=lambda s,ep=_ep:r13_rec_e456_state(s,ep)
    r13_rec_day_advance[_ep]=r13_rec_e456_advance
    r13_rec_advance_block[_ep]=r13_rec_e456_block
    r13_rec_episode_done[_ep]=r13_rec_e456_done

# Explicit world click targets. These are existing episode character IDs, not invented witnesses.
_r13_rec_e456_targets = {
'e4_escort':(None,'가족의 저녁 식기'),'e4_alone_tool':(None,'식기와 객실 문'),'e4_wait':(None,'객실 문'),
'e4_rescue':('nabi',None),'e4_nabi7':('nabi',None),'e4_clinic_alive':('resident_seori',None),'e4_clinic_dead':('resident_seori',None),
'e4_mechanism':(None,'판자문과 레버'),'e4_plan':('resident_ttadak',None),'e4_wedge':('buri',None),'e4_block_lever':('buri',None),'e4_watch':('nabi',None),'e4_work':('resident_ttadak',None),'e4_nabi9':('nabi',None),
'e5_school':('resident_teacher',None),'e5_pots':(None,'두 냄비'),'e5_pharmacy':('resident_seori',None),'e5_lock':(None,'보관 약장'),
'e5_serve_safe':('resident_bori',None),'e5_serve_accident':('resident_bori',None),'e5_interview':('resident_bori',None),'e5_saemi':('kid_saemi',None),'e5_bottle':(None,'반출 용기'),'e5_care_handoff':('resident_seori',None),
'e6_board':(None,'학교 배분판'),'e6_manifest':(None,'현재 출발 명단'),'e6_pandol':('npc_pandol',None),'e6_nabi':('nabi',None),'e6_munchi':('resident_mungchi',None),
'e6_hold':('resident_ppul',None),'e6_altar':('resident_badook',None),'e6_research':('mom',None),'e6_heat':(None,'공동 난로'),
'e6_beds':(None,'실제 이불 자리'),'e6_meals':('nabi',None),'e6_care':('resident_seori',None),'e6_route':('resident_siluk',None),'e6_cancel':('resident_ppul',None),
'e6_handoff':('resident_badook',None),'e6_split_duties':('resident_mungchi',None),'e6_night':(None,'가족의 잠자리')}
for _key, (_person, _object) in _r13_rec_e456_targets.items():
    r13_rec_actions[_key]['target_person'] = _person
    r13_rec_actions[_key]['target_object'] = _object


def r13_rec_e456_challenge(s):
    ep=s['episode']; h=s['episodes'][str(ep)]['hearing']
    if ep==4:
        lines=[('neoul','발견한 아이가 그 방에 있었잖습니까. 구조였다는 말만 믿으란 겁니까?'),
        ('neoul','그 사람이 다람이 오기 전에 이미 치명상을 입었을 수도 있지요.'),
        ('neoul','넘어져 다친 일까지 내 책임이라고 단정할 수는 없잖습니까.'),
        ('neoul','문이 낡아서 내려간 것일 수도 있습니다. 밖에서는 열 수 없었어요.'),
        ('neoul','시험해 봤다는 말과 내가 그때 여는 법을 알았다는 말은 다릅니다.'),
        ('neoul','그 안에 사람이 남았는지 알았다고요? 아이의 보고를 듣고 다른 길을 찾으라고 했을 뿐입니다.'),
        ('neoul','9일 주방에는 누구든 들어갈 수 있었잖습니까.'),
        ('neoul','안에 따닥이 있는 줄은 몰랐을 수도 있지요.')]
        return [lines[min(h,len(lines)-1)]]
    if ep==5 and s['e5_poison_blocked']:
        return [[('resident_teacher','내가 약을 넣었다고 심리하는 건가요? 가져가지도 않았어요.')],
                [('resident_teacher','그래도 학교에서 나가라고 하면 아이들이 갈 곳은 없어요.')]][min(h,1)]
    if ep==5:
        lines=[('resident_teacher','아이들 냄비는 건드리지 않았어요. 아이들에게 떠 준 건 보리예요.'),
        ('resident_teacher','그림이 바뀌었다고 수프가 바뀌나요? 아이들을 겨냥했다고 단정하지 마세요.'),
        ('resident_teacher','그렇다면 보리가 잘못 떠 준 일 아닌가요.'),
        ('resident_teacher','보리가 배식하며 뚜껑을 바꿨을 수도 있죠.'),
        ('resident_teacher','통이 비어 있다고 그 안에 무엇이 있었는지 어떻게 압니까?'),
        ('resident_teacher','순찰대 때문에 아이들이 쫓겨날까 봐 그랬어요. 아이를 해치려고 한 건 아니에요.')]
        return [lines[min(h,5)]]
    lines=[('resident_ppul','비축은 다음 폭설 때 진료소를 버틸 물자요. 남았다고 모두 풀 수는 없소.'),
    ('granny','떠날 사람을 미리 분류한 거야. 날짜를 조금 앞당긴 편의를 죄라고 하니?'),
    ('granny','나는 이미 떠났다고 보고받은 대로 적었을 뿐이야.'),
    ('granny','네 부탁을 들었다고 내가 지시한 건 아니잖아. 실무에서 잘못 적용했겠지.'),
    ('granny','그쪽에서 맡으면 되는 사람이야. 여기 명단에서 빼는 게 왜 문제니?'),
    ('granny','수레꾼이 못 봤다는 것만으로 그곳에 보호가 없다고 말하니?'),
    ('granny','멈춘 다음은? 엄마의 조각 몇 개로 온 마을이 영원히 살 수 있니?'),
    ('granny','따뜻한 방 하나면 식사와 돌봄도 저절로 생기니?'),
    ('granny','너울이 보내기로 한 사람의 몫을 처리한 것뿐이야. 이 마을의 모든 일을 내 탓으로 돌리지 마.')]
    return [lines[min(h,8)]]


def r13_rec_e6_choose_future(s, choice):
    if choice not in ('stay','departure_pending') or 'e6_shared_checks' not in s['done']:
        raise ValueError('Choose a family plan only after current protection is handed over')
    n=copy.deepcopy(s)
    n['episodes']['6']['future_choice']=choice
    return n


def r13_rec_e456_admin_seed(episode):
    """Disclosed QA fixture, not credit for earlier gameplay. Only later actions are tested."""
    s=r13_rec_new_state()
    for key in ('piko','heat','repair','records','contact','delivery_wait','reply','meet'):
        s=r13_rec_apply(s,key)
    s=r13_rec_evening(s)
    for key in ('room','shelter'):s=r13_rec_apply(s,key)
    s['piko']='safe';s['nabi']='supervised_relief';s['neoul']='active' if episode==4 else 'detained'
    s=r13_rec_e456_flag(s,'public_custody_procedure_heard')
    s['admin_fixture']='recommended-ep%d-direct-entry'%episode
    return r13_rec_e456_state(s,episode)


def r13_rec_e6_hold_lines(s):
    if s['episodes']['6']['transport']=='at_altar_waiting':
        return [('dad','여기서 누가 식사와 잠자리를 맡는지 먼저 알아봐야 합니다. 사람들을 두고 가면 안 돼요.'),('resident_ppul','수레를 멈추시오. 바둑이, 승객들이 추위 속에 흩어지지 않게 곁에서 기다리시오.'),('resident_badook','세 분 모두 수레 곁에 계십니다. 함께 기다리겠습니다.')]
    if {'e6_board_read','e6_pandol_seen'}<=set(s['done']):
        return [('dad','판돌 씨는 아직 학교에 있는데 이미 밖에서 보호받는다고 적혀 있어요. 다음 보호자도 확인하지 못했습니다.'),('resident_ppul','출발부터 멈춥시다. 확인할 동안 바둑이가 승객들과 학교에서 기다리시오.'),('resident_siluk','알겠소. 수레는 여기 두겠소.')]
    return [('dad','명단에는 제단까지만 적혀 있어요. 거기서 누가 식사와 잠자리를 맡는지는 아직 모르겠습니다. 출발 전에 알아보죠.'),('resident_ppul','그렇다면 먼저 확인하겠소. 바둑이, 지금 승객들을 데려와 함께 기다리시오.'),('resident_badook','학교 문 앞에서 세 분을 확인했습니다. 안으로 모시고 곁에서 기다리겠습니다.'),('resident_siluk','수레는 멈췄소. 확인할 때까지 움직이지 않겠소.')]
