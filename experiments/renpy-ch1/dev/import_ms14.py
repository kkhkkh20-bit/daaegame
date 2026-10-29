"""Build a deliberately bounded, explicitly routed adaptation; never interpret author guards."""
import json, pathlib, shutil, hashlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('source',type=pathlib.Path,help='Merged delivery folder containing 01_스토리기준본')
SOURCE=parser.parse_args().source.resolve()
DATA = ROOT / 'game/ms14'
DATA.mkdir(parents=True, exist_ok=True)
(ROOT/'docs/story-ms14/source').mkdir(parents=True,exist_ok=True)
story_path = next((SOURCE/'01_스토리기준본').glob('*대사연출조건.json'))
story = json.loads(story_path.read_text())
scenes = {s['scene_id']: s for s in story['scenes']}
blocks = {b['id']: b for s in story['scenes'] for b in s['blocks']}
records = {r['id']: r for b in blocks.values() for r in b['records']}
for path in (SOURCE/'01_스토리기준본').iterdir():
    if path.is_file(): shutil.copy2(path, ROOT/'docs/story-ms14/source'/path.name)

nodes = {}
def sid(day, scene): return 'MS14_D%02d_S%02d' % (day, scene)
def bid(day, scene, block): return sid(day,scene)+'_B%03d'%block
def line(day, scene, number): return sid(day,scene)+'_L%04d'%number
def block(name, day, scene, number, next, start=None, stop=None):
    b = blocks[bid(day,scene,number)]
    rows = b['records']
    if start: rows = rows[next_i(rows,start):]
    if stop: rows = rows[:next_i(rows,stop)]
    nodes[name] = dict(kind='block', scene=sid(day,scene), source_block=b['id'],
        records=[r['id'] for r in rows], next=next)
def next_i(rows, suffix): return next(i for i,r in enumerate(rows) if r['id'].endswith('_'+suffix))
def choice(name, scene, title, options):
    nodes[name] = dict(kind='choice', scene=scene, title=title, options=[dict(title=o[0],to=o[1],guard=o[2] if len(o)>2 else []) for o in options])
def gate(name, scene, title, to): choice(name,scene,title,[(title,to)])
def branch(name, field, value, yes, no): nodes[name]=dict(kind='branch',field=field,value=value,yes=yes,no=no)
def proof(name, scene, title, correct, to, wrong, hint, prerequisite=()):
    nodes[name]=dict(kind='proof',scene=scene,title=title,correct=correct,to=to,wrong=wrong,hint=hint,requires=list(prerequisite))
def chain(day,scene,nums,to,prefix=None):
    prefix=prefix or sid(day,scene)
    for i,n in enumerate(nums): block(prefix+':'+str(n),day,scene,n,prefix+':'+str(nums[i+1]) if i+1<len(nums) else to)
    return prefix+':'+str(nums[0])

# Day 1: explicit observation and proof inputs, including the early correct answer.
block('start',1,1,1,'letter_open')
gate('letter_open',sid(1,1),'편지를 펼친다','letter_read')
block('letter_read',1,1,2,'letter_menu')
choice('letter_menu',sid(1,1),'편지를 살펴볼까?', [('마지막 줄을 본다','letter_last'),('글씨를 살핀다','letter_hand'),('편지를 접는다','letter_close')])
block('letter_last',1,1,3,'letter_menu'); block('letter_hand',1,1,4,'letter_menu')
branch('letter_close','K01a',True,'letter_any','letter_close_b')
branch('letter_close_b','K01b',True,'letter_any','letter_none')
block('letter_any',1,1,5,'carriage_end');block('letter_none',1,1,6,'carriage_end')
block('carriage_end',1,1,7,'leave_carriage')
gate('leave_carriage',sid(1,1),'마차에서 내린다', 'gate_arrival')
nodes['leave_carriage']['options'][0]['effects']=['carriage_stopped=true']
block('gate_arrival',1,2,1,'gate_request',stop='L0019')
gate('gate_request',sid(1,2),'초소 처리 명단을 읽는다','gate_list')
block('gate_list',1,2,1,'gate_choice',start='L0019')
choice('gate_choice',sid(1,2),'어떤 자료부터 보여 줄까?', [('초대 편지를 보여 준다','gate_letter'),('가족 방문 신청서를 찾는다','gate_original')])
block('gate_letter',1,2,2,'gate_original_out');block('gate_original',1,2,3,'gate_original_out')
block('gate_original_out',1,2,4,'gate_investigate')
choice('gate_investigate',sid(1,3),'자료를 살펴본다',[
    ('신청 원본을 읽는다','gate_read_original'),('겨울철 입장 규칙을 읽는다','gate_read_rules'),
    ('초소 처리 명단을 다시 본다','gate_reread_list'),
    ('두 종이의 항목을 비교한다','gate_purpose',[['evidence','E03',True]]),
    ('숙소 확인 칸을 본다','gate_lodging',[['evidence','E03',True]]),
    ('자료를 함께 제시한다','gate_proof'),('힌트를 생각한다','gate_hint'),
    ('왜 일꾼으로 적혔는지 묻는다','gate_reason',[['state','purpose_difference_known',True],['state','reason_heard',False]])])
