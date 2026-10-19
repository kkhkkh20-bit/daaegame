# Keep the shared overlay, but never route a recommended campaign into old records.
init 935 python:
    _r13_rec_legacy_shortcut_records = r13_shortcut_records
    def r13_shortcut_records():
        campaign=(getattr(store,'room13',None) or {}).get('campaign_id')
        if campaign not in ('room13_recommended_v1','room13_recommended_qa_v1'):
            return _r13_rec_legacy_shortcut_records()
        if not getattr(store,'r13_recommended',None):return
        busy=('r13_recommended_notebook','r13_recommended_catalog','r13_recommended_cards',
            'r13_recommended_card_detail','r13_rec_evidence_enlarged','r13_recommended_map','r13_rec_stage_pause',
            'r13_rec_stage_choice','r13_rec_cloth_comparison','r13_rec_piko_contact_sequence',
            'r13_rec_piko_intact_cloth','r13_rec_e3_route_map','r13_rec_e456_pick',
            'save','load','pause_menu','confirm','r13_confirm')
        if any(renpy.get_screen(name) for name in busy):return
        return renpy.call_in_new_context('r13_rec_stage_notebook')
