# Recommended route: isolated saved state; never migrates legacy room13 facts.
default r13_recommended = None
default r13_recommended_choice = None
init 900 python:
    """Isolated B/C route. Pure transitions; no legacy flags, evidence or clock mutations."""
    import copy
    
    r13_rec_revision = 'recommended-bccaabc-v2-day1-catalog'
    # Static exact-source geometry passed; native display/interaction remains a separate hold.
    r13_rec_piko_source_geometry_verified = True
    r13_rec_piko_native_geometry_verified = False
    r13_rec_piko_contact_art_verified = r13_rec_piko_source_geometry_verified and r13_rec_piko_native_geometry_verified
    def r13_rec_piko_geometry_ready(s):
        isolated = s.get('qa_fixture') == 'native_geometry_probe_v1' and s.get('qa_native_gates',{}).get('piko',False)
        return bool(r13_rec_piko_contact_art_verified or (r13_rec_piko_source_geometry_verified and isolated))
    
    r13_rec_effects = {}
    r13_rec_location_overrides = {1: lambda s,loc: ('학교 뒤 장작창고','ep_woodshed_intact') if loc=='store' else None}
    r13_rec_backgrounds = {'library': ('우체국 기록실', 'winter_post')}
    r13_rec_episodes = {1: dict(title='엄마 B / 피코 C', start_day=1, end_day=4, hearing_label='r13_recommended_hearing', next_label=None)}
    r13_rec_episode_start = {}
    r13_rec_day_advance = {}
    r13_rec_advance_block = {}
    r13_rec_episode_done = {1: lambda s: s['verdict'] in ('handoff_responsibility','direct_removal')}
    
    r13_rec_cards = {
     'repair': ('부리 · 엄마의 방문', '1일 수리점, 부리의 직접 관찰. 엄마는 물건을 맡긴 것이 아니라 낮과 저녁의 난방 차이를 물었고 기록실로 간다고 말했다.'),
     'ledger': ('연속 날짜 관측 장부', '기록실 원본. 같은 방의 낮 관측은 양호하다. 저녁과 사용 인원이 많던 날의 몇 줄은 없다. 원인과 삭제자는 모른다.'),
     'librarian': ('사서 · 연락을 맡긴 사람', '1일 기록실, 사서의 직접 대화. 엄마는 초롱에게 가족이 오면 전할 말을 맡겼다고 했다. 사서는 현재 은신처를 모른다.'),
     'reply': ('엄마 · 전달받은 답', '초롱의 전달 지점에서 받은 답. 가족의 질문에 답했고, 답을 받은 날 수리점 앞 공개 자리에서 만나기로 했다. 은신처 주소가 아니며 다른 날까지 같은 약속이 계속된다는 뜻도 아니다.'),
     'room': ('같은 방의 저녁 상태', '가족의 직접 관찰. 낮 장부와 같은 방이다. 돌 가까이에는 온기가 있지만 방 전체에서 밤을 보낼 상태인지는 별도 확인이 필요하다.'),
     'research': ('엄마 연구 원본', '재회 뒤 엄마에게 직접 받았다. 잠깐의 온기와 지속해서 지낼 조건은 다르다. 확인하지 않은 날짜의 진위와 누락 원인은 아직 모른다.'),
     'piko': ('피코 · 오늘 밤의 계획', '2일 광장에서 다람과 아빠가 직접 들었다. 방값이 없어 3번 등 아래에서 자려 한다. 엄마의 설명과 닮은 사람을 기록실 앞에서 보았으며 당시 관측 장부를 찾았다고 했다. 얼굴만으로 현재 위치를 확정할 수 없다.'),
     'empty_heat': ('아빠와 다람 · 짧은 잔열', '2일 낮 점검에 동석. 조각을 꺼내 빈 내부를 직접 본 직후에도 받침을 만지자 잠깐 온기가 남았다. 밤새 따뜻하다는 뜻은 아니다.'),
     'chorong': ('초롱 · 만진 곳', '3일 광장에서 들은 직접 관찰. 전날 해질 무렵 손을 댄 곳은 받침 겉면이었다. 당시 뚜껑 안의 돌은 보지 못했다.'),
     'pedestal': ('광장 3번 등의 빈 받침', '3일 현장. 안쪽에 17번 표기가 있고 돌은 없다. 온기가 있었다는 말만으로 그때 돌이 안에 있었다고 할 수 없다.'),
     'stone': ('아이 거처의 17번 돌', '3일 아이 거처에서 번호를 직접 대조했다. 광장 받침에 적힌 번호와 같다.'),
     'child': ('꼬미 · 용기의 전후 인계', '3일 아이 거처에서 들은 직접 경험. 2일 저녁 자기 천을 직접 펼쳐 모서리와 두 줄무늬를 펴서 확인하고 빈 용기에 접어 넣었다. 그때 찢김이 없었다. 용기와 천을 함께 빌려줬고, 나비가 돌아와 뚜껑을 열자 안에 17번 돌이 있었다. 같은 저녁 나비가 천을 풀어 돌을 내려놓을 때, 빌려줄 때 맞춰 접었던 모서리가 이미 찢어진 것을 봤다. 돌만 내려놓은 뒤 용기와 천은 나비가 계속 빌려 쓰고 있으며 아직 돌려받지 않았다. 광장에서 꺼내는 장면은 보지 못했다.'),
     'piko_portrait': ('피코가 그린 엄마 초상', '2일 아빠·다람의 설명과 피코의 기억을 맞춰 그린 초상. 3일 아침 약속대로 받은 같은 그림이다. 생존 여부로 숨겨진 정보가 새로 생기지 않으며 현재 위치를 증명하지 않는다.'),
     'container': ('배식 용기와 천 깔개', '나비가 실제로 보여 준 배식 용기와 천. 둘 다 꼬미가 함께 빌려줬고 아직 나비가 계속 쓰고 있다. 꼬미는 빌려주기 전 같은 천을 직접 펼쳐 온전한 것을 봤다. 사용자의 설명과 현장 조각을 함께 대조해야 한다.'),
    }
    
    def r13_rec_action(title, place, lines, need=(), forbid=(), give=(), flags=(), day=None, episode=1, background_key=None, label=None, target_person=None, target_object=None, min_period=0, max_period=2):
        return dict(title=title, place=place, lines=lines, need=tuple(need), forbid=tuple(forbid), give=tuple(give), flags=tuple(flags), day=day, episode=episode, background_key=background_key, label=label, target_person=target_person, target_object=target_object, min_period=min_period, max_period=max_period)
    
    r13_rec_actions = {
     'repair': r13_rec_action('부리에게 엄마가 맡긴 물건을 묻는다', 'workshop', [
      ('dad','아내가 이 수리점에 왔다는 말을 들었습니다. 맡긴 물건을 찾으러 다시 옵니까?'),
      ('buri','맡긴 물건은 없어요. 같은 방이 낮에는 따뜻한데 저녁에는 어떠냐고 물었죠.'),
      ('daram','그럼 수리가 끝날 때까지 여기서 기다리는 게 아니야?'),
      ('buri','응. 지난번 사용 기록을 보러 기록실에 간다고 했어.'),
      ('dad','어디로 갔는지는 알았구나. 기록실에 가 보자.')], give=('repair',), flags=('repair',), episode=0),
     'records': r13_rec_action('엄마가 읽은 기록과 마지막 방문을 확인한다', 'library', [
      ('dad','수리점에서 아내가 여기로 갔다고 들었습니다. 어떤 기록을 봤습니까?'),
      ('resident_librarian','이 방의 관측 장부예요. 방문하신 것도 제가 직접 봤고요.'),
      (None,'날짜가 이어지는 원본에 관측 시각과 그때 사용 상태가 적혀 있었다. 낮 관측은 양호했다. 몇 날짜의 저녁 줄은 비어 있었다.'),
      ('dad','여기 없는 관측은 다른 곳에 보관돼 있습니까?'),
      ('resident_librarian','아직 확인하지 못했어요. 없다는 이유만으로 누가 지웠다고 할 수는 없지요.'),
      ('resident_librarian','가족이 오면 전할 말을 초롱에게 맡겼다고 했어요. 현재 계신 곳은 저도 모릅니다.')], need=('repair',), give=('ledger','librarian'), flags=('records',), episode=0),
     'contact': r13_rec_action('초롱에게 가족이 도착했다고 알린다', 'square', [
      ('dad','사서에게 들었습니다. 제 아내가 가족에게 전할 말을 맡겼습니까?'),
      ('resident_lamplighter','두 분이 그 가족이군요. 이제 직접 확인했네요. 여관에서 계속 기다리지 말라는 말이었어요.'),
      ('dad','초대 편지를 받았을 때는 거기서 만나기로 했는데요.'),
      ('resident_lamplighter','그 뒤에 누군가 발자국을 따라오는 걸 보셨대요. 가족 이름을 공개적으로 부르면 그 사람에게도 연락 상대를 알려 주게 되지요.'),
      ('dad','그럼 아내에게 우리가 왔다고 전해 주세요. 다람이가 엄마와 오늘 같이 있을 수 있는지 묻습니다.'),
      ('resident_lamplighter','은신처는 몰라요. 답을 주고받기로 한 전달 지점은 알아요. 거기 다녀올게요. 두 분은 여관에서 젖은 장화도 말리고 기다리세요. 돌아오면 광장에서 뵐게요.')], need=('records',), flags=('contact_sent',), episode=0),
     'room': r13_rec_action('장부에 나온 방을 저녁에 직접 살펴본다', 'guestroom', [
      (None,'낮 관측 장부에 적힌 방으로 저녁에 다시 갔다. 저녁에는 사람들이 모여 있었다.'),
      ('daram','돌 옆은 따뜻한데, 내 자리는 차가워.'),
      ('dad','낮 기록이 틀린 건 아니야. 다만 그 기록만 보고 우리도 밤새 잘 수 있다고 생각하면 안 되겠구나.')], need=('records',), give=('room',), flags=('room_checked',), episode=0, min_period=2),
     'reply': r13_rec_action('돌아온 초롱에게 엄마의 답을 받는다', 'square', [
      (None,'여관에서 장화를 말리고 광장으로 돌아오자 초롱이 등불을 걸고 있었다. 전달 지점을 다녀온 신발에 새 눈이 묻어 있었다.'),
      ('resident_lamplighter','답을 받아 왔어요. 다람이가 오늘 같이 있을 수 있냐고 물은 말도 전했어요.'),
      (None,'“둘 다 왔구나. 정말 보고 싶어. 나는 무사해. 지금 수리점 앞에서 만나자. 처음 약속한 방에서는 기다리지 마.”'),
      ('daram','내가 물은 말에 답했어. 오늘 만날 수 있대!'),
      ('dad','응. 수리점 앞길이 열려 있는지 확인하고 함께 가자.')], need=('delivery_elapsed',), give=('reply',), flags=('current_reply',), episode=0),
     'meet': r13_rec_action('열린 수리점 앞길을 확인하고 엄마를 만난다', 'workshop', [
      (None,'수리점 앞은 아직 열려 있었다. 부리가 작업대를 정리하는 동안 아빠와 다람은 약속한 공개 자리에서 기다렸다.'),
      ('mom','다람아!'),
      (None,'다람이 엄마 품으로 달려갔다. 아빠도 두 사람 곁에 앉았다.'),
      ('daram','편지에는 여관에 있다고 했잖아.'),
      ('mom','편지를 보낼 때는 그럴 생각이었어. 너희가 오는 동안 누가 내 발자국을 따라왔어. 그래서 그곳을 떠났어.'),
      ('dad','우리는 오는 길이라 바뀐 소식을 몰랐어. 이제 같이 있자.'),
      ('mom','응. 초롱에게 도착하면 전할 말을 맡겼어. 너희 질문을 받고서야 둘이 도착한 걸 알았어.'),
      ('mom','연구 원본은 여기 있어. 하지만 먼저 오늘 함께 잘 곳부터 정하자. 낮의 좋은 기록만으로 밤의 방을 고를 수는 없으니까.')], need=('current_reply',), give=('research',), flags=('reunited',), episode=0),
     'shelter': r13_rec_action('나비와 가족의 방·식사·출입을 실제 확인한다', 'inn', [
      ('dad','셋이 오늘 밤 함께 있을 자리가 필요합니다. 지금 쓸 수 있는 방이 있습니까?'),
      ('nabi','임시 객실에 세 자리 있어요. 여관에서 쓰도록 내준 자리예요. 같이 확인해요.'),
      (None,'세 사람이 들어갈 자리에 이불을 폈다. 난로는 작동하고 있었고, 나비가 준비한 저녁 세 그릇을 가져왔다.'),
      ('nabi','복도 문은 안에서 열 수 있어요. 밤에는 제가 주방에 있어요. 필요하면 부르세요.'),
      ('daram','오늘은 셋이 같이 자는 거지?'),('mom','응. 남은 일도 같이 정하자.')], need=('reunited','room_checked'), flags=('family_shelter',), episode=0, min_period=2),
     'piko': r13_rec_action('그림을 그리는 피코에게 오늘 밤을 묻는다', 'square', [
      ('dad','아내를 찾고 있습니다. 얼굴 생김새를 설명해 드릴게요. 혹시 이런 분을 보셨습니까?'),('resident_piko','기록실 앞에서 뵌 분 같아요. 이름은 모르지만, 관측 장부를 찾는다고 하셨어요. 제가 본 얼굴을 그려 볼게요.'),('daram','엄마 그림이 생기면 우리도 같이 볼 수 있겠다.'),('resident_piko','내일 아침에 판자를 드릴게요. 그분을 본 얘기는 지금도 더 물으셔도 돼요.'),('daram','그럼 해가 지면 어디서 그려요?'),('resident_piko','오늘 방값이 없어서 이 등 밑에서 자려고. 다 그리면 여기서 쉬어야지.'),
      ('dad','등 하나에만 기대고 자도 괜찮겠습니까?'),('resident_piko','어제도 손이 좀 시렸어요. 다른 자리가 있으면 좋겠지만요.')], give=('piko',), flags=('piko_plan',), day=2),
     'heat': r13_rec_action('초롱의 낮 점검에 함께한다', 'square', [
      (None,'초롱이 게시판 옆에 걸린 3번 등을 내려 벤치에 놓았다. 뚜껑을 열고 천으로 손바닥만 한 돌을 꺼냈다. 아빠와 다람은 안이 빈 것을 직접 보았다.'),
      ('resident_lamplighter','이 바깥 받침은 지금 손대도 괜찮아요.'),('daram','비었는데 아직 조금 따뜻해.'),
      ('dad','방금 꺼냈으니까 온기가 잠깐 남아 있구나. 따뜻하다고 꼭 돌이 들어 있는 건 아니네.'),
      (None,'점검을 마친 초롱이 돌을 넣고 뚜껑을 닫았다. 등은 원래 갈고리에 다시 걸렸다.')], give=('empty_heat',), flags=('heat_seen',), day=2, max_period=1),
     'escort': r13_rec_action('피코와 여관의 실제 잠자리를 확인하고 함께 옮긴다', 'inn', [
      ('dad','피코 씨가 오늘 등 밑에서 잔다고 합니다. 오늘만이라도 실제로 쉴 곳이 있습니까?'),
      ('nabi','식당 난로 옆에 한 자리 비어 있어요. 불도 밤에 지킬 거고요.'),
      (None,'아빠와 다람이 피코의 판자와 붓을 함께 날랐다. 피코가 식당 안에 들어가 이불을 폈다.'),
      ('resident_piko','여기까지 같이 와 줘서 고마워요. 오늘 밤은 밖에서 안 잘게요.')], need=('piko_plan',), flags=('piko_moved',), day=2),
     'pedestal': r13_rec_action('빈 3번 등 안쪽을 살펴본다', 'square', [
      (None,'3일 아침. 초롱과 함께 3번 등을 내려 벤치에 놓았다. 뚜껑 안은 비어 있었다. 돌이 놓이던 안쪽 받침에 17이라는 번호가 적혀 있었다.'),
      ('dad','먼저 없어진 물건의 번호를 기억하자. 누가 가져갔는지는 아직 몰라.')], give=('pedestal',), flags=('pedestal_seen',), day=3),
     'chorong': r13_rec_action('초롱에게 어제 만진 곳을 정확히 묻는다', 'square', [
      ('resident_lamplighter','어제 해질 때까진 따뜻했어요. 그래서 그 뒤에 없어진 줄 알았죠.'),
      ('dad','그때 손을 댄 건 어느 부분이었습니까? 안의 돌도 보셨나요?'),
      ('resident_lamplighter','겉 받침이요. 안은 열어 보지 않았어요.'),
      ('dad','우리가 낮에 본 빈 받침에도 잠깐 온기가 남았습니다. 온기만으로 반출 뒤 시간을 정할 수는 없겠군요.')], need=('pedestal_seen','heat_seen'), give=('chorong',), flags=('heat_limit',), day=3),
     'child': r13_rec_action('나비의 배식길을 따라 아이 거처에서 실제 인계를 묻는다', 'store', [
      ('dad','여관에서 아이들에게 음식을 나른다고 들었어. 이 돌은 어떻게 왔니?'),
      ('kid_kkomi','나는 꼬미예요. 이 용기는 제 거예요. 어제 저녁에 빈 걸 나비 누나한테 빌려줬어요.'),
      ('kid_kkomi','천도 제 거예요. 빈 통 밑에 제가 직접 펴 넣었어요. 두 줄무늬를 펴서 모서리까지 맞추고 접었죠. 그땐 찢어진 데가 없었어요.'),
      ('kid_kkomi','누나가 돌아와서 내 앞에서 뚜껑을 열었어요. 안에 돌이 있었어요. 천을 풀어 돌을 내려놓는데, 아까 맞춰 접은 그 모서리가 찢어져 있었어요. 광장에서 꺼내는 건 못 봤어요.'),
      ('kid_kkomi','돌만 여기 내려놓았어요. 통과 천은 음식도 나른다고 계속 빌려 쓰고 있어요. 그 뒤 아직 돌려받지는 않았어요.'),
      ('dad','광장에서 꺼낸 사람까지 봤다는 말은 아니구나. 그때 안에서 본 번호와 지금 돌을 함께 확인해도 될까?'),
      (None,'아이가 허락했다. 돌에는 17이 적혀 있었다. 광장 받침의 번호와 같았다.')], need=('children_route',), give=('stone','child'), flags=('handoff_seen','piko_cloth_intact_at_loan','piko_cloth_torn_at_delivery'), day=3, background_key='ep_woodshed_intact', label='r13_rec_piko_intact_loan'),
    }
    
    
    r13_rec_actions['delivery_wait'] = r13_rec_action('초롱이 다녀오는 동안 장화를 말리며 쉰다', 'inn',
     [(None,'아빠가 난로에서 조금 떨어진 곳에 젖은 장화를 놓았다. 다람은 과자를 반으로 나눠 하나를 남겨 두었다.'),('daram','이건 엄마 거야. 초롱 아저씨 오면 바로 가자.'),(None,'장화의 눈이 녹고 난 뒤 두 사람은 광장으로 돌아갔다. 초롱이 전달 지점을 오갈 시간이 흘렀다.')],
     need=('contact_sent',), flags=('delivery_elapsed',), episode=0, target_object='난로 옆 장화')
    
    r13_rec_actions['nabi_route'] = r13_rec_action('나비에게 광장 돌과 배식길을 묻는다', 'kitchen',
     [('dad','광장 돌이 없어졌습니다. 밤에 음식을 나르실 때 무엇을 보셨습니까?'),('nabi','제가 돌을 아이들 거처에 갖다줬어요. 아이들이 너무 추워했어요.'),('dad','아이들이 있는 곳과 옮겨 간 현물을 함께 확인할 수 있을까요?'),('nabi','장작 창고 안쪽이에요. 꼬미에게 제가 보냈다고 해 주세요. 아이를 몰아세우지는 말아 주세요.'),('dad','그 아이가 직접 겪은 인계만 묻겠습니다. 다른 사람의 일까지 떠넘기지 않을게요.')],
     need=('pedestal_seen',), flags=('children_route',), day=3, target_person='nabi')
    
    r13_rec_actions['pedestal']['lines'].append((None,'열린 뚜껑 아래, 안쪽 쇠붙이에 작은 천 조각이 걸려 있었다. 초롱이 뚜껑을 닫자 그 자리는 바깥에서 닿지 않게 가려졌다.'))
    
    r13_rec_actions['contact_match'] = r13_rec_action(
     '등 테두리와 용기 천의 접촉 흔적을 대조한다', 'square',
     [('dad','같은 돌을 인계한 사실만으로 광장에서 직접 꺼낸 사람까지 알 수는 없다. 등 테두리의 흔적과 용기에 남은 천을 실제로 대조하자.')],
     need=('handoff_seen','piko_cloth_available'), flags=('cloth_contact_matched',), label='r13_recommended_contact_inspect')
    
    def r13_rec_contact_effect(s):
        if not r13_rec_piko_geometry_ready(s):
            raise ValueError('Unverified contact geometry cannot establish removal')
        n=copy.deepcopy(s)
        if n['verdict']=='handoff_responsibility':
            n['verdict']=None
            n['hearing']=3
        return n
    r13_rec_effects['contact_match']=r13_rec_contact_effect
    
    def r13_rec_new_state():
        return dict(revision=r13_rec_revision, location='inn', period=0, episode=1, episodes={}, neoul='active', daram='with_parent', e3_school_handoff=False, e4_lever_blocked=False, e5_poison_blocked=False, day=2, done=[], facts=[], mother='M0', piko='outside', nabi='working', hearing=0, verdict=None, selected=[], log=[], observed={})
    
    def r13_rec_available(s):
        if s.get('revision') != r13_rec_revision:
            return []
        have=set(s['done'])
        return [(key,a['title']) for key,a in r13_rec_actions.items() if a.get('min_period',0)<=s.get('period',0)<=a.get('max_period',2) and a.get('episode',1) in (0,s.get('episode',1)) and (key not in have or key=='refresh_reply') and (key!='meet' or s.get('observed',{}).get('reply')==s['day']) and (key!='refresh_reply' or (s['mother']=='M1' and s.get('observed',{}).get('reply')!=s['day'])) and set(a['need'])<=have and not set(a['forbid'])&have and (a['day'] is None or a['day']==s['day'])]
    
    def _r13_rec_apply_core(s,key):
        if key=='contact_match' and not r13_rec_piko_geometry_ready(s):
            raise ValueError('Contact illustration is not verified')
        if key not in dict(r13_rec_available(s)):
            raise ValueError('Unavailable r13_rec_action: '+key)
        n=copy.deepcopy(s); a=r13_rec_actions[key]
        n['done']=list(dict.fromkeys(n['done']+[key]+list(a['flags'])))
        n['facts']=list(dict.fromkeys(n['facts']+list(a['give'])))
        n['log'].append(key)
        for card in a['give']: n['observed'][card]=s['day']
        if key=='reply' and n['mother']=='M0': n['mother']='M1'
        if key=='meet': n['mother']='M2'
        if key=='escort': n['piko']='sheltered'
        if key in r13_rec_effects: n=r13_rec_effects[key](n)
        return n
    
    def _r13_rec_next_day_core(s):
        ep=s.get('episode',1)
        if ep in r13_rec_day_advance: return r13_rec_day_advance[ep](copy.deepcopy(s))
        n=copy.deepcopy(s)
        if s['day']==2:
            if not {'heat_seen','piko_plan'}<=set(s['done']):
                raise ValueError('First observe the lamp and hear Piko plan')
            n['day']=3
            n['period']=0
            n['piko']='safe' if s['piko']=='sheltered' else 'dead'
            n['facts']=list(dict.fromkeys(n['facts']+['piko_portrait']))
            n['observed']['piko_portrait']=3
        elif s['day']==3:
            if not {'heat_limit','handoff_seen'}<=set(s['done']):
                raise ValueError('First investigate the r13_rec_available witnesses')
            n['day']=4
            n['period']=0
        return n
    
    r13_rec_hearing = (
     ('“받침이 따뜻했으니 그때 돌이 있었다.” 무엇을 제시할까?', 'empty_heat', '돌을 꺼낸 뒤에도 안쪽은 잠깐 따뜻했어요. 따뜻했다는 말만으로 그때 돌도 있었다고 할 수는 없겠네요.'),
     ('아이 거처의 돌과 광장의 물건을 어떻게 연결할까?', 'stone', '이 돌에도, 광장의 등 안에도 17이 적혀 있어요. 이제 이 돌이 누구 손을 거쳐 여기 왔는지 물어볼 수 있겠네요.'),
     ('누가 그 돌을 아이에게 넘겼는가? 인물 카드를 제시하자.', 'child', '꼬미는 빈 용기를 빌려줬고, 나비 씨가 돌을 담아 돌아온 것도 봤어요. 다만 광장에서 꺼내는 순간까지 본 것은 아니에요.'),
    )
    
    def r13_rec_present(s,key):
        if s['day']!=4 or s['verdict'] is not None or key not in s['facts']:
            raise ValueError('Presentation outside hearing or unearned card')
        n=copy.deepcopy(s); step=s['hearing']
        steps=r13_rec_hearing_steps(s)
        if step==3 and not {'piko_container_exclusive_claim','piko_cloth_intact_at_loan','piko_cloth_torn_at_delivery'}<=set(s['done']):
            return n, '빌려줄 때 천 상태와 그 뒤 누가 썼는지를 함께 확인해야 해요.', False
        if key!=steps[step][1]:
            return n, '그 자료가 보여 주는 범위를 다시 보자. 지금 질문에 필요한 관찰과는 다르다.', False
        if step==1 and 'pedestal' not in s['facts']:
            return n, '광장의 받침 번호를 먼저 현장에서 확인해야 한다.', False
        n['selected'].append(key); n['hearing']+=1
        if n['hearing']==len(steps):
            n['verdict']='direct_removal' if len(steps)==4 else 'handoff_responsibility'
            n['nabi']='supervised_relief'
        return n, steps[step][2], True
    
    def r13_rec_hearing_ready(s):
        return s['day']==4 and {'empty_heat','pedestal','stone','child','chorong'}<=set(s['facts'])
    
    
    def r13_rec_block_reason(s):
        ep=s.get('episode',1)
        if ep in r13_rec_advance_block: return r13_rec_advance_block[ep](s)
        if ep==1 and s['day']==2 and not {'heat_seen','piko_plan'}<=set(s['done']):
            return '가기 전에 피코 씨의 오늘 계획과 초롱의 점검을 확인하자.'
        if ep==1 and s['day']==3 and not {'heat_limit','handoff_seen'}<=set(s['done']):
            return '오늘 현장과 실제 인계를 확인하고 내일 회의에서 말하자.'
        return None
    
    def r13_rec_next_available(s):
        ep=s.get('episode',1)
        return ep+1 if r13_rec_episode_done.get(ep,lambda s:False)(s) and ep+1 in r13_rec_episode_start else None
    
    def _r13_rec_begin_episode_core(s, episode):
        if r13_rec_next_available(s)!=episode: raise ValueError('Episode not unlocked')
        n=r13_rec_episode_start[episode](copy.deepcopy(s))
        if n['episode']!=episode: raise ValueError('Plugin failed to set episode')
        for key in ('mother','piko','nabi'):
            if key=='mother' and s[key]=='M2' and n[key]!='M2': raise ValueError('Reunion cannot be undone')
            if key=='piko' and s[key]=='safe' and n[key]!='safe': raise ValueError('Prevention cannot be undone')
        return n
    
    
    def r13_rec_hearing_steps(s):
        if r13_rec_piko_geometry_ready(s) and 'cloth_contact_matched' in s['done']:
            return r13_rec_hearing+((
              '돌의 인계뿐 아니라 광장 테두리에서 찢긴 흔적까지 잇는 물건은?',
              'container',
              '꼬미가 빌려줄 때 직접 펴 넣은 천은 온전했어요. 그날 돌을 내려놓을 때는 이미 그 모서리가 찢어져 있었어요. 그 사이 혼자 쓰셨고 등 안에는 손대지 않았다고 했죠. 그 떨어진 부분이 등 뚜껑에 가려지는 안쪽 조각과 이어져요. 밖에 놓인 돌만 담았다는 설명으로는 그동안 안쪽에서 찢어진 이 부분을 설명할 수 없어요.'),)
        return r13_rec_hearing
    
    
    for _key,_person in {'repair':'buri','records':'resident_librarian','contact':'resident_lamplighter','reply':'resident_lamplighter','meet':'mom','shelter':'nabi','piko':'resident_piko','heat':'resident_lamplighter','escort':'nabi','chorong':'resident_lamplighter','child':'kid_kkomi'}.items():
        r13_rec_actions[_key]['target_person']=_person
    for _key,_object in {'room':'장부에 나온 방','pedestal':'3번 등의 빈 받침','contact_match':'등 테두리와 배식 용기'}.items():
        r13_rec_actions[_key]['target_object']=_object
    
    def r13_rec_validate_transition(before, after):
        if before.get('mother')=='M2' and after.get('mother')!='M2':
            raise ValueError('An actual reunion cannot be undone')
        if before.get('piko')=='safe' and after.get('piko')!='safe':
            raise ValueError('Piko prevention cannot be undone')
        if before.get('neoul')=='detained' and after.get('neoul')!='detained':
            raise ValueError('Detained Neoul cannot resume field actions')
        for flag in ('e3_school_handoff','e4_lever_blocked','e5_poison_blocked'):
            if before.get(flag) and not after.get(flag):
                raise ValueError('Completed prevention cannot be undone: '+flag)
        return after
    
    def r13_rec_apply(s,key):
        return r13_rec_validate_transition(s,_r13_rec_apply_core(s,key))
    
    def r13_rec_next_day(s):
        n=_r13_rec_next_day_core(s)
        if n['day']!=s['day']:n['period']=0
        return r13_rec_validate_transition(s,n)
    
    def r13_rec_begin_episode(s,episode):
        return r13_rec_validate_transition(s,_r13_rec_begin_episode_core(s,episode))
    
    
    def r13_rec_evening(s):
        if s.get('period',0)>=2: return copy.deepcopy(s)
        if s.get('episode',1)==1 and s['day']==2 and not {'heat_seen','piko_plan'}<=set(s['done']):
            raise ValueError('Observe the daytime lamp and Piko plan first')
        n=copy.deepcopy(s);n['period']=2
        return n
    
    
    def r13_rec_controls(s):
        commands=[]
        if s.get('period',0)<2:commands.append(('evening','저녁까지 기다린다'))
        end=r13_rec_episodes[s['episode']]['end_day']
        if s['day']<end:commands.append(('advance','오늘을 마친다'))
        if s['day']==end and not r13_rec_episode_done.get(s['episode'],lambda s:False)(s):commands.append(('hearing','공개 회의'))
        if r13_rec_next_available(s):commands.append(('next_episode','다음 사건'))
        return commands+[('save','저장'),('title','제목 화면')]
    
    # A meeting promise is current only on the day the reply was actually received.
    r13_rec_actions['refresh_reply']=r13_rec_action('초롱과 전달 지점에 다녀와 오늘 만날 곳을 다시 확인한다','square',[
     ('dad','답을 받은 뒤 날이 지났습니다. 그때 약속한 자리로 그냥 가도 될까요?'),
     ('resident_lamplighter','그대로 기다리고 계실 거라고는 못 해요. 전달 지점에서 오늘 답을 다시 확인해요.'),
     (None,'초롱과 함께 골목 끝 전달 지점에 갔다. 초롱이 약속된 방법으로 도착을 알리는 동안 아빠는 다람의 젖은 장갑을 갈아 끼웠다. 잠시 뒤 돌아온 초롱이 새 답을 전했다.'),
     ('resident_lamplighter','오늘도 수리점 앞 공개 자리에서 만나실 수 있대요. 지금 길이 열려 있는지 확인하고 가세요.')],need=('current_reply',),forbid=('reunited',),give=('reply',),episode=0,target_person='resident_lamplighter')
    
    def r13_rec_action_lines(s,key):
        lines=list(r13_rec_actions[key]['lines'])
        if key=='piko' and s.get('mother')=='M2':
            lines[0]=('dad','아내와 다시 만났습니다. 기록실에 다녀왔다고 하더군요. 얼굴을 설명해 드릴 테니 여기서 보셨던 분인지 말씀해 주시겠어요?')
        return lines
    
    # UI identities are not additional evidence. Multiple observations share one profile/object.
    r13_rec_identity_groups = {
     'buri':('person','부리',('repair',)),
     'librarian':('person','사서',('librarian',)),
     'mom':('person','엄마',('reply',)),
     'piko':('person','피코',('piko',)),
     'chorong':('person','초롱',('chorong',)),
     'kkomi':('person','꼬미',('child',)),
     'somi':('person','솜이',('e2_card_somi',)),
     'bami':('person','밤이',('e2_card_bami',)),
     'badook':('person','바둑이',('e2_card_badook','e6_card_badook')),
     'dolmok':('person','돌목',('e2_card_dolmok',)),
     'teacher':('person','선생님',('e3_card_handoff','e3_card_teacher','e5_card_teacher')),
     'bori':('person','보리',('e3_card_bori','e5_card_bori')),
     'nubi':('person','누비',('e3_card_nubi',)),
     'nubi_child':('person','누비의 큰아이',('e3_card_child',)),
     'daram':('person','다람',('e4_card_daram',)),
     'dad':('person','아빠',('e4_card_parent',)),
     'seori':('person','서리',('e4_card_seori','e5_card_cabinet','e5_card_seori')),
     'nabi':('person','나비',('e4_card_nabi7','e4_card_nabi9','e6_card_nabi')),
     'ttadak':('person','따닥',('e4_card_ttadak',)),
     'neoul':('person','너울',('e4_card_neoul',)),
     'saemi':('person','새미',('e5_card_saemi',)),
     'pandol':('person','판돌',('e6_card_pandol',)),
     'munchi':('person','뭉치',('e6_card_munchi',)),
     'granny':('person','할머니',('e6_card_granny',)),
     'siluk':('person','실룩',('e6_card_siluk',)),
     'ledger':('physical','관측 장부',('ledger',)),
     'research':('physical','엄마 연구 원본',('research',)),
     'portrait':('physical','피코의 엄마 초상',('piko_portrait',)),
     'lamp':('physical','광장 3번 등',('empty_heat','pedestal')),
     'stone':('physical','17번 돌',('stone',)),
     'container':('physical','배식 용기와 천',('container',)),
     'cart':('physical','수레와 고정끈',('e2_card_rail','e2_card_ties')),
     'oilcan':('physical','빨래터 통과 주둥이',('e3_card_can',)),
     'tool':('physical','벌림 도구',('e4_card_tool',)),
     'mechanism':('physical','13호 개폐 장치',('e4_card_lever',)),
     'pots':('physical','두 냄비와 뚜껑',('e5_card_pots',)),
     'bottle':('physical','반출 약통',('e5_card_bottle',)),
     'board':('physical','학교 배분판',('e6_card_board',)),
     'manifest':('physical','출발 명단',('e6_card_manifest',)),
     'room':('scene','장부에 나온 방',('room',)),
     'woodshed':('scene','장작창고 현장',('e3_card_wall','e3_card_layout')),
     'school':('scene','학교의 실제 자리',('e5_card_notice','e6_card_school')),
    }
    
    def r13_rec_card_episode(key):
        if key in ('repair','ledger','librarian','reply','room','research'): return 0
        if key.startswith('e') and key[1:2].isdigit() and key[2:3]=='_': return int(key[1])
        return 1
    
    def r13_rec_catalog_entries(s,folder,category):
        known=set(s['facts']); result=[]
        for ident,(kind,title,keys) in r13_rec_identity_groups.items():
            held=tuple(key for key in keys if key in known)
            if not held or not any(r13_rec_card_episode(k)==folder for k in held):continue
            if (kind=='person') != (category=='person'):continue
            result.append((ident,title,held,kind))
        return result
    
    def r13_rec_identity_facts(s,ident):
        return [k for k in r13_rec_identity_groups[ident][2] if k in s['facts']]
    
    r13_rec_cards['piko_nabi_defense']=('나비 · 회의에서 밝힌 운반 설명','4일 공개 회의에서 직접 들었다. 돌은 등 밖에 놓여 있던 것을 주워 담았다고 주장했다. 빈 용기를 빌린 뒤 지금까지 용기와 천은 혼자 썼고 다른 사람에게 맡기지 않았다고 답했다. 이 말은 해명이지 독립적으로 확인된 사실이 아니다.')
    _kind,_title,_keys=r13_rec_identity_groups['nabi']
    r13_rec_identity_groups['nabi']=(_kind,_title,('piko_nabi_defense',)+_keys)
    
    def r13_rec_piko_hear_defense(s):
     if s['day']!=4 or s.get('episode',1)!=1:raise ValueError('The public explanation belongs to the scheduled meeting')
     n=copy.deepcopy(s)
     n['done']=list(dict.fromkeys(n['done']+['piko_container_exclusive_claim','piko_cloth_available']))
     n['facts']=list(dict.fromkeys(n['facts']+['piko_nabi_defense','container']))
     n['observed']['piko_nabi_defense']=s['day']
     n['observed']['container']=s['day']
     return n
    
    # Optional owner-consent route: an observant player may compare earlier without amnesia.
    r13_rec_actions['piko_cloth_consent']=r13_rec_action('나비에게 지금 쓰는 용기와 천을 함께 살펴봐도 되는지 묻는다','kitchen',[
     ('dad','꼬미에게 빌린 통과 천을 아직 쓰고 계신다고 들었어요. 광장 등 안에 남은 조각과 천을 맞춰 보고 싶습니다. 잠깐 보여 주실 수 있습니까?'),
     ('nabi','이 그릇들만 내려놓고 같이 가요. 천도 통도 꼬미에게 빌린 거예요. 찢어 내거나 가져가지는 말아 주세요.'),
     (None,'나비가 배식 그릇을 내려놓았다. 용기와 천을 챙겨 아빠·다람과 광장으로 갔다. 초롱이 등을 벤치에 내려놓았다.'),
     ('dad','허락해 주셔서 고맙습니다. 있는 그대로 대 볼게요.')],need=('handoff_seen',),give=('container',),flags=('piko_cloth_available',),day=3,target_person='nabi')
    
    r13_rec_effects['piko_cloth_consent']=lambda s:dict(s,location='square')
    
    # A player may ask the obvious source question before the meeting as well.
    r13_rec_actions['piko_cloth_consent']['lines'][0:0]=[
     ('dad','돌을 광장의 등에서 직접 꺼내셨나요?'),
     ('nabi','아니요. 등 밖에 놓인 걸 주워 담았어요.'),
     ('dad','그 사이 용기나 천을 다른 분이 쓴 적은 있습니까?'),
     ('nabi','없어요. 빈 통을 빌린 뒤 지금까지 저 혼자 들고 다녔고, 천도 저만 썼어요. 등 뚜껑을 열거나 안을 닦은 적도 없어요.')]
    r13_rec_actions['piko_cloth_consent']['give']=('container','piko_nabi_defense')
    r13_rec_actions['piko_cloth_consent']['flags']=('piko_cloth_available','piko_container_exclusive_claim','piko_source_claim_early')
    r13_rec_cards['piko_nabi_defense']=('나비 · 돌을 담은 곳과 운반 설명','나비에게 직접 들은 해명. 돌은 등 밖에 놓여 있던 것을 주워 담았다고 주장했다. 빈 용기를 빌린 뒤 지금까지 용기와 천은 혼자 썼고 다른 사람에게 맡기지 않았다고 답했다. 이 말 자체는 해명이며, 실제 흔적과 따로 맞춰 봐야 한다.')
    
    def r13_rec_piko_summarize_prior(s):
     if not {'piko_source_claim_early','cloth_contact_matched'}<=set(s['done']) or not r13_rec_piko_geometry_ready(s):
      raise ValueError('No completed prior comparison to summarize')
     n=copy.deepcopy(s)
     while n['hearing']<len(r13_rec_hearing_steps(n)):
      n,message,ok=r13_rec_present(n,r13_rec_hearing_steps(n)[n['hearing']][1])
      if not ok:raise ValueError(message)
     return n


