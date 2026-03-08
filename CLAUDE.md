# claude-code-plugin

개인 생산성 Claude Code 플러그인.

## 플러그인 구조

```
claude-code-plugin/
├── .claude-plugin/plugin.json   ← 플러그인 메타데이터
├── .mcp.json                    ← 플러그인 의존 MCP 서버
├── skills/                      ← 모든 스킬 (명령 포함)
│   ├── wrap/SKILL.md            ← /wrap: 세션 요약 저장
│   ├── youtube/SKILL.md         ← /youtube: YouTube 노트 저장
│   ├── transcribe/SKILL.md      ← /transcribe: 음성 변환
│   └── interview-prep/SKILL.md  ← 면접 대비 (자동 트리거)
└── audio-to-text/               ← transcribe 스킬이 사용하는 Python 스크립트
    └── scripts/transcribe.py
```

## 로컬 테스트

```bash
# 현재 디렉토리를 플러그인으로 직접 로드
claude --plugin-dir ~/dev/claude-code-plugin
```

## 다른 환경 설치 (symlink)

```bash
git clone https://github.com/heeyounggoo/claude-code-plugin ~/dev/claude-code-plugin
mkdir -p ~/.claude/plugins
ln -s ~/dev/claude-code-plugin ~/.claude/plugins/claude-code-plugin
```

`~/.claude/settings.json`에 추가:

```json
{
  "plugins": ["~/.claude/plugins/claude-code-plugin"]
}
```

## Skill / Agent / Plugin 선택 기준

공식 문서 기준: https://code.claude.com/docs/en/

| 단위                 | 위치                         | 언제 사용                                                                                                    |
| -------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Skill**            | `skills/<name>/SKILL.md`     | 재사용 가능한 지시 묶음. 사용자 명시 호출(`/name`)이나 Claude 자동 트리거 모두 가능. 단일 책임 작업에 적합   |
| **Agent (Subagent)** | `agents/<name>/AGENT.md`     | 독립 context window가 필요할 때. 복잡한 다단계 작업, 비용 최적화, 역할 격리가 필요할 때                      |
| **Plugin**           | `.claude-plugin/plugin.json` | Skills/Agents/MCP를 묶어 **여러 프로젝트·환경에 공유**할 때. 단일 프로젝트 한정이면 `.claude/skills/`로 충분 |

### Skills 내 자동 트리거 vs 명시 호출 구분

`description` 필드가 Claude의 자동 트리거 여부를 결정한다.

```yaml
# 자동 트리거 (대화 맥락 기반) — interview-prep 같은 경우
description: |
  면접 준비를 돕는 스킬. 사용자가 "면접 연습", "기술 면접 준비" 등을 언급하면 자동 활성화...

# 사용자 명시 호출만 (side effect 있는 경우) — wrap, youtube, transcribe
description: 세션 마무리 및 Obsidian 저장
# → 자연어로 잘 매칭되지 않는 설명 + 사용자가 /wrap으로 직접 호출
```

side effect가 있는 스킬(파일 저장, 외부 서비스 호출)은 description을 협소하게 작성하여 의도치 않은 자동 실행을 방지한다.

## 설계 원칙

### commands/ 사용 금지

`commands/` 디렉토리는 공식적으로 `skills/`로 통합되었다. 새 명령은 반드시 `skills/<name>/SKILL.md`로 작성한다.

### MCP 의존성 관리

플러그인이 특정 MCP 서버에 의존할 경우 반드시 `.mcp.json`에 선언한다.
전역 `~/.claude/settings.json`에만 등록하면 다른 환경에서 이식되지 않는다.

### 개인 데이터 처리

런타임 생성 파일(이력서 캐시, 세션 로그, 패턴 기록 등)은 반드시 `.gitignore`로 제외한다.
`skills/<name>/memory/`, `skills/<name>/resume/`, `skills/<name>/tmp/` 경로 사용.

### 공식 플러그인 우선

`skill-creator`, `claude-hud` 등 공식 Claude 플러그인이 존재하면 로컬 복사본 대신 공식 버전을 사용한다.

### audio-to-text/ 위치

`audio-to-text/`는 Python 스크립트 디렉토리로, `skills/transcribe/`가 내부적으로 사용하는 실행 도구다.
Claude-facing 인터페이스(`/transcribe`)는 `skills/transcribe/SKILL.md`가 담당하며, `audio-to-text/`는 플러그인이 아니다.
독립적으로 재사용이 필요하면 별도 플러그인으로 분리할 수 있다.
