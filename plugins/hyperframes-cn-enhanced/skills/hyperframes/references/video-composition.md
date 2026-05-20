# Video Composition

Rules for making HyperFrames output feel like designed video rather than a web page.

## Core Rules

- Treat `design.md` as brand input, not layout instruction. Use its colors and type, but compose for the video frame.
- Prefer large, sparse, readable frames. A viewer should understand the primary message in one glance.
- Build the hero frame first: final positions, full visibility, no overlap, then add motion.
- Use strong foreground/background separation. When using photos, add an overlay but keep the image visible.
- Keep text away from the canvas edge. In portrait, use at least `80px` top/bottom and `48px` left/right padding.

## Portrait Mode (1080x1920)

Vertical short videos need taller rhythm and bigger text than horizontal compositions.

| Element | Recommended range |
| --- | --- |
| Hero headline | 72-128px |
| Secondary text | 34-56px |
| Data labels | 28-42px |
| Content padding | 80px vertical, 48px horizontal minimum |
| Scene count | 10-12 scenes for dense short videos |

Use vertical flex layouts instead of wide horizontal grids. Push transitions should usually move on the `y` axis. For generated background images, prefer portrait-oriented 1080x1920 assets when possible.

## Dense Data Scenes

- Use one dominant number or claim per scene.
- Put supporting details into short rows, not paragraphs.
- If text overflows, shorten copy first. Only then reduce type size.
- For photo backgrounds, use semi-transparent cards or text stroke on critical numbers.
