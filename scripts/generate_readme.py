#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_readme.py
==================
Scans all .cpp files in the repo root (excluding template.cpp),
parses the structured header comment, and auto-generates README.md.

Header format expected in every solution file:
    * Problem:    Two Sum
    * Platform:   LeetCode
    * Link:       https://leetcode.com/problems/two-sum/
    * Difficulty: Easy
    * Topics:     Arrays, Hashing

Run manually:   python scripts/generate_readme.py
Auto-runs via:  .git/hooks/pre-commit
"""

import io
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── Config ────────────────────────────────────────────────────────────────────

REPO_ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(REPO_ROOT, "README.md")
EXCLUDE     = {"template.cpp"}

DIFFICULTY_ORDER = {"Easy": 0, "Medium": 1, "Hard": 2, "Unknown": 3}

# ── Parser ────────────────────────────────────────────────────────────────────

FIELD_RE = re.compile(r"\*\s*(Problem|Platform|Link|Difficulty|Topics)\s*:\s*(.+)", re.IGNORECASE)

def parse_file(path: str):
    """Extract metadata from the structured header comment of a .cpp file."""
    meta = {
        "file":       os.path.basename(path),
        "problem":    "",
        "platform":   "",
        "link":       "",
        "difficulty": "Unknown",
        "topics":     [],
    }
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            in_header = False
            for line in f:
                stripped = line.strip()
                if stripped.startswith("/*"):
                    in_header = True
                if in_header:
                    m = FIELD_RE.search(stripped)
                    if m:
                        key, val = m.group(1).lower(), m.group(2).strip()
                        if key == "problem":
                            meta["problem"] = val
                        elif key == "platform":
                            meta["platform"] = val
                        elif key == "link":
                            meta["link"] = val if val.startswith("http") else ""
                        elif key == "difficulty":
                            meta["difficulty"] = val.capitalize()
                        elif key == "topics":
                            meta["topics"] = [t.strip() for t in val.split(",") if t.strip()]
                if stripped.endswith("*/") and in_header:
                    break
    except Exception:
        return None

    # Skip files with no problem title (e.g. files you haven't filled yet)
    if not meta["problem"] or meta["problem"].startswith("<"):
        return None
    return meta


def collect_solutions() -> list[dict]:
    solutions = []
    for fname in os.listdir(REPO_ROOT):
        if not fname.endswith(".cpp"):
            continue
        if fname in EXCLUDE:
            continue
        path = os.path.join(REPO_ROOT, fname)
        meta = parse_file(path)
        if meta:
            solutions.append(meta)

    # Sort: difficulty first, then problem name alphabetically
    solutions.sort(key=lambda x: (
        DIFFICULTY_ORDER.get(x["difficulty"], 3),
        x["problem"].lower()
    ))
    return solutions


# ── README Builder ────────────────────────────────────────────────────────────

def build_readme(solutions: list[dict]) -> str:
    total   = len(solutions)
    easy    = sum(1 for s in solutions if s["difficulty"] == "Easy")
    medium  = sum(1 for s in solutions if s["difficulty"] == "Medium")
    hard    = sum(1 for s in solutions if s["difficulty"] == "Hard")

    # Collect all unique topics for the topic index
    topic_map = defaultdict(list)  # topic -> list of solution dicts
    for s in solutions:
        for t in s["topics"]:
            topic_map[t].append(s)

    lines = []

    # Header
    lines += [
        "# Daily Coding - DSA Practice (C++)",
        "",
        "> One problem every day, all solutions in the root directory.",
        "",
        "---",
        "",
    ]

    # Stats
    lines += [
        "## Stats",
        "",
        "| Total | Easy | Medium | Hard |",
        "|:-----:|:----:|:------:|:----:|",
        f"| **{total}** | {easy} | {medium} | {hard} |",
        "",
        "---",
        "",
    ]

    # All Problems Table
    if solutions:
        lines += [
            "## All Problems",
            "",
            "| # | Problem | Difficulty | Topics | Platform | File |",
            "|:-:|---------|:----------:|--------|----------|------|",
        ]
        for i, s in enumerate(solutions, 1):
            topics_str   = ", ".join(s["topics"]) if s["topics"] else "-"
            platform_str = s["platform"] if s["platform"] else "-"
            diff_str     = s["difficulty"]

            if s["link"]:
                problem_cell = f"[{s['problem']}]({s['link']})"
            else:
                problem_cell = s["problem"]

            file_cell = f"[`{s['file']}`]({s['file']})"

            lines.append(
                f"| {i} | {problem_cell} | {diff_str} | {topics_str} | {platform_str} | {file_cell} |"
            )
        lines.append("")
        lines.append("---")
        lines.append("")
    else:
        lines += [
            "## All Problems",
            "",
            "> No solutions yet. Add a `.cpp` file with a filled header and run `python scripts/generate_readme.py`.",
            "",
            "---",
            "",
        ]

    # Topic Index
    if topic_map:
        lines += [
            "## Topic Index",
            "",
            "| Topic | Count | Problems |",
            "|-------|:-----:|----------|",
        ]
        for topic in sorted(topic_map):
            probs = topic_map[topic]
            links = ", ".join(
                f"[{p['problem']}]({p['link']})" if p["link"] else p["problem"]
                for p in probs
            )
            lines.append(f"| {topic} | {len(probs)} | {links} |")
        lines.append("")
        lines.append("---")
        lines.append("")

    # How to Use
    lines += [
        "## How to Use",
        "",
        "```bash",
        "# 1. Copy the template",
        "cp template.cpp problem_name.cpp",
        "",
        "# 2. Fill in the header comment and write your solution",
        "",
        "# 3. Commit -- the README updates automatically",
        "git add problem_name.cpp",
        'git commit -m "Day XX: Problem Name [Difficulty]"',
        "git push",
        "```",
        "",
        "---",
        "",
    ]

    # ── Template Reference ────────────────────────────────────────────────
    lines += [
        "## Solution Template",
        "",
        "```cpp",
        "/*",
        " * Problem:    <Problem Title>",
        " * Platform:   LeetCode",
        " * Link:       https://leetcode.com/problems/...",
        " * Difficulty: Easy | Medium | Hard",
        " * Topics:     Arrays, Hashing",
        " *",
        " * Approach:",
        " *   -",
        " *",
        " * Complexity:",
        " *   Time:  O(?)",
        " *   Space: O(?)",
        " */",
        "```",
        "",
        "---",
        "",
        f"*README auto-generated on {datetime.now().strftime('%Y-%m-%d')} by [`scripts/generate_readme.py`](scripts/generate_readme.py)*",
    ]

    return "\n".join(lines) + "\n"


# ── Entry Point ───────────────────────────────────────────────────────────────

def main():
    solutions = collect_solutions()
    readme    = build_readme(solutions)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"README.md updated -- {len(solutions)} solution(s) indexed.")


if __name__ == "__main__":
    main()
