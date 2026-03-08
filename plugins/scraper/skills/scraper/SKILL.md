---
name: scraper
description: YouTube 영상, 웹 아티클, 파일을 받아 분석하고 Obsidian에 구조화된 노트로 저장. "유튜브 정리", "아티클 저장", "파일 요약", URL이나 파일 경로를 전달하며 Obsidian에 저장하고 싶을 때, 또는 어떤 리소스든 읽고 정리하고 싶을 때 이 스킬을 사용.
allowed-tools:
  - AskUserQuestion
  - Skill
argument-hint: "[youtube|article|file] <URL 또는 파일경로>"
---

# /scraper — 범용 리소스 라우터

입력을 파싱하여 리소스 타입을 결정한 뒤, 전담 스킬로 위임한다.

---

## Phase 0: 입력 파싱

`$ARGUMENTS`를 파싱하여 `TYPE`과 `RESOURCE`를 추출한다.

### 파싱 규칙

1. 첫 번째 토큰이 `youtube` / `article` / `file`이면 → `TYPE`으로 설정, 나머지를 `RESOURCE`로 설정
2. 첫 번째 토큰이 URL 형태(`http`로 시작)이면 URL을 보고 추론:
   - `youtube.com` 또는 `youtu.be` 포함 → `TYPE=youtube`
   - 그 외 URL → `TYPE=article`
3. 경로 패턴 (`/`, `~/`, `./` 시작 또는 확장자 포함) → `TYPE=file`
4. 타입은 결정됐으나 `RESOURCE`가 없으면 AskUserQuestion으로 URL/경로 요청
5. `$ARGUMENTS`가 비어 있으면 AskUserQuestion으로 타입 선택:

```
어떤 리소스를 정리할까요?
options:
  - youtube: YouTube 영상 URL
  - article: 웹 아티클 또는 블로그 URL
  - file: 로컬 파일 경로
```

---

## Phase 1: 전담 스킬 위임

`TYPE`에 따라 해당 스킬을 호출하고, `RESOURCE`를 인자로 전달한다.

| TYPE    | 호출 스킬 | args         |
| ------- | --------- | ------------ |
| youtube | `youtube` | `{RESOURCE}` |
| article | `article` | `{RESOURCE}` |
| file    | `file`    | `{RESOURCE}` |

Skill 도구로 해당 스킬을 실행한다. 이후 모든 처리는 해당 스킬이 담당한다.
