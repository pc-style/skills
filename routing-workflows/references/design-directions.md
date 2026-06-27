# Design Directions

Use when the user wants several possible visual directions before choosing one to productionize.

## Intent

Create real, reviewable design options, not one generic compromise.

## Workflow

1. Inspect the current product, brand material, screenshots, and existing code before designing.
2. Create isolated options, such as `/1`, `/2`, `/3`, `/beta/1`, or standalone HTML files.
3. Give each option a distinct design thesis:
   - one close iteration on the current direction,
   - one strong but safe alternative,
   - one meaningful creative divergence.
4. Avoid overwriting the production route until the user chooses.
5. Keep each option coherent: typography, spacing, color, motion, components, and copy hierarchy should all support the same thesis.
6. Verify the options build/render before presenting them.

## Output

Report:

- where each option lives,
- the thesis of each option,
- any tradeoffs,
- what should happen after the user picks one.

## Avoid

- five variants of the same template,
- vague “modern” styling with no thesis,
- prematurely refactoring the production design system before a direction is chosen.
