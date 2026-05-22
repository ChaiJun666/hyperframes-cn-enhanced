---
name: release-note-video
description: Turn changelogs, release notes, and feature announcements into concise HyperFrames launch videos.
---

# Release Note Video

Use this workflow for changelog entries, release notes, feature lists, app update notes, or new-feature launch videos. Read `production-workflow.md` first, then use this reference to shape the release-specific brief, structure, assets, and quality checks.

## Inputs

- Release notes
- Changelog diff
- Feature screenshots
- Before/after screenshots
- Issue or PR summaries
- Version number
- Target users
- Migration/upgrade notes

## Brief Focus

- What changed: name the user-visible difference, not only the internal implementation.
- Who benefits: identify the role, team, or workflow that gets the most value.
- Why it matters now: connect the release to urgency, timing, reliability, speed, or a current user pain.
- What users can do now that they could not before: show the new action, shortcut, automation, insight, or outcome.
- Upgrade action/CTA: make the next step explicit, especially when migration, opt-in, or configuration is required.

## Recommended Structures

### What's New -> Why It Matters -> Try It

1. Title scene: show product, version number, and the release headline.
2. What's New: introduce the main feature or top change with a screenshot, UI zoom-in, or short demo clip.
3. Why It Matters: translate the change into a concrete benefit for the target user.
4. Proof scene: show before/after, a workflow comparison, or a small changelog excerpt for credibility.
5. Try It: end with the upgrade action, feature location, migration note, or CTA.

### Three Improvements

1. Title scene: present the version number and a concise release theme.
2. Improvement 1: show the highest-value user-facing change with supporting UI evidence.
3. Improvement 2: show the next practical benefit, using a demo clip or before/after screenshot.
4. Improvement 3: show the final notable change, keeping minor fixes grouped or omitted.
5. CTA scene: summarize the release benefit and state any upgrade, rollout, or migration instruction.

## Asset Priority

1. Before/after screenshots
2. UI zoom-ins
3. Short demo clips
4. Changelog excerpts
5. PR/issue references
6. Generated backgrounds only for title/transition scenes

## Visual Direction

- Cleaner than News Flash by default: use restrained motion, precise hierarchy, and product evidence over spectacle.
- SaaS/dev releases: use Swiss Pulse for structured layouts, sharp typography, and clear technical credibility.
- Major launches: use Maximalist Type when the release needs a bolder, higher-energy reveal.
- Enterprise releases: use Velvet Standard for polished, trusted, executive-ready messaging.
- AI features: use Data Drift for model, automation, or intelligence themes without hiding the actual UI.

## Narration Guidance

- Lead with benefits and outcomes.
- Avoid reading the changelog line by line.
- Translate implementation details into user-facing outcomes.
- Keep migration warnings short and explicit.
- Name the upgrade action only after the value is clear, unless the release is security-critical or breaking.

## Quality Checks

### Before Composition

- Confirm every featured change is supported by release notes, changelog entries, screenshots, issue/PR summaries, or provided source material.
- Confirm the storyboard includes at least one outcome or proof scene, not only a list of changed items.
- Confirm before/after comparisons are visually obvious and screenshots are readable in the target format.
- Confirm migration, compatibility, rollout, or upgrade warnings are visible and spoken when applicable.

### After Composition

Run validation from the HyperFrames composition project:

```bash
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect --timeout 30000
```

Review the output for timing issues, render or contrast failures, layout overflow, unreadable screenshots, and missing migration or upgrade instructions when applicable.

## Common Pitfalls

- Listing every minor fix instead of choosing the few changes users will notice.
- Leading with implementation details before user value.
- Using tiny UI screenshots that become unreadable in portrait.
- Forgetting upgrade/migration instructions when they matter.
