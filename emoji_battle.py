#!/usr/bin/env python3
"""Emoji Battle Royale — 16 emoji enter, 1 emoji leaves."""

import argparse
import random
import unicodedata


# ── Emoji Pool (64 single-codepoint battle-ready emoji) ──────────────────────

def load_emoji_pool() -> list[str]:
    return [
        "\U0001F409",  # 🐉 dragon
        "\U0001F525",  # 🔥 fire
        "\U0001F30A",  # 🌊 water wave
        "\U0001F480",  # 💀 skull
        "\U0001F47B",  # 👻 ghost
        "\U0001F916",  # 🤖 robot
        "\U0001F9D9",  # 🧙 mage
        "\U0001F981",  # 🦁 lion
        "\U0001F40D",  # 🐍 snake
        "\U0001F985",  # 🦅 eagle
        "\U0001F43A",  # 🐺 wolf
        "\U0001F988",  # 🦈 shark
        "\U0001F419",  # 🐙 octopus
        "\U0001F30B",  # 🌋 volcano
        "\U0001FAA8",  # 🪨 rock
        "\U0001F48E",  # 💎 gem stone
        "\U0001F3F9",  # 🏹 bow and arrow
        "\U0001FA93",  # 🪓 axe
        "\U0001F4A3",  # 💣 bomb
        "\U0001F3AF",  # 🎯 bullseye
        "\U0001F9E8",  # 🧨 firecracker
        "\U0001F52E",  # 🔮 crystal ball
        "\U0001FA84",  # 🪄 magic wand
        "\U0001F479",  # 👹 ogre
        "\U0001F47A",  # 👺 goblin
        "\U0001F982",  # 🦂 scorpion
        "\U0001F577",  # 🕷 spider
        "\U0001F432",  # 🐲 dragon face
        "\U0001F996",  # 🦖 t-rex
        "\U0001F98D",  # 🦍 gorilla
        "\U0001F40A",  # 🐊 crocodile
        "\U0001F405",  # 🐅 tiger
        "\U0001F9AC",  # 🦬 bison
        "\U0001F98F",  # 🦏 rhinoceros
        "\U0001F418",  # 🐘 elephant
        "\U0001F9A7",  # 🦧 orangutan
        "\U0001F43B",  # 🐻 bear
        "\U0001F987",  # 🦇 bat
        "\U0001F41D",  # 🐝 honeybee
        "\U0001F41C",  # 🐜 ant
        "\U0001FAB2",  # 🪲 beetle
        "\U0001F98E",  # 🦎 lizard
        "\U0001F438",  # 🐸 frog
        "\U0001F344",  # 🍄 mushroom
        "\U0001F335",  # 🌵 cactus
        "\U0001F94A",  # 🥊 boxing glove
        "\U0001FA83",  # 🪃 boomerang
        "\U0001F531",  # 🔱 trident
        "\U0001F383",  # 🎃 jack-o-lantern
        "\U0001F921",  # 🤡 clown
        "\U0001F4A9",  # 💩 pile of poo
        "\U0001F9CA",  # 🧊 ice
        "\U0001F311",  # 🌑 new moon
        "\U0001FAE7",  # 🫧 bubbles
        "\U0001F9FF",  # 🧿 nazar amulet
        "\U0001F3B2",  # 🎲 game die
        "\U0001F40E",  # 🐎 horse
        "\U0001F989",  # 🦉 owl
        "\U0001F99D",  # 🦝 raccoon
        "\U0001F994",  # 🦔 hedgehog
        "\U0001F47E",  # 👾 alien monster
        "\U0001F608",  # 😈 smiling face with horns
        "\U0001F52A",  # 🔪 kitchen knife
        "\U0001F9F2",  # 🧲 magnet
    ]


# ── Selection & Bracket ──────────────────────────────────────────────────────

def select_combatants(pool: list[str], rng: random.Random) -> list[str]:
    return rng.sample(pool, 16)


