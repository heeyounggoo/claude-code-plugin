---
allowed-tools: Bash
description: 음성 파일을 Markdown 텍스트로 변환. WhisperX 기반 화자 구분 포함.
argument-hint: "<파일명> [--timestamps] [--speakers N]"
---

## 환경 상태

- 입력 파일 목록: !`ls audio-to-text/resources/ 2>/dev/null | grep -v '.gitkeep' || echo "(없음)"`
- WhisperX: !`pip show whisperx 2>/dev/null | grep Version || echo "미설치 — pip install whisperx 필요"`
- HF_TOKEN: !`[ -n "$HF_TOKEN" ] && echo "설정됨 ✓" || echo "미설정 — export HF_TOKEN='...' 필요"`

## 실행

`$ARGUMENTS`에서 파일명과 옵션을 파싱하여 아래 명령을 실행하라.

```bash
python audio-to-text/scripts/transcribe.py \
  audio-to-text/resources/<파일명> \
  [--timestamps] \
  [--speakers N]
```

환경 상태에 문제가 있으면 해결 방법을 안내하고 멈춰라.

완료 시 출력 파일 경로를 알려줘라: `audio-to-text/output/<파일명>.md`
