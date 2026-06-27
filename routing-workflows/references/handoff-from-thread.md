# Handoff From Thread

Use when continuing from a prior Amp thread or the user references a thread URL/ID.

## Intent

Continue from the actual unresolved state instead of rediscovering or replaying the whole prior session.

## Workflow

1. Read the referenced thread with a focused question.
2. Extract only continuation-relevant state:
   - goal,
   - what was completed,
   - what was diagnosed but not fixed,
   - files touched,
   - commands run,
   - commits/branches/PRs,
   - blockers,
   - exact next action.
3. Distinguish clearly between:
   - fixed and verified,
   - implemented but unverified,
   - diagnosed only,
   - user decision pending.
4. Inspect current workspace state before editing; the prior thread may be stale.
5. Continue with the smallest next action.

## Output

Report:

- prior thread link,
- continuation summary,
- current action taken,
- verification result.

## Avoid

- summarizing the whole thread when only next state matters,
- assuming old file contents are still current,
- treating a proposed plan in the prior thread as already implemented.
