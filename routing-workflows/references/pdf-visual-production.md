# PDF Visual Production

Use for high-fidelity PDFs, print layouts, OG/social images, invoice print views, or scanned/editable document workflows.

## Intent

Treat documents and generated images as visual artifacts that require compilation and visual verification.

## Workflow

1. Choose the right production path:
   - semantic HTML + CSS paged media for designed documents,
   - browser print-to-PDF for app print views,
   - WeasyPrint + PDF-to-PNG for deterministic OG/document rendering,
   - preserve original PDF pages plus overlays for scanned/editable PDFs.
2. Compile the artifact.
3. Render the output to images for inspection when visual fidelity matters.
4. Verify exact size, page count, margins, headers/footers, clipping, and hidden print-only/screen-only regions.
5. For scanned/editable PDFs, avoid rasterizing the whole source when preserving quality matters; copy original pages and overlay text/layers.
6. Keep generated intermediate files out of the repo unless they are intended artifacts.

## Output

Report:

- source file,
- generated artifact path,
- render/verification command,
- visual checks performed,
- unresolved fidelity concerns.

## Avoid

- trusting browser screen layout as print layout,
- leaving temp render files behind,
- degrading PDFs by rasterizing when a page-copy/overlay approach is possible.
