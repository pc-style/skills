# Audit Report Parallel Fix

Use when the user wants a thorough audit that should turn into tracked remediation, not just prose.

## Intent

Create a severity-ranked issue ledger, then fix it safely in scoped batches.

## Workflow

1. Read the rule source first: prompt file, AGENTS.md, memories, issue list, checklist, style guide, or user-provided criteria.
2. Run targeted scans in parallel for each rule family.
3. Create a report file with severity tiers:
   - Critical,
   - High,
   - Medium,
   - Low.
4. Each finding should include:
   - file/path,
   - line(s),
   - issue,
   - current behavior,
   - recommended fix.
5. If fixing, split work by independent file groups or issue families.
6. Before editing any file, re-read it to ensure the finding still exists.
7. Mark fixed findings as resolved in the report when practical.
8. Run verification appropriate to the changed scope.

## Output

Report:

- audit file path,
- number of findings by severity,
- fixes completed,
- remaining unresolved items,
- verification result.

## Avoid

- broad refactors hidden inside audit fixes,
- stale edits when another agent/user already fixed a finding,
- untracked prose-only audits when the user expects remediation.
