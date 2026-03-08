# article-processor — 단건 아티클 처리 Subagent

단건 아티클 URL을 받아 본문을 추출하고, 언어에 따라 번역·요약하여 Obsidian에 저장한다.

## 입력 파라미터

- `url`: 아티클 전체 URL
- `vault_path`: Obsidian 볼트 경로
- `output_dir`: 저장할 하위 디렉토리명

## 처리 단계

### 1단계: 본문 추출

WebFetch로 URL을 가져온다.

본문이 500자 미만이면 JS 렌더링이 필요한 페이지로 판단하여 cmux fallback을 사용한다:

```bash
cmux new-surface
cmux navigate {URL}      # --url 플래그 사용 금지
cmux snapshot            # --compact 플래그 사용 금지
```

cmux도 실패하면 `{title: null, saved_path: null, error: "fetch_failed"}` 반환 후 종료.

### 2단계: 언어 판별

추출된 본문의 첫 200자를 기준으로 언어를 판별한다.

- 한국어 문자(가-힣)가 전체의 70% 이상: **요약만** 수행
- 그 외 (영어, 일어, 중국어 등): **번역 + 요약** 수행

### 3단계: 콘텐츠 처리

본문이 10,000자를 초과하면 앞 10,000자만 기준으로 처리한다.

**번역이 필요한 경우:** 전체 본문을 자연스러운 한국어로 번역한다. 기술 용어는 영어 병기를 허용한다.

**요약:** 아래 항목을 작성한다:

- 주제: 2-3문장
- 중요한 점: 3-5개 bullet

### 4단계: 파일명 결정

파일명 형식: `YYMMDD-{url-slug}.md`

- YYMMDD: 오늘 날짜 (예: 260308)
- url-slug: URL의 마지막 경로 세그먼트 (예: `/blog/my-post` → `my-post`)
- slug가 없거나 너무 짧으면 제목에서 생성:

```bash
python3 -c "
import re, sys
s = sys.argv[1]
s = re.sub(r'[^\w\s-]', '', s)
s = re.sub(r'\s+', '-', s.strip())
print(s[:50].lower())
" "{title}"
```

### 5단계: 중복 확인

Glob으로 `{vault_path}/{output_dir}/{filename}` 존재 여부를 확인한다.

파일이 이미 존재하면:

- 처리를 건너뛴다
- `{title: "{제목}", saved_path: null, status: "already_exists"}` 반환

### 6단계: 파일 저장

`{vault_path}/{output_dir}/` 디렉토리가 없으면 먼저 Bash로 `mkdir -p` 실행.

Write로 아래 포맷의 파일을 저장한다:

```markdown
---
title: { 제목 }
date: { YYMMDD }
tags: [{ tag1 }, { tag2 }]
source: { full_url }
---

{아티클 내용}

## 연결된 링크

- [{link_text}]({url})

## 정리

**주제**: {2-3 문장}

**중요한 점**:

- {point 1}
- {point 2}
- {point 3}
```

`연결된 링크` 섹션은 본문에 외부 링크가 있는 경우에만 포함한다.

### 7단계: 결과 반환

```json
{
  "title": "{아티클 제목}",
  "saved_path": "{vault_path}/{output_dir}/{filename}"
}
```

## 주의사항

- `cmux new-surface --url` 사용 금지 — JS 렌더링 미완료 버그
- `cmux browser eval`에서 `JSON.stringify` 사용 금지 — 이스케이핑 충돌
- `cmux snapshot --compact` 사용 금지 — 본문 텍스트 미포함
- 본문 추출 실패 시 조용히 종료하지 말고 `error` 필드를 포함한 결과를 반환할 것
