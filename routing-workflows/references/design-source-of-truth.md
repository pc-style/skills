# Design Source Of Truth

Use after a prototype or option has been chosen and the task is to preserve its design language durably.

## Intent

Convert a selected design into reusable rules before rebuilding the production app.

## Workflow

1. Identify the chosen design and treat it as the visual source, not necessarily as production-quality code.
2. Extract the design language:
   - color system,
   - typography roles,
   - spacing rhythm,
   - layout grammar,
   - motion rules,
   - component motifs,
   - imagery and texture rules,
   - interaction tone.
3. Save the source of truth in a durable file such as `design.md`, `STYLEGUIDE.md`, or design tokens.
4. If the user asks to reset prototype code, strip noisy prototype scaffolding while preserving the design rules.
5. Rebuild the real route/components from the source of truth, not by blindly copying temporary files.
6. Verify the rebuilt implementation visually.

## Output

Report:

- the source-of-truth file created/updated,
- the production files changed,
- what was preserved from the prototype,
- what was intentionally discarded.

## Avoid

- letting throwaway prototype structure become permanent architecture,
- losing the selected vibe during cleanup,
- mixing multiple rejected directions into the chosen one.
