---
name: og
description: Switch back to SPEC_MODE to work on the spec
disable-model-invocation: true
allowed-tools: Read, Bash, Glob
---

# /og — Switch from IMPL_MODE back to SPEC_MODE

Execute these steps in order:

1. **Verify mode**: Read `.vibecontrol-mode`. If already `SPEC_MODE`, tell the user "Already in SPEC_MODE" and stop.

2. **Commit any uncommitted implementation work**:
   ```
   git add -A && git reset HEAD -- spec/ && git diff --cached --quiet || git commit -m "impl: $(git diff --cached --stat | head -1 | sed 's/^ *//')" --no-verify
   ```

3. **Switch mode**: Run `echo SPEC_MODE > .vibecontrol-mode` (must use Bash, not Write tool)

4. **Announce**: Tell the user you've switched back to SPEC_MODE. They can now work on the spec. Use `/go` again when ready to implement.
