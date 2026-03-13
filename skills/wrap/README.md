# wrap 스킬

세션 내용을 Obsidian에 저장하는 스킬. 두 가지 모드로 동작한다.

## 모드

### 모드 A: 내용 추가

특정 내용을 Obsidian에 메모로 저장할 때 사용.

**트리거 예시:**

- "옵시디언에 추가해줘"
- "obsidian에 저장해줘"
- "이거 옵시디언 정리해줘"

**동작:** `$ARGUMENTS`의 내용을 읽기 좋은 메모/문서로 가공하여 저장.

### 모드 B: 세션 요약

대화 세션을 마무리할 때 전체 내용을 요약하여 저장.

**트리거 예시:**

- `/wrap`
- "세션 정리해줘"
- "세션 마무리"
- "대화 정리해줘"

**동작:** 전체 대화를 분석하여 세션 흐름 / 주요 내용 / 이어서 할 것 구조로 요약. 세션 유형(코딩/학습/기획/토론)을 자동 감지하여 적합한 형식으로 작성.

## 설치 및 설정

### 1. config.json 생성

```bash
cp config.example.json config.json
```

`config.json`을 열어 Obsidian vault 경로를 설정한다:

```json
{
  "obsidian_vault_path": "/Users/yourname/path/to/obsidian-vault"
}
```

`config.json`은 `.gitignore`에 포함되어 있어 커밋되지 않는다.

### 2. 경로 결정 우선순위

1. 인수로 직접 경로 전달 (`/wrap ~/my-vault`)
2. `config.json`의 `obsidian_vault_path`
3. `$OBSIDIAN_VAULT_PATH` 환경변수
4. 기본값: `~/obsidian-vault/claude-sessions/`

## 저장 포맷

날짜별 파일(`YYMMDD.md`)에 저장. 같은 날 여러 세션은 `---` 구분선으로 구분되어 append됨. 동일 주제의 연속 세션(모드 B)은 자동으로 병합.

```markdown
## {제목}

| Field         | Value         |
| ------------- | ------------- |
| 날짜          | 260211 14:30  |
| 프로젝트/주제 | {컨텍스트}    |
| 태그          | #태그1 #태그2 |

### 세션 흐름

...

### 주요 내용

...
```

## 파일 구조

```
wrap/
├── SKILL.md           # 스킬 실행 지침 (영어)
├── README.md          # 이 파일
├── config.json        # 개인 설정 (gitignore)
└── config.example.json  # 설정 포맷 예시
```
