---
name: production-workflow
description: Shared staged workflow for producing HyperFrames videos from source material, including brief, storyboard, asset plan, narration, timeline, composition, optional music plan, and delivery notes.
---

# Production Workflow

Use this staged workflow when source material needs to become a HyperFrames video with clear review points and reproducible outputs. Keep each stage small, reviewable, and tied to files in one run directory.

## Run Directory

Create one run folder per production:

```text
runs/<scenario>-YYYYMMDD-<slug>/
```

Examples:

```text
runs/wechat-article-20260522-ai-policy/
runs/news-flash-20260522-product-launch/
runs/explainer-20260522-cloud-costs/
```

## Stage Artifacts

```text
01-brief.md
02-storyboard.md
03-asset-plan.md
04-narration.md
narration.json
05-timeline.json
06-composition/
07-music-plan.md
08-delivery.md
manifest.json
```

## Stage Responsibilities

### 01-brief.md

Define the source, audience, objective, scenario, duration target, constraints, required claims, and approval criteria. Include links or copied excerpts needed by later stages.

Pause point: confirm the brief before storyboard work.

### 02-storyboard.md

Break the video into scenes with scene IDs, purpose, on-screen content, visual direction, narration intent, timing estimate, and transitions. The storyboard should be detailed enough to plan assets without guessing.

Pause point: confirm scene structure before asset planning.

### 03-asset-plan.md

List required visuals, screenshots, icons, generated images, video clips, charts, fonts, and source attribution. Mark each asset as existing, to capture, to generate, or to create in composition.

Pause point: confirm asset sources and generation needs before narration or composition.

### 04-narration.md and narration.json

Write the human-readable narration script in `04-narration.md`, aligned to storyboard scene IDs. Store machine-readable narration segments in `narration.json` for TTS or downstream tooling.

Example:

```json
{
  "voice": "zh-CN-XiaoxiaoNeural",
  "rate": "+20%",
  "segments": [
    {
      "scene_id": "scene-01",
      "filename": "scene-01.mp3",
      "text": "A concise narration sentence for this scene."
    }
  ]
}
```

### 05-timeline.json

Convert storyboard, narration duration, and asset timing into a structured timeline. Include scene IDs, start/end timing, media references, track indexes, captions, transitions, and any timing assumptions.

### 06-composition/

Build the HyperFrames composition files. HTML remains the source of truth; register timelines in `window.__timelines`, set explicit `data-duration`, and use `data-track-index` for media clips.

### 07-music-plan.md

Use only when background music or audio beds are needed. Specify mood, reference style, source/license, timing, ducking rules, and where music should enter or exit.

Pause point: confirm music plan when applicable before final audio mix or render.

### 08-delivery.md

Record final render settings, validation results, known limitations, exported file names, captions/subtitles, thumbnail notes, and handoff instructions.

Pause point: confirm final render and validation before delivery.

### manifest.json

Track the run metadata: scenario, slug, source links, artifact paths, generated media paths, render outputs, validation status, and reviewer decisions.

## Validation

Run validation from the composition project directory:

```bash
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect --timeout 30000
```

Use `lint` for structural and timing issues, `validate` for render/contrast checks, and `inspect` for layout overflow.

## Quality Checklist

- Brief states audience, goal, constraints, and acceptance criteria.
- Storyboard uses stable scene IDs and covers the full target duration.
- Asset plan names every required visual/audio source and license concern.
- Narration matches scene IDs and has both readable Markdown and JSON segments.
- Timeline references real assets and has explicit timing for each scene.
- Composition has explicit duration, registered timelines, and correct media tracks.
- Music plan exists when music is used and includes source/license notes.
- Delivery notes include validation results, render output paths, and handoff details.
- Manifest points to all stage artifacts and reflects final approval state.
