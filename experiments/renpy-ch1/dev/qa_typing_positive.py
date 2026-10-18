"""Reusable native ReviewQA probe. Call on a newly entered LONG ordinary say.
Caller must set CPS before entering the line (24 or 34), disable skip/AFM, and
choose a safe say-body coordinate, not a meeting toolbar button. Run once in
normal play and once via admin Replay. This helper does not alter preferences.
"""
import asyncio
SNAPSHOT='''import renpy
s=renpy.store
t=renpy.get_displayable("say","what") if renpy.get_screen("say") else None
result=dict(cps=s.preferences.text_cps, slow=bool(t and t.slow), text=str(t.text) if t else None, location=renpy.get_filename_line(), revealed=getattr(t,"r13_revealed",0), typing=renpy.music.get_playing(channel="typing"))
'''
async def check_live_say(q, click_x, click_y):
    before=await q.py(SNAPSHOT)
    assert before['cps'] in (24,34), before
    assert before['slow'], 'Need a freshly entered long line, not an instant/completed QA fixture.'
    await q.input(click_x,click_y)
    await asyncio.sleep(.12)
    completed=await q.py(SNAPSHOT)
    assert completed['text']==before['text'], (before,completed)
    assert completed['location']==before['location'], (before,completed)
    assert not completed['slow'], completed
    assert not completed['typing'], completed
    await q.input(click_x,click_y)
    await asyncio.sleep(.12)
    advanced=await q.py(SNAPSHOT)
    assert (advanced['location'],advanced['text']) != (completed['location'],completed['text']), (completed,advanced)
    return dict(before=before,first_click=completed,second_click=advanced)
