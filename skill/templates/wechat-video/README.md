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

## Environment Settings

`build.py` reads edge-tts defaults from `.env` files with this override order:

1. Repository root `.env`
2. `templates/wechat-video/.env`
3. Process environment variables

Supported keys are `EDGE_TTS_VOICE`, `EDGE_TTS_RATE`, `EDGE_TTS_VOLUME`, and `EDGE_TTS_PITCH`. Process environment variables always override `.env` values.

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
3. Generate one MP3 per scene with edge-tts.
4. Measure audio with ffprobe before writing timeline.
5. Put `<audio>` clips outside the root composition div.
6. Store current stage and errors in `manifest.json`.

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
- If audio overlaps, rebuild `timeline.json` from measured durations.
- If render has no audio, check audio placement, `data-duration`, and MP4 streams.
