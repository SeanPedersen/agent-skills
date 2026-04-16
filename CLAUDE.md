Collection of reusable agent skills for Claude Code (and other coding agents).

## Structure

Each subdirectory is a self-contained skill with a `SKILL.md` (instructions + frontmatter) and optional helper scripts. `{baseDir}` in skill files resolves to that skill's directory at runtime.

## Install (Claude Code)

Claude Code needs each skill folder directly under the skills directory. Symlink each skill:

```bash
mkdir -p ~/.claude/skills
for skill in "$(pwd)"/*/; do
  [ -f "$skill/SKILL.md" ] && ln -sf "$skill" ~/.claude/skills/$(basename "$skill")
done
```

For project-level install, use `.claude/skills/` instead of `~/.claude/skills/`.
