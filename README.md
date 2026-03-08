# claude-code-plugin

GitHub으로 관리하는 개인 생산성 Claude Code 플러그인.
세션 요약, YouTube 노트, 음성 변환, 면접 대비 기능을 포함한다.

## 기능

| 명령 / 스킬 | 설명 | 트리거 방식 |
|------------|------|------------|
| `/wrap` | 세션 요약을 Obsidian에 저장 | 사용자 명시 호출 |
| `/youtube <url>` | YouTube 영상 내용 정리 후 Obsidian 저장 | 사용자 명시 호출 |
| `/transcribe <file>` | 음성 파일 → 텍스트 변환 | 사용자 명시 호출 |
| `interview-prep` | 면접 Q&A 연습, 이력서 기반 피드백 | 자동 트리거 (Agent Skill) |

## 설치

### 신규 환경 설치

```bash
# 1. 저장소 클론
git clone https://github.com/heeyounggoo/claude-code-plugin ~/dev/claude-code-plugin

# 2. 플러그인 디렉토리 심볼릭 링크 생성
mkdir -p ~/.claude/plugins
ln -s ~/dev/claude-code-plugin ~/.claude/plugins/claude-code-plugin
```

`~/.claude/settings.json`에 추가:

```json
{
  "plugins": ["~/.claude/plugins/claude-code-plugin"]
}
```

### 개발/테스트 (플러그인 디렉토리 직접 로드)

```bash
claude --plugin-dir ~/dev/claude-code-plugin
```

## 설정

### Obsidian 볼트 경로 (`/wrap`, `/youtube`)

```bash
export OBSIDIAN_VAULT_PATH="$HOME/your-obsidian-vault"
```

`.zshrc` / `.bashrc`에 추가하면 매번 설정할 필요가 없다.

**경로 우선순위:**
1. 명령 인자: `/wrap /path/to/vault`
2. `OBSIDIAN_VAULT_PATH` 환경변수
3. 기본값: `~/obsidian-vault/`

### 음성 변환 의존성 (`/transcribe`)

```bash
pip install openai-whisper
```

음성 파일은 `audio-to-text/resources/`에 넣거나 경로를 직접 전달한다.

### interview-prep 이력서 등록

`skills/interview-prep/resume/` 디렉토리에 이력서 파일 저장 (`.gitignore`로 git 제외됨).

## 구조

```
claude-code-plugin/
├── .claude-plugin/plugin.json   ← 플러그인 메타데이터
├── .mcp.json                    ← youtube-transcript MCP 의존성
├── .gitignore                   ← 개인 런타임 파일 제외
├── CLAUDE.md                    ← 개발 가이드
├── skills/                      ← 모든 스킬 (명령 포함)
│   ├── wrap/SKILL.md            ← /wrap
│   ├── youtube/SKILL.md         ← /youtube
│   ├── transcribe/SKILL.md      ← /transcribe
│   └── interview-prep/SKILL.md  ← 자동 트리거
└── audio-to-text/               ← transcribe 스킬용 Python 스크립트
    └── scripts/transcribe.py
```

## /wrap 출력 포맷

- **세션 메타** — 주제, 날짜, 프로젝트, 태그
- **목표와 결과** — 달성 항목(✅)과 미완료 항목(⬜)
- **핵심 의사결정** — 결정/이유/기각된 대안 테이블
- **코드 변경 요약** — 파일별 변경 내용 테이블
- **회고** — 배운 것, 개선 필요, 다음에 적용

파일명은 `YYMMDD.md` 형식. 같은 날 여러 번 실행하면 기존 파일에 `---` 구분선과 함께 append된다.
