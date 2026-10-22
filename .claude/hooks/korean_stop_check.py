#!/usr/bin/env python3
# 답을 끝내기 전에 마지막 답변의 글자를 센다. 영어 글자가 한글보다 많으면 끝내지 못하게 막는다.
# (2026-10-22 소유자: "훅이라도 걸어서 한글로 뱉어야지")
import json, re, sys
try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if data.get("stop_hook_active"):
    sys.exit(0)  # 다시 쓰는 중이면 한 번만 막고 넘어간다(무한 반복 방지)
path = data.get("transcript_path")
if not path:
    sys.exit(0)
last = None
try:
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
            except Exception:
                continue
            msg = row.get("message") or {}
            if row.get("type") == "user" or msg.get("role") == "user":
                content = msg.get("content")
                # 사용자가 직접 보낸 글이면 그 뒤 답변부터 센다
                if isinstance(content, str) or (isinstance(content, list) and any(c.get("type") == "text" for c in content if isinstance(c, dict))):
                    last = []
            elif row.get("type") == "assistant" or msg.get("role") == "assistant":
                for c in msg.get("content") or []:
                    if isinstance(c, dict) and c.get("type") == "text":
                        if last is None:
                            last = []
                        last.append(c.get("text", ""))
except Exception:
    sys.exit(0)
if not last:
    sys.exit(0)
text = last[-1]
text = re.sub(r"```.*?```", " ", text, flags=re.S)      # 코드 블록 제외
text = re.sub(r"`[^`]*`", " ", text)                     # 인라인 코드 제외
text = re.sub(r"https?://\S+|\([^)]*\.(png|md|docx|py|rpy|json)\)", " ", text)  # 주소·파일 경로 제외
text = re.sub(r"[\w./-]+\.(png|md|docx|py|rpy|json|webp|txt)\b", " ", text)
hangul = len(re.findall(r"[가-힣]", text))
latin = len(re.findall(r"[A-Za-z]", text))
if latin > 40 and latin > hangul:
    print(json.dumps({"decision": "block",
                      "reason": "마지막 답변이 영어로 쓰였습니다(영문자 %d, 한글 %d). 같은 내용을 한글로 다시 써서 답하세요. 사과는 붙이지 마세요." % (latin, hangul)},
                     ensure_ascii=False))
sys.exit(0)
