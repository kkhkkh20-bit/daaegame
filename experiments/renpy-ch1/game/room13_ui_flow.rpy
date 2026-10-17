# Display-only helpers. No persistent discovery, story, evidence, or clock writes.
init 99 python:
    import re as r13_ui_re

    def r13_dialogue_profile(who):
        packet=getattr(store,"r13_packet",None)
        person=packet[0] if packet else None
        # Use the actual named speaker, not an inferred identity or a new crop.
        return person if who and person in CAST and R13_NAMES.get(person)==who else None

    # The automatic name/place/evidence colouring (and its {b}) was retired in 0.18.24;
    # r13_semantic_text now lives in systems/room13_typography_roles.rpy.

    # Footer skip modes (owner, 0.18.4, from player comments). One-shot: they
    # run to the next choice or menu screen and then switch themselves off.
    def r13_sync_skip_unseen():
        # Ren'Py's slow skip obeys skip_unseen even when our "all" mode is on.
        # Keep the backup outside rollback state: a story rollback must not lose it.
        # Temporarily override it, then return the user's original preference.
        if getattr(store,"r13_fast_all",False):
            if getattr(renpy,"_r13_skip_unseen_before",None) is None:
                renpy._r13_skip_unseen_before=preferences.skip_unseen
            preferences.skip_unseen=True
        elif getattr(renpy,"_r13_skip_unseen_before",None) is not None:
            preferences.skip_unseen=renpy._r13_skip_unseen_before
            renpy._r13_skip_unseen_before=None

    def r13_toggle_read_skip():
        store.r13_fast_all=False
        store.r13_fast_read=not store.r13_fast_read
        r13_sync_skip_unseen()
        renpy.stop_skipping()
        if store.r13_fast_read:
            if getattr(store,"r13_read_id",None) in persistent.room13_read:
                renpy.config.skipping="slow"
            else:
                store.r13_fast_read=False
                renpy.notify("이 대사는 처음 보는 대사예요.")
        renpy.restart_interaction()

    def r13_toggle_fast_all():
        store.r13_fast_read=False
        store.r13_fast_all=not store.r13_fast_all
        r13_sync_skip_unseen()
        renpy.stop_skipping()
        if store.r13_fast_all:
            renpy.config.skipping="slow"
        renpy.restart_interaction()

    def r13_end_skip_modes():
        store.r13_fast_read=False
        store.r13_fast_all=False
        r13_sync_skip_unseen()
        renpy.stop_skipping()

    def r13_stop_skip_at_choices():
        # Other paths (e.g. live meetings) can also clear the mode directly.
        r13_sync_skip_unseen()
        if not getattr(store,"room13_mode",False):return
        if any(renpy.get_screen(name) for name in ("main_menu","pause_menu","save","load","confirm","choice","r13_topics","r13_entry_topics","r13_entry_karo_topics","r13_resident_approach","r13_book","r13_debate_board","r13_meeting_agenda","r13_meeting_ballot","r13_confirm")):
            r13_end_skip_modes()
    config.interact_callbacks.append(r13_stop_skip_at_choices)
