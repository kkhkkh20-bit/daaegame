# Key words in dialogue (owner, 0.18.56): "중요한 단어들만 색상 다르게 넣어서, 읽다가도 뭐가
# 중요한지만 확 오게." A word written 【like this】 in a line is shown in gold. Line data keeps the
# brackets, so read-tracking and expression cues still match the stored text.
init 60 python:
    R13_KEY_WORD_COLOR="#ffcf66"

    def r13_line_markup(text):
        if "【" not in text:return text
        return text.replace("【","{color="+R13_KEY_WORD_COLOR+"}").replace("】","{/color}")