block('gate_read_original',1,3,1,'gate_investigate',start='L0002',stop='L0007')
block('gate_read_rules',1,3,1,'gate_investigate',start='L0007',stop='L0008')
nodes['gate_reread_list']=dict(kind='read',key='E02',next='gate_investigate',scene=sid(1,3))
block('gate_purpose',1,3,2,'gate_investigate');block('gate_lodging',1,3,3,'gate_investigate')
proof('gate_proof',sid(1,3),'함께 들어갈 근거를 고른다', ['E02','E03','E04'],'gate_proven_dispatch','gate_wrong','gate_hint')
nodes['gate_proof']['wrong_routes']={'E03':'gate_number'}
branch('gate_proven_dispatch','purpose_difference_known',True,'gate_proven','gate_early')
block('gate_proven',1,3,4,'registered');block('gate_early',1,3,5,'registered')
block('gate_number',1,3,6,'gate_investigate');block('gate_wrong',1,3,7,'gate_investigate')
block('gate_hint',1,3,9,'gate_investigate');block('gate_reason',1,3,10,'gate_investigate')
block('registered',1,4,1,'registered_menu')
choice('registered_menu',sid(1,4),'짐을 찾으러 가기 전에',[
    ('왜 일꾼으로 바뀌었습니까?','registered_reason',[['state','reason_heard',False]]),('짐을 찾아 여관으로 간다','registered_depart')])
block('registered_reason',1,4,2,'registered_menu');block('registered_depart',1,4,3,'inn')
block('inn',1,5,1,'room_observe',stop='L0015')
gate('room_observe',sid(1,5),'빈방을 살핀다','room_empty')
block('room_empty',1,5,1,'note_pick',start='L0015',stop='L0018')
gate('note_pick',sid(1,5),'책상 메모를 집는다','room_note')
block('room_note',1,5,1,'bundle_open',start='L0018')
gate('bundle_open',sid(1,5),'책상 아래 보따리를 연다','bundle')
block('bundle',1,5,2,'letter_compare')
proof('letter_compare',sid(1,5),'두 편지를 나란히 본다',['E01','E06'],'room_compare',None,None)
block('room_compare',1,5,3,'sleep1')
gate('sleep1',sid(1,5),'과자를 두고 잠든다','day2')
nodes['sleep1']['options'][0]['effects']=['day=2']

