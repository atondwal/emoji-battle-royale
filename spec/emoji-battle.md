# Emoji Battle Royale — Spec

## Overview

A Python CLI game where 16 random emoji drop into a tournament bracket and battle head-to-head until one champion remains. Each matchup is decided by deterministic (but silly) rules, and every round is narrated with fun auto-generated commentary.

## Goals

- Zero dependencies beyond the Python 3.10+ standard library
- Single file: `emoji_battle.py`
- Fully deterministic given the same random seed (for reproducibility / shareability)
- Entertaining terminal output that works in any emoji-capable terminal

## CLI Interface

```
python emoji_battle.py [--seed SEED]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--seed` | random | Integer seed for `random`. Printed at the start so users can replay a bracket. |

No other arguments. Run it and enjoy.

## Emoji Pool

A hardcoded list of **64 battle-ready emoji** (no flags, no skin-tone variants, no ZWJ sequences — single codepoint only). Examples:

```
⚔️ 🐉 🔥 🌊 🗡️ 🛡️ 💀 👻 🤖 🧙 🦁 🐍 🦅 🐺 🦈 🐙
🌋 ⚡ 🪨 🌪️ 💎 🏹 🪓 💣 🎯 🧨 🔮 🪄 👹 👺 🦂 🕷️
🐲 🦖 🦍 🐊 🐅 🦬 🦏 🐘 🦧 🐻 🦇 🐝 🐜 🪲 🦎 🐸
🍄 🌵 🥊 🪃 ⛏️ 🔱 🏴‍☠️ 🎃 🤡 💩 🧊 ☄️ 🌑 🫧 🧿 🎲
```

At game start, 16 are selected at random (using the seeded RNG) from this pool.

## Tournament Structure

Single-elimination bracket, 4 rounds:

| Round | Name | Matchups |
|-------|------|----------|
| 1 | Round of 16 | 8 fights |
| 2 | Quarterfinals | 4 fights |
| 3 | Semifinals | 2 fights |
| 4 | The Final | 1 fight |

Seeding is by selection order (first selected = seed 1, etc.). Standard bracket pairing: seed 1 vs 16, 2 vs 15, … 8 vs 9.

## Battle Rules

Each matchup is decided by **one deterministic rule chosen per round** (cycling through them). The rules are intentionally silly:

### Rule 1 — "Codepoint Clash"
The emoji with the **higher Unicode codepoint** wins. Commentary flavor: *"Raw numeric power!"*

### Rule 2 — "Name Game"
Compare the official Unicode name (via `unicodedata.name()`). The emoji whose name has **more characters** wins. Tie-break: alphabetically later name wins. Commentary flavor: *"Whoever has the longer title commands more respect!"*

### Rule 3 — "Digital Root Duel"
Take the Unicode codepoint, sum its digits repeatedly until a single digit remains (the digital root). **Higher digital root wins.** Tie-break: higher codepoint wins. Commentary flavor: *"Mystical numerology decides the fate!"*

### Rule 4 — "Byte Brawl"
UTF-8 encode both emoji. The one that produces **more bytes** wins. Tie-break: higher codepoint wins. Commentary flavor: *"The heavier fighter crushes the competition!"*

Round 1 uses Rule 1, Round 2 uses Rule 2, Round 3 uses Rule 3, The Final uses Rule 4.

## Output Format

### Header
```
╔══════════════════════════════════════╗
║     🏟️  EMOJI BATTLE ROYALE  🏟️      ║
║         Season of the Seed: 42       ║
╚══════════════════════════════════════╝
```

### Contestant Intro
```
⚔️  THE COMBATANTS  ⚔️

 [1] 🐉  vs  [16] 💩
 [2] 🔥  vs  [15] 🧊
 ...
 [8] 🐍  vs   [9] 🦅
```

### Each Round
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚔️  ROUND 1 — Round of 16  ⚔️
  Rule: Codepoint Clash
  "Raw numeric power!"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🐉 vs 💩  →  💩 WINS!
    💩 (U+1F4A9) overpowers 🐉 (U+1F409) by sheer codepoint supremacy!

  🔥 vs 🧊  →  🧊 WINS!
    🧊 (U+1F9CA) freezes out 🔥 (U+1F525) with a higher code!

  ...
