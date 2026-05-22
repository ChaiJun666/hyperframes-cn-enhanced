---
name: product-promo-video
description: Produce product promo videos from product URLs, descriptions, screenshots, or docs using staged brief, storyboard, assets, narration, music, composition, and delivery artifacts.
---

# Product Promo Video

Use this workflow for product, service, SaaS, app, and website promo videos. Read `production-workflow.md` first; this guide adapts that staged workflow to product marketing, demo, launch, and conversion-oriented videos.

## Inputs

Collect the strongest available source material before planning scenes:

- Product URL or live website URL
- One-sentence product description
- Target audience and buyer or user context
- Screenshots, screen recordings, app captures, or product walkthrough clips
- Brand colors, logo files, typography notes, or `design.md`
- Landing page copy, headline, value proposition, and testimonials
- Feature list, use cases, integrations, and differentiators
- Pricing, plan names, or savings claims when relevant and supportable
- Platform and duration, such as 9:16 social, 16:9 launch video, 1:1 ad, 15 seconds, 30 seconds, or 60 seconds

## Brief Questions

Answer these in `01-brief.md` before storyboard work:

- Viewer: who is watching, what do they already know, and what level of technical detail will they tolerate?
- Painful or expensive problem: what current workflow, cost, risk, delay, or missed opportunity makes the viewer care now?
- Product promise: what practical outcome does the product make easier, faster, safer, cheaper, or more credible?
- Proof: what real UI, customer quote, metric, workflow step, demo moment, pricing point, or documentation supports the promise?
- CTA: what should the viewer do next, such as visit the site, book a demo, start a trial, join a waitlist, or contact sales?

If source material is thin, state assumptions directly in the brief and keep the video modest. Do not inflate claims, imply customer proof that is not provided, or build a launch-scale story from a single vague sentence.

## Recommended Structures

Choose one structure in `02-storyboard.md`, then adapt scene count to duration and platform.

### Problem -> Product -> Proof -> CTA

Best for general SaaS, services, apps, and landing-page promos where the viewer needs context before the pitch.

1. Hook: name the painful problem in one concrete moment.
2. Stakes: show the wasted time, money, risk, or complexity.
3. Product reveal: introduce the product with logo, product name, and core promise.
4. Demo moment: show the real UI solving the problem.
5. Proof: show customer evidence, metrics, recognizable workflow, integrations, or pricing value.
6. CTA: end with the next step and a clear product visual.

### Feature Trio

Best when the product has three strong, visually demonstrable capabilities.

1. Opening promise: define the product category and outcome.
2. Feature 1: show the most important UI action and its result.
3. Feature 2: show a second capability that expands the use case.
4. Feature 3: show the differentiator or advanced workflow.
5. Combined benefit: connect the three features to one business or user outcome.
6. CTA: invite the viewer to try, book, buy, or learn more.

### Demo-First

Best for developer tools, AI products, workflow apps, and products where the UI is the proof.

1. Cold open: start directly inside the product or website with a satisfying before/after or input/output moment.
2. Context card: briefly explain what the viewer just saw and why it matters.
3. Guided demo: show two or three UI steps with concise narration.
4. Result: show the generated output, dashboard, report, shipped artifact, or completed workflow.
5. Differentiator: show what makes the product faster, clearer, safer, or more powerful than the old way.
6. CTA: finish on the product URL, trial, demo, waitlist, or sales motion.

## Asset Priority

Plan assets in `03-asset-plan.md` using this order:

1. Real UI screenshots, product captures, dashboards, app screens, and website hero sections
2. Website sections that already explain positioning, proof, pricing, logos, or user flow
3. Screen recordings that show real interaction and time-based feedback
4. Docs diagrams, README images, architecture diagrams, command output, or API examples
5. Logo, brand assets, color palette, icons, typography, and design system references
6. Generated supporting backgrounds, abstract textures, symbolic objects, or scene plates

Do not build only from abstract generated images when UI exists. Generated visuals can support mood, transitions, and category context, but the product itself should remain the primary evidence.

## Visual Direction

Match the visual system to the product category and audience:

- SaaS and dev tools: crisp UI magnification, terminal or editor details when relevant, restrained motion, precise callouts, dark or neutral workspace surfaces, and readable typography.
- Premium enterprise: confident pacing, structured layouts, customer-proof moments, polished UI closeups, subtle depth, conservative color use, and strong logo discipline.
- AI and data: input-to-output transformations, animated data flows, model or workflow diagrams, before/after states, and clear guardrails around what the product actually does.
- Big launch: bold product name reveal, high-contrast hero moments, fast montage of capabilities, memorable visual rhythm, and a final CTA that feels event-grade.
- Security: trust-forward design, audit trails, access controls, threat-to-protection sequences, restrained urgency, and claims grounded in real features or certifications.

## Music

Create `07-music-plan.md` unless the user explicitly says no music.

Include:

- BPM target and reference energy, such as 90 BPM restrained enterprise, 110 BPM modern SaaS, or 125 BPM launch montage
- Energy curve by scene, including intro lift, demo bed, proof emphasis, and CTA resolve
- Hit points for product reveal, feature transitions, proof moments, pricing reveal, and final CTA
- Voiceover ducking notes so narration stays intelligible
- Source decision: generated music, user-supplied track, licensed library track, or omitted by request

Treat music as part of timing and storyboard planning, not late decoration. It affects pacing, transitions, narration spacing, and the perceived confidence of the promo.

## Quality Checks

### Before Composition

- Confirm `01-brief.md` states viewer, problem, promise, proof, CTA, assumptions, duration, and platform.
- Confirm `02-storyboard.md` has scene IDs, purpose, timing estimates, visual source, narration intent, and CTA.
- Confirm `03-asset-plan.md` prioritizes real UI and marks each asset as existing, to capture, to generate, or to create in composition.
- Confirm `07-music-plan.md` exists unless music was explicitly omitted.
- Check that every claim shown or narrated is supported by provided source material.

### After Composition

Run validation from the HyperFrames composition project:

```bash
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect --timeout 30000
```

Review the rendered or inspected output for readable UI, no clipped text, no unsupported claims, no excessive text density, aligned audio/music timing, and a visible CTA.

## Common Pitfalls

- Feature list instead of story: organize the promo around viewer pain, outcome, proof, and action.
- Ignoring real UI: use screenshots, website sections, and recordings as primary evidence whenever available.
- Too much on-screen text: let narration carry explanation and use concise labels on screen.
- Treating music as late decoration: plan tempo, hit points, and ducking before composition.
- Inventing unsupported claims: do not fabricate metrics, customer names, certifications, pricing savings, or competitive superiority.
