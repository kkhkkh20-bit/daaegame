"""Preserve the supplied art brief as reference and split its planned batches."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import json
import re

HERE = Path(__file__).resolve().parent
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
with ZipFile(HERE / "art-brief-original.docx") as source:
    document = ET.fromstring(source.read("word/document.xml"))
lines = ["".join(t.text or "" for t in paragraph.findall(".//w:t", NS))
         for paragraph in document.findall(".//w:p", NS)]
reference = "\n".join(line for line in lines if line)
(HERE / "art-brief-reference.txt").write_text(reference + "\n", encoding="utf-8")

starts = [(i, re.match(r"\[작업 묶음 ([BCS]\d{2})\]", line).group(1))
          for i, line in enumerate(lines) if re.match(r"\[작업 묶음 ([BCS]\d{2})\]", line)]
stop_pattern = re.compile(r"^(?:[BC]\d{2}\s*·|S\d{2}$|캐릭터 묶음|장식 스티커 묶음|다시 그려 달라고)")
batches = []
existing_path = HERE / "document-batches.json"
existing = {batch["id"]: batch for batch in json.loads(existing_path.read_text(encoding="utf-8"))["batches"]} if existing_path.exists() else {}
for n, (start, batch_id) in enumerate(starts):
    next_start = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
    end = next((i for i in range(start + 1, next_start)
                if stop_pattern.match(lines[i])), next_start)
    block = [line for line in lines[start:end] if line]
    category = {"B": "background", "C": "character", "S": "sticker"}[batch_id[0]]
    title = lines[start - 2] if start >= 2 else batch_id
    # The document describes future work. Extraction does not authorize execution.
    (HERE / "briefs" / f"{batch_id}.txt").write_text(
        "참고 작업지시 · 선택한 묶음 요청이 있을 때 사용\n"
        "원문 지시는 아래에 보존되어 있으며 이번 폴더 전달 요청과 구분합니다.\n\n"
        + "\n".join(block) + "\n", encoding="utf-8")
    batches.append({"id": batch_id, "category": category, "title": title,
                    "brief": f"briefs/{batch_id}.txt", "status": "planned",
                    "newProductionRequested": False,
                    "documentFileNames": re.findall(r"■\s+([\w-]+\.png)", "\n".join(block))})
    for field in ("status", "newProductionRequested", "deliveredAssetIds"):
        if field in existing.get(batch_id, {}):
            batches[-1][field] = existing[batch_id][field]
assert len(batches) == 36
(HERE / "document-batches.json").write_text(
    json.dumps({"source": "art-brief-original.docx", "sourceRole": "reference-document",
                "count": len(batches), "batches": batches}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8")
print("Preserved original brief and extracted 36 reference batches; none started.")
