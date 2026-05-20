# Prompt Expansion

Turn a vague video request into a stable composition brief before writing HTML.

## Output

For non-trivial compositions, produce a compact brief with:

- Audience and platform.
- Visual identity source: `design.md`, named style, or explicit user direction.
- Narrative arc: hook, evidence, turn, takeaway.
- Scene list with purpose and duration intent.
- Audio plan: narration, captions, music, silence.
- Validation plan: lint, inspect timestamps, render target.

## Rules

- Expand intent, not scope. Do not add scenes or features the user did not ask for unless they clearly improve the video.
- Use the user's source material as the authority for facts.
- For Chinese short videos, prefer concise scene narration and measured audio durations.
- For WeChat article URLs, route to `references/wechat-article-video.md` and the `templates/wechat-video/` scaffold when available.

