---
name: qa-processor
description: |
  Notion QA 데이터베이스에서 할당된 QA 항목을 자동으로 가져와 분석하고, 코드 수정 후 검증까지 처리하는 워크플로우 자동화 스킬.
  사용 시점: "QA 처리해줘", "QA 돌려줘", "qa 자동화", "노션 QA 처리", "QA 이슈 수정해줘", "qa-processor", "통합 QA 처리", "QA 돌려", "qa 해줘" 등 QA 이슈를 일괄 처리하고 싶을 때.
  Notion에서 QA 항목을 가져오거나, QA 버그를 자동으로 수정하고 싶다는 요청이 있으면 이 스킬을 사용한다.
---

# QA Processor

Notion QA DB에서 이슈를 가져와 **분석 -> 코드 수정 -> 검증 -> 보고 -> 커밋/Notion 업데이트**까지 자동화한다.

## 사전 준비

스킬 디렉토리의 `config.json`이 필요하다. 없으면 `config.example.json`을 참고해 생성하도록 사용자에게 안내한다.

DB 스키마 상세 정보는 `references/notion-schema.md`를 참조한다.

---

## Step 1: Notion QA 항목 조회

Notion REST API를 `curl`로 직접 호출한다 (MCP 사용 금지).

config.json에서 `notion.token`, `notion.database_id`, `user.notion_user_id`, `filter`, `max_items`를 읽는다.

### 1-1. 데이터베이스 쿼리

```bash
curl -s -X POST "https://api.notion.com/v1/databases/${DATABASE_ID}/query" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "filter": {
      "and": [
        {
          "property": "개발 상태",
          "status": { "equals": "<config.filter.개발 상태>" }
        },
        {
          "property": "처리할 사람",
          "people": { "contains": "<config.user.notion_user_id>" }
        },
        {
          "property": "대분류",
          "rollup": {
            "any": {
              "select": { "equals": "<config.filter.대분류>" }
            }
          }
        }
      ]
    },
    "page_size": <config.max_items>
  }'
```

`config.filter.대분류` 값이 없으면 해당 필터 조건은 `and` 배열에서 생략한다.

결과가 0건이면 "처리할 QA 항목이 없습니다"를 알리고 종료한다.

### 1-2. 각 항목에서 추출할 정보

| 필드        | JSON 경로                                                 |
| ----------- | --------------------------------------------------------- |
| 페이지 ID   | `results[].id`                                            |
| 이슈 제목   | `results[].properties.이슈.title[0].text.content`         |
| 기대결과    | `results[].properties.기대결과.rich_text[0].text.content` |
| 우선순위    | `results[].properties.우선순위.select.name`               |
| 시나리오 ID | `results[].properties.시나리오.relation[].id`             |
| 개발 상태   | `results[].properties.개발 상태.status.name`              |

Notion 페이지 링크: `https://www.notion.so/{page_id에서 하이픈 제거}`

### 1-3. 시나리오 상세 조회

시나리오 relation의 페이지 ID로 추가 맥락을 가져온다:

```bash
curl -s "https://api.notion.com/v1/pages/${SCENARIO_PAGE_ID}" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Notion-Version: 2022-06-28"
```

추출: 시나리오명, 도메인, 대분류, 구분(TC/BUG/기획변경), 유형

### 1-4. 페이지 본문 조회

이슈의 상세 설명이 필요하면 블록 내용을 가져온다:

```bash
curl -s "https://api.notion.com/v1/blocks/${PAGE_ID}/children?page_size=100" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Notion-Version: 2022-06-28"
```

---

## Step 2: 병렬 분석

가져온 QA 항목을 **병렬로** 분석한다. 각 항목당 하나의 subagent(Agent 도구)를 생성한다.

### subagent에게 전달할 정보

- QA 이슈 제목, 기대결과
- 시나리오 정보 (도메인, 대분류, 구분, 유형)
- 페이지 본문 내용
- 프로젝트 루트 경로

### subagent 분석 지시

각 subagent는 코드베이스를 탐색하여 다음을 반환한다:

```
## QA-{번호}: {이슈 제목}

### 시나리오
{시나리오 설명}

### 기대 결과
{기대 결과}

### 현재 문제점
{코드를 분석하여 발견한 구체적 문제}

### 수정 대상 파일
- {파일경로}: {수정 내용 요약}

### 수정 방안
{구체적인 코드 수정 방안 - 어떤 코드를 어떻게 바꿔야 하는지}
```

subagent는 코드를 **분석만** 하고, 직접 수정하지 않는다.

---

## Step 2-1: 분석 결과 리뷰 & 사용자 확인

모든 분석이 완료되면:

1. **파일 충돌 체크**: 여러 QA 항목이 같은 파일을 수정해야 하는지 확인
   - 충돌 발견 시 사용자에게 알리고, 충돌 항목의 실행 순서를 조정
