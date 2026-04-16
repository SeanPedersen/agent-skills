---
name: optimize-design
description: Tools and techniques for creating and optimizing web app user interfaces (UI) and user experience (UX).
---

# Optimize Design

## Good Design

- Information Hierarchy (pack UI elements together based on their semantics)
  - Minimizes mouse movement / provide keyboard shortcuts for common inputs
- Iterative complexity (progressive disclosure of options)
- Minimize visual shift / movement (every moving pixel must add value)
- Use rows instead of boxes for items that have numerical values to compare
- Use hover highlight effects only for interactive components (links, buttons)

## Bad Design

Bad UI:
- Pop-ups (visual distractions)
- Deviating significantly from proven historical UI patterns
- Inconsistent navigation patterns between pages
- Overusage of animations (only move UI elements with a clear signal / purpose)
- Loading spinners that never end / indicate no progress
- Auto-playing videos with sound
- Confirmation dialogs for every minor action
- Non-descriptive error messages
- Disabling zoom on mobile
- Missing auto-focus of text input (search bars etc.)
- Low contrast text (poor accessibility)
- Visual shift on scrollbar appearance (use css `scrollbar-gutter: stable` to prevent this)
