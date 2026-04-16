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
- **Never use em dashes (—) or en dashes (–).** Use commas, periods, or parentheses instead.
- **Write like a human, not an AI.** Specifically:
  - Use simple, everyday words. Write "use" not "utilize", "help" not "facilitate", "start" not "embark", "show" not "showcase", "change" not "revolutionize".
  - Ban these AI slop words/phrases entirely: "delve", "tapestry", "landscape", "paradigm", "leverage", "robust", "comprehensive", "cutting-edge", "groundbreaking", "game-changing", "pivotal", "seamlessly", "furthermore", "moreover", "it's worth noting", "in today's world", "at its core", "in the realm of", "the power of".
  - Keep sentences short. If a sentence has more than 25 words, split it.
  - Write in active voice. Not "the results were analyzed" but "we analyzed the results".
  - Be direct. State the point first, then support it. No flowery introductions.
  - Vary sentence length and structure. Monotone rhythm = AI smell.
  - Write at a 8th grade reading level. If a simpler word exists, use it.
- Use proper markdown headings, paragraphs, and formatting
- No generic "compelling" introductions or "in conclusion" wrapups. Start with the most interesting fact or claim. End when you're done.

### 3. Add a References Section

At the end of the post, add a `## References` section with numbered external links. Each reference must:

- Link to a real, accessible URL
- Have anchor text that accurately describes the linked content
- Be relevant to the blog post topic

Example:

```markdown
## References

1. [Understanding Modern Web Frameworks](https://example.com/web-frameworks)
2. [Performance Benchmarks 2025](https://example.com/benchmarks)
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