2. **태스크 목록 생성**: 우선순위 순으로 정렬 (최상 > 상 > 중 > 하)
3. **전체 분석 결과 표시**: 각 QA 항목의 분석 결과를 사용자에게 보여준다
4. **사용자 확인**: 사용자가 확인/수정 지시한 후에만 Step 3로 진행한다

각 태스크별로 다음 포맷으로 전체 분석 결과를 출력한다:

```
---
[TASK-1] QA-{번호} | {이슈 제목} | 우선순위: {값}

시나리오: {시나리오 설명}
기대 결과: {기대 결과}
현재 문제점: {코드를 분석하여 발견한 구체적 문제}
수정 대상 파일:
  - {파일경로}: {수정 내용 요약}
수정 방안: {구체적인 코드 수정 방안}

---
[TASK-2] QA-{번호} | {이슈 제목} | 우선순위: {값}
...
```

충돌이 있는 경우 해당 태스크에 표시:

```
[TASK-3] QA-{번호} | {이슈 제목} | ⚠ TASK-1과 파일 충돌: {파일명}
```

사용자는 분석 결과를 확인한 뒤 다음과 같은 지시를 할 수 있다:
- **특정 태스크 제외**: "TASK-2는 빼줘" → 해당 태스크를 실행 목록에서 제거
- **수정 방안 변경**: "TASK-1은 이렇게 수정해줘: ..." → 해당 태스크의 수정 방안을 사용자 지시로 대체
- **전체 승인**: "진행해줘" → 모든 태스크를 현재 분석 결과대로 실행

사용자의 명시적 승인이 있을 때까지 Step 3으로 진행하지 않는다.

---

## Step 3: 직렬 실행

사용자 확인 후, 태스크를 **하나씩 순서대로** 실행한다.

### 각 태스크 실행 흐름

```
코드 수정 -> type-check 실행
  -> 성공: 태스크 완료, 다음 태스크로
  -> 실패: 에러 분석 후 재수정 (최대 2회 재시도)
    -> 여전히 실패: 변경 롤백, 태스크 실패 기록
```

### Type-check 규칙

변경된 파일 경로에 따라 해당 패키지만 type-check 실행:

| 파일 경로 prefix   | 명령어                                              |
| ------------------ | --------------------------------------------------- |
| `apps/admin/`      | `pnpm --filter admin type-check`                    |
| `apps/b2c/`        | `pnpm --filter b2c type-check`                      |
| `packages/shared/` | `pnpm --filter @ridenow-frontend/shared type-check` |
| `packages/rui/`    | `pnpm --filter @ridenow-frontend/rui type-check`    |

여러 패키지가 변경된 경우 영향받는 모든 패키지에 대해 실행한다.

### 실패 시 롤백

재시도 2회 후에도 실패하면 해당 태스크의 변경사항을 모두 되돌린다:

```bash
git checkout -- <변경된 파일들>
```

---

## Step 3-1: 결과 보고

모든 태스크 완료 후 아래 포맷으로 보고한다:

```
{TASK_NUMBER}[{notion_link}] / 처리 결과: 성공 / {작업 내용 1줄 요약}
{TASK_NUMBER}[{notion_link}] / 처리 결과: 실패 / {실패 사유 1줄 요약}
```

예시:

```
1[https://notion.so/abc123] / 처리 결과: 성공 / 상품 목록 페이지 정렬 로직 수정
2[https://notion.so/def456] / 처리 결과: 실패 / type-check 실패 - ProductType 타입 호환 불가
3[https://notion.so/ghi789] / 처리 결과: 성공 / 계약 상세 날짜 포맷 수정
```

---

## Step 3-2: 완료 처리

**성공한 태스크에 대해서만** 수행한다.

### Git Commit

각 성공 태스크별로 개별 커밋한다:

```bash
git add <변경된 파일들>
git commit -m "fix: {작업 내용 1줄 요약}"
```

커밋 메시지에는 Co-Authored-By를 추가하지 않는다.

### Notion 상태 업데이트

config.json의 `on_complete`에 지정된 컬럼과 값으로 업데이트한다:

```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/${PAGE_ID}" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "properties": {
      "개발 상태": {
        "status": {
          "name": "<config.on_complete.개발 상태>"
        }
      }
    }
  }'
```

업데이트 실패 시 사용자에게 알리되, 커밋은 유지한다.

---

## 주의사항

- 코드 수정 시 프로젝트의 CLAUDE.md와 .claude/rules/ 에 정의된 컨벤션을 반드시 따른다
- Notion API 호출 실패 시 에러 내용을 사용자에게 알리고 재시도 여부를 확인한다
- config.json에 유효한 Notion token이 없으면 사용자에게 안내한다