# Day 2: all necessary actions are inputs, not automatic completion on scene entry.
block('day2',2,1,1,'lamp_rope',stop='L0009')
block('square2',2,1,1,'lamp_rope',start='L0009')
nodes['day2']['next']='square2'
gate('lamp_rope',sid(2,1),'덮개 지지 끈을 잡는다','chorong')
block('chorong',2,1,2,'go_box',stop='L0030')
gate('go_box',sid(2,1),'초롱과 교환함으로 간다','box_path')
block('box_path',2,1,2,'box_inspect',start='L0030',stop='L0033')
gate('box_inspect',sid(2,1),'함과 주변을 직접 확인한다','box_empty')
block('box_empty',2,1,2,'box_note',start='L0033')
gate('box_note',sid(2,1),'도착 쪽지를 직접 넣는다','box_written')
block('box_written',2,1,3,'post')
block('post',2,2,1,'envelope_show')
gate('envelope_show',sid(2,2),'초대 편지의 봉투를 보여 준다','post_checked')
block('post_checked',2,2,2,'post_menu')
choice('post_menu',sid(2,2),'더 물을까?', [('대필도 합니까?','post_scribe'),('편지를 돌려받는다','post_return')])
block('post_scribe',2,2,3,'post_menu');block('post_return',2,2,4,'piko2')
block('piko2',2,3,1,'portrait_ask',stop='L0009')
gate('portrait_ask',sid(2,3),'스케치를 보여 주고 부탁한다','portrait_commission')
block('portrait_commission',2,3,1,'lamp_observe',start='L0009')
choice('lamp_observe',sid(2,3),'3번 등을 살핀다',[(t,'lamp_seen_'+str(i)) for i,t in enumerate(['번호판을 본다','덮개를 본다','담요를 본다','받침과 바닥을 본다'])]+[('살펴보기를 마친다','lamp_details',[['state','lamp_part_'+str(i),True] for i in range(4)])])
for i in range(4):
    nodes['lamp_seen_'+str(i)]=dict(kind='mark',effects=['lamp_part_%d=true'%i],next='lamp_observe',scene=sid(2,3))
block('lamp_details',2,3,2,'diner_offer')
block('diner_offer',2,4,1,'afternoon')
choice('afternoon',sid(2,4),'해가 지기 전에', [('피코의 잠자리를 마련한다','shelter_choice'),('네로를 만나러 간다','nero_choice')])
nodes['afternoon']['options'][0]['effects']=['D02_afternoon=shelter'];nodes['afternoon']['options'][1]['effects']=['D02_afternoon=nero']
block('shelter_choice',2,4,2,'shelter_work')
gate('shelter_work',sid(2,4),'포대를 옮기고 천을 빌린다','shelter_prepare')
block('shelter_prepare',2,4,3,'shelter_enter',stop='L0029')
gate('shelter_enter',sid(2,4),'피코와 식당에 들어간다','shelter_done')
block('shelter_done',2,4,3,'evening2',start='L0029')
block('nero_choice',2,4,4,'nero_work')
gate('nero_work',sid(2,4),'침구를 옮겨 묶고 이름을 적는다','nero_done')
block('nero_done',2,4,5,'evening2')
block('evening2',2,5,1,'evening2_route')
branch('evening2_route','piko_sheltered',True,'evening2_alive','evening2_outside')
block('evening2_alive',2,5,2,'evening2_end');block('evening2_outside',2,5,3,'evening2_end')
block('evening2_end',2,5,4,'sleep2')
gate('sleep2',sid(2,5),'아침 약속을 적고 잠든다','day3')
nodes['sleep2']['options'][0]['effects']=['day=3']