def pair_bracket(combatants: list[str]) -> list[tuple[str, str]]:
    """Standard bracket: seed 1v16, 2v15, … 8v9."""
    n = len(combatants)
    return [(combatants[i], combatants[n - 1 - i]) for i in range(n // 2)]


def pair_adjacent(winners: list[str]) -> list[tuple[str, str]]:
    """Pair adjacent winners for the next round."""
    return [(winners[i], winners[i + 1]) for i in range(0, len(winners), 2)]


# ── Battle Rules ─────────────────────────────────────────────────────────────

RULES = {
    1: {
        "name": "Codepoint Clash",
        "flavor": "Raw numeric power!",
        "verbs": ["overpowers", "demolishes", "outranks", "crushes", "dominates"],
        "reason": "by sheer codepoint supremacy",
    },
    2: {
        "name": "Name Game",
        "flavor": "Whoever has the longer title commands more respect!",
        "verbs": ["out-titles", "flexes on", "schools", "big-names", "overshadows"],
        "reason": "with a mightier name",
    },
    3: {
        "name": "Digital Root Duel",
        "flavor": "Mystical numerology decides the fate!",
        "verbs": [
            "mystically overcomes",
            "spiritually transcends",
            "out-vibes",
            "hexes",
            "channels energy past",
        ],
        "reason": "through arcane digit magic",
    },
    4: {
        "name": "Byte Brawl",
        "flavor": "The heavier fighter crushes the competition!",
        "verbs": ["body-slams", "steamrolls", "flattens", "pile-drives", "out-weighs"],
        "reason": "with superior byte mass",
    },
}

ROUND_NAMES = {1: "Round of 16", 2: "Quarterfinals", 3: "Semifinals", 4: "The Final"}


def emoji_name(ch: str) -> str:
    try:
        return unicodedata.name(ch)
    except ValueError:
        return f"U+{ord(ch):04X}"


def digital_root(n: int) -> int:
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def fight(a: str, b: str, rule_id: int, rng: random.Random) -> tuple[str, str, str]:
    """Return (winner, loser, commentary_line)."""
    rule = RULES[rule_id]
    cp_a, cp_b = ord(a), ord(b)

    if rule_id == 1:
        winner, loser = (a, b) if cp_a > cp_b else (b, a)
        w_detail = f"U+{ord(winner):04X}"
        l_detail = f"U+{ord(loser):04X}"

    elif rule_id == 2:
        name_a, name_b = emoji_name(a), emoji_name(b)
        if len(name_a) != len(name_b):
            winner, loser = (a, b) if len(name_a) > len(name_b) else (b, a)
        else:
            winner, loser = (a, b) if name_a > name_b else (b, a)
        w_detail = f"{len(emoji_name(winner))} chars"
        l_detail = f"{len(emoji_name(loser))} chars"

    elif rule_id == 3:
        dr_a, dr_b = digital_root(cp_a), digital_root(cp_b)
        if dr_a != dr_b:
            winner, loser = (a, b) if dr_a > dr_b else (b, a)
        else:
            winner, loser = (a, b) if cp_a > cp_b else (b, a)
        w_detail = f"root {digital_root(ord(winner))}"
        l_detail = f"root {digital_root(ord(loser))}"

    elif rule_id == 4:
        bytes_a = len(a.encode("utf-8"))
        bytes_b = len(b.encode("utf-8"))
        if bytes_a != bytes_b:
            winner, loser = (a, b) if bytes_a > bytes_b else (b, a)
        else:
            winner, loser = (a, b) if cp_a > cp_b else (b, a)
        w_detail = f"{len(winner.encode('utf-8'))}B"
        l_detail = f"{len(loser.encode('utf-8'))}B"

    else:
        raise ValueError(f"Unknown rule: {rule_id}")

    verb = rng.choice(rule["verbs"])
    commentary = f"    {winner} ({w_detail}) {verb} {loser} ({l_detail}) {rule['reason']}!"
    return winner, loser, commentary


def run_round(
    matchups: list[tuple[str, str]], rule_id: int, rng: random.Random
) -> tuple[list[str], list[tuple[str, str, str]]]:
    """Run all fights. Returns (winners, fight_results) where each result is (winner, loser, commentary)."""
    winners = []
    results = []
    for a, b in matchups:
        winner, loser, commentary = fight(a, b, rule_id, rng)
        winners.append(winner)
        results.append((winner, loser, commentary))
    return winners, results


# ── Display ──────────────────────────────────────────────────────────────────

BAR = "\u2501" * 38  # ━


def print_header(seed: int) -> None:
    print()
    print("\u2554" + "\u2550" * 38 + "\u2557")
    print("\u2551" + f"     \U0001F3DF\uFE0F  EMOJI BATTLE ROYALE  \U0001F3DF\uFE0F      " + "\u2551")
    print("\u2551" + f"         Season of the Seed: {seed:<9}" + "\u2551")
    print("\u255A" + "\u2550" * 38 + "\u255D")
    print()


def print_combatants(matchups: list[tuple[str, str]]) -> None:
    print("  \u2694\uFE0F  THE COMBATANTS  \u2694\uFE0F")
    print()
    for i, (a, b) in enumerate(matchups):
        seed_a = i + 1
        seed_b = 16 - i
        print(f"   [{seed_a:>2}] {a}   vs   [{seed_b:>2}] {b}")
    print()


def print_round(round_num: int, results: list[tuple[str, str, str]], rule_id: int) -> None:
    rule = RULES[rule_id]
    round_name = ROUND_NAMES[round_num]
    print(BAR)
    print(f"  \u2694\uFE0F  ROUND {round_num} \u2014 {round_name}  \u2694\uFE0F")
    print(f"  Rule: {rule['name']}")
    print(f'  "{rule["flavor"]}"')
    print(BAR)
    print()
    for winner, loser, commentary in results:
        # Show the matchup in original order isn't critical; show winner highlighted
        print(f"  {winner} vs {loser}  \u2192  {winner} WINS!")
        print(commentary)
        print()


def print_champion(emoji: str, seed: int) -> None:
    print(BAR)
    print("  \U0001F3C6  THE CHAMPION  \U0001F3C6")
    print(BAR)
    print()
    print(f"        \U0001F451")
    print(f"        {emoji}")
    print()
    print(f"  {emoji} is the Emoji Battle Royale champion!")
    print()
    print(f'  "All hail {emoji}, supreme warrior of Seed {seed}!"')
    print(BAR)
    print()


def print_bracket_final(
    initial_matchups: list[tuple[str, str]],
    all_rounds: list[list[tuple[str, str, str]]],
) -> None:
    """Print a bracket recap showing the tournament progression."""
    print("  \U0001F4CB BRACKET RECAP")
    print()

    champion = all_rounds[3][0][0]

    # Gather round winners
    r1w = [r[0] for r in all_rounds[0]]  # 8 winners
    r2w = [r[0] for r in all_rounds[1]]  # 4 winners
    r3w = [r[0] for r in all_rounds[2]]  # 2 winners

    # Print the bracket as a list of progressions
    # Show each initial matchup and trace the path

    print("  Round of 16    Quarters      Semis         Final")
    print("  " + "\u2500" * 55)

    # The bracket is structured as:
    # Matches 0-1 feed into R2 match 0, matches 2-3 feed into R2 match 1, etc.
    # R2 matches 0-1 feed into R3 match 0, R2 matches 2-3 feed into R3 match 1
    # R3 matches 0-1 feed into R4 match 0

    lines: list[str] = []

    for half in range(2):  # top half (matches 0-3), bottom half (matches 4-7)
        for qpair in range(2):  # two pairs per half
            for mpair in range(2):  # two R1 matches per quarter
                m_idx = half * 4 + qpair * 2 + mpair
                a, b = initial_matchups[m_idx]
                w = r1w[m_idx]

                # First fighter of this R1 match
                lines.append(f"  {a} \u2500\u2510")

                # After first match of a pair: show R2 winner connector
                if mpair == 0:
                    r2_idx = half * 2 + qpair
                    lines.append(f"       \u251C\u2500 {r2w[r2_idx]} \u2500\u2510")
                else:
                    lines.append(f"       \u251C\u2500 {w} \u2500\u2518")

                # Second fighter
                lines.append(f"  {b} \u2500\u2518")

            # After each quarter-pair, show R3 connector
            if qpair == 0:
                r3_idx = half
                lines.append(f"               \u251C\u2500 {r3w[r3_idx]} \u2500\u2510")
            else:
                lines.append(f"               \u251C\u2500 {r3w[r3_idx]} \u2500\u2518")

        # After top half, show final connector
        if half == 0:
            lines.append(f"                       \u251C\u2500 {champion} \U0001F451")

    for line in lines:
        print(line)

    print()


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Emoji Battle Royale")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed for reproducibility")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 999999)
    rng = random.Random(seed)

    pool = load_emoji_pool()
    combatants = select_combatants(pool, rng)
    matchups = pair_bracket(combatants)

    print_header(seed)
    print_combatants(matchups)

    all_rounds: list[list[tuple[str, str, str]]] = []
    current_matchups = matchups

    for round_num in range(1, 5):
        rule_id = round_num
        winners, results = run_round(current_matchups, rule_id, rng)
        all_rounds.append(results)
        print_round(round_num, results, rule_id)

        if round_num < 4:
            current_matchups = pair_adjacent(winners)

    champion = all_rounds[3][0][0]
    print_champion(champion, seed)
    print_bracket_final(matchups, all_rounds)


if __name__ == "__main__":
    main()
