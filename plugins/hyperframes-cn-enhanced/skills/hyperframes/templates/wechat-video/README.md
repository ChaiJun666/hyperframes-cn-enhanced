# WeChat Video Template

Agent-first scaffold for converting a WeChat article or local markdown article into a HyperFrames video with edge-tts narration.

## Inputs

- `--url "https://mp.weixin.qq.com/..."` for a WeChat article URL.
- `--article path/to/article.md` when URL parsing is unavailable or a human has already saved markdown.
- `--scene-plan path/to/scene-plan.json` to use a reviewed Agent-authored scene plan.
- `--narration path/to/narration.json` to use a reviewed Agent-authored narration script.

## Outputs

Each run writes to `runs/wx-YYYYMMDD-<slug>/`:

- `article.md`
- `manifest.json`
- `scene-plan.json`
- `image-prompts.json`
- `narration.json`
- `timeline.json`
- `img/`
- `audio/`
- `video/index.html`
- `video/styles.css`

## Execution

Run the template build script from the repository root:

```bash
python templates/wechat-video/build.py --article templates/wechat-video/examples/article.sample.md --slug sample
python templates/wechat-video/build.py --url "https://mp.weixin.qq.com/..." --slug my-topic
python templates/wechat-video/build.py --article article.md --scene-plan scene-plan.json --narration narration.json --slug my-topic
```

When `--scene-plan` or `--narration` is omitted, `build.py` generates a minimal smoke-test draft from the article. Production Agent runs should provide and review `scene-plan.json` and `narration.json` before building audio and timeline artifacts.

## Image Workflow

`scene-plan.json` supports two image fields per scene:

- `image_prompt` — prompt text for Codex image generation.
- `image` — actual image file path, usually `img/s01.png`.

`build.py` always writes `image-prompts.json` from the scene plan. An Agent can use those prompts with Codex image generation, save the generated files into the run directory's `img/` folder, then set each scene's `image` field before rendering HTML.

Example scene:

```json
{
  "id": "s03",
  "type": "showcase",
  "title": "半导体成最强主线",
  "visual_source": "semiconductor wafer close-up",
  "image_prompt": "1080x1920 cinematic macro photo of semiconductor wafers, dark News Flash lighting, no text, no logo",
  "image": "img/s03.png",
  "key_points": ["华虹公司涨超18%创新高，中芯国际涨超12%。"],
  "narration_intent": "强调半导体龙头带动盘面"
}
```

When `image` exists, the template injects it as a full-bleed background:

```html
<img class="scene-bg-img" src="../img/s03.png" alt="">
```

If `image` is absent, the scene falls back to the built-in abstract gradient background.

## Environment Settings

`build.py` reads edge-tts defaults from `.env` files with this override order:

1. Repository root `.env`
2. `templates/wechat-video/.env`
3. Process environment variables

Supported keys are `EDGE_TTS_VOICE`, `EDGE_TTS_RATE`, `EDGE_TTS_VOLUME`, `EDGE_TTS_PITCH`, `VIDEO_BRAND_TEXT`, `VIDEO_SCENE_AUDIO_BUFFER`, `VIDEO_MIN_SCENE_DURATION`, and `VIDEO_CN_FONT_PATH`. Process environment variables always override `.env` values.

Defaults:

- `VIDEO_BRAND_TEXT=` leaves the top-right brand bar hidden.
- `VIDEO_SCENE_AUDIO_BUFFER=0.35` keeps scenes tight after narration.
- `VIDEO_MIN_SCENE_DURATION=4.5` avoids long silent holds in fast short videos.
- `VIDEO_CN_FONT_PATH=` auto-detects common Windows Chinese fonts under WSL and embeds the font into `video/fonts/`.

## Preflight Checklist

- Confirm the article source exists as either a WeChat URL or local markdown file.
- Choose the run directory slug before generating artifacts.
- Review `.env` settings for edge-tts and template options.
- Confirm edge-tts is available.
- Confirm ffprobe is available.
- Confirm `npx hyperframes` is available.

## Agent Rules

1. Run preflight before generating files.
2. Do not skip `scene-plan.json` or `narration.json`.
3. Use `image-prompts.json` with Codex image generation when article images are missing.
4. Save generated images under `img/` and write `scene.image` before final HTML render.
5. Generate one MP3 per scene with edge-tts.
6. Measure audio with ffprobe before writing timeline.
7. Put `<audio>` clips outside the root composition div.
8. Store current stage and errors in `manifest.json`.

## Validation

Run inside the generated run directory:

```bash
npx hyperframes lint video
npx hyperframes inspect video --timeout 30000
npx hyperframes render video
ffprobe renders/output.mp4
```

## Recovery

- If URL parsing fails, save article text to `article.md` and rerun with `--article`.
- If edge-tts fails, retry only missing audio files.
- If audio feels disconnected, lower `VIDEO_SCENE_AUDIO_BUFFER`; if transitions feel rushed, raise it slightly.
- If audio overlaps, rebuild `timeline.json` from measured durations.
- If render has no audio, check audio placement, `data-duration`, and MP4 streams.