# Day 3: proof stages are separate; a fitting knife is never the theft verdict.
branch('day3','piko_sheltered',True,'piko_alive3','piko_dead3')
block('piko_alive3',3,1,3,'lamp3',stop='L0035')
gate('piko_clean',sid(3,1),'약속한 자리를 치운다','piko_receive')
nodes['piko_alive3']['next']='piko_clean'
block('piko_receive',3,1,3,'lamp3',start='L0035')
block('piko_dead3',3,1,2,'lamp3')
block('lamp3',3,2,1,'lamp_inspect3')
gate('lamp_inspect3',sid(3,2),'번호판·받침·자국을 살핀다','lamp_interior3')
block('lamp_interior3',3,2,2,'fragment_request',stop='L0016')
gate('fragment_request',sid(3,2),'톡에게 안쪽 파편을 확인받는다','lamp_fragment3')
block('lamp_fragment3',3,2,2,'lamp_log_request',start='L0016')
gate('lamp_log_request',sid(3,2),'초롱의 점검장을 확인한다','lamp_log3')
block('lamp_log3',3,2,3,'workshop3')
block('workshop3',3,3,1,'loan_read',stop='L0007')
gate('loan_read',sid(3,3),'대여 쪽지를 읽는다','loan3')
block('loan3',3,3,1,'clinic3',start='L0007',stop='L0012')
block('clinic3',3,3,1,'measurement_read',start='L0012')
gate('measurement_read',sid(3,3),'측정지를 읽는다','measurement3')
block('measurement3',3,3,2,'measurement_proof')
proof('measurement_proof',sid(3,3),'측정 종료와 점검 기록을 대조한다',['E13','E11'],'measurement_correct','measurement_wrong','measurement_hint')
block('measurement_correct',3,3,4,'measurement_after')
block('measurement_wrong',3,3,6,'measurement_proof');block('measurement_hint',3,3,7,'measurement_proof')
block('measurement_after',3,3,5,'silluk3')
block('silluk3',3,4,1,'transport_read',stop='L0009')
gate('transport_read',sid(3,4),'운반표를 본다','transport3')
block('transport3',3,4,1,'knife_permission',start='L0009',stop='L0010')
gate('knife_permission',sid(3,4),'칼을 보여 달라고 요청한다','knife_observed')
block('knife_observed',3,4,1,'store_visit',start='L0010',stop='L0021')
gate('store_visit',sid(3,4),'수취 창고에서 확인한다','store3')
block('store3',3,4,1,'stone_check',start='L0021',stop='L0025')
gate('stone_check',sid(3,4),'톡에게 각인 확인을 부탁한다','stone3')
block('stone3',3,4,1,'sale_check',start='L0025',stop='L0032')
gate('sale_check',sid(3,4),'매입 기록을 본다','sale3')
block('sale3',3,4,1,'trial_open',start='L0032')
block('trial_open',3,5,1,'trial_repair')
proof('trial_repair',sid(3,5),'수리와 반출을 가릴 자료를 낸다',['E11','E12','E13'],'trial_repair_ok','trial_wrong','trial_hint')
block('trial_repair_ok',3,5,3,'trial_sale')
proof('trial_sale',sid(3,5),'돌과 매입 기록을 낸다',['E15','E16'],'trial_sale_ok','trial_wrong_sale','trial_hint_sale')
block('trial_sale_ok',3,5,5,'trial_knife')
choice('trial_knife',sid(3,5),'파편과 칼을 살핀다', [('깨진 칼끝을 안쪽 조각에 맞대 본다','knife_fit',[['state','silluk_knife_comparison_consent',True],['evidence','E32',True]]),('칼끝 모양을 안벽의 긁힌 자국에 견준다','knife_wrong'),('자료를 다시 본다','trial_knife_records')])
nodes['trial_knife_records']=dict(kind='notebook',next='trial_knife',scene=sid(3,5))
block('knife_fit',3,5,7,'trial_latch')
block('knife_wrong',3,5,21,'trial_knife')
proof('trial_latch',sid(3,5),'바깥 걸쇠 주장과 발견 위치를 대조한다',['E17','E32','E33'],'trial_latch_ok','trial_wrong_latch','trial_hint_latch')
block('trial_latch_ok',3,5,9,'trial_stone')
proof('trial_stone',sid(3,5),'마지막 점검과 인수한 돌을 연결한다',['E11','E15','E16'],'trial_stone_ok','trial_wrong_stone','trial_hint_stone')
block('trial_stone_ok',3,5,11,'badugi_arrives')
block('badugi_arrives',3,5,12,'trial_piko')
branch('trial_piko','piko_alive',True,'trial_alive','trial_dead')
block('trial_alive',3,5,14,'trial_choices');block('trial_dead',3,5,13,'trial_choices')
block('trial_choices',3,5,15,'stone_choice')
choice('stone_choice',sid(3,5),'3번 돌은 어떻게 할까?', [('3번 돌을 돌려받는다','stone_return'),('지금은 반환을 보류한다','stone_defer')])
block('stone_return',3,5,16,'custody_choice');block('stone_defer',3,5,17,'custody_choice')
choice('custody_choice',sid(3,5),'실룩을 지금 데려가겠다는 너울에게', [('즉시 인계에 반대한다','silluk_report'),('기록과 함께 인계한다','silluk_transfer')])
block('silluk_report',3,5,19,'restore_route');block('silluk_transfer',3,5,20,'restore_route')
for suffix,back in [('', 'trial_repair'),('_sale','trial_sale'),('_latch','trial_latch'),('_stone','trial_stone')]:
    block('trial_wrong'+suffix,3,5,22,back);block('trial_hint'+suffix,3,5,23,back)
