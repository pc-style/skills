# Browser To API Wrapper

Use when a website has useful data/actions but no stable public API for agents.

## Intent

Capture browser behavior once, derive a stable interface, and stop future agents from ad-hoc scraping.

## Workflow

1. Drive the real flow in a browser while capturing network traffic and request/response bodies.
2. Preserve the raw trace before reusing or overwriting capture directories.
3. Infer endpoints, schemas, auth/session requirements, and response quirks from the captured traffic.
4. Produce a thin wrapper script or OpenAPI spec over only the useful high-level operations.
5. Hide fragile details inside the wrapper:
   - tokens,
   - XSSI prefixes,
   - cookies/headers,
   - pagination quirks,
   - rate limits,
   - response normalization.
6. Add a help command and examples for future agents.
7. Document the recapture/regenerate path when the target site changes.

## Output

Report:

- what flows were captured,
- wrapper commands or generated spec path,
- confidence/coverage gaps,
- recapture instructions.

## Avoid

- exposing raw internal endpoints directly to future agents,
- assuming captured APIs are stable forever,
- storing secrets in generated specs or examples.
