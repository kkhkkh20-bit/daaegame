# Longer, ordered conversations (owner, 0.18.58): "대사 량을 더 늘리고 … 좀 더 길게 서로 확인하고
# 대화해야 할 것 같음. 중요한 단어는 색을 확 칠해 두고." Reviewed rewrites live in
# room13-dialogue-expand.json as {topic: {old, new}}. A rewrite is used only while the topic's
# current lines are exactly the reviewed "old" lines, so a state-dependent variant or a later
# edit elsewhere falls back to the original instead of showing a stale rewrite.
init 140 python:
    R13_DIALOGUE_EXPAND=json.load(renpy.file("room13-dialogue-expand.json")) if renpy.loadable("room13-dialogue-expand.json") else {}

    def r13_expand_norm(rows):
        out=[]
        for row in rows or []:
            row=list(row)
            item=[row[0],row[1]]
            if len(row)>2 and row[2]:item.append(row[2])
            out.append(item)
        return out

    _r13_expand_topic_lines=r13_conversation_topic_lines
    def r13_conversation_topic_lines(key):
        rows=_r13_expand_topic_lines(key)
        current=r13_expand_norm(rows)
        # Variants of one topic are stored as "topic#condition".
        for name,spec in R13_DIALOGUE_EXPAND.items():
            if (name==key or name.startswith(key+"#")) and current==r13_expand_norm(spec.get("old")):
                return [tuple(row[:2])+((row[2],) if len(row)>2 and row[2] else ()) for row in spec["new"]]
        return rows
