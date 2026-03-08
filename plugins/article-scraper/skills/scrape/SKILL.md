---
name: scrape
description: URL을 받아 아티클을 정리하여 Obsidian에 저장. 단건·목록 페이지 모두 지원.
allowed-tools:
  - WebFetch
  - Bash
  - Write
  - Read
  - Glob
  - Agent
  - AskUserQuestion
argument-hint: "<URL>"
---

# /scrape <URL> — 범용 아티클 스크랩 & Obsidian 저장

URL을 받아 아티클을 자동으로 스크랩하고, 번역·요약하여 Obsidian에 저장한다.
단건 아티클과 목록 페이지 모두 지원한다.

---

## Phase 0: 초기 설정

### 0-1. 설정 파일 로드

`.claude/scrape.local.md`를 Read로 읽어 `vault_path`와 `output_dir`을 가져온다.

- 파일이 없으면 기본값 사용:
  - `vault_path`: `$OBSIDIAN_VAULT_PATH` 환경변수 → 없으면 `~/obsidian-vault`
  - `output_dir`: `Articles`
- 기본값 사용 시 아래 안내를 출력한다:

```
설정 파일이 없습니다. 기본값으로 진행합니다.
  vault_path: {사용할 경로}
  output_dir: Articles
저장 경로를 변경하려면 /scrape:config 를 실행하세요.
```

### 0-2. URL 확인

`$ARGUMENTS`에서 URL을 추출한다.

URL이 없으면 AskUserQuestion으로 요청한다:

```
스크랩할 URL을 입력해주세요.
(단건 아티클 또는 목록 페이지 URL 모두 가능)
```

---

## Phase 1: 페이지 가져오기

WebFetch로 URL을 가져온다.

본문이 500자 미만이면 JS 렌더링이 필요한 페이지로 판단하여 cmux fallback을 사용한다:

```bash
cmux new-surface          # --url 플래그 금지
cmux navigate {URL}
cmux snapshot             # --compact 플래그 금지
```

cmux도 실패하면 사용자에게 알리고 종료한다.

---

## Phase 2: URL 타입 판별

가져온 HTML/콘텐츠를 분석하여 단건 아티클인지 목록 페이지인지 판별한다.

**목록 페이지 기준 (하나라도 해당되면):**

- `<article>` 태그가 3개 이상 반복
- 날짜 + 제목 + 링크 패턴이 반복적으로 등장
- URL이 `/blog`, `/posts`, `/articles`, `/news` 등 목록성 경로

**단건 아티클 기준 (하나라도 해당되면):**

- `<p>` 태그가 다수 (5개 이상)
- `og:type=article` 메타태그
- reading time 정보 존재
- 하나의 연속된 긴 본문

**판단 불가:**

AskUserQuestion으로 확인한다:

```
이 URL이 단건 아티클인가요, 아니면 여러 글이 나열된 목록 페이지인가요?
1. 단건 아티클
2. 목록 페이지
```

---

## Phase 3-A: 단건 아티클 처리

article-processor subagent를 1개 실행한다:

```
Agent(
  agent: "article-processor",
  inputs: {
    url: "{URL}",
    vault_path: "{vault_path}",
    output_dir: "{output_dir}"
  }
)
```

결과를 받아 Phase 4로 이동한다.

---

## Phase 3-B: 목록 페이지 처리

### 3-B-1. 아티클 URL 목록 추출

HTML에서 개별 아티클 URL을 추출한다.

추출 방법 (순서대로 시도):

1. `<article>` 내 `<a>` 링크
2. 날짜 + 제목 + 링크 패턴 반복 구조
3. `<a>` 태그 중 본문 경로로 보이는 링크 (`/blog/`, `/post/`, `/article/` 등 포함)

상대경로는 원본 도메인으로 절대경로 변환.

추출된 URL이 0개이면 AskUserQuestion으로 URL을 직접 입력받는다.

### 3-B-2. 배치 처리 (3개씩 병렬)

추출된 URL을 3개씩 묶어 처리한다.

**각 배치에서 3개 subagent를 단일 응답에 병렬 실행한다:**

```
Agent(article-processor, {url: url1, vault_path, output_dir})
Agent(article-processor, {url: url2, vault_path, output_dir})
Agent(article-processor, {url: url3, vault_path, output_dir})
```

한 배치 완료 후 다음 배치를 실행한다.

### 3-B-3. 페이지네이션

배치 완료 후 HTML에서 다음 페이지 링크를 탐색한다.

```
다음 페이지 감지 기준:
- <a> href에 "next", "다음", "page=N+1" 패턴
- .pagination-next, [aria-label="Next"] 등 네비게이션 요소
```

다음 페이지가 있으면 Phase 1부터 반복한다 (최대 10페이지).

---

## Phase 4: 완료 메시지

처리 결과를 수집하여 완료 메시지를 출력한다.

```
요청한 아티클 정리가 끝났습니다 :)
- 저장 경로: {vault_path}/{output_dir}/
- 처리한 포스팅: {N}개

|제목|경로|
|--|--|
|{제목}|{경로}|
|{제목}|이미 존재|
|{제목}|실패|
```

---

## 에러 처리

| 상황                           | 처리                                               |
| ------------------------------ | -------------------------------------------------- |
| `.claude/scrape.local.md` 없음 | 기본값 사용 + `/scrape:config` 안내                |
| WebFetch 빈 응답               | cmux fallback 시도                                 |
| cmux도 실패                    | 사용자에게 알리고 해당 URL 건너뜀                  |
| 파일 중복                      | skip + 완료 테이블에 "이미 존재" 표시              |
| 목록 URL 추출 실패             | AskUserQuestion으로 URL 직접 입력 요청             |
| 페이지네이션 감지 실패         | HTML에서 직접 다음 페이지 링크 탐색 후 없으면 종료 |

---

## 주의사항

- `cmux new-surface --url` 사용 금지 — JS 렌더링 미완료 버그
- `cmux browser eval`에서 `JSON.stringify` 사용 금지 — 이스케이핑 충돌
- `cmux snapshot --compact` 사용 금지 — 본문 텍스트 미포함
- 배치 크기는 3개로 제한 — 병렬 context 과소비 방지
- side effect(파일 저장)가 있으므로 사용자가 명시적으로 `/scrape`를 호출할 때만 실행
