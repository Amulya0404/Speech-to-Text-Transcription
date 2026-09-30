#!/usr/bin/env python3
"""
Simple speech-to-text tool.

Converts an audio recording into text using the SpeechRecognition library
and Google's free Web Speech API (internet connection required).

Usage:
    python transcribe.py recording.wav
    python transcribe.py meeting.mp3 -o transcript.txt
    python transcribe.py interview.wav --language es-ES --chunk 30

Native formats: WAV, AIFF, FLAC
Other formats (MP3, M4A, OGG...): install pydub + ffmpeg (see README notes below).
"""

import argparse
import os
import sys
import tempfile

import speech_recognition as sr

NATIVE_FORMATS = {".wav", ".aiff", ".aif", ".flac"}


def convert_to_wav(path: str) -> str:
    """Convert MP3/M4A/OGG/etc. to a temporary WAV file using pydub."""
    try:
        from pydub import AudioSegment
    except ImportError:
        sys.exit(
            "This file format needs pydub and ffmpeg.\n"
            "  pip install pydub\n"
            "  and install ffmpeg (https://ffmpeg.org/download.html)"
        )
    audio = AudioSegment.from_file(path)
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    audio.export(tmp.name, format="wav")
    return tmp.name


def transcribe(path: str, language: str = "en-US", chunk_seconds: int = 30) -> str:
    """Transcribe an audio file, processing it in chunks to stay within API limits."""
    recognizer = sr.Recognizer()
    temp_file = None

    ext = os.path.splitext(path)[1].lower()
    if ext not in NATIVE_FORMATS:
        temp_file = convert_to_wav(path)
        path = temp_file

    parts = []
    try:
        with sr.AudioFile(path) as source:
            total = source.DURATION
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            source.stream.seek(0)  # rewind after noise calibration

            offset = 0.0
            while offset < total:
                audio = recognizer.record(source, duration=chunk_seconds)
                try:
                    text = recognizer.recognize_google(audio, language=language)
                    parts.append(text)
                    print(f"[{offset:6.1f}s] {text}")
                except sr.UnknownValueError:
                    print(f"[{offset:6.1f}s] (unintelligible or silent)")
                except sr.RequestError as e:
                    sys.exit(f"API request failed: {e}")
                offset += chunk_seconds
    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)

    return " ".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Convert audio recordings to text.")
    parser.add_argument("audio", help="Path to the audio file")
    parser.add_argument("-o", "--output", help="Save transcript to this text file")
    parser.add_argument("-l", "--language", default="en-US",
                        help="Language code, e.g. en-US, es-ES, fr-FR (default: en-US)")
    parser.add_argument("-c", "--chunk", type=int, default=30,
                        help="Chunk length in seconds (default: 30)")
    args = parser.parse_args()

    if not os.path.isfile(args.audio):
        sys.exit(f"File not found: {args.audio}")

    transcript = transcribe(args.audio, args.language, args.chunk)

    print("\n=== Full transcript ===")
    print(transcript or "(no speech detected)")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
