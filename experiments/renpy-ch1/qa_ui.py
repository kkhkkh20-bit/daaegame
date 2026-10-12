"""Read-only checks of the actual native UI, reusable in the chapter QA routes.

Call after the corresponding screen is ready. These helpers inspect rendered
widgets; they never change story progress, resident knowledge or screen state.
"""


async def _native(trial, source):
    return await trial.page.evaluate(
        "source => renpy_exec(source)", "import renpy\n" + source)


async def check_topic_actor(trial, screenname):
    assert screenname in ("arrival_questions", "source_questions", "village_contact_questions")
    result = await _native(trial, """
actor = renpy.exports.get_widget(%r, 'topic_actor')
screen = renpy.exports.get_screen(%r)
portrait = None
pending = [screen.child] if screen is not None else []
visited = set()
while pending:
    node = pending.pop()
    if id(node) in visited:
        continue
    visited.add(id(node))
    if getattr(node, 'child', None) is actor and hasattr(node, 'state'):
        portrait = node
        break
    pending.extend(node.visit())
def plain_position(value):
    if hasattr(value, 'absolute'):
        return [float(value.absolute), float(value.relative)]
    return value
result = dict(exists=actor is not None,
              placement=[plain_position(v) for v in portrait.get_placement()] if portrait is not None else None,
              size=[plain_position(v) for v in portrait.state.size] if portrait is not None else None,
              duplicate_visitor=renpy.exports.showing('visitor'))
""" % (screenname, screenname))
    assert result["exists"], ("Missing question portrait", screenname, result)
    assert result["placement"] is not None, ("Missing question transform", result)
    assert result["placement"][0] == [950, 0], ("Questions cover the face", result)
    assert result["placement"][1] == [551, 0] and result["placement"][3] == [0, 1], (
        "Question portrait feet are misplaced", result)
    assert result["size"] == [[300, 0], [440, 0]], ("Unexpected portrait bounds", result)
    assert not result["duplicate_visitor"], ("Duplicate question portrait", result)
    return result


async def check_roundtable_foreground(trial):
    result = await _native(trial, """
debate = renpy.exports.get_screen('source_debate')
table = renpy.exports.get_screen('round_table')
people = ('granny', 'nabi', 'buri', 'doto', 'seryeon', 'neoul', 'karo', 'bami')
result = dict(actor=debate.scope.get('actor') if debate is not None else None,
              foreground=table.scope.get('foreground') if table is not None else None,
              world=[p for p in people if renpy.exports.get_widget('round_table', 'table_'+p) is not None],
              portrait=renpy.exports.get_widget('source_debate', 'debate_actor') is not None,
              duplicate_visitor=renpy.exports.showing('visitor'))
""")
    assert result["portrait"] and result["actor"], ("Missing debate portrait", result)
    assert result["foreground"] == result["actor"], (
        "Table foreground does not follow the selected speaker", result)
    assert result["actor"] not in result["world"], ("Resident appears twice", result)
    assert len(result["world"]) == 7, ("Other residents vanished", result)
    assert not result["duplicate_visitor"], ("Old speech portrait leaked into debate", result)
    return result


async def check_volume_sliders(trial):
    result = await _native(trial, """
result = {}
for name in ('music_volume', 'fx_volume'):
    widget = renpy.exports.get_widget('pause_menu', name)
    result[name] = dict(exists=widget is not None,
                        left=type(widget.style.fore_bar).__name__ if widget is not None else None,
                        right=type(widget.style.aft_bar).__name__ if widget is not None else None,
                        thumb=type(widget.style.thumb).__name__ if widget is not None else None)
""")
    for name, widget in result.items():
        assert widget["exists"], ("Missing volume control", name, widget)
        assert widget["left"] == widget["right"] == widget["thumb"] == "Solid", (
            "Volume slider lacks a visible track or handle", name, widget)
    return result


async def check_resident_scroll(trial):
    result = await _native(trial, """
rows = renpy.exports.get_widget('village_timetable', 'resident_rows')
screen = renpy.exports.get_screen('village_timetable')
scrollbar = None
pending = [screen.child] if screen is not None else []
visited = set()
while pending:
    node = pending.pop()
    if id(node) in visited:
        continue
    visited.add(id(node))
    if isinstance(node, renpy.display.behavior.Bar) and rows is not None and node.adjustment is rows.yadjustment:
        scrollbar = node
        break
    pending.extend(node.visit())
result = dict(exists=rows is not None,
              scroll_range=rows.yadjustment.range if rows is not None else None,
              page=rows.yadjustment.page if rows is not None else None,
              scrollbar_size=[scrollbar.width,scrollbar.height] if scrollbar is not None else None,
              vertical=bool(scrollbar.style.bar_vertical) if scrollbar is not None else None)
""")
    assert result["exists"], ("Resident notebook is not scrollable", result)
    assert result["page"] == 365 and result["scroll_range"] > 0, (
        "Resident notebook cannot reach the remaining rows", result)
    assert result["vertical"] and result["scrollbar_size"][0] <= 20, (
        "Resident scrollbar covers the notebook content", result)
    return result


async def check_motherlead(trial):
    result = await _native(trial, """
screen = renpy.exports.get_screen('source_inspect')
result = dict(key=screen.scope.get('key') if screen is not None else None,
              papers=[p for p in ('book','ledger') if renpy.exports.get_widget('source_inspect','mother_'+p) is not None])
""")
    assert result["key"] == "motherlead" and result["papers"] == ["book", "ledger"], (
        "Mother handwriting comparison fell back to a generic notebook", result)
    return result


async def check_clock_viewpoints(trial):
    result = await _native(trial, """
ours = renpy.exports.get_widget('source_proof', 'proof_clock_ours')
bami = renpy.exports.get_widget('source_proof', 'proof_clock_bami')
result = dict(ours=float(ours.state.rotate or 0) if ours is not None else None,
              bami=float(bami.state.rotate or 0) if bami is not None else None)
""")
    assert result == {"ours": 0.0, "bami": 180.0}, (
        "The two clock viewpoints are not visibly distinct", result)
    return result
