# 당근 스페인어 스터디 사이트

주소: https://lkj640.github.io/carrot_spanish/

매주 일요일 오전 10시 · 이디야커피 일산허유재병원

## 구성

| 파일 | 역할 |
|---|---|
| `index.html` | 첫 화면 — 다음 모임 공지 + 모임 목록 |
| `meeting.html?d=YYYY-MM-DD` | 모임별 페이지 — 듣기(유튜브/MP3) · 교재 · 단어장 |
| `meetings.json` | **모임 목록과 공지 내용. 매주 여기에 한 항목만 추가하면 돼요.** |
| `meetings/<날짜>/` | `data.json`(대본·번역·단어), `audio.mp3`, `workbook.pdf`, `workbook.html` 또는 `pages/*.jpg` |
| `assets/` | 공통 디자인(`style.css`)과 화면 코드 |
| `tools/` | 자료 만드는 스크립트 (아래 참고) |

공지 규칙: 오늘 이후 가장 가까운 모임이 맨 위 '다음 모임 공지'에 나와요. 모임 당일은 낮 12시(한국 시간)까지 '오늘 모임'으로 보이고, 그 뒤에는 다음 주 모임으로 바뀌어요.

## 매주 새 모임 올리기

1. 원본 폴더(`../<날짜>/`)에 팟캐스트 mp3와 유튜브 대본 txt를 넣어요.
2. 자료 만들기 (Claude에게 "○월 ○일 모임 자료 만들어서 사이트에 올려줘"라고 부탁해도 돼요)
   - `tools/asr.py`로 음성 인식 → `tools/align.py`로 문장별 시작 시간 맞추기
   - `tools/<날짜>/lines.py`(문장·번역), `vocab.py`(단어), `times.json`(시간)
   - `python3 tools/make_data.py src tools/<날짜> meetings/<날짜>/data.json`
   - 교재: `tools/<날짜>/build_book.py` → `workbook.html` → Chrome으로 PDF 저장
   - 음성: `ffmpeg -i 원본.mp3 -ac 1 -b:a 48k meetings/<날짜>/audio.mp3`
3. `meetings.json`의 `meetings` 배열에 항목 추가 (`youtube`에는 영상 ID, 예: `F9zOIHrW88M`)
4. `git add . && git commit -m "○월 ○일 모임 추가" && git push`

항목 예시:
```json
{
  "date": "2026-11-01", "ep": 7, "level": "A1", "emoji": "🏠",
  "title": "모임 주제", "es": "대표 스페인어 문장",
  "duration": "20:00", "youtube": "영상ID",
  "audio": "audio.mp3", "pdf": "workbook.pdf", "workbookHtml": "workbook.html",
  "topics": ["배울 내용 1", "배울 내용 2"],
  "notice": "이번 주 공지 문구"
}
```
시간·장소·준비물을 그 주만 바꾸려면 항목에 `"time"`, `"place"`, `"mapUrl"`, `"bring"`을 넣으면 돼요.

## 음원에 대해

듣기 기본값은 Easy Spanish Podcast 공식 유튜브 영상을 페이지에 넣어 재생하는 방식이에요. MP3 듣기를 빼려면 해당 모임 항목에서 `"audio"` 줄을 지우고 mp3 파일을 삭제하면 돼요.
