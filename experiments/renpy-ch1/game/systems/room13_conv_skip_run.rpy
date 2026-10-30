# 2026-10-30 눈가림 플레이: 「건너뛰기」가 한 줄씩만 넘어갔다. 4일부터의 장면은 r13_lines 를 한 줄마다 따로 부르므로
# 「지금 묶음」이 곧 한 줄이었다. 누른 뒤에는 플레이어가 무언가 골라야 하는 화면(현장·지도·선택지·자료·증명·질문)이
# 뜰 때까지 이어지는 대사 묶음을 모두 넘긴다. 그런 화면이 뜨면 r13_conv_skip_until_choice 가 끈다.
default r13_conv_skip_run = False
init 66 python:
    # 플레이어가 고르는 화면: menu 의 choice 와, 게임 안에서 call screen 으로 부르는 화면 전부(2026-10-30 grep 기준).
    R13_CONV_SKIP_STOP_SCREENS=("choice","r13_confirm","r13_book","r13_life_closeup","r13_hub","r13_topics","r13_shop","r13_map",
        "r13_winter_board","r13_records","r13_meeting_retry_choice","r13_episode_aftermath_view","r13_cinematic_view","r13_work_board",
        "r13_tool_closeup","r13_resident_approach","r13_rescue_notes","r13_q1_checkpoint_wait","r13_proof_workspace","r13_plan_read",
        "r13_plan_comparison","r13_object_context","r13_nearby","r13_meeting_ballot","r13_meeting_agenda","r13_life_group_conversation",
        "r13_lever_actions","r13_ending_story_view","r13_ending_screen","r13_end_card","r13_desk_inspection","r13_debate_board",
        "r13_crisis_proof","r13_crisis","r13_admin_meeting_finished","r13_debate","r13_entry_karo_topics","main_menu","game_menu","confirm")
    def r13_conv_skip_until_choice():
        if getattr(store,"r13_conv_skip_run",False) and any(renpy.get_screen(n) for n in R13_CONV_SKIP_STOP_SCREENS):
            store.r13_conv_skip_run=False
    config.interact_callbacks.append(r13_conv_skip_until_choice)
