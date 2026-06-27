# Visual Regression Browser Pass

Use when UI/design work must be proven with rendered evidence.

## Intent

Close the loop between code changes and what the user actually sees.

## Workflow

1. Capture the current state before editing when practical.
2. Inspect source and DOM measurements before guessing.
3. Make the smallest targeted edit for the diagnosed issue.
4. Verify in a browser with screenshots and, where useful, DOM measurements.
5. Check relevant breakpoints:
   - mobile: 390, 768,
   - desktop: 1200, 1440, 1920,
   - large: 2560 when the issue is large-screen layout.
6. Check interactions that matter: scroll, hover, menu open/close, carousel, modal, animation reveal, form states.
7. Iterate until screenshots/measurements support the claim.

## Evidence to collect

- screenshots or crops,
- element rects,
- overflow/scrollHeight checks,
- computed opacity/visibility for reveal animations,
- console errors only when relevant.

## Output

Report:

- what changed,
- which viewports/interactions were checked,
- any viewport or state not verified.

## Avoid

- saying a design is fixed after only reading CSS,
- relying on the default viewport for responsive work,
- starting a dev server unless the user allowed it.
