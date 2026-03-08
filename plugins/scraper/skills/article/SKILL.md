---
name: article
description: 웹 아티클 URL을 받아 분석하고 Obsidian에 구조화된 한국어 노트로 저장. "아티클 저장", "글 정리", "블로그 요약", 웹 URL을 주며 읽고 정리하고 싶을 때 이 스킬을 사용. 단건 아티클과 목록 페이지 모두 지원.
allowed-tools:
  - WebFetch
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
  - Agent
argument-hint: "<URL>"
---

# /article — 웹 아티클 스크랩 & Obsidian 저장

URL을 받아 아티클을 스크랩하고, 번역·요약하여 Obsidian에 저장한다.
단건은 스킬이 직접 처리, 다건은 `article-analyzer` 에이전트를 병렬 호출한다.

시작 전에 Read로 아래 두 파일을 읽어 규칙·포맷을 파악한다:
- `${CLAUDE_PLUGIN_ROOT}/references/config.md` — 공통 변수·저장 절차
- `${CLAUDE_PLUGIN_ROOT}/references/note.md` — 통일 노트 포맷

---

## Phase 0: URL 확인

`$ARGUMENTS`에서 URL을 추출한다.

URL이 없으면 AskUserQuestion으로 요청한다:

```
스크랩할 URL을 입력해주세요.
(단건 아티클 또는 목록 페이지 URL 모두 가능)
```

---

## Phase 1: 단건/다건 선택

AskUserQuestion으로 사용자에게 처리 방식을 선택하게 한다:

```
URL을 어떻게 처리할까요?
options:
  - single: 단건 아티클로 처리
  - list: 목록 페이지에서 여러 아티클 선택
```

- `single` → Phase 2-A (단건 처리)
- `list` → Phase 2-B (다건 처리)

---

## Phase 2-A: 단건 처리

### A. 내용 가져오기

WebFetch로 URL을 가져온다.

본문이 500자 미만이면 cmux fallback을 시도한다:

```bash
cmux new-surface
cmux navigate {URL}
cmux snapshot
```

**주의사항:**
- `cmux new-surface --url` 플래그 사용 금지 — JS 렌더링 미완료 버그
- `cmux snapshot --compact` 플래그 사용 금지 — 본문 텍스트 미포함

cmux도 실패하면 사용자에게 알리고 종료한다.

### B. 노트 작성

`references/note.md`의 통일 포맷으로 한국어 노트를 작성한다.

**`{CONTENT}` 구조:**

```markdown
## 주요 내용

{내용 흐름에 따라 섹션별 정리. 다른 언어는 한국어로 번역.}

### {섹션 제목}
- {핵심 포인트}
```

**변수 채우기:**
- `{SOURCE}`: 아티클 URL
- `{TAGS}`: 내용 주제 태그 + `#article`
- `{SUBJECT}`: 아티클 핵심 주제 2-3줄
- `{인사이트}`: 중요한 점/생각해볼 점 1-5가지

작성 규칙: `references/config.md`의 **작성 규칙**을 따른다.

### C. 저장

`references/config.md`의 **저장 절차**를 따른다. 저장 경로: `{VAULT_BASE}/article/`

→ Phase 5-A

---

## Phase 2-B: 다건 처리

### 2-B-1. 목록 URL 가져오기

WebFetch로 URL을 가져온다.

본문이 500자 미만이면 cmux fallback을 시도한다:

```bash
cmux new-surface
cmux navigate {URL}
cmux snapshot
```

**주의사항:**
- `cmux new-surface --url` 플래그 사용 금지 — JS 렌더링 미완료 버그
- `cmux snapshot --compact` 플래그 사용 금지 — 본문 텍스트 미포함

cmux도 실패하면 사용자에게 알리고 종료한다.

### 2-B-2. 아티클 URL 목록 추출

HTML에서 개별 아티클 URL을 추출한다.

추출 방법 (순서대로 시도):
1. `<article>` 내 `<a>` 링크
2. 날짜 + 제목 + 링크 패턴 반복 구조
3. `<a>` 태그 중 본문 경로로 보이는 링크 (`/blog/`, `/post/`, `/article/` 등 포함)

상대경로는 원본 도메인으로 절대경로 변환한다.

추출된 URL이 0개이면 AskUserQuestion으로 URL을 직접 입력받는다.

### 2-B-3. 처리할 아티클 선택

추출된 URL 목록을 사용자에게 보여주고 AskUserQuestion으로 선택:

```
총 {N}개의 아티클을 찾았습니다:

1. {제목 또는 URL}
2. {제목 또는 URL}
...

어떻게 처리할까요?
options:
  - all: 전체 처리
  - select: 처리할 번호를 입력 (예: 1,3,5)
  - cancel: 취소
```

`select` 선택 시 추가로 번호를 입력받는다.

### 2-B-4. 병렬 처리 & pagination

선택된 URL마다 Agent 도구로 `article-analyzer`를 동시에 호출한다 (병렬 실행):

```
agent: article-analyzer
입력:
  url: {각 URL}
```

각 에이전트 완료 시 진행 상황을 출력한다: `[{N}/{전체}] {제목} 저장 완료`

**Pagination (목록 페이지에 다음 페이지가 있을 경우):**
- 최대 3페이지까지 자동으로 처리
- 3페이지 초과 시 AskUserQuestion으로 확인:

```
이미 3페이지를 처리했습니다. 계속 진행할까요?
options:
  - continue: 계속 (최대 3페이지 추가)
  - stop: 여기서 종료
```

→ Phase 5-B

---

## Phase 5-A: 단건 완료 메시지

```
✅ 아티클 노트가 저장되었습니다
   제목: {제목}
   경로: {저장된 파일의 전체 경로}
   태그: {태그 목록}
```

---

## Phase 5-B: 다건 완료 메시지

모든 에이전트 결과를 취합하여 출력한다:

```
✅ 아티클 정리가 완료되었습니다
   저장 경로: {VAULT_BASE}/article/
   처리한 아티클: {N}개

| 제목 | 경로 | 상태 |
|------|------|------|
| {제목} | {경로} | 저장완료 |
| {제목} | {경로} | 이미존재 |
| {제목} | {경로} | 실패 |
```

---

## 에러 처리

| 상황               | 처리                                   |
| ------------------ | -------------------------------------- |
| WebFetch 빈 응답   | cmux fallback 시도                     |
| cmux도 실패        | 사용자에게 알리고 종료                 |
| 에이전트 실패      | 해당 아티클 건너뛰고 오류 기록         |
| 목록 URL 추출 실패 | AskUserQuestion으로 URL 직접 입력 요청 |
