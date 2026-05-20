# External TTS Integration

Add TTS voiceover to a HyperFrames video. The default provider is `edge-tts`, which generates Microsoft Edge online TTS voices without a TTS API key. The workflow still supports other providers, but do not require provider keys unless the user explicitly asks for one.

## Core Principles

1. **Per-scene audio** — one audio file per narrated scene, each with its own `<audio>` element. Never use a single continuous file.
2. **Every scene narrated** — all scenes including the title card should have voiceover unless silence is intentional.
3. **Measure before timing** — generate audio first, measure each file with `ffprobe`, then calculate scene duration.
4. **Explicit `data-duration`** — always use seconds, never `"auto"`.
5. **Audio outside composition div** — `<audio>` elements are top-level clips in `<body>`.

## Setup

Install `edge-tts` in the composition project or active Python environment:

```bash
pip install edge-tts
edge-tts --list-voices
```

No TTS key is required in `.env`. Keep `.env` for voice and template settings:

```env
EDGE_TTS_VOICE=zh-CN-XiaoxiaoNeural
EDGE_TTS_RATE=+20%
EDGE_TTS_VOLUME=+0%
EDGE_TTS_PITCH=+0Hz
```

The `EDGE_TTS_*` values are optional defaults for scripts. If absent, use `zh-CN-XiaoxiaoNeural`, `+20%`, `+0%`, and `+0Hz`. A `.env` file is only read if the build script loads it; otherwise set these values as environment variables.

## Step 1: Map Narration to Scenes

For each scene, define:

- `label`, such as `S01`
- narration text
- output filename, such as `s01.mp3`

Keep narration short enough that the final video has room for entrances and transitions. Do not rely on a fixed chars-per-second table for edge-tts; voices and rate settings vary. Use this default rule instead:

```python
scene_duration = max(actual_audio_dur + 0.35, 4.5)
```

The short buffer lets narration finish before the transition without creating obvious silence between scenes. If a segment makes the scene feel slow, shorten the text and regenerate.

## Step 2: Generate Audio Per Scene

CLI example:

```bash
edge-tts --voice zh-CN-XiaoxiaoNeural --rate=+20% \
  --text "这里是第一段旁白。" \
  --write-media audio/s01.mp3 \
  --write-subtitles captions/s01.srt
```

Python example for batch generation:

```python
import asyncio
import os
import subprocess
import edge_tts

AUDIO_DIR = "audio/project"
VOICE = os.getenv("EDGE_TTS_VOICE", "zh-CN-XiaoxiaoNeural")
RATE = os.getenv("EDGE_TTS_RATE", "+20%")
VOLUME = os.getenv("EDGE_TTS_VOLUME", "+0%")
PITCH = os.getenv("EDGE_TTS_PITCH", "+0Hz")

segments = [
    ("S01", "s01.mp3", "摆摊三天，亏明白了。深圳清湖市集血泪经验大公开。"),
    ("S02", "s02.mp3", "从来没做过市集，想体验线下真实流量，七个品类去深圳清湖摆摊。"),
]

os.makedirs(AUDIO_DIR, exist_ok=True)

def audio_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True
    )
    return float(r.stdout.strip())

async def main():
    results = []
    for label, filename, text in segments:
        path = os.path.join(AUDIO_DIR, filename)
        communicate = edge_tts.Communicate(text, VOICE, rate=RATE, volume=VOLUME, pitch=PITCH)
        await communicate.save(path)
        dur = audio_duration(path)
        results.append({"label": label, "filename": filename, "audio_dur": dur})
        print(f"{label}: {dur:.2f}s -> {path}")
    return results

results = asyncio.run(main())
```

## Step 3: Build Timeline

Use measured audio durations, not estimated speech speed:

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

for i in range(len(scenes) - 1):
    end = scenes[i]["start"] + scenes[i]["duration"]
    if end > scenes[i + 1]["start"]:
        scenes[i]["duration"] = round(scenes[i + 1]["start"] - scenes[i]["start"] - 0.01, 2)
```

## Step 4: Wire Into Composition

Place audio clips in `<body>`, outside the root composition:

```html
<body>
  <div data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="85">
    <!-- scenes... -->
  </div>

  <audio id="narr-s01" data-start="0" data-duration="8.4" data-track-index="2"
         src="audio/project/s01.mp3" data-volume="1"></audio>
  <audio id="narr-s02" data-start="8.4" data-duration="10.2" data-track-index="2"
         src="audio/project/s02.mp3" data-volume="1"></audio>
</body>
```

Required audio attributes:

| Attribute | Notes |
|:---|:---|
| `data-start` | Must match the scene start time exactly |
| `data-duration` | Explicit seconds; never `"auto"` |
| `data-track-index` | Use `"2"` for narration |
| `src` | Path relative to the HTML file |
| `id` | Unique per clip |

## Step 5: Verify

```bash
npx hyperframes lint
npx hyperframes render
ffprobe renders/output.mp4
```

The rendered MP4 must contain both video and audio streams.

## Troubleshooting

| Symptom | Cause | Fix |
|:---|:---|:---|
| No audio in rendered video | `<audio>` inside composition div, or `data-duration="auto"` | Move audio outside composition div and use explicit duration |
| Narration overlaps | Adjacent clips overlap on `data-track-index="2"` | Recompute starts/durations from measured audio and round down by 0.01s |
| Speech is cut off | Audio was trimmed to fit a scene | Use the full generated file and extend the scene |
| Scene feels slow | Narration text is too long | Shorten text and regenerate |
| Voice sounds wrong | Default voice was used | Run `edge-tts --list-voices` and set `EDGE_TTS_VOICE` |