branch('restore_route','public_stones','returned_uninstalled','restore_input','restore_defer')
gate('restore_input',sid(3,6),'톡·초롱과 3번 돌을 복구한다','restore3')
block('restore3',3,6,2,'box_news3');block('restore_defer',3,6,3,'box_news3')
block('box_news3',3,6,4,'memorial_route')
branch('memorial_route','piko_alive',True,'piko_evening','piko_memorial')
block('piko_evening',3,6,6,'somi_lead');block('piko_memorial',3,6,5,'somi_lead')
block('somi_lead',3,6,7,'blankets_route')
branch('blankets_route','nero_bedding_reserved',True,'blankets_receive','stairs3')
gate('blankets_receive',sid(3,6),'예약한 침구를 확인해 받는다','blankets3')
block('blankets3',3,6,8,'stairs3');block('stairs3',3,6,9,'sleep3')
gate('sleep3',sid(3,6),'그림을 세워 두고 잠든다','day4')
nodes['sleep3']['options'][0]['effects']=['day=4']

# Day 4 ordinary conversation pilot, preserving arrival, departure and missed supply cost.
branch('day4','silluk_status','detained_work_waiting_station','labor4','nero4')
block('labor4',4,1,2,'nero4')
block('nero4',4,1,3,'nero4_route')
branch('nero4_route','nero_met_day2',True,'nero4_again','nero4_first')
block('nero4_again',4,1,4,'somi4');block('nero4_first',4,1,5,'nero4_help')
gate('nero4_help',sid(4,1),'물통을 바꾸고 침구를 함께 짠다', 'nero4_work')
block('nero4_work',4,1,6,'somi4');block('somi4',4,1,7,'d4_depart')

# Days 4-5: source actions are explicit inputs. No guessed suspect, witness or timer.
gate('d4_depart',sid(4,1),'광장으로 돌아간다','d4_eaves')
block('d4_eaves',4,2,1,'d4_portrait_offer',stop='L0016')
gate('d4_portrait_offer',sid(4,2),'초상을 기대 놓고 물러난다','d4_bami')
block('d4_bami',4,2,1,'d4_afternoon_visit',start='L0016',stop='L0029')
gate('d4_afternoon_visit',sid(4,2),'오후에 솜이네를 다시 찾는다','d4_visit_declined')
block('d4_visit_declined',4,2,1,'d4_gate_cry',start='L0029')
block('d4_gate_cry',4,3,1,'d4_light_observe')
gate('d4_light_observe',sid(4,3),'다람을 뒤에 세우고 살핀다','d4_first_statement')
block('d4_first_statement',4,3,2,'d4_hear_bami')
block('d4_hear_bami',4,4,1,'d4_field',stop='L0033')
choice('d4_field',sid(4,4),'초소 불빛 안에서 살핀다',[
    ('울타리의 천을 본다','d4_seen_fence'),('겹친 발자국을 본다','d4_seen_tracks'),
    ('엎어진 양동이를 본다','d4_seen_bucket'),
    ('관찰을 정리한다','d4_field_talk',[['state','d4_fence_seen',True],['state','d4_tracks_seen',True],['state','d4_bucket_seen',True]])])
for key in ('fence','tracks','bucket'):
    nodes['d4_seen_'+key]=dict(kind='mark',scene=sid(4,4),effects=['d4_'+key+'_seen=true'],next='d4_field')
