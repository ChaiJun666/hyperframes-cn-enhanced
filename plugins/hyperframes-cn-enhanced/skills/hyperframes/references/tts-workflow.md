# TTS → HTML Workflow

End-to-end workflow for producing a voiceover video: script splitting, edge-tts audio generation, measured timeline calculation, composition wiring, and validation.

## Overview

```
Script (.md)
    ↓  1. Split into scenes
Narration segments
    ↓  2. Generate edge-tts audio
Audio files (mp3)
    ↓  3. Measure & build timeline
timeline.json
    ↓  4. Build HTML composition
index.html + audio files
    ↓  5. Lint & Inspect
0 errors
    ↓  6. Render
output.mp4 (video + audio)
```

## Step 1: Script → Scene Narration

Read the source script and split it into one narration segment per scene.

Rules:

- Every scene gets narration, including title and closing, unless silence is intentional.
- Keep segment text concise. Prefer one strong sentence for quick scenes and two for data-heavy scenes.
- Scene duration is typically 6-15 seconds.
- Do not estimate final timing from character count. edge-tts voice, rate, and punctuation all affect duration.

Output a list of `(label, text)` pairs, one per scene.

## Step 2: Generate Audio

Install and inspect voices:

```bash
pip install edge-tts
edge-tts --list-voices
```

Single segment example:

```bash
edge-tts --voice zh-CN-XiaoxiaoNeural --rate=+20% \
  --text "这里是第一段旁白。" \
  --write-media audio/project/s01.mp3 \
  --write-subtitles audio/project/s01.srt
```

Batch generation example:

```python
import asyncio
import json
import os
import subprocess
import edge_tts

AUDIO_DIR = "audio/project"
VOICE = os.getenv("EDGE_TTS_VOICE", "zh-CN-XiaoxiaoNeural")
RATE = os.getenv("EDGE_TTS_RATE", "+20%")
VOLUME = os.getenv("EDGE_TTS_VOLUME", "+0%")
PITCH = os.getenv("EDGE_TTS_PITCH", "+0Hz")

narrations = [
    ("S01", "Scene 1 narration text here..."),
    ("S02", "Scene 2 narration text here..."),
]

os.makedirs(AUDIO_DIR, exist_ok=True)

def measure_audio(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True
    )
    return float(r.stdout.strip())

async def generate_all():
    results = []
    for label, text in narrations:
        filename = f"pd_{label.lower()}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        tts = edge_tts.Communicate(text, VOICE, rate=RATE, volume=VOLUME, pitch=PITCH)
        await tts.save(filepath)
        actual_dur = measure_audio(filepath)
        results.append({"label": label, "filename": filename, "audio_dur": actual_dur})
        print(f"{label}: {actual_dur:.2f}s")
    return results

results = asyncio.run(generate_all())
```

## Step 3: Build Timeline

Calculate scene timing from actual audio durations:

```python
BUFFER = 0.35
MIN_SCENE = 4.5
current_time = 0.0
scenes = []

for item in results:
    scene_dur = max(item["audio_dur"] + BUFFER, MIN_SCENE)
    scenes.append({
        "label": item["label"],
        "filename": item["filename"],
        "start": round(current_time, 2),
        "duration": round(scene_dur, 2),
        "audio_dur": round(item["audio_dur"], 2),
    })
    current_time += scene_dur

total = round(current_time, 2)
print(f"Total: {total:.2f}s ({total/60:.1f}min)")

for i in range(len(scenes) - 1):
    end = scenes[i]["start"] + scenes[i]["duration"]
    if end > scenes[i + 1]["start"]:
        scenes[i]["duration"] = round(scenes[i + 1]["start"] - scenes[i]["start"] - 0.01, 2)

with open(f"{AUDIO_DIR}/timeline.json", "w", encoding="utf-8") as f:
    json.dump(scenes, f, ensure_ascii=False, indent=2)
```

Key formula:

```python
scene_duration = max(audio_duration + 0.35, 4.5)
```

Never trim generated audio to fit a scene. Extend the scene or shorten text and regenerate. For fast short-video pacing, keep the post-audio buffer short; long buffers create audible gaps between narration segments.

## Step 4: Wire Audio Into Composition

Each audio file becomes an `<audio>` element in `<body>`, outside the composition div:

```html
<body>
  <div data-composition-id="main" data-width="1080" data-height="1920"
       data-start="0" data-duration="189">
    <div id="scene1" class="scene">...</div>
    <div id="scene2" class="scene" style="opacity:0">...</div>
  </div>

  <audio id="narr-s01" data-start="0" data-duration="8.4" data-track-index="2"
         src="audio/project/pd_s01.mp3" data-volume="1"></audio>
  <audio id="narr-s02" data-start="8.4" data-duration="14.7" data-track-index="2"
         src="audio/project/pd_s02.mp3" data-volume="1"></audio>
</body>
```

Critical attributes:

- `data-start` — must match scene start time exactly.
- `data-duration` — explicit seconds, never `"auto"`; for narration clips, use the measured audio duration plus a tiny safety margin, not the full scene hold.
- `data-track-index="2"` — all narration on the same track.
- `src` — path relative to the HTML file.

No overlaps: `data-start + data-duration <= next clip's data-start`. If lint reports `overlapping_clips_same_track`, round the earlier `data-duration` down by 0.01-0.1s.

## Step 5: Lint & Inspect

```bash
npx hyperframes lint
npx hyperframes inspect --at 2,10,45,100 --no-contrast --timeout 30000
```

Common lint fixes:

- `overlapping_clips_same_track` → reduce the earlier `data-duration`.
- `composition_file_too_large` → warning only, acceptable for single-file compositions.

## Step 6: Render & Verify

```bash
npx hyperframes render
ffprobe renders/output.mp4
```

The final MP4 must show both video and audio streams.

## Troubleshooting

| Problem | Cause | Fix |
|:---|:---|:---|
| Rendered video has no audio | `<audio>` inside composition div, or `data-duration="auto"` | Move outside div, use explicit seconds |
| Audio does not match scenes | Single continuous file | Split into per-scene segments |
| `overlapping_clips_same_track` | Audio durations overlap on same track | Round down `data-duration`, verify timeline alignment |
| Narration cut off mid-sentence | Audio trimmed, or text too long | Use full file and extend scene, or shorten text and regenerate |
| Scenes feel slow or narration has gaps | Buffer too long or too many words per scene | Use a short buffer such as 0.35s, reduce text, and regenerate |

## Related References

- `external-tts.md` — edge-tts setup, voice generation, timing, and composition wiring
- `narration.md` — Script writing: pacing, tone, structure, opening lines
- `tts.md` — Built-in local TTS (Kokoro-82M)
- `news-flash-images.md` — generated background image workflow for News Flash style
