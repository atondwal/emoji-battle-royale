---
name: go
description: Commit the spec and switch to IMPL_MODE to begin implementation
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Edit, Glob, Grep
---

# /go — Switch from SPEC_MODE to IMPL_MODE

Execute these steps in order:

1. **Verify mode**: Read `.vibecontrol-mode`. If already `IMPL_MODE`, tell the user "Already in IMPL_MODE" and stop.

2. **Commit the spec**:
   ```
   git add spec/
   git diff --cached --quiet || git commit -m "spec: $(git diff --cached --stat | head -1 | sed 's/^ *//')" --no-verify
   ```

3. **Switch mode**: Run `echo IMPL_MODE > .vibecontrol-mode` (must use Bash, not Write tool)

4. **Read the spec**: Read all files in `spec/` to understand what to implement.

5. **Get the spec diff**: Run `git diff HEAD~1 -- spec/` to see what changed.

6. **Announce**: Tell the user you've switched to IMPL_MODE and what you're about to implement.

7. **Implement**: Begin implementing the spec. Do not touch `spec/`.