init 920 python:
    _r13_rec_original_save_status = r13_save_status
    _r13_rec_original_save_caption = r13_save_caption
    _r13_rec_original_load_action = r13_load_action
    _r13_rec_original_continue_slot = r13_continue_slot
    def r13_rec_save_metadata(data):
        state = getattr(store, "r13_recommended", None)
        if state and (getattr(store, "room13", None) or {}).get("campaign_id") in ("room13_recommended_v1","room13_recommended_qa_v1"):
            data["r13_recommended_revision"] = state["revision"]
            data["r13_recommended_episode"] = state["episode"]
    config.save_json_callbacks.append(r13_rec_save_metadata)
    def r13_save_status(data):
        if data and data.get("r13_campaign") in ("room13_recommended_v1","room13_recommended_qa_v1"):
            return "compatible" if data.get("r13_recommended_revision") == r13_rec_revision else "incompatible"
        return _r13_rec_original_save_status(data)
    def r13_save_caption(data):
        if data and data.get("r13_campaign") == "room13_recommended_qa_v1":
            return "미검증 QA 전용 · %s일 · 명시 확인 후 불러오기" % data.get("r13_day")
        if data and data.get("r13_campaign") == "room13_recommended_v1":
            return "추천 검증판 · %s일 · %s" % (data.get("r13_day"), "이어갈 수 있음" if r13_save_status(data)=="compatible" else "새로 시작 필요")
        return _r13_rec_original_save_caption(data)
    def r13_continue_slot():
        slot = _r13_rec_original_continue_slot()
        if slot is None or (renpy.slot_json(slot) or {}).get("r13_campaign") != "room13_recommended_qa_v1":
            return slot
        candidates=[((renpy.slot_json(slot) or {}).get("_ctime",0),slot) for slot in r13_save_slots()
            if (renpy.slot_json(slot) or {}).get("r13_campaign") != "room13_recommended_qa_v1" and r13_save_status(renpy.slot_json(slot))=="compatible"]
        return max(candidates)[1] if candidates else None
    def r13_load_action(slot):
        data=renpy.slot_json(slot) or {}
        if data.get("r13_campaign")=="room13_recommended_qa_v1" and r13_save_status(data)=="compatible":
            return Confirm("미검증 QA 전용 저장입니다. 일반 추천판이 아니라 최종 단계 시험 상태를 불러올까요?",FileLoad(slot,slot=True,confirm=False))
        return _r13_rec_original_load_action(slot)


