# Narration Prompt

Read `scene-plan.json` and produce strict JSON only. No prose outside JSON.

Return:

```json
{
  "voice": "zh-CN-XiaoxiaoNeural",
  "rate": "+20%",
  "segments": [
    {
      "scene_id": "s01",
      "filename": "s01.mp3",
      "text": "短视频旁白，一到两句话。"
    }
  ]
}
```

Rules:

- One narration segment per scene.
- Keep text concise.
- Do not calculate final duration from character count.
- After generating audio, measure each file with ffprobe before writing `timeline.json`.
- Avoid long enumerations and nested clauses.
