# agent-skills

A collection of agent skills compatible with Claude Code, Codex CLI, Amp, and Droid.

Fork of [pi-skills](https://github.com/badlogic/pi-skills) with modifications.

## Available Skills

| Skill | Description |
|-------|-------------|
| [blog-post](blog-post/SKILL.md) | Create researched blog posts with validated reference links |
| [browser-tools](browser-tools/SKILL.md) | Interactive browser automation via Chrome DevTools Protocol |
| [ddgs-search](ddgs-search/SKILL.md) | Web search and content extraction via DuckDuckGo (free, no API key) |
| [free-domain-search](free-domain-search/SKILL.md) | Check domain name availability via HTTP + WHOIS |
| [optimize-design](optimize-design/SKILL.md) | Tools and techniques for creating and optimizing web app UI/UX |
| [optimize-website](optimize-website/SKILL.md) | Audit and optimize website performance targeting Core Web Vitals |
| [security-audit](security-audit/SKILL.md) | Audit web apps for OWASP Top 10 security vulnerabilities |
| [youtube-transcript](youtube-transcript/SKILL.md) | Fetch YouTube video transcripts |

## Installation

### Claude Code

Claude Code only looks one level deep for `SKILL.md` files, so each skill folder must be directly under the skills directory. Clone the repo somewhere, then symlink individual skills:

```bash
git clone https://github.com/SeanPedersen/agent-skills
cd agent-skills

# Symlink all skills (user-level)
mkdir -p ~/.claude/skills
for skill in "$(pwd)"/*/; do
  [ -f "$skill/SKILL.md" ] && ln -sf "$skill" ~/.claude/skills/$(basename "$skill")
done

# Or project-level
mkdir -p .claude/skills
for skill in "$(pwd)"/*/; do
  [ -f "$skill/SKILL.md" ] && ln -sf "$skill" .claude/skills/$(basename "$skill")
done
```

### Codex CLI

```bash
git clone https://github.com/SeanPedersen/agent-skills ~/.codex/skills/agent-skills
```

### Amp

Amp finds skills recursively in toolboxes:

```bash
git clone https://github.com/SeanPedersen/agent-skills ~/.config/amp/tools/agent-skills
```

### Droid (Factory)

```bash
# User-level
git clone https://github.com/SeanPedersen/agent-skills ~/.factory/skills/agent-skills

# Or project-level
git clone https://github.com/SeanPedersen/agent-skills .factory/skills/agent-skills
```

## Skill Format

Each skill follows the Claude Code skill format:

```markdown
---
name: skill-name
description: Short description shown to agent
---

# Instructions

Detailed instructions here...
Helper files available at: {baseDir}/
```

The `{baseDir}` placeholder is replaced with the skill's directory path at runtime.

## Requirements

Some skills require additional setup. Generally, the agent will walk you through that. But if not:

- **blog-post**: Requires Python 3.10+ and uv. Also requires the ddgs-search skill.
- **browser-tools**: Requires Chrome and Node.js. Run `npm install` in the skill directory.
- **ddgs-search**: Requires Python 3.10+ and uv. No API key needed.
- **free-domain-search**: Requires Python 3.10+, uv, and `whois` CLI tool.
- **youtube-transcript**: Requires Node.js. Run `npm install` in the skill directory.

## License

MIT
