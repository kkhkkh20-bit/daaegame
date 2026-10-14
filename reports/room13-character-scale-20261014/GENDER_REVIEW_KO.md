# 성별 근거 검토 — 읽기 전용

기준 main `f903bc8523d4a7d28b58712138c3fa3e9b6ff79c` (0.17.13). 외모·옷·이름·직업으로 성별을 추정하지 않았다. 성별·이름·대사·가족관계를 수정하지 않았다.

범위는 현재 Room13 주민 35명 + 아빠·다람·엄마·세련·돌목, 총 40명이다. 사용하지 않는 구판 아트 식별자 elder/bodum/workshop은 별도 사람으로 더하지 않았다. 화면에서 사용자가 박 부인으로 지칭한 인물의 현재 표기는 **백 부인(resident_madam)** 이다.

| 근거 범위 | 남성 | 여성 | 미명시 |
|---|---:|---:|---:|
| 현행 대사·호칭·가족관계 | 12 | 6 | 22 |
| 현행 + 원안의 직접적인 성별 명시 | 16 | 10 | 14 |

두 번째 행은 `legacy-resident-roster.json`의 original_spec.prompt에 직접 적힌 boy/girl/male/woman을 추가한 참고치이다. 원안은 **optional_concept / legacy_plot_canon:false** 이므로 현재 성별 확정이나 과거 사건 확정으로 사용하지 않는다. 옛 사건의 간접 대인 호칭은 추가 집계에서 제외했다. 미명시는 논바이너리 등의 정체성을 뜻하지 않고, 이 검토의 자료에서 명시를 확인하지 못했다는 뜻이다. 이름표 중심 잠정 집계(4/5/31), 첫 만남 대사 반영 집계(11/6/23)는 최종치가 아니다. 가족 보호 항목의 **손자=부리**까지 대조한 최종 집계는 위 표와 같다. 첫 만남 대사의 아저씨 7명과 가족관계 근거를 모두 반영했다.

| 후보 | 남성 근거 | 변경 영향 검토 |
|---|---|---|
| 은호 | 원안 prompt `male jeweler` | 거래·가격·견습생 관계를 유지할 수 있다. 가족 사건 축이 적다. 현재 성별은 미명시이므로 원안 수정에 해당한다. |
| 도토 | 원안 prompt `squirrel boy` | 시간·기록 역할과 추리 기능은 그대로 유지 가능. 기존 소년 원안·표정 원화 전체를 검토해야 한다. |
| 콩이 | 원안 prompt `puppy boy` | 친구·시계·후각 관찰 중심. 핵심 부녀·모자 관계와 분리된다. |
| 슬링 | 현행 첫 만남의 ‘저 아저씨’ | 우편·배달 역할은 성별과 무관. 현행 호칭을 고쳐야 하므로 위 세 후보보다 영향이 크다. |
| 따닥 | 현행 첫 만남의 ‘저 아저씨’ | 벽·수리 관찰 역할 유지 가능. 현행 호칭 및 다른 간접 지칭 전수 확인이 필요하다. |

위는 제안이며 승인·적용이 아니다. 뭉치(백 부인의 아들), 초롱(할머니의 아들), 부엉이 할아버지(부리와의 관계·사건), 아빠는 우선 제외한다. 보리는 현행 ‘아저씨’와 원안의 `boy`가 연령상 충돌하고 가족 돌봄 역할도 있어 우선 후보에서 내렸다. 나비·밤이는 원안에 명시된 여성이고 누비는 현행 호칭으로 확인된다.

## 인물별 근거

