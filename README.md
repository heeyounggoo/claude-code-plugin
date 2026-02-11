# claude-code-plugin

Claude Code 세션을 마무리할 때 대화 내용을 구조화된 한국어 마크다운으로 정리하고 Obsidian 볼트에 자동 저장하는 플러그인.

## 설치

### 방법 1: `--plugin-dir` 옵션으로 실행

```bash
claude --plugin-dir /path/to/claude-code-plugin
```

### 방법 2: 프로젝트 내에 포함

프로젝트 루트에 이 저장소를 클론하거나 복사한 뒤 플러그인 디렉토리로 지정한다.

## 설정

### Obsidian 볼트 경로

세션 요약이 저장될 경로를 환경변수로 설정한다:

```bash
export OBSIDIAN_VAULT_PATH="$HOME/your-obsidian-vault/claude-sessions"
```

`.bashrc`, `.zshrc` 등에 추가하면 매번 설정할 필요가 없다.

**경로 우선순위:**
1. 명령어 인자로 전달한 경로 (`/wrap /path/to/vault`)
2. `OBSIDIAN_VAULT_PATH` 환경변수
3. 기본값: `~/obsidian-vault/claude-sessions/`

## 사용법

세션 작업을 마친 뒤 다음 명령어를 입력한다:

```
/wrap
```

또는 정규화된 이름으로:

```
/claude-code-plugin:wrap
```

특정 경로를 직접 지정할 수도 있다:

```
/wrap ~/my-vault/sessions
```

## 세션 요약 포맷

`/wrap` 실행 시 다음 구조의 마크다운이 생성된다:

- **세션 메타** — 주제, 날짜, 프로젝트, 태그
- **목표와 결과** — 달성 항목(✅)과 미완료 항목(⬜)
- **핵심 의사결정** — 결정/이유/기각된 대안 테이블
- **코드 변경 요약** — 파일별 변경 내용 테이블
- **회고** — 배운 것, 개선 필요, 다음에 적용

파일명은 `YYMMDD.md` 형식이며, 같은 날 여러 번 실행하면 기존 파일에 `---` 구분선과 함께 append된다.
