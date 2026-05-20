# Repository Guidelines

## Project Structure & Module Organization

This repository packages a HyperFrames skill and supporting documentation. The root contains project-level docs such as `README.md`, `CHANGELOG.md`, and this guide. The skill entry point is `skill/SKILL.md`; keep core rules and workflow instructions there. Extended, task-specific guidance belongs in `skill/references/`, for example `wechat-article-video.md`, `tts-workflow.md`, `external-tts.md`, and `news-flash-images.md`.

There is no application source tree, bundled asset directory, or committed test suite in this checkout. If you add examples, keep generated media and temporary render outputs out of the repo unless they are intentionally small reference artifacts.

## Build, Test, and Development Commands

This repo has no local build command. For Markdown-only changes, review the rendered Markdown and check links manually.

When validating a HyperFrames composition created from this skill, run the commands in that composition project, not necessarily from this repository:

```bash
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect --timeout 30000
```

Use `lint` for structural timing issues, `validate` for render and contrast checks, and `inspect` for layout overflow. On Windows, prefer the explicit `--timeout 30000` shown above.

## Coding Style & Naming Conventions

Write contributor-facing guidance in concise Markdown with descriptive headings and actionable bullets. Use fenced code blocks for commands and short examples. Keep file names in `skill/references/` lowercase kebab-case, such as `wechat-article-video.md`. Preserve existing front matter in `skill/SKILL.md`, especially `name` and `description`.

For HyperFrames examples, follow the repository's conventions: HTML is the source of truth, timelines are registered in `window.__timelines`, root compositions include explicit `data-duration`, and media clips use `data-track-index`.

## Testing Guidelines

No automated tests are currently defined for this repository. Validate documentation changes by reading the affected workflow end to end and checking relative links. For any added composition example, include enough command output or notes to show `npx hyperframes lint` and `npx hyperframes validate` were run.

## Commit & Pull Request Guidelines

Recent history uses short commit messages such as `fix` plus focused README updates. Prefer clearer imperative messages going forward, for example `docs: clarify TTS workflow` or `fix: update WeChat image guidance`.

Pull requests should summarize the changed workflow, list affected files, and call out validation performed. Include screenshots or rendered video links when changing visual composition guidance.
