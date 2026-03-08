---
description: 음성 파일을 Markdown 텍스트로 변환. WhisperX 기반 화자 구분 포함.
allowed-tools:
  - Bash
argument-hint: "<파일 절대경로 or 파일명> [--timestamps] [--speakers N]"
---

## 환경 상태

- WhisperX: !`pip show whisperx 2>/dev/null | grep Version || echo "미설치 — pip install whisperx 필요"`
- HF_TOKEN: !`[ -n "$HF_TOKEN" ] && echo "설정됨 ✓" || echo "미설정 — export HF_TOKEN='...' 필요"`

## 실행

`$ARGUMENTS`에서 파일 경로와 옵션을 파싱한다.

**파일 경로 해석 규칙:**
1. 절대경로(`/`로 시작)면 그대로 사용
2. 파일명만 전달된 경우 `~/Downloads/`에서 탐색
3. 없으면 `~/Downloads/`의 오디오 파일 목록을 보여주고 선택 요청

```bash
python ~/.claude/plugins/claude-code-plugin/audio-to-text/scripts/transcribe.py \
  <파일 경로> \
  [--timestamps] \
  [--speakers N]
```

출력 파일은 입력 파일과 같은 디렉토리에 `<파일명>.md`로 저장된다.

환경 상태에 문제가 있으면 해결 방법을 안내하고 멈춰라.
