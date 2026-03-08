# Scraper Plugin — 공통 설정

스킬 실행 시 이 파일을 Read하여 아래 정의를 따른다.

---

## VAULT_BASE 결정

아래 우선순위로 결정한다:

1. `$OBSIDIAN_VAULT_PATH` 환경변수
2. `~/.claude/scraper.local.md`의 `vault_path` 필드 (YAML frontmatter)
3. 기본값: `~/obsidian-vault`

`~/.claude/scraper.local.md` 읽기: Read로 파일을 읽고 YAML frontmatter에서 `vault_path` 추출.

---

## 변수

| 변수         | 값                                           |
| ------------ | -------------------------------------------- |
| `VAULT_BASE` | 위 우선순위로 결정                           |
| `DATE`       | 오늘 날짜를 `YYMMDD` 형식으로 (예: `260308`) |

---

## 파일명 규칙

형식: `{slug}.md`

- `slug`: 제목에서 한글/영문/숫자만 남기고 공백은 `-`로 변환, 최대 40자
- 예: `claude-code-plugin-만들기.md`

---

## 작성 규칙

- 모든 내용은 **한국어**로 작성 (원본이 영어여도 번역하여 정리)
- 추론 불가한 부분은 생략 (내용을 꾸며내지 않음)
- 광고, 구독 요청, 보일러플레이트 등 비내용성 텍스트 제외

---

## 저장 절차

저장 경로: `{VAULT_BASE}/{스킬명}/` (예: `~/obsidian-vault/youtube/`)

1. Bash로 `mkdir -p {경로}` 실행
2. Glob으로 `{경로}/{파일명}`이 존재하는지 확인
3. **있으면:** AskUserQuestion으로 처리 방법 선택:

```
같은 파일이 이미 존재합니다: {파일 경로}
options:
  - overwrite: 덮어쓰기
  - rename: 새 파일명으로 저장 (접미사 추가)
  - skip: 건너뜀
```

4. **없으면:** Write로 새 파일 생성
