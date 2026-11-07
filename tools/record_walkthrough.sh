#!/usr/bin/env bash
# Run under xvfb-run on a disposable Linux CI runner, never on the Pi by default.
set -euo pipefail
: "${DISPLAY:?Run under xvfb-run with a 1280x800 display}"
: "${NIGHTMAN_BUILD:?Select the frozen ordinary build}"
record_dir="${NIGHTMAN_RECORD_DIR:-build/walkthrough}"
mkdir -p "$record_dir"
pulseaudio --start --exit-idle-time=-1
sink_module=$(pactl load-module module-null-sink sink_name=nightman_record sink_properties=device.description=NightmanRecording)
export PULSE_SINK=nightman_record
recorder_pid=''
cleanup() {
  if [[ -n "$recorder_pid" ]]; then
    kill -INT "$recorder_pid" 2>/dev/null || true
    wait "$recorder_pid" || true
  fi
  pactl unload-module "$sink_module" || true
}
trap cleanup EXIT INT TERM
ffmpeg -nostdin -y -thread_queue_size 512 -f x11grab -video_size 1280x800 -framerate 30 -i "$DISPLAY" \
  -thread_queue_size 512 -f pulse -i nightman_record.monitor \
  -c:v libx264 -preset veryfast -crf 27 -maxrate 900k -bufsize 1800k -pix_fmt yuv420p \
  -c:a aac -b:a 96k -movflags +faststart "$record_dir/full-walkthrough.mp4" \
  >"$record_dir/ffmpeg.log" 2>&1 &
recorder_pid=$!
export NIGHTMAN_RECORD=1
npx playwright test --project=chromium --grep 'full three-act keyboard journey and ending' --workers=1
kill -INT "$recorder_pid"
if wait "$recorder_pid"; then
  :
else
  recorder_status=$?
  # FFmpeg reports an orderly SIGINT stop as 255 on some runner builds.
  [[ "$recorder_status" -eq 255 ]] || exit "$recorder_status"
fi
recorder_pid=''
ffprobe -v error -show_streams -show_format -of json "$record_dir/full-walkthrough.mp4" > "$record_dir/media.json"
python3 - "$record_dir" <<'PY'
import hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[1]);info=json.loads((root/'media.json').read_text())
assert {'video','audio'} <= {s['codec_type'] for s in info['streams']}, 'Recording needs video and game audio'
assert float(info['format']['duration'])>60, 'Recording is unexpectedly short'
video=root/'full-walkthrough.mp4'
(root/'sha256.txt').write_text(hashlib.sha256(video.read_bytes()).hexdigest()+'  '+video.name+'\n')
PY
