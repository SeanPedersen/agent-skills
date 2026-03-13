# Agent Skills

Collection of useful skills for coding agents.

## Skills

| Skill | Description |
|---|---|
| [browser-tools](browser-tools/) | Interactive browser automation via Chrome DevTools Protocol. Use when you need to interact with web pages, test frontends, or when user interaction with a visible browser is required. |
| [optimize-design](optimize-design/) | Tools and techniques for creating and optimizing web app user interfaces (UI) and user experience (UX). |
| [optimize-website](optimize-website/) | Audit and optimize website performance targeting Core Web Vitals (LCP, CLS, INP). Use when the user wants to improve page speed, reduce bundle size, or fix performance issues. |
| [security-audit](security-audit/) | Audit web applications for security vulnerabilities. Covers OWASP Top 10 with actionable checklists for injection, auth, XSS, CSRF, secrets, headers, dependencies, and more. |

## Setup

### Claude Code

Claude Code only looks one level deep for `SKILL.md` files, so each skill folder must be directly under the skills directory. Clone the repo somewhere, then symlink individual skills:

```bash
# Clone to a convenient location
git clone https://github.com/SeanPedersen/agent-skills ~/agent-skills

# Symlink individual skills (user-level)
mkdir -p ~/.claude/skills
ln -s ~/agent-skills/browser-tools ~/.claude/skills/browser-tools
ln -s ~/agent-skills/optimize-design ~/.claude/skills/optimize-design
ln -s ~/agent-skills/optimize-website ~/.claude/skills/optimize-website
ln -s ~/agent-skills/security-audit ~/.claude/skills/security-audit

# Or project-level
mkdir -p .claude/skills
ln -s ~/agent-skills/browser-tools .claude/skills/browser-tools
ln -s ~/agent-skills/optimize-design .claude/skills/optimize-design
ln -s ~/agent-skills/optimize-website .claude/skills/optimize-website
ln -s ~/agent-skills/security-audit .claude/skills/security-audit
```
