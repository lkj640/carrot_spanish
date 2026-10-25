# 당근 스페인어 스터디 사이트

주소: https://lkj640.github.io/carrot_spanish/

매주 일요일 오전 10시 · 이디야커피 일산허유재병원

## 구성

| 파일 | 역할 |
|---|---|
| `index.html` | 첫 화면 — 다음 모임 공지 + 모임 목록 |
| `meeting.html?d=YYYY-MM-DD` | 모임별 페이지 — 듣기(유튜브) · 교재 · 단어장 |
| `meetings.json` | **모임 목록과 공지 내용. 매주 여기에 한 항목만 추가하면 돼요.** |
| `meetings/<날짜>/` | `data.json`(대본·번역·단어), `workbook.pdf`, `workbook.html` 또는 `pages/*.jpg` |
| `assets/` | 공통 디자인(`style.css`)과 화면 코드 |
| `tools/` | 자료 만드는 스크립트 (아래 참고) |

공지 규칙: 오늘 이후 가장 가까운 모임이 맨 위 '다음 모임 공지'에 나와요. 모임 당일은 낮 12시(한국 시간)까지 '오늘 모임'으로 보이고, 그 뒤에는 다음 주 모임으로 바뀌어요.

## 매주 새 모임 올리기

1. 유튜브 영상의 스페인어 자막(대본)과 단어별 시간을 준비해요. (3주차부터는 영상 자막에서 바로 가져왔어요: `tools/2026-11-01/`)
2. 자료 만들기 (Claude에게 "○월 ○일 모임 자료 만들어서 사이트에 올려줘"라고 부탁해도 돼요)
   - `tools/asr.py`로 음성 인식 → `tools/align.py`로 문장별 시작 시간 맞추기
   - `tools/<날짜>/lines.py`(문장·번역), `vocab.py`(단어), `times.json`(시간)
   - `python3 tools/make_data.py src tools/<날짜> meetings/<날짜>/data.json`
   - 교재: `tools/<날짜>/build_book.py` → `workbook.html` → Chrome으로 PDF 저장
3. `meetings.json`의 `meetings` 배열에 항목 추가 (`youtube`에는 영상 ID, 예: `F9zOIHrW88M`)
4. `git add . && git commit -m "○월 ○일 모임 추가" && git push`

항목 예시:
```json
{
  "date": "2026-11-01", "ep": 7, "level": "A1", "emoji": "🏠",
  "title": "모임 주제", "es": "대표 스페인어 문장",
  "duration": "20:00", "youtube": "영상ID",
  "pdf": "workbook.pdf", "workbookHtml": "workbook.html",
  "topics": ["배울 내용 1", "배울 내용 2"],
  "notice": "이번 주 공지 문구"
}
```
추가 자료(다른 유튜브 영상)를 붙이려면 그 모임 항목에 `"extras"` 배열을 넣어요. 자료는 `meetings/<날짜>/<id>/data.json`에 두고 `meeting.html?d=<날짜>&x=<id>`로 열려요. 공지 카드와 모임 페이지에 '자료 2, 3…'으로 나와요.
```json
"extras": [{ "id": "frutas", "short": "과일 단어", "emoji": "🍎", "title": "과일 단어 24개 · 예문",
  "es": "Vocabulario: Frutas", "channel": "엘라르테 ELArte", "duration": "9:40", "youtube": "6lFHRBpwo8k" }]
```
자료 만들기는 같아요: `tools/<날짜>-<id>/`에 `lines.py`·`vocab.py`·`times.json` → `make_data.py`. 화자 이름을 바꾸려면 `lines.py`에 `SPEAKERS = {"S": "단어", "M": "예문"}`.

시간·장소·준비물을 그 주만 바꾸려면 항목에 `"time"`, `"place"`, `"mapUrl"`, `"bring"`을 넣으면 돼요.

## A1 학습 순서 (`plan.json`)

Easy Spanish Podcast A1 플레이리스트에서 겹치는 주제를 하나로 줄인 18편을 주 1편씩 공부하는 순서예요. (빠진 편: Ep.18 자기소개, 19 부모님, 2 나의 하루, 8 아침 식사, 16 저녁 루틴, 5 우리 집(영어 제목 영상), 14 내 방, 27 교실, 12 스포츠, 26 가격 묻기) 첫 화면 공지 아래에 단계별로 나오고, 날짜가 지난 주차는 ✓, 이번 주는 강조돼요.
- 주차 날짜는 `start`(1주차 = 2026-10-18)부터 매주 일요일로 계산해요. 모임을 한 주 쉬면 해당 주차부터 `"date": "YYYY-MM-DD"`를 넣어 주세요.
- `meetings.json`에 같은 날짜의 모임이 있으면 그 모임 자료로, 없으면 유튜브 영상으로 연결돼요.
- 다음 모임 항목이 아직 없으면 공지 카드에 학습 순서의 다음 주차 주제가 대신 나와요.

## 음원에 대해

듣기는 Easy Spanish Podcast 공식 유튜브 영상을 페이지에 넣어 재생해요. 저작권 때문에 MP3 파일은 올리지 않아요. (2026-10-25에 1·2주차 MP3를 내렸어요. 이 채널은 Spotify·Apple 팟캐스트에는 없어요.)
