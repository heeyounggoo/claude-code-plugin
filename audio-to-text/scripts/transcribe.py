#!/usr/bin/env python3
"""
audio-to-text 변환 스크립트
WhisperX 기반 한국어 음성 → Markdown 변환 (화자 구분 포함)

사용법:
    python transcribe.py <audio_file> [options]

옵션:
    --timestamps        타임스탬프 포함 출력
    --speakers N        화자 수 힌트 (기본: 자동 감지)
    --device cpu/cuda   실행 디바이스 (기본: auto)
    --model MODEL       Whisper 모델 크기 (기본: large-v3)
    --output DIR        출력 디렉토리 (기본: ../output/)
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path


def check_dependencies():
    """필수 패키지 설치 여부 확인"""
    try:
        import whisperx
    except ImportError:
        print("ERROR: whisperx가 설치되지 않았습니다.")
        print("설치: pip install whisperx")
        sys.exit(1)

    hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if not hf_token:
        print("ERROR: HF_TOKEN 환경변수가 설정되지 않았습니다.")
        print("HuggingFace 토큰 발급: https://huggingface.co/settings/tokens")
        print("설정: export HF_TOKEN='your_token_here'")
        sys.exit(1)

    return hf_token


def format_timestamp(seconds: float) -> str:
    """초를 HH:MM:SS 형식으로 변환"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def transcribe(audio_path: str, model_name: str, device: str, hf_token: str, num_speakers: int = None):
    """WhisperX로 음성 파일 변환 + 화자 구분"""
    import whisperx
    import torch

    # 디바이스 자동 감지
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"

    compute_type = "float16" if device == "cuda" else "int8"
    print(f"디바이스: {device} | 모델: {model_name} | compute_type: {compute_type}")

    # 1. Whisper 모델 로드 & 전사
    print("모델 로딩 중...")
    model = whisperx.load_model(model_name, device, compute_type=compute_type, language="ko")

    print("음성 파일 로딩 중...")
    audio = whisperx.load_audio(audio_path)

    print("전사 중 (시간이 걸릴 수 있습니다)...")
    result = model.transcribe(audio, batch_size=16, language="ko")

    # 2. 단어 정렬 (타임스탬프 정확도 향상)
    print("단어 정렬 중...")
    model_a, metadata = whisperx.load_align_model(language_code="ko", device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device,
                            return_char_alignments=False)

    # 3. 화자 구분 (Diarization)
    print("화자 구분 중...")
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_token, device=device)

    diarize_kwargs = {}
    if num_speakers:
        diarize_kwargs["num_speakers"] = num_speakers

    diarize_segments = diarize_model(audio, **diarize_kwargs)
    result = whisperx.assign_word_speakers(diarize_segments, result)

    return result


def build_markdown(result: dict, audio_path: str, model_name: str, include_timestamps: bool) -> str:
    """변환 결과를 Markdown 형식으로 변환"""
    filename = Path(audio_path).name
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# 음성 변환: {filename}",
        f"변환일시: {now}",
        f"모델: whisperx {model_name} | 언어: 한국어",
        "",
        "---",
        "",
    ]

    current_speaker = None

    for segment in result.get("segments", []):
        speaker = segment.get("speaker", "Unknown")
        text = segment.get("text", "").strip()
        start = segment.get("start", 0)

        if not text:
            continue

        # 화자가 바뀔 때 헤더 출력
        if speaker != current_speaker:
            if current_speaker is not None:
                lines.append("")
            if include_timestamps:
                lines.append(f"**[{speaker}]** `{format_timestamp(start)}`")
            else:
                lines.append(f"**[{speaker}]**")
            current_speaker = speaker

        lines.append(text)

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="음성 파일 → Markdown 변환 (화자 구분 포함)")
    parser.add_argument("audio", help="입력 음성 파일 경로")
    parser.add_argument("--timestamps", action="store_true", help="타임스탬프 포함")
    parser.add_argument("--speakers", type=int, default=None, help="화자 수 힌트")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"], help="실행 디바이스")
    parser.add_argument("--model", default="large-v3", help="Whisper 모델 크기")
    parser.add_argument("--output", default=None, help="출력 디렉토리")
    args = parser.parse_args()

    # 의존성 확인
    hf_token = check_dependencies()

    # 파일 존재 확인
    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"ERROR: 파일을 찾을 수 없습니다: {audio_path}")
        sys.exit(1)

    # 출력 디렉토리 설정
    if args.output:
        output_dir = Path(args.output)
    else:
        # 스크립트 위치 기준 ../output/
        output_dir = Path(__file__).parent.parent / "output"

    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / (audio_path.stem + ".md")
    print(f"\n입력: {audio_path}")
    print(f"출력: {output_path}")
    print(f"타임스탬프: {'포함' if args.timestamps else '미포함'}")
    print(f"화자 수 힌트: {args.speakers or '자동'}")
    print()

    # 변환 실행
    result = transcribe(
        str(audio_path),
        model_name=args.model,
        device=args.device,
        hf_token=hf_token,
        num_speakers=args.speakers,
    )

    # Markdown 생성
    markdown = build_markdown(result, str(audio_path), args.model, args.timestamps)

    # 파일 저장
    output_path.write_text(markdown, encoding="utf-8")
    print(f"\n완료! 저장 위치: {output_path}")


if __name__ == "__main__":
    main()
