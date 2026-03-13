# Agent Skills

Collection of useful skills for coding agents.

## Setup

### Claude Code

Claude Code only looks one level deep for `SKILL.md` files, so each skill folder must be directly under the skills directory. Clone the repo somewhere, then symlink individual skills:

```bash
# Clone to a convenient location
git clone https://github.com/SeanPedersen/agent-skills ~/agent-skills

# Symlink individual skills (user-level)
mkdir -p ~/.claude/skills
ln -s ~/agent-skills/browser-tools ~/.claude/skills/browser-tools

# Or project-level
mkdir -p .claude/skills
ln -s ~/agent-skills/browser-tools .claude/skills/browser-tools
```
