# 대사창 줄바꿈 (소유자 지시, 0.18.12): 문장이 끝나면 다음 줄에서 시작하고, 한 줄이 길면
# 쉼표·띄어쓰기에서 나눠 두 줄을 쓴다. 대사 원문(읽음 표시·대사집·테스트 기준)은 바꾸지 않고
# 화면에 보일 때만 나눈다. 한 줄 기준은 보통 30자, 세 줄을 넘으면 33·35자로 넓힌다.
init 112 python:
    import re as _r13_lb_re
    _R13_LB_TAG=_r13_lb_re.compile(r'\{[^{}]*\}')
    _R13_LB_END=_r13_lb_re.compile(r'(?<=[.?!…」』])\s+')

    def _r13_lb_len(s):
        return len(_R13_LB_TAG.sub('',s))

    def _r13_lb_split(s,limit):
        if _r13_lb_len(s)<=limit:return [s]
        cands=[];depth=0
        for i,ch in enumerate(s):
            if ch in '{[':depth+=1
            elif ch in '}]':depth-=1
            elif ch==' ' and depth==0 and i>0:cands.append(i)
        if not cands:return [s]
        half=_r13_lb_len(s)/2.0
        i=min(cands,key=lambda i:abs(_r13_lb_len(s[:i])-half)+(-4 if s[i-1] in u',，' else 0))
        return _r13_lb_split(s[:i],limit)+_r13_lb_split(s[i+1:],limit)

    def _r13_lb_blocks(text,large):
        """Sentences, each as its wrapped lines; the line limit widens until it fits three lines."""
        best=None
        for limit in ((26,28,29) if large else (30,33,35)):
            blocks=[_r13_lb_split(part,limit) for part in _R13_LB_END.split(text.strip()) if part]
            if best is None or sum(map(len,blocks))<sum(map(len,best)):best=blocks
            if sum(map(len,blocks))<=3:break
        return best

    def r13_dialogue_lines(text,large=False):
        if not text or '\n' in text:return text
        return '\n'.join(line for block in _r13_lb_blocks(text,large) for line in block)

    def r13_dialogue_pages(text):
        """Up to three lines show at once. Longer text goes about two lines per click,
        keeping each sentence whole on one page (a page may take three lines to do so)."""
        if not text or '\n' in text:return [text]
        blocks=_r13_lb_blocks(text,bool(persistent.room13_large_text))
        if sum(map(len,blocks))<=3:return ['\n'.join(l for b in blocks for l in b)]
        pages=[];cur=[]
        for block in blocks:
            while len(block)>3:
                if cur:pages.append(cur);cur=[]
                pages.append(block[:2]);block=block[2:]
            if cur and (len(cur)+len(block)>3 or (len(cur)>=2 and len(cur)+len(block)>2)):
                pages.append(cur);cur=[]
            cur=cur+block
        if cur:pages.append(cur)
        return ['\n'.join(p) for p in pages]

    _r13_lb_prev_filter=config.say_menu_text_filter
    def _r13_lb_filter(text):
        if _r13_lb_prev_filter:text=_r13_lb_prev_filter(text)
        if getattr(store,"room13_mode",False):
            text=r13_dialogue_lines(text,bool(persistent.room13_large_text))
        return text
    config.say_menu_text_filter=_r13_lb_filter
