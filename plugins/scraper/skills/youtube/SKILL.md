---
name: youtube
description: YouTube 영상을 구조화된 한국어 노트로 정리하여 Obsidian에 저장. YouTube URL이 포함된 요청이거나 "유튜브 정리", "영상 노트", "영상 요약" 등의 맥락이면 이 스킬을 사용하세요.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - AskUserQuestion
  - mcp__youtube-transcript__get_transcript
argument-hint: "<youtube-url>"
---

# /youtube — YouTube 영상 정리 & Obsidian 저장

YouTube URL을 받아 자막을 추출하고, 구조화된 한국어 노트로 정리하여 Obsidian에 저장한다.

시작 전에 Read로 아래 두 파일을 읽어 규칙·포맷을 파악한다:

- `${CLAUDE_PLUGIN_ROOT}/references/config.md` — 공통 변수·저장 절차
- `${CLAUDE_PLUGIN_ROOT}/references/note.md` — 통일 노트 포맷

---

## 1단계: URL 확인

`$ARGUMENTS`에서 YouTube URL을 추출한다.

URL이 없으면 AskUserQuestion으로 URL을 요청한다.

## 2단계: 자막 추출

`mcp__youtube-transcript__get_transcript` 도구로 자막을 가져온다.

- `url`: `$ARGUMENTS`의 YouTube URL
- `lang`: `ko` 우선, 실패 시 `en`으로 재시도

자막 추출에 실패하면 사용자에게 알리고 종료한다.

## 3단계: 노트 생성

추출된 자막 전체를 분석하여 `references/note.md`의 통일 포맷으로 한국어 노트를 작성한다.

**`{CONTENT}` 구조 (youtube 전용):**

```markdown
## 주요 내용

{영상 흐름에 따라 섹션별 정리}

### {섹션 제목}

- {핵심 포인트}
```

**변수 채우기:**

- `{SOURCE}`: YouTube URL
- `{TAGS}`: 영상 주제 태그
- `{SUBJECT}`: 영상 핵심 주제 2-3줄
- `{인사이트}`: 가장 인상적이거나 실용적인 아이디어 3-5개

작성 규칙: `references/config.md`의 **작성 규칙**을 따른다.
추가 규칙: 자막이 없는 부분은 추론하지 말고 생략.

## 4단계: 미리보기 및 확인

생성한 노트를 사용자에게 보여준 뒤, AskUserQuestion으로 확인한다.

- "이대로 저장" → 5단계 진행
- "수정 요청" → 피드백 반영 후 다시 4단계 반복
- "저장 취소" → 저장 없이 종료

## 5단계: 저장

`references/config.md`의 **저장 절차**를 따른다. 저장 경로: `{VAULT_BASE}/youtube/`

## 6단계: 완료 메시지

```
✅ YouTube 노트가 저장되었습니다
   영상: {영상 제목}
   경로: {저장된 파일의 전체 경로}
   태그: {태그 목록}
```
