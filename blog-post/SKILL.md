---
name: blog-post
description: Create a well-researched blog post about a requested topic. Researches the area, writes without hyphens, and adds a validated References section with external links.
---

# Blog Post Writer

Create a well-researched blog post on a given topic.

## Process

Follow these steps in order:

### 1. Research the Topic

Use the ddgs-search skill to research the topic thoroughly:

```bash
uv run {baseDir}/../ddgs-search/search.py "<topic>" -n 10
```

Read the top results to gather facts, perspectives, and sources:

```bash
uv run {baseDir}/../ddgs-search/content.py "<url>"
```

Gather at least 3 high quality external sources to reference.

### 2. Write the Blog Post

Write the blog post as a markdown file. Follow these rules strictly:

- **Never use hyphens (`-`) anywhere in the text.** Use alternative phrasing instead. For example:
  - "well known" instead of "well-known"
  - "state of the art" instead of "state-of-the-art"
  - "long term" instead of "long-term"
  - Use "to" instead of hyphens in ranges: "5 to 10" not "5-10"
  - Use em dashes (—) for parenthetical statements if needed
- Write in a clear, engaging style
- Use proper markdown headings, paragraphs, and formatting
- Include a compelling introduction and conclusion

### 3. Add a References Section

At the end of the post, add a `## References` section with numbered external links. Each reference must:

- Link to a real, accessible URL
- Have anchor text that accurately describes the linked content
- Be relevant to the blog post topic

Example:

```markdown
## References

1. [Understanding Modern Web Frameworks](https://example.com/web-frameworks) — Overview of current framework landscape
2. [Performance Benchmarks 2025](https://example.com/benchmarks) — Comparative analysis of framework performance
```

### 4. Validate All Reference Links

After writing, validate every link in the References section:

```bash
uv run {baseDir}/validate_links.py '[{"url": "https://...", "anchor": "link text"}, ...]'
```

Pass all reference links as a JSON array. Each entry needs a `url` and `anchor` field.

If any link fails validation:
- **Not reachable**: Find an alternative URL for the same topic
- **Content mismatch**: Update the anchor text to match the actual page content, or find a better URL

Re-validate until all links pass.

## Output

Save the blog post as a markdown file in the current working directory. Use a slug derived from the title as the filename (e.g., `understanding-web-frameworks.md`). Note: hyphens are allowed in filenames, just not in the blog post content itself.

## Dependencies

This skill requires the `ddgs-search` skill to be available at `{baseDir}/../ddgs-search/`.