```

### Commentary Lines

Each fight gets one auto-generated commentary line. The format is:

```
    {winner} ({winner_detail}) {verb} {loser} ({loser_detail}) {reason}!
```

Where:
- `{winner_detail}` / `{loser_detail}` depend on the rule (codepoint hex, name length, digital root, or byte count)
- `{verb}` is randomly chosen from a per-rule verb list (seeded RNG):
  - Rule 1 verbs: "overpowers", "demolishes", "outranks", "crushes", "dominates"
  - Rule 2 verbs: "out-titles", "flexes on", "schools", "big-names", "overshadows"
  - Rule 3 verbs: "mystically overcomes", "spiritually transcends", "out-vibes", "hexes", "channels energy past"
  - Rule 4 verbs: "body-slams", "steamrolls", "flattens", "pile-drives", "out-weighs"
- `{reason}` is a short clause explaining the win (e.g., "by sheer codepoint supremacy", "with a mightier name")

### Final Result
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🏆  THE CHAMPION  🏆
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        👑
        💩

  💩 is the Emoji Battle Royale champion!

  "All hail 💩, supreme warrior of Seed 42!"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Full Bracket Recap

After the champion reveal, print a visual bracket recap:

```
  📋 BRACKET RECAP

  Round of 16       Quarters        Semis          Final
  ─────────────────────────────────────────────────────
  💩 ─┐
       ├─ 💩 ─┐
  🐉 ─┘       │
               ├─ 💩 ─┐
  🧊 ─┐       │       │
       ├─ 🧊 ─┘       │
  🔥 ─┘               │
                       ├─ 💩 👑
  🦅 ─┐               │
       ├─ 🐍 ─┐       │
  🐍 ─┘       │       │
               ├─ 🐍 ─┘
  🐙 ─┐       │
       ├─ 🐙 ─┘
  🦁 ─┘
```

(Exact bracket layout may vary; the key requirement is that it clearly shows the progression from 16 → 8 → 4 → 2 → 1.)

## Architecture

### Functions

| Function | Purpose |
|----------|---------|
| `load_emoji_pool() -> list[str]` | Returns the hardcoded list of 64 emoji |
| `select_combatants(pool, rng) -> list[str]` | Picks 16 random emoji, returns them in seeded order |
| `pair_bracket(combatants) -> list[tuple]` | Pairs seeds: (1,16), (2,15), … (8,9) |
| `fight(a, b, rule_id, rng) -> tuple[str, str]` | Returns `(winner, commentary_line)` |
| `digital_root(n) -> int` | Computes the digital root of an integer |
| `run_round(matchups, rule_id, rng) -> tuple[list[str], list[str]]` | Runs all fights in a round; returns `(winners, commentary_lines)` |
| `print_header(seed)` | Prints the title card |
| `print_matchups(matchups, round_name, rule)` | Prints round header and matchup results |
| `print_champion(emoji, seed)` | Prints the champion reveal |
| `print_bracket(rounds_data)` | Prints the full bracket recap |
| `main()` | Parses args, orchestrates the tournament |

### Data Flow

```
main()
  ├── parse --seed (argparse)
  ├── seed RNG
  ├── load_emoji_pool()
  ├── select_combatants()
  ├── pair_bracket()
  └── for each round:
        ├── run_round() → winners + commentary
        ├── print round output
        └── pair next round (adjacent winners)
  ├── print_champion()
  └── print_bracket()
```

## Edge Cases

- **Emoji with no `unicodedata.name()`**: The pool is curated to avoid these (e.g., no component emoji). If one slips through, fall back to `f"U+{ord(c):04X}"` as the name (length 6+).
- **Tie-breaks**: Every rule has a defined tie-break (higher codepoint). Since all emoji in a matchup are distinct, codepoints can never tie, so every fight always has a winner.
- **Terminal rendering**: Some emoji render as two characters wide. The bracket recap should account for this by using consistent spacing. Use `wcwidth`-style logic or simply pad generously.
- **VS emoji (U+FE0F)**: The pool should store base codepoints only (e.g., `"\u2694"` not `"\u2694\uFE0F"`). Display may append VS16 for rendering but comparisons use the base codepoint.

## Testing

The implementation should be verifiable by:

1. Running with `--seed 42` twice and getting identical output
2. Manually checking one fight per rule against the documented logic
3. Confirming all 15 fights produce a single champion

No test file is required — the deterministic seed _is_ the test.