block('d4_field_talk',4,4,2,'d4_collect_input')
gate('d4_collect_input',sid(4,4),'위치를 그리고 바둑이를 부른다','d4_collect')
block('d4_collect',4,4,3,'d4_diner',stop='L0051')
block('d4_diner',4,4,3,'d4_box_news',start='L0051',stop='L0060')
block('d4_box_news',4,4,3,'sleep4',start='L0060')
gate('sleep4',sid(4,4),'관찰과 추측을 나눠 적고 잔다','day5')
nodes['sleep4']['options'][0]['effects']=['day=5']

block('day5',5,1,1,'d5_enter',stop='L0008')
gate('d5_enter',sid(5,1),'솜이의 동의를 받고 들어간다','d5_inside')
block('d5_inside',5,1,1,'d5_wait',start='L0008')
gate('d5_wait',sid(5,1),'기다렸다가 옷을 확인한다','d5_consent')
block('d5_consent',5,2,1,'d5_cloth_input')
gate('d5_cloth_input',sid(5,2),'허락받은 옷과 천을 나란히 본다','d5_cloth_compare')
block('d5_cloth_compare',5,2,2,'d5_clinic_handover',stop='L0029')
block('d5_clinic_handover',5,2,2,'d5_gate_visit',start='L0029')
gate('d5_gate_visit',sid(5,2),'돌목의 말을 다시 확인한다','d5_gate_open')
block('d5_gate_open',5,3,1,'d5_rebuttal_menu')
choice('d5_rebuttal_menu',sid(5,3),'밤이를 붙잡아 둘 근거를 확인한다',[
    ('키가 작으니 불가능하다고 한다','d5_height_wrong'),('자료를 함께 제시한다','d5_proof'),
    ('힌트를 생각한다','d5_hint')])
block('d5_height_wrong',5,3,3,'d5_rebuttal_menu')
proof('d5_proof',sid(5,3),'최초 진술과 현장·귀가 관찰을 제시한다',['E20','E22','E23','E24'],
    'd5_bami_cleared','d5_wrong','d5_hint')
block('d5_wrong',5,3,5,'d5_rebuttal_menu');block('d5_hint',5,3,6,'d5_rebuttal_menu')
block('d5_bami_cleared',5,3,4,'d5_chorong')
block('d5_chorong',5,4,1,'d5_open_letter',stop='L0005')
gate('d5_open_letter',sid(5,4),'바람을 피해 봉투를 연다','d5_warning')
block('d5_warning',5,4,1,'d5_warning_compare',start='L0005')
proof('d5_warning_compare',sid(5,4),'초대 편지와 답장을 비교한다',['E01','E27'],'d5_warning_contrast',None,None)
block('d5_warning_contrast',5,4,2,'d5_review_choice')
choice('d5_review_choice',sid(5,4),'앞서 들은 말도 다시 볼까?',[
    ('여관과 연락에 관한 말을 다시 본다','d5_review_day1'),('지금의 편지 이야기를 이어간다','d5_warning_talk')])
block('d5_review_day1',5,4,3,'d5_warning_talk')
block('d5_warning_talk',5,4,4,'d5_reply_input',stop='L0027')
gate('d5_reply_input',sid(5,4),'함께 답장을 쓴다','d5_reply')
block('d5_reply',5,4,4,'d5_reply_handover',start='L0027',stop='L9501')
gate('d5_reply_handover',sid(5,4),'초롱에게 직접 답장을 건넨다','d5_reply_given')
block('d5_reply_given',5,4,4,'d5_water_return',start='L9501')
gate('d5_water_return',sid(5,4),'솜이네에 물통을 돌려준다','d5_night_visit')
block('d5_night_visit',5,5,1,'d5_diner_guard',stop='L0018')
block('d5_diner_guard',5,5,1,'d5_inn_lobby',start='L0018',stop='L0027')
block('d5_inn_lobby',5,5,1,'d5_hall',start='L0027',stop='L0033')
block('d5_hall',5,5,1,'d5_lock_input',start='L0033',stop='L0038')
gate('d5_lock_input',sid(5,5),'걸쇠와 창문 잠금을 확인한다','d5_safety')
block('d5_safety',5,5,1,'d5_blanket_route',start='L0038')
branch('d5_blanket_route','carried_dry_blankets',2,'d5_pack_blankets','d5_no_blankets')
nodes['d5_blanket_route']['otherwise_value']=0
block('d5_pack_blankets',5,5,2,'d5_cookie');block('d5_no_blankets',5,5,3,'d5_cookie')
block('d5_cookie',5,5,4,'sleep5')
gate('sleep5',sid(5,5),'아침 일정을 정하고 잠든다','review_end')
nodes['review_end']=dict(kind='end',scene=sid(5,5))

