---
name: scenario-matrix
description: Routes common Chinese HyperFrames video requests to the right workflow and scenario reference.
---

# Scenario Matrix

Use this matrix to route common Chinese HyperFrames video requests to the most relevant workflow and scenario reference.

| Scenario | Common Inputs | Primary Reference | Default Format | Routing Notes |
| --- | --- | --- | --- | --- |
| WeChat Article Video | `mp.weixin.qq.com` URL or markdown article | `wechat-article-video.md` | `1080x1920` | Use `templates/wechat-video/` when available. |
| Product Promo Video | Product website, description, screenshots | `product-promo-video.md` | `1920x1080` or `1080x1920` | Start with brief/proof points before visuals. |
| Open Source Project Intro | GitHub repository URL, README, open-source launch | `open-source-project-video.md` | `1920x1080` | Prefer README/docs/screenshots/demos/install commands. |
| Release Note Video | Changelog, release notes, new feature list | `release-note-video.md` | `1080x1920` or `1920x1080` | Focus on what changed and why users care. |
| News Flash / Market Update | News, market update, data-heavy social content | `news-flash-images.md` | `1080x1920` | Use urgent editorial pacing and visible background images. |

## Default Choices

- Use portrait for Chinese social distribution.
- Use landscape for websites, Bilibili, YouTube, conference demos, and product explainers.
- Prefer real screenshots, docs, and source images before generated images for product and open-source videos.
- Use generated editorial backgrounds for News Flash when a real visual source is missing or needs mood.
- Use `production-workflow.md` for requests with multiple scenes, narration, assets, or music.

The product promo, open-source project, and release note references are part of the scenario expansion set. If one is not present in the current checkout yet, use `production-workflow.md` as the temporary shared workflow.

## When Unsure

Ask one question:

> Where will this video be published: social feed, product website, presentation, or internal demo?

Fallback defaults:

- Use `1080x1920` when the answer suggests Chinese social distribution or is still unclear.
- Use `1920x1080` for websites, Bilibili, YouTube, conference demos, product explainers, presentations, and internal demos.
- Use the scenario whose input source is closest to the user's material, then apply the default choices above.
