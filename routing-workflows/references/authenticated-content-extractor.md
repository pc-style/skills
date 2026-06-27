# Authenticated Content Extractor

Use when scraping or exporting structured content/assets from authenticated or semi-authenticated systems.

## Intent

Turn messy web content into durable raw, normalized, and indexed outputs while handling sessions and retries safely.

## Workflow

1. Define the allowed scope: URLs, domains, content types, and media types to skip.
2. Establish session handling: cookies, headers, CSRF/XSRF, user agent, and refresh/rotation from responses.
3. Implement fetch with retry/backoff and per-item error isolation.
4. Deduplicate inputs and discovered links.
5. For each item, save:
   - raw HTML/source,
   - normalized Markdown/text,
   - structured JSON metadata,
   - downloaded allowed assets.
6. Classify links/assets by extension, MIME type, and context.
7. Skip forbidden or huge media by default unless the user explicitly wants it.
8. Produce an aggregate index/map and an errors log.

## Output

Report:

- output directory,
- item counts,
- downloaded asset counts by type,
- skipped media types,
- errors and retry failures.

## Avoid

- aborting the whole run for one bad item,
- redownloading duplicates,
- mixing normalized content with raw source without keeping both.