screen r13_recommended_setup():
    modal True
    add Solid("#172421")
    frame:
        xalign .5 yalign .5 xsize 980
        vbox:
            spacing 24
            text "추천 스토리 · 개발 검증판" size 32
            text "마차 도착과 입구 조사부터 새 추천안의 대사·조사·선택을 시험하는 별도 경로입니다. 기존 저장은 변환하지 않습니다. 직접 반출에 쓰이는 등/천 그림과 후속 회차는 검수 상태에 따라 제한됩니다." size 24
            text "아직 전체 캠페인 적용 완료가 아니며, 확인된 결과와 검수 중인 부분을 구분합니다." size 24
            text r13_rec_e456_art_status size 18
            textbutton "새 추천 이야기 시작" action Return(True)
            textbutton "제목 화면" action MainMenu(confirm=False)

screen r13_recommended_actions():
    modal True
    add Solid("#172421ef")
    frame:
        xpos 24 ypos 24 xsize 1232 ysize 646
        vbox:
            spacing 12
            text ("추천 스토리 검증판 · %d일 · 엄마 %s" % (r13_recommended["day"], r13_recommended["mother"])) size 28
            text (r13_rec_episodes[r13_recommended["episode"]]["title"]+" · 기존 저장과 분리") size 19
            if r13_recommended.get("qa_fixture"):
                text "미검증 QA 전용 · 최종 단계 시험 허용" size 19 color "#ffb76b"
            hbox:
                spacing 18
                vbox:
                    xsize 610 spacing 8
                    viewport:
                        ysize 350 mousewheel True draggable True scrollbars "vertical"
                        vbox:
                            spacing 5
                            for key, caption in r13_rec_available(r13_recommended):
                                textbutton caption action Return(key) xsize 578 text_size 20
                    $ commands = r13_rec_controls(r13_recommended)
                    grid 2 ((len(commands)+1)//2):
                        spacing 6
                        for command, caption in commands:
                            textbutton caption xsize 285 text_size 18 action (ShowMenu("save") if command=="save" else MainMenu(confirm=True) if command=="title" else Return(command))
                        if len(commands)%2:
                            null
                vbox:
                    xsize 525 spacing 8
                    textbutton "QA 전용 새 이야기 · 미검증 gate 시험" action Return("native_qa_start") text_size 17
                    textbutton "회의 연출 시연 · 미적용" action Return("staging_preview") text_size 18
                    text "확인한 물증 · 인물 카드" size 24
                    viewport:
                        ysize 440 mousewheel True draggable True scrollbars "vertical"
                        vbox:
                            spacing 8
                            for key in r13_recommended["facts"]:
                                textbutton r13_rec_cards[key][0] action Return("card:"+key) xsize 490 text_size 20

screen r13_recommended_cards(question):
    use r13_recommended_catalog(question)

label r13_recommended_start:
    call screen r13_recommended_setup
    $ room13_mode = True
    $ winter_mode = True
    $ winter = winter_new()
    $ source_mode = False
    $ room13 = r13_new()
    $ r13_rec_stage_memory = {}
    $ r13_recommended = r13_rec_opening_state()
    $ room13["campaign_id"] = "room13_recommended_v1"
    $ room13["day"] = r13_recommended["day"]
    $ r13_upgrade()
    $ r13_scene_key = None
    $ r13_world_cameras = {}
    $ r13_inspection_location = None
    $ room13["learning_archive"] = r13_learning_archive_seed()
    $ typing_allowed = True
    hide screen r13_hud
    hide screen winter_hud
    hide screen hud
    call r13_recommended_carriage_opening
    jump r13_recommended_hub

label r13_recommended_read_card:
    call screen r13_recommended_card_detail(r13_recommended_choice.split(":",1)[1])
    call screen r13_recommended_notebook
    if _return is not None:
        $ r13_recommended_choice = _return
        jump r13_recommended_read_card
    jump r13_recommended_hub

label r13_recommended_hub:
    $ r13_rec_stage_exit()
    if r13_recommended is None or r13_recommended.get("revision") != r13_rec_revision:
        call r13_lines([(None,"이 검증판 저장은 현재 이야기 버전과 다릅니다. 사실을 자동으로 바꾸지 않습니다. 제목 화면의 추천 스토리에서 새로 시작해 주세요.")], "recommended:version")
        return
    call r13_recommended_pick
    $ r13_recommended_choice = _return
    if r13_recommended_choice == "native_qa_start":
        jump r13_recommended_native_qa_start
    if r13_recommended_choice == "staging_preview":
        call r13_recommended_staging_admin
        jump r13_recommended_hub
    if r13_recommended_choice.startswith("card:"):
        jump r13_recommended_read_card
    if r13_recommended_choice == "evening":
        if r13_recommended["episode"] == 1 and r13_recommended["day"] == 2 and not {"heat_seen","piko_plan"} <= set(r13_recommended["done"]):
            call r13_lines([("dad","낮 점검과 피코 씨의 계획을 먼저 확인하자.")], "recommended:evening:before")
            jump r13_recommended_hub
        if r13_recommended["episode"] == 3 and r13_recommended["day"] == 5 and not r13_recommended["e3_school_handoff"]:
            menu:
                "저녁까지 기다리면 아직 하지 않은 낮 활동은 지나갑니다. 기다릴까요?"
                "아직 낮에 할 일을 한다":
                    jump r13_recommended_hub
                "저녁까지 기다린다":
                    pass
        $ r13_recommended = r13_rec_evening(r13_recommended)
        $ room13["period"] = 2
        call r13_lines([(None,"마을의 저녁 등불이 켜졌다. 낮에 보았던 곳도 지금은 다른 사람들이 쓰고 있었다.")], "recommended:evening")
        jump r13_recommended_hub
    if r13_recommended_choice == "advance":
        $ r13_recommended_block = r13_rec_block_reason(r13_recommended)
        if r13_recommended_block:
            call r13_lines([("dad",r13_recommended_block)], "recommended:day:open")
            jump r13_recommended_hub
        menu:
            "오늘을 마칠까요? 오늘 가능한 예방 행동을 놓칠 수 있습니다."
            "아직 조사한다":
                jump r13_recommended_hub
            "다음 날로 간다":
                $ r13_recommended = r13_rec_next_day(r13_recommended)
                $ room13["day"] = r13_recommended["day"]
                $ room13["period"] = r13_recommended.get("period",0)
        if r13_recommended["episode"] == 1 and r13_recommended["day"] == 3:
            call r13_scene("winter_square", "3일 아침 · 광장", "quiet")
            if r13_recommended["piko"] == "safe":
                call r13_scene("council", "3일 아침 · 여관 식당", "calm")
                call r13_lines([(None,"식당에서 피코가 붓을 털었다. 밤새 말린 초상을 다람에게 건넸다."),("resident_piko","약속한 그림이에요. 그분을 본 곳은 기록실 앞이 맞아요. 이름이나 지금 계신 곳까지는 모르지만요."),("daram","고마워요. 엄마한테 이것도 보여 줄래요." if r13_recommended["mother"]=="M2" else "고마워요. 엄마 만나면 이것도 보여 줄래요.")], "recommended:piko:portrait")
                call r13_scene("winter_square", "3일 아침 · 광장", "quiet")
                call r13_lines([(None,"식당을 나서자 광장 쪽에서 초롱의 목소리가 들렸다. 3번 등 뚜껑이 열려 있었고, 안은 비어 있었다."),("resident_lamplighter","돌이 없어졌어요. 어젯밤 여기서 주무셨으면 큰일 날 뻔했어요."),("resident_piko","어제는 우리가 자리를 옮겼죠. 제가 저기서 자려고 했다는 건 직접 말할게요."),("dad","그림도 고맙습니다. 우리가 아는 어제 일부터 함께 확인하죠.")], "recommended:piko:safe")
            else:
                call r13_lines([(None,"약속한 그림을 받으러 광장에 갔다. 초롱이 3번 등 아래에 무릎을 꿇고 있었다."),("resident_lamplighter","피코 씨, 들려요? 누구 진료소에 가 주세요!"),(None,"부리가 달려갔다. 다람이 아빠의 소매를 잡았다. 피코의 손 옆에는 어제 그리던 초상이 마른 채 놓여 있었다."),("daram","아빠, 어제 여기서 잔다고 했잖아."),("dad","응. 다람아, 아빠 곁에 있자."),(None,"서리 검사원이 와서 피코를 살폈다. 오래 살핀 뒤 고개를 저었다."),("resident_seori","너무 늦었습니다. 밤 추위를 견디지 못한 것으로 보입니다. 자세한 경과는 더 살펴야 합니다."),(None,"초롱이 피코에게 천을 덮었다. 약속한 초상은 젖지 않도록 아빠에게 건넸다."),("resident_lamplighter","이걸 드리려고 그렸다고 했어요. 돌까지 없어질 줄은 몰랐어요."),("dad","아내를 봤다고 말해 준 분이었는데…. 어제 계획과 오늘 빈 등이 어떻게 이어지는지 알고 싶습니다. 제가 직접 본 것도 있어요.")], "recommended:piko:dead")
            call r13_lines([("resident_ppul","내일 아침 식당에 모입시다. 돌이 어디로 갔는지, 누구에게 어떤 위험이 남았는지 확인해야겠소."),("resident_lamplighter","어제 점검 때 두 분도 계셨지요. 만진 곳과 안에서 본 것을 나눠 말해 주세요."),("dad","그러겠습니다. 오늘은 현물과 실제 본 사람의 말을 확인하겠습니다.")], "recommended:meeting:invitation")
        jump r13_recommended_hub
    if r13_recommended_choice == "next_episode":
        $ r13_recommended = r13_rec_begin_episode(r13_recommended, r13_rec_next_available(r13_recommended))
        $ room13["day"] = r13_recommended["day"]
        jump r13_recommended_hub
    if r13_recommended_choice == "hearing":
        jump expression r13_rec_episodes[r13_recommended["episode"]]["hearing_label"]
    $ room13["day"] = r13_recommended["day"]
    $ r13_recommended_spec = r13_rec_actions[r13_recommended_choice]
    $ r13_recommended_place = r13_recommended_spec["place"]
    $ r13_recommended_background = (r13_recommended_spec.get("background_key") or r13_rec_location_info(r13_recommended_place,r13_recommended)[1])
    call r13_scene(r13_recommended_background, r13_recommended_spec["title"], "calm")
    call r13_lines(r13_rec_action_lines(r13_recommended,r13_recommended_choice), "recommended:"+r13_recommended_choice)
    if r13_recommended_spec.get("label"):
        call expression r13_recommended_spec["label"]
        if _return is False:
            jump r13_recommended_hub
    $ r13_recommended = r13_rec_apply(r13_recommended, r13_recommended_choice)
    if r13_recommended_choice == "shelter":
        call r13_lines([(None,"세 사람의 식사가 같은 상 위에 놓였다. 다람이 이불 세 자리를 손으로 짚으며 세었다."),("daram","하나, 둘, 셋. 오늘은 아무도 다른 데 가면 안 돼."),("mom","응. 오늘은 여기 같이 있자.")], "recommended:family:complete")
    jump r13_recommended_hub

label r13_recommended_hearing:
    if not r13_rec_hearing_ready(r13_recommended):
        call r13_lines([("dad","피코 씨가 기대고 있던 등이 왜 비었는지 알고 싶어요. 따뜻한 등 안을 직접 본 일, 돌의 번호, 돌을 건네받은 사람의 말을 더 확인해야겠어요.")], "recommended:hearing:missing")
        jump r13_recommended_hub
    call r13_scene("council", "4일 · 광장의 돌 공개 회의", "calm")
    $ r13_rec_stage_enter(1)
    if "piko_container_exclusive_claim" not in r13_recommended["done"]:
        call r13_lines([("resident_ppul","돌을 받은 아이의 말은 들었소. 이제 광장의 등을 누가 열었는지 설명해 주시오."),("nabi","아이들에게 돌을 가져다준 건 맞아요. 하지만 등에서 꺼낸 건 아니에요. 밖에 놓여 있던 돌을 주워 담았어요."),("dad","그럼 돌을 담기 전이나 아이에게 주기 전에, 그 용기나 깔개 천을 다른 사람에게 맡긴 적은 있습니까?"),("nabi","아니요. 꼬미에게 빈 통을 빌린 뒤 지금까지 줄곧 제가 들고 다녔어요. 천도 저만 썼어요. 등 뚜껑을 열거나 안을 닦은 적도 없고요."),(None,"나비가 오늘 배식에 쓰던 용기와 천을 탁자 위에 놓았다. 초롱도 광장의 등을 가져와 나란히 놓았다."),("nabi","제 설명이 맞는지 이것도 봐 주세요."),("dad","그 말씀이군요. 아이에게 넘긴 일과 등에서 꺼낸 일을 구별해서 보겠습니다.")], "recommended:hearing:new-defense")
        $ r13_recommended = r13_rec_piko_hear_defense(r13_recommended)
        if "cloth_contact_matched" in r13_recommended["done"]:
            call r13_lines([("dad","먼저 맞춰 본 천 조각이 마음에 걸렸어. 이제 나비 씨가 말한 운반 과정과도 맞춰 보자.")], "recommended:hearing:prior-deduction")
    if "piko_source_claim_early" in r13_recommended["done"]:
        call r13_lines([(None,"초롱이 광장의 등을 회의 탁자에 내려놓았다."),("nabi","먼저 보여드렸던 통과 천을 다시 가져왔어요."),("dad","그때 들은 설명도 기억합니다. 밖의 돌만 담았고, 용기와 천은 혼자 쓰셨다고 했지요.")], "recommended:hearing:earlier-account")
        if "cloth_contact_matched" in r13_recommended["done"] and r13_rec_piko_geometry_ready(r13_recommended):
            menu (screen="r13_rec_stage_choice"):
                "이미 직접 확인한 대조를 어떻게 설명할까?"
                "확인한 흔적과 나비의 설명을 잇는다":
                    call r13_lines([("dad","돌을 받은 사람과 17번 번호를 먼저 확인했고, 그다음 허락받은 천을 맞춰 봤어요. 뚜껑 안쪽 조각과 이어졌지요. 꼬미가 빌려줄 때 펼친 천은 온전했고, 그날 돌을 내려놓을 때 그 모서리는 이미 찢어져 있었어요. 그 사이 혼자 쓰셨고 등 안에는 손대지 않았다고 하셨지요. 그 찢김이 뚜껑 안쪽 조각과 이어집니다. 밖의 돌만 담았다는 설명과는 맞지 않아요.")], "recommended:hearing:prior-case")
                    $ r13_recommended = r13_rec_piko_summarize_prior(r13_recommended)
                "자료를 하나씩 나란히 보여 준다":
                    pass
    if "cloth_contact_matched" not in r13_recommended["done"]:
        menu (screen="r13_rec_stage_choice"):
            "나비가 가져온 천을, 미리 확인한 등 안쪽 조각과 맞춰 볼까?"
            "허락받은 천의 찢김과 안쪽 조각을 맞춰 본다":
                call r13_recommended_contact_inspect
                if _return:
                    $ r13_recommended = r13_rec_apply(r13_recommended,"contact_match")
            "우선 들은 말과 돌의 이동부터 정리한다":
                pass
    while r13_recommended["hearing"] < len(r13_rec_hearing_steps(r13_recommended)):
        $ r13_rec_stage_step = r13_rec_hearing_steps(r13_recommended)[r13_recommended["hearing"]][1]
        $ r13_rec_stage_prompt(r13_rec_stage_step)
        call screen r13_recommended_cards(r13_rec_hearing_steps(r13_recommended)[r13_recommended["hearing"]][0])
        if _return is None:
            jump r13_recommended_hub
        $ r13_recommended, r13_recommended_feedback, r13_recommended_correct = r13_rec_present(r13_recommended, _return)
        $ r13_rec_stage_answer(r13_rec_stage_step,r13_recommended_correct)
        call r13_lines([("dad",r13_recommended_feedback)], "recommended:hearing:answer")
    if r13_recommended["verdict"] == "direct_removal":
        call r13_lines([("nabi","제가 그 천으로 돌을 들어서 용기에 넣었어요. 아이들 자리를 덥히려고 가져갔어요."),("dad","나비 씨가 돌을 옮긴 건 알겠어요. 앞으로는 가져가는 사람과 받는 사람이 함께 알려 주세요. 하지만 이걸로 피코 씨를 해치려 했다고 말할 수는 없어요."),("resident_ppul","나비는 배식을 계속 맡으시오. 공공 물자를 옮길 때는 인계 상대와 함께 확인하고 기록을 남기시오.")], "recommended:hearing:direct-removal")
    else:
        call r13_lines([("nabi","아이들이 추워서 돌을 갖다줬어요. 피코 씨에게는 자리를 옮기라고 말하지 못했어요."),("dad","아이들을 먹이는 일은 계속 맡아 주세요. 대신 공공 돌을 옮길 때는 함께 확인하고 어디에 놓았는지 알려야 합니다."),("dad","아이에게 돌을 준 건 알겠어요. 광장에서 직접 꺼냈는지는 아직 더 봐야겠어요. 두 일을 같은 말로 넘기지는 않을게요."),("resident_ppul","나비는 배식을 계속 맡으시오. 공공 물자를 옮길 때는 인계 상대와 함께 확인하고 기록을 남기시오."),("nabi","알겠어요. 오늘 아이들 식사부터 준비할게요.")], "recommended:hearing:result")
    if r13_recommended["piko"] == "safe":
        call r13_lines([("resident_piko","그때 옮겨 준 덕분에 여기서 직접 말할 수 있네요.")], "recommended:hearing:survivor")
    call r13_lines([(None,"회의가 끝나자 사람들이 자리에서 일어났다. 나비는 주방으로 돌아갔다. 다람이 아빠 손을 잡았다."),("daram","아빠, 이제 우리 할 일 하러 가자.")], "recommended:slice:end")
    jump r13_recommended_hub

label r13_recommended_contact_inspect:
    call screen r13_rec_cloth_comparison
    if _return != "matched":
        return False
    call screen r13_rec_piko_contact_sequence
    if not _return:
        return False
    if not r13_rec_piko_geometry_ready(r13_recommended):
        call screen r13_recommended_status("등과 천의 형상 검수 상태와 실제 화면 검증을 구분합니다. 아직 실행 화면의 대조·좌표 검증이 끝나지 않아 직접 반출 확정은 잠겨 있습니다.")
        return False
    call r13_lines([(None,"뚜껑을 닫으면 가려지는 안쪽 쇠붙이의 조각이다. 밖에 놓인 돌만 집어 넣는 동안에는 닫힌 뚜껑 너머 그 자리에 천이 닿지 않는다."),(None,"용기의 천을 풀어 대자 찢긴 가장자리와 두 줄무늬가 같은 위치에서 이어졌다. 천 중앙은 찢어지지 않았다."),("dad","두 줄과 찢긴 자리가 이어지는구나. 누가 빌려 썼고 돌을 내려놓을 때 천이 어땠는지도 꼬미에게 들은 말과 함께 보자.")], "recommended:contact:match")
    return True

screen r13_recommended_status(message):
    modal True
    add Solid("#172421ed")
    frame:
        xalign .5 yalign .5 xsize 950
        vbox:
            spacing 24
            text "개발 검증 상태" size 28
            text message size 24
            textbutton "돌아가기" action Return(True)

# New explicit testimony detail, not Dad's invented memory or a new evidence item.
label r13_rec_piko_intact_loan:
    call screen r13_rec_piko_intact_cloth
    return True

screen r13_rec_piko_intact_cloth(as_overlay=False):
    modal True
    default after_delivery = False
    add Solid("#20202bea")
    frame:
        align (.5,.5) xsize 960 padding (30,24)
        vbox:
            spacing 20
            text ("꼬미가 설명한 같은 저녁 · 돌을 내려놓을 때" if after_delivery else "꼬미가 설명한 2일 저녁 · 빌려주기 전") size 28
            text ("나비가 천을 풀어 돌을 내려놓았다. 꼬미가 맞춰 접었던 같은 모서리는 이미 찢어져 있었다." if after_delivery else "빈 통에 넣기 전 직접 펼쳐 보고 접었다. 그때는 모서리와 두 줄무늬가 끊기지 않았다.") size 23 xsize 880
            if after_delivery:
                add r13_rec_cloth_part("parent") xalign .5
            else:
                add Transform(Transform(Crop(R13_REC_CLOTH_SOURCE_RECT,R13_REC_CLOTH_TEXTURE),xysize=(300,174),nearest=False),xysize=(600,348),nearest=True) xalign .5
            text "동일한 천의 전후 · 꼬미의 관찰을 그린 재구성" size 19
            textbutton ("빌려주기 전 모습" if after_delivery else "돌을 내려놓을 때 모습") action ToggleScreenVariable("after_delivery")
            textbutton "꼬미의 이야기로 돌아간다" action (Hide("r13_rec_piko_intact_cloth") if as_overlay else Return(True)) sensitive (as_overlay or after_delivery)


screen r13_rec_piko_contact_sequence():
    modal True
    default frame_index = 0
    default fitting_seen = False
    $ frames = [('open__640x400.png','등을 벤치 받침에 놓고 뚜껑을 연 모습'),('grip__640x400.png','천을 접어 뜨거운 돌을 감싸는 동작'),('contact__640x400.png','천이 닿는 안쪽 고정부를 직접 짚어 보자'),('lifted__640x400.png','돌이 빠진 뒤에도 같은 안쪽 고정부에 남은 조각'),('container_unfolded__640x400.png','같은 천을 용기에서 펼쳐 본 모습'),('inner_fitting_section.png','뚜껑을 닫으면 가려지는 고정부 단면')]
    add Solid('#20202bea')
    frame:
        area (150,30,980,660) padding (0,0)
        fixed:
            text '등·돌·천의 접촉 · 동작 재구성' xpos 28 ypos 24 size 28
            text frames[frame_index][1] xpos 28 ypos 68 size 22
            # Exact contract: final640x400 at screen(320,140), no rescaling.
            add ('assets/recommended-story-icons/piko-native-v4/'+frames[frame_index][0]) xpos 170 ypos 110
            if frame_index==2:
                button:
                    area (584,232,54,54)
                    background Solid('#f6d58a25') hover_background Solid('#f6d58a88')
                    action SetScreenVariable('fitting_seen',True)
                    alt '천 모서리가 스치는 안쪽 금속 고정부'
                if fitting_seen:
                    text '고정부 위치 확인' xpos 680 ypos 240 size 18 color '#3a4934'
            text '실제 반출 시점은 꼬미가 본 천의 전후와 함께 판단한다.' xpos 28 ypos 530 size 18
            hbox:
                xpos 28 ypos 577 spacing 28
                textbutton '앞 장면' action SetScreenVariable('frame_index',max(0,frame_index-1)) sensitive frame_index>0
                textbutton '다음 장면' action SetScreenVariable('frame_index',min(len(frames)-1,frame_index+1)) sensitive frame_index<len(frames)-1
                textbutton '구조 확인을 마친다' action Return(True) sensitive (frame_index==len(frames)-1 and fitting_seen)
                textbutton '돌아가기' action Return(False)
            if frame_index==len(frames)-1 and not fitting_seen:
                text '앞 장면의 천 접촉 위치를 직접 확인하자.' xpos 28 ypos 627 size 18
    key 'game_menu' action Return(False)


label r13_recommended_art_admin:
    # Native-only disposable inspection fixture, never awards facts or opens gates.
    call screen r13_rec_cloth_comparison
    call screen r13_rec_piko_contact_sequence
    return
