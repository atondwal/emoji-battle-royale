This repo uses VibeControl for spec-driven development.

## How it works

There are two modes, controlled by `.vibecontrol-mode`:

- **SPEC_MODE** (default): Help design specs in `spec/`. Don't write implementation code.
- **IMPL_MODE**: Implement the spec. Don't touch `spec/`.

Hooks enforce this automatically — you don't need to worry about it, just follow the mode.

Commits are auto-generated with `spec:` / `impl:` / `task:` prefixes.

Use `/go` when the spec is ready. Use `/og` to go back and work on the spec. Use `/vc-status` to check where things stand.

## About this file

This is the starter CLAUDE.md. Once the project has real code, rewrite this file to describe the actual project — architecture, conventions, key files, whatever helps you work effectively. Keep the VibeControl paragraph above (or just a one-liner noting the repo uses VibeControl) so future sessions know the workflow.

Details on how VibeControl works are in `.claude/docs/vibecontrol.md` if you need them.
