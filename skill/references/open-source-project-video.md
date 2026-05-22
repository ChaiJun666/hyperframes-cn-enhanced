---
name: open-source-project-video
description: Produce intro and launch videos for GitHub and open-source projects using README, docs, screenshots, examples, install commands, and repository signals.
---

# Open Source Project Video

Use this workflow for a GitHub repo URL, README, open-source project, package, plugin, framework, or developer tool. Read `production-workflow.md` first; this guide adapts the staged workflow to developer-facing intro, demo, and launch videos.

## Inputs

Collect the strongest available project material before planning scenes:

- GitHub repository URL
- README, quickstart, architecture notes, examples, and contribution or community docs
- Docs site, API reference, changelog, migration guide, or tutorial pages
- Demo screenshots, GIFs, screen recordings, playground captures, or generated output examples
- Install commands, setup requirements, package names, and usage examples
- Release notes, launch post, benchmark notes, roadmap, or known limitations
- Star count, forks, downloads, contributors, adopters, or other community proof only when current and verified in the current run

Do not rely on repository metrics unless they are fetched or provided in the current run. If metrics are unavailable or stale, omit them instead of implying popularity.

## Brief Focus

Answer these in `01-brief.md` before storyboard work:

- What does the project help users do in one concrete workflow?
- Who is it for, such as frontend engineers, data teams, ML researchers, security engineers, framework authors, plugin developers, or maintainers?
- What painful setup, manual work, hidden complexity, operational risk, or missing abstraction does it remove?
- What is the fastest proof that it works: a command, API call, before/after output, screenshot, benchmark, test result, or live demo moment?
- What should viewers try after watching: install the package, run the quickstart, open the docs, star the repo, join the community, or test the demo?

Keep the brief practical. Open-source videos work best when the viewer can understand the job, see the smallest useful path, and know exactly what to try next.

## Recommended Structures

Choose one structure in `02-storyboard.md`, then adapt scene count to duration and platform.

### Problem -> CLI or API -> Result

Best for libraries, CLIs, SDKs, plugins, and tools where a small workflow proves value quickly.

1. Problem: show the awkward old workflow, missing capability, slow setup, or fragile manual step.
2. Project reveal: name the project and state the concrete thing it automates, simplifies, or enables.
3. Install or import: show the shortest relevant install command, package import, or setup step.
4. Smallest useful action: show one CLI command, API call, config snippet, or code example.
5. Result: show the generated output, passing check, rendered screen, saved file, deployed artifact, or measurable improvement.
6. Next step: point to the repo, docs, quickstart, examples, or release page.

### Architecture Reveal

Best for frameworks, infrastructure tools, data systems, AI/ML stacks, and projects where the design is a major reason to care.

1. Value first: open with the outcome the architecture makes easier, safer, faster, or more observable.
2. System map: show a simplified diagram from the README or create a clear composition diagram from documented components.
3. Data or control flow: animate the path through the main modules, services, agents, runtime, plugins, or adapters.
4. Developer touchpoint: show where users configure, call, extend, or inspect the system.
5. Proof moment: show a real command, log, dashboard, test, benchmark, or example output.
6. Try it: end with the quickstart, docs path, or example project.

### README to Launch Video

Best for turning an existing README, release announcement, or docs landing page into a concise launch asset.

1. Repo identity: show the project name, logo or mark, and one-sentence purpose.
2. README promise: pull the clearest value statement into a visual hook.
3. Feature sequence: turn two or three README sections into short capability scenes with real screenshots or commands.
4. Demo proof: show the quickest working example from the quickstart or examples directory.
5. Community or maturity signal: show verified current release, docs coverage, tests, stars, adopters, or contributors only when provided or freshly fetched.
6. CTA: finish with the repository URL, install command, docs URL, or contribution path.

## Asset Priority

Plan assets in `03-asset-plan.md` using this order:

1. README diagrams, screenshots, architecture images, badges, and example outputs
2. CLI commands, terminal output, install steps, and test or benchmark output
3. Docs screenshots, API reference pages, tutorial steps, and quickstart sections
4. Code snippets that show the smallest useful API, config, or extension point
5. Demo GIFs, screen recordings, playground captures, and generated artifacts
6. Repo logo, package icon, maintainer-provided branding, or a generated project mark when no brand asset exists

Use code and terminal visuals sparingly. They are proof, not the whole video; crop tightly, keep text readable, and pair them with visible results.

## Visual Direction

Match the visual system to the project category and audience:

- Swiss Pulse default for developer tools: clean grids, precise typography, crisp terminal/editor details, restrained motion, and confident information hierarchy.
- Data Drift for AI/ML, analytics, data infrastructure, and model workflow projects: flowing data paths, input-to-output transformations, charts, embeddings, and structured motion.
- Deconstructed for security, infrastructure, compilers, runtimes, storage engines, observability, and low-level systems when a raw technical mood fits: exposed layers, system traces, logs, packets, memory maps, or component teardown visuals.

## Narration Guidance

Write concrete narration in `04-narration.md`:

- Say what the project does before explaining how it is built.
- Show the smallest useful workflow the viewer can repeat.
- Use project terms from the README and docs, but define specialized terms through visuals or context.
- Avoid exaggerated claims such as "revolutionary", "production-ready", "best", or "fastest" unless the source material directly supports them.
- Mention install and usage only when they fit the platform and duration; for very short videos, show the command visually and narrate the outcome.
- Keep architecture narration tied to value, not internal complexity for its own sake.

## Quality Checks

### Before Composition

- Confirm `01-brief.md` states project, audience, problem, proof, CTA, assumptions, duration, and platform.
- Confirm `02-storyboard.md` has scene IDs, purpose, timing estimates, visual source, narration intent, and CTA.
- Confirm `03-asset-plan.md` prioritizes README/docs/demo assets and marks each asset as existing, to capture, to generate, or to create in composition.
- Confirm current repository metrics, release details, benchmarks, or community claims were fetched or provided in the current run before using them.
- Confirm the planned quickstart, command, or API example is small enough to read on the target format.

### After Composition

Run validation from the HyperFrames composition project:

```bash
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect --timeout 30000
```

Review the rendered or inspected output for readable code, visible terminal output, no clipped text, no stale metrics, no unsupported claims, clear scene order, and a CTA that points to the repo, docs, install command, or quickstart.

## Common Pitfalls

- README slideshow: do not animate the README section by section without a viewer problem, workflow, proof, and next step.
- Too much code: one readable command or snippet is stronger than a wall of source.
- Outdated metrics: do not show stars, downloads, contributors, releases, benchmarks, or adopters unless current and verified.
- Explaining architecture before value: start with what the project helps users do, then reveal the system design only when it clarifies the benefit.
