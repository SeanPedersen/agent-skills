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
| [youtube-transcript](youtube-transcript/SKILL.md) | Fetch YouTube video transcripts |

## Installation

### Claude Code

Claude Code only looks one level deep for `SKILL.md` files, so each skill folder must be directly under the skills directory. Clone the repo somewhere, then symlink individual skills:

```bash
# Clone to a convenient location
git clone https://github.com/joshuaalsen/agent-skills ~/agent-skills

# Symlink individual skills (user-level)
mkdir -p ~/.claude/skills
ln -s ~/agent-skills/blog-post ~/.claude/skills/blog-post
ln -s ~/agent-skills/browser-tools ~/.claude/skills/browser-tools
ln -s ~/agent-skills/ddgs-search ~/.claude/skills/ddgs-search
ln -s ~/agent-skills/free-domain-search ~/.claude/skills/free-domain-search
ln -s ~/agent-skills/youtube-transcript ~/.claude/skills/youtube-transcript

# Or project-level
mkdir -p .claude/skills
ln -s ~/agent-skills/blog-post .claude/skills/blog-post
ln -s ~/agent-skills/browser-tools .claude/skills/browser-tools
ln -s ~/agent-skills/ddgs-search .claude/skills/ddgs-search
ln -s ~/agent-skills/free-domain-search .claude/skills/free-domain-search
ln -s ~/agent-skills/youtube-transcript .claude/skills/youtube-transcript
```

### Codex CLI

```bash
git clone https://github.com/joshuaalsen/agent-skills ~/.codex/skills/agent-skills
```

### Amp

Amp finds skills recursively in toolboxes:

```bash
git clone https://github.com/joshuaalsen/agent-skills ~/.config/amp/tools/agent-skills
```

### Droid (Factory)

```bash
# User-level
git clone https://github.com/joshuaalsen/agent-skills ~/.factory/skills/agent-skills

# Or project-level
git clone https://github.com/joshuaalsen/agent-skills .factory/skills/agent-skills
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
