# 우선 3종 동작 접수 (2026-10-15 11:16 PDT)

접수·보관만 했다. 게임에는 넣지 않았다(이 브랜치에만 있음).
- ZIP SHA-256: d0d0f070cbcf342ca88d7b9f2873f14da0b004f2f319bdf48152b6abb44d1df7
- PNG 3장(1024×1536 RGBA)의 SHA-256은 부록 JSON에 적힌 값과 일치한다.

```
4aab5040bc774feac8db7b459176e21bdd411ff4f42de862cf34304332006280  granny/granny-key-ledger-v3.png
d5c35cdbe005836f14caf450e5e72ccf5200e7ff6dca2cf99e7a98bb7dde7dc8  owlgp/owlgp-notebook-binding-v2.png
4de994f5c66c053293de74f13e6713859ac823cd26f1330d49054bb034062d08  karo/karo-axlewrap-v2.png
```

| 파일 | 인물 | 동작 | 바탕 디자인 |
|---|---|---|---|
| granny/granny-key-ledger-v3.png | granny 할머니 | 열쇠와 장부 맞추기 | 승인된 새 디자인 |
| owlgp/owlgp-notebook-binding-v2.png | resident_owlgp 부엉이 할아버지 | 수첩 제본 묶기 | 승인된 새 디자인 |
| karo/karo-axlewrap-v2.png | karo 까로 | 마차 축 감기 | 원래 그림 |

- 슬링은 앞서 받은 event_steam을 다시 쓴다. 우체국 아침 2160 기준 발 [1060,620] 후보, 옛 1280 좌표는 폐기.
- head/foot/hand는 crop 기준 원본 픽셀의 육안 추정이다. 실제 접지·손 접점·가림·클릭 검수가 필요하다.
- 사건 동작 9종(event-actions9)은 지우지 않고 별도 보강 후보로 그대로 둔다.