| 인물 | 현행 | 원안 포함 참고 | 근거 |
|---|---|---|---|
| 밤이 (`bami`) | 미명시 | 여성 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 / 원안: Teenage BAT GIRL with large pointed bat ears, subtle dark-purple animal muzzle and curious pale-violet eyes, folded bat wings behind shoulders, dusty-lavender scarf, dark plum asymmetrical hooded cape over a charcoal tunic, little silver moon pin. Cynical independent, cool but not sexualized. |
| 부리 (`buri`) | 남성 | 남성 | room13-content.json: residents/resident_owlgp/protects «과거 오판의 정정과 손자» + 부리가 할아버지로 부르는 대사/가족관계 |
| 아빠 (`dad`) | 남성 | 남성 | room13-content.json: E01 establishes «아빠와 딸» |
| 다람 (`daram`) | 여성 | 여성 | room13-content.json: E01 establishes «아빠와 딸» |
| 도토 (`doto`) | 미명시 | 남성 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 / 원안: Young chestnut squirrel boy, striped squirrel forehead and huge curled fluffy tail visible behind one shoulder, small round glasses, precise navy-and-ochre checked vest, ivory shirt, sleeve garters, mechanical stopwatch in one paw and a tiny closed notebook. A meticulous library regular. Visually distinct from the detective heroine. |
| 토끼 할머니 (`granny`) | 여성 | 여성 | room13-content.json 및 room13.rpy의 «할머니» 호칭 |
| 돌목 (`guard`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 까로 (`karo`) | 남성 | 남성 | room13-dialogue-openings.json: first_meetings/karo/notice_child «까로 아저씨가 마차 옆에 쪼그려 앉아 있었다. 손을 뻗었다가 장갑을 벗고 다시 뻗었다.» |
| 엄마 (`mom`) | 여성 | 여성 | room13-content.json: topics의 «제 아내입니다. 아이 엄마고요.» |
| 나비 (`nabi`) | 미명시 | 여성 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 / 원안: Young white cat girl with green eyes, triangular ears, neat navy sailor-collar dress, pale lilac sleeves, unmistakable GOLD BELL necklace on a burgundy ribbon. Aloof outwardly, lonely inside. Never omit the gold bell. |
| 너울 (`neoul`) | 남성 | 남성 | room13-dialogue-openings.json: first_meetings/neoul/notice_child «아빠, 저 아저씨는 누구 기다려?» |
| 바둑이 (`resident_badook`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 보리 (`resident_bori`) | 남성 | 남성 | room13-dialogue-openings.json: first_meetings/resident_bori/notice_child «저 아저씨 앞이 보여?» |
| 은호 사장 (`resident_eunho`) | 미명시 | 남성 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 / 원안: Adult WHITE FOX male jeweler with narrow silver-blue eyes, perfectly neat fur, fine GOLD-RIMMED spectacles, charcoal silk shirt, elegant navy vest with conspicuous SILVER BUTTONS, white cuffs, dark forest-green cravat, single small gemstone ring. Sophisticated measured wealthy merchant, slim upright silhouette. |
| 구슬 (`resident_guseul`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 꽥순 (`resident_kkwak`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 콩이 (`resident_kongi`) | 미명시 | 남성 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 / 원안: Young golden-tan puppy boy with floppy ears and dark wet dog nose, friendly brown eyes, faded teal hoodie under a brown vest, short red scarf, a round pocket watch hanging from a belt. Sleepy but observant nose. |
| 초롱 (`resident_lamplighter`) | 남성 | 남성 | room13-content.json: residents/resident_lamplighter/name «등불지기 아저씨» |
| 사서 선생님 (`resident_librarian`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 백 부인 (`resident_madam`) | 여성 | 여성 | room13-content.json: residents/resident_madam/name «백 부인» |
| 모모 관장 (`resident_momo`) | 미명시 | 여성 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 / 원안: Middle-aged cream-colored GOAT WOMAN museum curator with short gently curved horns, kind green eyes, aubergine dress with cream lace collar, soft rose ribbon at neckline, white cuff gloves, small wicker basket with a few wrapped cookies held naturally. Elegant warm hostess with a composed hidden depth. |
| 뭉치 (`resident_mungchi`) | 미명시 | 남성 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 / 원안: Fifteen-year-old anthropomorphic PANDA BOY, unmistakable black rounded panda ears and black eye patches, white panda animal face with small black nose, smug dark eyes, deep-wine beret, expensive navy velvet short coat, ivory shirt with gold clasp, pale white gloves, shiny brass pocket-chain. Spoiled collector household heir, adolescent silhouette, not a hedgehog, no spines. |
| 무쇠 할아버지 (`resident_musoe`) | 남성 | 남성 | room13-content.json: residents/resident_musoe/name «무쇠 할아버지» |
| 네로 (`resident_nero`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 누비 아주머니 (`resident_nubi`) | 여성 | 여성 | room13-content.json: residents/resident_nubi/name «누비 아주머니» |
| 부엉이 할아버지 (`resident_owlgp`) | 남성 | 남성 | room13_rules.rpy: R13_NAMES «부엉이 할아버지» |
| 피코 (`resident_piko`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 뿔이 촌장 (`resident_ppul`) | 남성 | 남성 | room13-dialogue-openings.json: first_meetings/resident_ppul/notice_child «아빠, 저 아저씨한테 다 물어봐.» |
| 설이 (`resident_seol`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 서리 검사원 (`resident_seori`) | 남성 | 남성 | room13-dialogue-openings.json: first_meetings/resident_seori/notice_child «아빠, 저 아저씨도 같은 걸 또 읽어.» |
| 실룩 (`resident_siluk`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 슬링 (`resident_sling`) | 남성 | 남성 | room13-dialogue-openings.json: first_meetings/resident_sling/notice_child «아빠, 저 아저씨 편지 엄청 많아.» |
| 솜이 (`resident_somi`) | 여성 | 여성 | room13-content.json: life:resident_musoe:after의 «손녀 손도 따뜻하게» 및 원안의 솜이 연결. 손녀 대상 식별을 함께 확인 |
| 곰 선생님 (`resident_teacher`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 톡 (`resident_tok`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 토리 (`resident_tori`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 따닥 (`resident_ttadak`) | 남성 | 남성 | room13-dialogue-openings.json: first_meetings/resident_ttadak/notice_child «아빠, 저 아저씨는 벽이랑 얘기해?» |
| 우박 (`resident_ubak`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
| 여니 (`resident_yeoni`) | 미명시 | 여성 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 / 원안: Young orange fox girl, white muzzle and chest, dark ear tips, amber eyes, elegant turquoise neck bow, plum pinafore dress over cream blouse, craft apron pocket and tiny satin gift ribbon tied to a shoulder bag. Clever thoughtful gift maker. |
| 세련 (`seryeon`) | 미명시 | 미명시 | 검토한 현행 자료에 명시적 성별 표현을 확인하지 못함 |
