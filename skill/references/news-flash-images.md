# News Flash Image Workflow — Codex Image Generation

Workflow for creating background images for the News Flash (信息流快消) visual style with Codex image generation. Generated images should be saved as local project assets and referenced from the HyperFrames composition.

## Core Principles

1. **Generate local assets** — save final images under the run directory, usually `img/`, and reference them with relative paths.
2. **No readable text in images** — headlines, numbers, labels, and captions belong in HTML/CSS so they remain editable and inspectable.
3. **Leave negative space** — generate backgrounds with clean areas for large Chinese headline overlays.
4. **Prefer editorial realism** — use cinematic, high-contrast, news-like imagery for market, technology, finance, social, and policy topics.
5. **Use article images when factual detail matters** — screenshots, charts, UI captures, people, products, and event-specific visuals should come from the article or user-provided assets.

## Workflow

### Step 1: Plan Image Prompts by Scene Theme

Map each scene to an image direction before generating:

| Scene content | Prompt direction | Typical image |
|---|---|---|
| Title / Market overview | vertical editorial background, trading screens, dark cinematic finance desk | Digital charts, newsroom-like finance mood |
| Tech / AI | abstract artificial intelligence network, glowing chips, dark premium lighting | Circuits, data streams, model infrastructure |
| Semiconductor | macro semiconductor wafer, circuit board close-up, dramatic side light | Chips, wafers, clean-room mood |
| Energy / Battery | electric vehicle battery systems, charging infrastructure, industrial lighting | EVs, batteries, charging scenes |
| Mining / Minerals | mineral textures, industrial extraction, dramatic earth tones | Rocks, mine-like terrain, raw materials |
| Solar / Renewable | solar panels, grid infrastructure, bright but contrast-safe lighting | Solar farms, power networks |
| Financial data | abstract business chart environment, data wall, analyst desk | Charts, dashboards, market signals |
| Celebration / Closing | cinematic city lights, confetti-like particles, optimistic glow | Closing atmosphere |
| Risk / Warning | red market screens, warning signal, tense financial atmosphere | Volatility, alert state |

### Step 2: Generate and Save Assets

For each scene that needs a generated visual, produce a prompt like:

```text
Create a 1080x1920 vertical editorial background image for a Chinese short video.
Scene title: <scene title>.
Key point: <one concrete idea>.
Visual direction: <scene-specific direction>.
No readable text, no logos, no watermark.
Leave clean negative space for large Chinese headline overlays.
High contrast, cinematic lighting, urgent News Flash mood.
```

Save outputs with stable scene names:

```text
img/
  s01.png
  s02.png
  s03.png
```

When using the `wechat-video` template, write generated asset metadata back into `scene-plan.json`:

```json
{
  "id": "s01",
  "type": "cinema-title",
  "image_prompt": "1080x1920 vertical editorial finance background, no text, no logos...",
  "image": "img/s01.png"
}
```

### Step 3: Select and Assign Images

Choose generated images that:

1. **Match the scene theme** — financial data should feel like finance, not generic technology.
2. **Have dark or muted regions** — large text needs readable areas.
3. **Avoid fake charts with readable pseudo-text** — generated chart markings should be abstract or blurred.
4. **Vary across scenes** — avoid adjacent scenes with the same composition.
5. **Do not imply false factual evidence** — generated images are mood visuals, not proof.

### Step 4: Reference Images in CSS

Use local files as `background-image` on a full-bleed positioned div:

```css
.bg-img{position:absolute;top:0;left:0;width:100%;height:100%;
  background-size:cover;background-position:center;z-index:0}
#scene5 .bg-img{background-image:url('../img/s05.png')}
```

For `<img>` tags that load local generated assets, `crossorigin` is not required.

### Step 5: Add Overlay for Text Readability

Dark overlay on top of the image, below the content:

```html
<div class="bg-img"></div>
<div class="overlay ov-heavy"></div>
<div class="sc">...</div>
```

Overlay darkness guide:

- **55-65%** (`rgba(0,0,0,0.55-0.65)`) — for generated backgrounds with clear contrast.
- **65-75%** (`rgba(0,0,0,0.65-0.75)`) — for dense data scenes or bright images.
- **Gradient** — for title scenes where the image should remain visible around the subject.

## CSS Architecture

```css
/* Base layers */
.scene{position:absolute;top:0;left:0;width:1080px;height:1920px;overflow:hidden}
.bg-img{position:absolute;top:0;left:0;width:100%;height:100%;background-size:cover;background-position:center;z-index:0}
.overlay{position:absolute;top:0;left:0;width:100%;height:100%;z-index:1}
.ov-heavy{background:rgba(0,0,0,0.72)}
.ov-med{background:rgba(0,0,0,0.6)}
.ov-light{background:linear-gradient(180deg,rgba(0,0,0,0.5) 0%,rgba(0,0,0,0.8) 100%)}
.ov-grad-r{background:linear-gradient(135deg,rgba(0,0,0,0.3) 0%,rgba(0,0,0,0.85) 100%)}
.sc{position:relative;z-index:2;display:flex;flex-direction:column;width:100%;height:100%}
```

## Three-Segment Layout Pattern

The signature News Flash scene structure stacks three zones vertically:

```html
<div class="sc">
  <div class="scene-head" style="background:#DC2626">
    <div class="head-title" style="font-size:48px;font-weight:900">BREAKING HEADLINE</div>
  </div>

  <div class="scene-mid" style="background:#F59E0B">
    <span class="pill" style="background:rgba(0,0,0,0.85);padding:12px 24px">Tag 1</span>
    <span class="pill" style="background:rgba(0,0,0,0.85);padding:12px 24px">Tag 2</span>
  </div>

  <div class="scene-body" style="flex:1;background:rgba(0,0,0,0.55)">
    <div class="data-card">...</div>
  </div>
</div>
```

**Sizing caution:** The three segments must fit within the scene height (1920px portrait). If content overflows:

- Reduce padding (40px → 32px on banners).
- Reduce font sizes slightly (74px → 68px on titles).
- Use `flex:1` on the body section so it absorbs remaining space.
- Mark with `data-layout-allow-overflow` or `data-layout-ignore` only when overflow is intentional.

## Inspect Overflow Handling

The `hyperframes inspect` tool measures all scenes in the DOM, including hidden ones (`opacity:0`). For scenes that are intentionally packed tight with `overflow:hidden`:

- `data-layout-allow-overflow` — marks overflow as intentional on the element.
- `data-layout-ignore` — skips the element entirely from inspection. Use on decorative elements and hidden scenes only when the issue is not visible in the rendered moment.
