#!/usr/bin/env bash
# fetch-or-transcribe.sh: one transcript entry point, two stages, one contract.
#
# Stage 1: captions through the YouTube caption API (fetch_transcript.py).
# Stage 2 (only when stage 1 finds no captions): download the audio and
# transcribe it with a local Whisper CLI, then convert its JSON into the
# same output contract as stage 1:
#   {"video_id": ..., "segment_count": N, "duration": "M:SS",
#    "full_text": ..., "timestamped_text": ... (with --timestamps)}
# and the same --text-only / --timestamps / --language flags.
#
# Usage: fetch-or-transcribe.sh URL [--language en,tr] [--timestamps] [--text-only]
# Exit codes: 0 success, 1 a stage failed with no fallback left, 2 usage error.
set -u

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
URL=""
LANG=""
TIMESTAMPS=0
TEXT_ONLY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --language|-l) LANG="${2:-}"; shift 2 ;;
    --timestamps|-t) TIMESTAMPS=1; shift ;;
    --text-only) TEXT_ONLY=1; shift ;;
    -*) echo "fetch-or-transcribe: unknown option: $1" >&2; exit 2 ;;
    *) if [ -z "$URL" ]; then URL="$1"; else echo "fetch-or-transcribe: unexpected extra argument: $1" >&2; exit 2; fi; shift ;;
  esac
done
if [ -z "$URL" ]; then
  echo "fetch-or-transcribe: usage: fetch-or-transcribe.sh URL [--language en,tr] [--timestamps] [--text-only]" >&2
  exit 2
fi

PY="$(command -v python3 || true)"
if [ -z "$PY" ]; then
  echo "fetch-or-transcribe: python3 not found on PATH" >&2
  exit 1
fi

# Stage 1: captions.
FETCH_ARGS=("$URL")
[ -n "$LANG" ] && FETCH_ARGS+=(--language "$LANG")
[ "$TIMESTAMPS" -eq 1 ] && FETCH_ARGS+=(--timestamps)
[ "$TEXT_ONLY" -eq 1 ] && FETCH_ARGS+=(--text-only)
if "$PY" "$SCRIPT_DIR/fetch_transcript.py" "${FETCH_ARGS[@]}" 2>/tmp/fetch-or-transcribe-stage1.err; then
  exit 0
fi
echo "fetch-or-transcribe: no captions via the caption API; falling back to audio plus Whisper" >&2

# Stage 2: audio plus Whisper. Both tools are optional bindings; when one is
# missing the script says which one and stops, it does not install anything.
if ! command -v yt-dlp >/dev/null 2>&1; then
  echo "fetch-or-transcribe: fallback unavailable: yt-dlp not found on PATH (stage 1 error: $(cat /tmp/fetch-or-transcribe-stage1.err 2>/dev/null))" >&2
  exit 1
fi
WHISPER="$(command -v whisper || command -v faster-whisper || true)"
if [ -z "$WHISPER" ]; then
  echo "fetch-or-transcribe: fallback unavailable: no Whisper CLI (whisper or faster-whisper) found on PATH" >&2
  exit 1
fi

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
if ! yt-dlp -x --audio-format mp3 -o "$WORK/audio.%(ext)s" "$URL" >/dev/null 2>&1; then
  echo "fetch-or-transcribe: yt-dlp could not download audio for $URL" >&2
  exit 1
fi
AUDIO="$(ls "$WORK"/audio.* 2>/dev/null | head -n 1)"
if [ -z "$AUDIO" ]; then
  echo "fetch-or-transcribe: audio download produced no file" >&2
  exit 1
fi
WLANG="${LANG%%,*}"
WARGS=("$AUDIO" --output_format json --output_dir "$WORK")
[ -n "$WLANG" ] && WARGS+=(--language "$WLANG")
if ! "$WHISPER" "${WARGS[@]}" >/dev/null 2>&1; then
  echo "fetch-or-transcribe: Whisper transcription failed for $URL" >&2
  exit 1
fi
WJSON="$(ls "$WORK"/*.json 2>/dev/null | head -n 1)"
if [ -z "$WJSON" ]; then
  echo "fetch-or-transcribe: Whisper produced no JSON output" >&2
  exit 1
fi

# Convert Whisper JSON segments [{start, end, text}] into the stage 1 contract.
"$PY" - "$WJSON" "$URL" "$TIMESTAMPS" "$TEXT_ONLY" <<'PYEOF'
import json, re, sys

wjson_path, url, timestamps, text_only = sys.argv[1], sys.argv[2], sys.argv[3] == "1", sys.argv[4] == "1"
with open(wjson_path, encoding="utf-8") as fh:
    data = json.load(fh)
segments = [
    {"text": seg.get("text", "").strip(), "start": float(seg.get("start", 0)),
     "duration": float(seg.get("end", 0)) - float(seg.get("start", 0))}
    for seg in data.get("segments", [])
]
match = re.search(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([A-Za-z0-9_-]{11})", url)
video_id = match.group(1) if match else url

def fmt(seconds):
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

full_text = " ".join(seg["text"] for seg in segments)
stamped = "\n".join(f"{fmt(seg['start'])} {seg['text']}" for seg in segments)
if text_only:
    print(stamped if timestamps else full_text)
else:
    out = {"video_id": video_id, "segment_count": len(segments),
           "duration": fmt(segments[-1]["start"] + segments[-1]["duration"]) if segments else "0:00",
           "source": "audio+whisper", "full_text": full_text}
    if timestamps:
        out["timestamped_text"] = stamped
    print(json.dumps(out, ensure_ascii=False, indent=2))
PYEOF
