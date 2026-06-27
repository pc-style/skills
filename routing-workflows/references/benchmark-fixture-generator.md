# Benchmark Fixture Generator

Use when building synthetic benchmark/eval datasets where artifacts need authoritative labels or expected outputs.

## Intent

Generate artifacts and ground truth from the same deterministic source so they cannot drift.

## Workflow

1. Define the output contract first: manifest, artifacts, labels, results directory, and runner command.
2. Use a seeded generator for reproducibility.
3. Co-generate artifact and labels in the same code path.
4. Use a pluggable scenario registry so new cases are added as modules.
5. Run a tiny smoke variant before a full render/generation.
6. Validate structurally:
   - typecheck,
   - schema checks,
   - output file existence,
   - bounds/range checks,
   - non-empty expected labels.
7. Validate semantically with spot checks.
8. Validate visually/audibly when the artifact is media.
9. Fix the generator and rerender; do not manually patch labels to make results pass.

## Output

Report:

- dataset path,
- scenarios generated,
- smoke/full command,
- validation performed,
- known limitations.

## Avoid

- hand-written ground truth separate from generation,
- scaling before a smoke run passes,
- benchmark outputs with no stable manifest.
