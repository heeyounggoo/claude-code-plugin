---
description: YouTube 영상 내용을 정리하여 Obsidian에 저장
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

## 1단계: URL 확인

`$ARGUMENTS`에서 YouTube URL을 추출한다.

URL이 없으면 AskUserQuestion으로 URL을 요청한다.

## 2단계: 자막 추출

`mcp__youtube-transcript__get_transcript` 도구로 자막을 가져온다.

- `url`: `$ARGUMENTS`의 YouTube URL
- `lang`: `ko` 우선, 실패 시 `en`으로 재시도

자막 추출에 실패하면 사용자에게 알리고 종료한다.

## 3단계: Obsidian 저장 경로 결정

저장 경로를 아래 우선순위로 결정한다:

1. `$OBSIDIAN_VAULT_PATH` 환경변수가 있으면 `$OBSIDIAN_VAULT_PATH/youtube/`
2. 없으면 `~/obsidian-vault/youtube/`

Bash로 `mkdir -p <경로>` 를 실행한다.

## 4단계: 노트 생성

추출된 자막 전체를 분석하여 아래 템플릿으로 한국어 노트를 작성한다.

### 노트 템플릿

```markdown
# {영상 제목}

| 항목 | 내용 |
|------|------|
| 날짜 | {YYMMDD} |
| 출처 | {YouTube URL} |
| 태그 | {#태그1 #태그2 #태그3} |

## 핵심 요약

{영상 전체를 3-5문장으로 압축. 핵심 주장과 결론 중심으로.}

## 주요 내용

{영상의 흐름에 따라 섹션을 나눠 정리. 각 섹션은 소제목(###)과 핵심 포인트(bullet)로 구성.}

### {섹션 1 제목}

- {핵심 포인트}
- {핵심 포인트}

### {섹션 2 제목}

- {핵심 포인트}
- {핵심 포인트}

## 핵심 인사이트

- {가장 인상적이거나 실용적인 아이디어 3-5개}

## 메모

{개인 메모 공간 — 비워둠}
```

**작성 규칙:**
- 모든 내용은 **한국어**로 작성 (원본이 영어여도 번역하여 정리)
- 태그는 영상 주제를 반영 (`#기술 #개발 #AI` 등)
- 날짜 형식: `YYMMDD` (예: `260308`)
- 자막이 없는 부분은 추론하지 말고 생략
- 광고, 구독 요청 등 비내용성 발화는 제외

## 5단계: 미리보기 및 확인

생성한 노트를 사용자에게 보여준 뒤, AskUserQuestion으로 확인한다.

- "이대로 저장" → 6단계 진행
- "수정 요청" → 피드백 반영 후 다시 5단계 반복
- "저장 취소" → 저장 없이 종료

## 6단계: Obsidian에 저장

파일명은 `{YYMMDD}-{영상-제목-slug}.md` 형식이다.
- 영상 제목에서 한글/영문/숫자만 남기고, 공백은 `-`로 변환, 최대 40자
- 예: `260308-claude-code-plugin-만들기.md`

1. Glob으로 동일 파일이 있는지 확인
2. **있으면:** AskUserQuestion으로 덮어쓸지 확인 후 처리
3. **없으면:** Write로 새 파일 생성

## 7단계: 완료 메시지

```
✅ YouTube 노트가 저장되었습니다
   영상: {영상 제목}
   경로: {저장된 파일의 전체 경로}
   태그: {태그 목록}
```
