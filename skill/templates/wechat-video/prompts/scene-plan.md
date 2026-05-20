# Scene Plan Prompt

Read `article.md` and produce strict JSON only. No prose outside JSON.

Return:

```json
{
  "title": "short video title",
  "slug": "short-lowercase-slug",
  "format": "portrait",
  "scenes": [
    {
      "id": "s01",
      "type": "cinema-title",
      "title": "scene title",
      "visual_source": "generated image or article image or generated layout",
      "key_points": ["one concrete point"],
      "narration_intent": "what the voiceover should explain"
    }
  ]
}
```

Rules:

- Use 10-14 scenes for a typical article.
- Mix at least four scene types: `cinema-title`, `showcase`, `infographic-grid`, `comparison-bars`, `kinetic-quote`.
- Do not repeat the same scene type more than twice in a row.
- Preserve article screenshots with `object-fit: contain`.
- Extract statistics into infographic or comparison scenes.
