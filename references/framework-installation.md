# Framework Installation And Invocation

The skill uses the portable Agent Skills layout: one directory containing `SKILL.md`, optional `agents/openai.yaml`, scripts, and references. Keep this canonical directory as the single source of truth.

## Installer

Run from the canonical skill directory:

```bash
./scripts/install-skill.sh <target> [project-root]
```

Targets:

| Target | Discovery directory |
|---|---|
| `codex-global` | `${CODEX_HOME:-$HOME/.codex}/skills/` |
| `codex-project` | `<project-root>/.agents/skills/` |
| `claude-global` | `$HOME/.claude/skills/` |
| `claude-project` | `<project-root>/.claude/skills/` |
| `openclaw-global` | `${OPENCLAW_HOME:-$HOME/.openclaw}/skills/` |
| `openclaw-workspace` | `${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}/skills/` |
| `all-global` | Codex global, Claude global, and OpenClaw workspace together |
| `custom` | The second argument is the target skills directory |

The installer creates a symbolic link and refuses to replace an existing path. This prevents framework copies from drifting. Use `custom` for another Agent Skills-compatible runtime.

Use `all-global` for this machine when the same canonical skill should be immediately available to Codex, Claude Code, and the active OpenClaw workspace. It preflights every destination and refuses a partial installation if any destination already exists.

## Codex

Invoke explicitly:

```text
Use $goal-oriented-pbl-course to turn these workshop notes into a PBL course.
```

The `agents/openai.yaml` metadata provides the Codex UI label and default prompt. Project-local `.agents/skills` is appropriate when the course method belongs to one repository; global installation makes it available across workspaces.

## Claude Code

Install to `.claude/skills/goal-oriented-pbl-course` or `~/.claude/skills/goal-oriented-pbl-course`. Invoke by skill name or ask Claude Code to use the skill while designing a course. Claude-specific optional frontmatter is intentionally omitted so the same `SKILL.md` remains portable.

## OpenClaw

Install to `~/.openclaw/workspace/skills/goal-oriented-pbl-course` for the active workspace or `~/.openclaw/skills/goal-oriented-pbl-course` for a global skill. Ask OpenClaw to use `goal-oriented-pbl-course` and provide source files or a goal.

## Other Frameworks

Point the framework's skill discovery directory at the canonical folder with the installer `custom` target. A compatible framework must:

1. discover `SKILL.md`;
2. read YAML `name` and `description`;
3. make referenced files available relative to the skill root.

If a framework requires proprietary metadata, add an adapter under `agents/` without changing the canonical workflow in `SKILL.md`.