# Only known, exact effects are compiled. Author natural-language guards are retained as provenance.
def operation(text):
    if text.startswith('acquire(') and text.endswith(')'):
        item=text[8:-1]; key,sep,variant=item.partition(':')
        return dict(op='acquire',key=key,variant=variant if sep else 'observed')
    if '=' in text:
        field,value=text.split('=',1)
        parsed={'true':True,'false':False}.get(value,value)
        if value.isdigit(): parsed=int(value)
        return dict(op='set',field=field,value=parsed)
    raise ValueError('Uncompiled effect: '+text)

for node in nodes.values():
    if node['kind']=='block':
        for rid in node['records']:
            for e in records[rid]['effects']: operation(e)
    for opt in node.get('options',[]): opt['operations']=[operation(e) for e in opt.pop('effects',[])]
    if node['kind']=='mark': node['operations']=[operation(e) for e in node.pop('effects')]

used={rid for node in nodes.values() for rid in node.get('records',[])}
export_records={rid:dict(records[rid],operations=[operation(e) for e in records[rid]['effects']]) for rid in sorted(used)}

# Evidence is namespaced, so older saves and their E01..E35 meanings remain intact.
names={'E01':'초대 편지','E02':'초소 처리 명단','E03':'가족 방문 신청 원본','E04':'겨울철 입장 규칙','E05':'정정된 입장 기록','E06':'방의 메모','E07':'초대 봉투 접수 기록','E08':'3번 등의 상태','E09':'엄마의 초상','E10':'빈 받침과 자국','E11':'초롱의 점검장','E12':'공구 대여 쪽지','E13':'우박의 측정지','E14':'실룩의 운반표','E15':'창고의 3번 돌','E16':'백 부인의 매입 장부','E17':'실룩의 걸쇠 진술','E18':'솜이의 이야기','E30':'책상 아래 보따리','E31':'네로의 공급 경로','E32':'안쪽 받침의 칼끝 파편','E33':'동의받고 대조한 칼','E34':'실룩의 작업표','E35':'가족 침구 예약'}
names.update(E19='밤이의 제한된 목격',E20='돌목의 최초 진술',E22='울타리에서 수거한 천',E23='허락받고 대조한 겉옷',
    E24='네로의 귀가 관찰',E25='돌목의 재확인 진술',E26='밤이 혐의 정정 기록',
    E27='엄마의 경고 편지',E28='엄마에게 쓰는 답장',E29='다음 날 아침 보호 약속')
evidence={}
for s in story['scenes']:
    if s['day']>5:continue
    for b in s['blocks']:
        for i,r in enumerate(b['records']):
            for text in r['effects']:
                if not text.startswith('acquire('):continue
                op=operation(text); key=op['key']
                if key not in names:continue
                following=next((x for x in b['records'][i+1:i+4] if x['kind']=='evidence'),None)
                observed=following['text'] if following else (r['text'] if r['kind']=='evidence' else '')
                if observed:
                    evidence.setdefault(key,dict(name=names[key],kind='기록',variants={}))['variants'][op['variant']]=observed
for key in names:
    if key not in evidence:raise ValueError('Missing evidence text: '+key)
evidence['E17']['variants']['observed']=records[line(3,5,9102)]['text']
evidence['E35']['variants']['reserved']=records[line(2,4,9102)]['text']
evidence['E09']['variants']['complete']=records[line(3,1,9101)]['text']
evidence['E26']['variants']['observed']=records[line(5,3,9102)]['text']
for key in ('E19','E20','E24','E25'):evidence[key]['kind']='증언'
for key in ('E27','E28'):evidence[key]['private']=True

