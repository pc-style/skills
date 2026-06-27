---
name: routing-workflows
description: Routes pcstyle's recurring cross-project tasks to compact workflow references. Use for fuzzy multi-step work involving design directions, browser visual verification, audits, extraction, benchmark fixtures, PDF/document production, API discovery, client-source ingest, or continuation from prior threads.
---

# Routing Workflows

This is a workflow router, not a giant instruction dump.

Use it to recognize pcstyle's recurring cross-project work patterns and read only the one reference needed for the current task. If the task is a simple localized code edit, ignore this skill and proceed normally.

## Routing rule

1. Classify the request using the routes below.
2. Read at most one reference file unless the user explicitly asks for a multi-phase workflow.
3. Execute the task; do not spend the final answer explaining the workflow unless useful.

## Routes

- Multiple distinct design options before productionizing → `references/design-directions.md`
- Extract a chosen prototype/design into durable rules or tokens → `references/design-source-of-truth.md`
- UI/design changes that need visual proof → `references/visual-regression-browser-pass.md`
- Synthetic benchmark/eval data with ground truth → `references/benchmark-fixture-generator.md`
- Turn observed browser traffic into a stable agent API/script → `references/browser-to-api-wrapper.md`
- Scrape authenticated or semi-authenticated content/assets → `references/authenticated-content-extractor.md`
- Audit a repo/site and convert findings into tracked fixes → `references/audit-report-parallel-fix.md`
- Ingest messy client inputs into a brief/content map → `references/client-source-ingest.md`
- Produce or verify PDFs, print layouts, OG images, or document assets → `references/pdf-visual-production.md`
- Continue from a prior Amp thread without rediscovery → `references/handoff-from-thread.md`

## Guardrails

- Keep project-specific examples out of the active answer unless they help the task.
- Prefer smaller, verifiable artifacts over large speculative rewrites.
- If a workflow calls for browser/dev-server usage, still follow the user's global instruction not to start dev servers unless explicitly allowed.
- If no route matches, do not force this skill.
