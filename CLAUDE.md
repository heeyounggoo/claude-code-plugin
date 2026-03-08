# claude-code-plugin

개인 생산성 Claude Code 플러그인.

## 플러그인 구조

```
claude-code-plugin/
├── .claude-plugin/plugin.json   ← 플러그인 메타데이터
├── .mcp.json                    ← 플러그인 의존 MCP 서버
├── commands/                    ← 사용자 명시 호출 명령 (/wrap, /youtube, /transcribe)
├── skills/                      ← Agent Skills (자동 트리거)
│   └── interview-prep/SKILL.md
└── audio-to-text/               ← 보조 스크립트
```

- `commands/`: side effect가 있어 사용자가 명시적으로 호출해야 하는 명령
- `skills/`: 대화 내용에 따라 Claude가 자동으로 활성화하는 스킬

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

## 명령 개발 가이드

- 새 명령: `commands/<name>.md` 생성
- 새 스킬: `skills/<name>/SKILL.md` 생성 (YAML frontmatter 필수)
- interview-prep 런타임 파일 (resume, tmp, memory)은 `.gitignore`로 제외됨