initial=dict(day=1,carriage_stopped=False,father_with_daram=True,piko_sheltered=False,piko_alive=True,portrait='none',gate_registered=False,gate_basis_proven=False,reason_heard=False,purpose_difference_known=False,invitation_author='unknown',mother_warning_received=False,public_stones='with_baek',silluk_status='free',silluk_labor_transfer_known=False,unverified_stones_status='with_baek',nero_bedding_reserved=False,carried_dry_blankets=0,bami_status='free',musoe_alive=True,mother_box_checked_day2=False,nero_met_day2=False,nero_supply_route_known=False,under_desk_checked=False,lamp_theft_supported=False,nero_contact_lead=False,box_rechecked_day2=False,rumor_not_eyewitness=False,inn_information_hub_risk_known=False,K01a=False,K01b=False,K05=False)
for i in range(4):initial['lamp_part_'+str(i)]=False
initial.update(d4_fence_seen=False,d4_tracks_seen=False,d4_bucket_seen=False,
    afternoon_visit_declined=False,somi_entry_consent=False,mother_denies_invitation=False,
    supply_contact_pending=False,family_safety_changed=False)

result=dict(version=story['version'],runtime_schema=2,scope='D01-D05',source_sha256=hashlib.sha256(story_path.read_bytes()).hexdigest(),initial=initial,nodes=nodes,records=export_records,evidence=evidence,
    scenes={key:dict(title=s['title'],location=s['location'],day=s['day']) for key,s in scenes.items() if s['day']<=5})
(DATA/'route.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Compiled',len(nodes),'nodes,',len(export_records),'records;',len(story['scenes']),'source scenes preserved')


# Import only reviewed, branch-scoped art; never all 113 logical resources.
from PIL import Image
BASE=SOURCE/'02_기본리소스/phase2'
PROPS=SOURCE/'05_생활소품/daram-props-cleanup-20261020'
dest=ROOT/'game/assets/ms14';dest.mkdir(exist_ok=True)
entries={}
def add(key, path, role, status='existing_art_reused'):
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    # Keep exact PNG RGBA for cleaned props; no re-encoding of pixel boundaries.
    target=dest/(key+path.suffix)
    shutil.copy2(path,target)
    entries[key]=dict(file=str(target.relative_to(ROOT/'game')),size=list(Image.open(path).size),sha256=digest,
        source=str(path.relative_to(SOURCE)),role=role,status=status)
for key,file in dict(carriage='carriage-empty-winter.webp',gate='gate-morning.webp',room='wide-room13-before-morning.webp',
        inn='inn-morning.webp',square='square.webp',post='post.webp',dining='wide-dining-morning.webp',
        stable='wide-stable-afternoon.webp',clinic='ready-clinic0177-morning.webp',workshop='workshop.webp',
        store='ready-store0177-morning.webp',forest='wide-forest-morning.webp',
        somi_inside='wide-somi-home-afternoon.webp',hall='wide-hall-before-morning.webp',
        guardroom='ready-facility0177-morning.webp').items():
    add(key,BASE/'reuse/backgrounds'/file,'background')
for key,file in dict(bundle='D01_open_bundle.png',box='D02_exchange_box_empty.png',blanket_ochre='D11_blanket_ochre.png',blanket_teal='D11_blanket_teal.png').items():
    add(key,PROPS/'assets_native'/file,'prop','source_preserving_review_candidate')
add('family',BASE/'family/D01_family_drawing_three_arms.png','prop','original_crayon_media_preserved')
add('warning_private',SOURCE/'03_검수교체/replacement_assets/documents/D05_warning_private.png',
    'family_only_document','exact_text_guarded_review_candidate')
for key,file in dict(portrait_complete='D03_mother_portrait_completed.png',portrait_unfinished='D03_mother_portrait_unfinished.png',portrait_child='D03_mother_portrait_child_stroke.png').items():
    add(key,BASE/'branches'/file,'prop','branch_guarded_review_candidate')
(ROOT/'game/ms14/art.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
print(len(entries),'assets imported without re-encoding')
