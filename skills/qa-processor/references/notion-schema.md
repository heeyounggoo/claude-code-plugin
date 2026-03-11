# Notion DB Schema Reference

## 이슈 테이블: [고래] 통합 QA 작업

- Database ID: `312163b1524a801686b9f6d25d425bcc`
- Data Source: `collection://312163b1-524a-8096-81ad-000ba4681b20`

### 컬럼

| 컬럼명 | 타입 | 값/설명 |
|--------|------|---------|
| `이슈` | title | 이슈 제목 |
| `우선순위` | select | `최상`, `상`, `중`, `하` |
| `개발 상태` | status | `시작 전`, `진행 중`, `작업 완료`, `stage 배포 완료` |
| `기대결과` | text | 기대 결과 텍스트 |
| `시나리오` | relation | 시나리오 테이블 연결 |
| `처리할 사람` | person | 담당자 |
| `구분` | rollup | 시나리오에서 가져옴 |
| `도메인` | rollup | 시나리오에서 가져옴 |
| `대분류` | rollup | 시나리오에서 가져옴 |
| `QA 담당자` | rollup | 시나리오에서 가져옴 |

### Notion API 응답 구조 (properties)

```json
{
  "이슈": {
    "type": "title",
    "title": [{ "type": "text", "text": { "content": "이슈 제목" } }]
  },
  "기대결과": {
    "type": "rich_text",
    "rich_text": [{ "type": "text", "text": { "content": "기대 결과 내용" } }]
  },
  "우선순위": {
    "type": "select",
    "select": { "name": "상" }
  },
  "개발 상태": {
    "type": "status",
    "status": { "name": "시작 전" }
  },
  "시나리오": {
    "type": "relation",
    "relation": [{ "id": "scenario-page-id" }]
  },
  "처리할 사람": {
    "type": "people",
    "people": [{ "id": "user-id", "name": "이름" }]
  }
}
```

---

## 시나리오 테이블: 통합 QA

- Database ID: `2e2163b1524a809cb1b4cf6d4cdb3f0e`

### 컬럼

| 컬럼명 | 타입 | 값/설명 |
|--------|------|---------|
| `시나리오` | title | 시나리오명 |
| `대분류` | select | `관리자 관리`, `구매조건관리`, `구매혜택관리`, `구매상담관리`, `계약관리`, `대기자관리`, `로그인`, `회원관리`, `회사관리`, `공지사항`, `FAQ`, `약관관리`, `포인트정책관리`, `상품관리`, `재고관리`, `방문정비관리`, `홈배너관리`, `구매배너관리`, `정비배너관리`, `이벤트관리` |
| `도메인` | select | `차량판매`, `방문정비`, `공통` |
| `유형` | select | `기능`, `디자인`, `알림톡`, `기타` |
| `우선순위` | select | `필수`, `상`, `중`, `하`, `보류` |
| `구분` | select | `TC`, `BUG`, `기획변경` |
| `QA 상태` | status | `시작 전`, `진행 중`, `FAIL`, `PASS`, `완료` |
| `QA 담당자` | person | QA 담당자 |
| `이슈 내용` | relation | 이슈 테이블 연결 |

### Notion API 응답 구조 (properties)

```json
{
  "시나리오": {
    "type": "title",
    "title": [{ "type": "text", "text": { "content": "시나리오명" } }]
  },
  "대분류": {
    "type": "select",
    "select": { "name": "상품관리" }
  },
  "도메인": {
    "type": "select",
    "select": { "name": "차량판매" }
  },
  "유형": {
    "type": "select",
    "select": { "name": "기능" }
  },
  "구분": {
    "type": "select",
    "select": { "name": "BUG" }
  }
}
```

---

## Notion API Endpoints

### 데이터베이스 쿼리
```
POST https://api.notion.com/v1/databases/{database_id}/query
```

### 페이지 조회
```
GET https://api.notion.com/v1/pages/{page_id}
```

### 페이지 업데이트
```
PATCH https://api.notion.com/v1/pages/{page_id}
```

### 블록(본문) 조회
```
GET https://api.notion.com/v1/blocks/{block_id}/children?page_size=100
```

### 공통 헤더
```
Authorization: Bearer {token}
Content-Type: application/json
Notion-Version: 2022-06-28
```
