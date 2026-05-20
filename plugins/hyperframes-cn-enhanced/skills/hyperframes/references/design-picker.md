# Design Picker

Use this only when no `design.md` exists and the user wants to choose a visual direction interactively.

## Minimal Agent Workflow

1. Offer 2-3 named styles from `visual-styles.md` that match the user's content.
2. Ask for mood, canvas brightness, and any brand colors or font constraints.
3. Generate a small `design.md` with:
   - Style prompt
   - 3-5 color tokens with roles
   - 1-2 type families or fallbacks
   - Motion direction
   - What not to do
4. Use that `design.md` as the source of truth for the composition.

For urgent Chinese social/news content, recommend `News Flash` by default.

