"""Authoring validation only. No runtime state or story execution."""
VERSION = 'DT_STORY_1.1_PRODUCTION_BASIS_01_20261020'
PREFIX = 'MS14_D01_'
SPEAKERS = {'아빠': 'dad', '다람': 'daram', '까로': 'karo', '돌목': 'guard'}
GUARDS = {'S01_B001': 'always', 'S01_B002': 'always AND input_completed(MS14_D01_S01:2)', 'S01_B003': 'input=inspect_letter_last', 'S01_B004': 'input=inspect_letter_hand', 'S01_B005': '(K01a=true OR K01b=true) AND letter_close_selected=true', 'S01_B006': 'letter_close_selected=true AND K01a=false AND K01b=false', 'S01_B007': 'always', 'S02_B001': 'always', 'S02_B002': 'input=show_invitation', 'S02_B003': 'input=request_original', 'S02_B004': 'always', 'S03_B001': 'always', 'S03_B002': 'input=connect(E03.family_visit,E02.worker) AND gate_basis_proven=false', 'S03_B003': 'input=inspect(E03.lodging) AND gate_basis_proven=false', 'S03_B004': 'input=submit AND E02,E03,E04 acquired AND selected=family_visit+two_person_lodging+family_registration_rule AND purpose_difference_known=true', 'S03_B005': 'input=submit AND E02,E03,E04 acquired AND selected=family_visit+two_person_lodging+family_registration_rule AND purpose_difference_known=false', 'S03_B006': 'input=submit_only_application_count', 'S03_B007': 'input=submit_only_passenger_confirmation', 'S03_B008': 'input=submit_other_house_application', 'S03_B009': 'input=hint', 'S03_B010': 'input=ask_worker_reason AND purpose_difference_known=true AND reason_heard=false', 'S04_B001': 'always'}
EFFECTS = {'acquire(E01)': ('evidence', 'E01'), 'acquire(E02)': ('evidence', 'E02'), 'acquire(E03)': ('evidence', 'E03'), 'acquire(E04)': ('evidence', 'E04'), 'acquire(E05)': ('evidence', 'E05'), **{key + '=true': ('flag', key) for key in ('K01a', 'K01b', 'K05', 'reason_heard', 'purpose_difference_known', 'gate_basis_proven', 'gate_registered')}}
ENTRY_GUARDS = {'MS14_D01_S01': ['new_game=true', 'day=1', 'father.alive=true', 'daram.alive=true', 'father.location=carriage', 'daram.location=carriage'], 'MS14_D01_S02': ['day=1', 'carriage_stopped=true', 'father_with_daram=true'], 'MS14_D01_S03': ['day=1', 'E02 acquired', 'father.location=guardhouse', 'daram.location=guardhouse', 'gate_registered=false'], 'MS14_D01_S04': ['day=1', 'gate_basis_proven=true', 'gate_registered=false']}

def validate(data):
    if data['version'] != VERSION:
        raise ValueError('Unsupported production basis')
    seen = set()
    for scene in data['scenes']:
        if scene['enter_when'] != ENTRY_GUARDS[scene['scene_id']]:
            raise ValueError('Unmapped scene entry condition')
        for block in scene['blocks']:
            key = block['id'].removeprefix(PREFIX)
            if GUARDS[key] != block['when']:
                raise ValueError('Unmapped block condition: ' + block['id'])
            seen.add(key)
            for record in block['records']:
                if record.get('requires'):
                    raise ValueError('Unmapped record requirement: ' + record['id'])
                if record['kind'] not in ('action', 'dialogue', 'narration', 'evidence', 'choice'):
                    raise ValueError('Unmapped record kind')
                if record['kind'] == 'dialogue' and record['speaker'] not in SPEAKERS:
                    raise ValueError('Unmapped speaker')
                for effect in record['effects']:
                    if effect not in EFFECTS:
                        raise ValueError('Unmapped effect: ' + effect)
                for option in record.get('options', []):
                    if option['when'] not in ('always', 'E03 acquired', 'gate_basis_proven=false', 'reason_heard=false', 'purpose_difference_known=true AND reason_heard=false'):
                        raise ValueError('Unmapped option condition')
    if seen != set(GUARDS):
        raise ValueError('Missing D01 blocks')
