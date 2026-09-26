"""Verify each A/B citation against its own overlapping transcript.

This complements transcript_check.py audit, whose multi-file checks use a union.
Usage: python transcript_source_check.py NOTE SOURCE_A SOURCE_B
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TIMESTAMP = re.compile(r"(?:(?P<src>[AB])\s+)?`(?P<ts>\d{1,2}:\d{2}(?::\d{2})?)`")
QUOTE = re.compile(r'(?<!\*)\*["“]([^"“”*|一-鿿]+?)["”]\*(?!\*)')


def seconds(ts: str) -> int:
    part = [int(x) for x in ts.split(":")]
    return part[0] * 60 + part[1] if len(part) == 2 else part[0] * 3600 + part[1] * 60 + part[2]


def parse(path: Path) -> list[tuple[int, str]]:
    seg = []
    now = None
    words = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if re.fullmatch(r"\d{1,2}:\d{2}(?::\d{2})?", line):
            if now is not None:
                seg.append((now, " ".join(words)))
            now, words = seconds(line), []
        elif now is not None and line:
            words.append(line)
    if now is not None:
        seg.append((now, " ".join(words)))
    return seg


def wordlist(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower().replace("'", ""))


def overlap(quote: str, window: str) -> float:
    core = re.sub(r"\[[^\]]*\]", " ", quote)
    sample = wordlist(core)
    source = wordlist(window)
    if len(sample) < 3:
        return 1.0
    n = 3 if len(sample) >= 6 else 2
    shingles = set(zip(*(source[i:] for i in range(n))))
    target = list(zip(*(sample[i:] for i in range(n))))
    return sum(sh in shingles for sh in target) / len(target) if target else 1.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("note", type=Path)
    ap.add_argument("source_a", type=Path)
    ap.add_argument("source_b", type=Path)
    args = ap.parse_args()
    pools = {"A": parse(args.source_a), "B": parse(args.source_b)}
    secset = {key: {s for s, _ in val} for key, val in pools.items()}
    missing_ts = []
    missing_label = []
    low_quote = []
    n_ts = n_q = 0
    in_cited_cell = False
    for line_no, line in enumerate(args.note.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("**🎙️ 课堂补充**"):
            in_cited_cell = True
        elif line.startswith(("**💡", "**⚠️", "**所以呢", "### ", "#### ", "---")):
            in_cited_cell = False
        hits = list(TIMESTAMP.finditer(line))
        labelled = []
        current = None
        for hit in hits:
            if hit.group("src"):
                current = hit.group("src")
            if current is None:
                continue
            ts = hit.group("ts")
            labelled.append((hit.start(), current, seconds(ts), ts))
            n_ts += 1
            if seconds(ts) not in secset[current]:
                missing_ts.append((line_no, current, ts))
        quotes = list(QUOTE.finditer(line))
        if in_cited_cell and quotes and not labelled:
            missing_label.append(line_no)
        for q in quotes:
            if not labelled:
                continue
            nearest = min(labelled, key=lambda x: (x[0] < q.end(), abs(x[0] - q.end())))
            _, src, sec, ts = nearest
            window = " ".join(text for t, text in pools[src] if sec - 60 <= t <= sec + 120)
            score = overlap(q.group(1), window)
            n_q += 1
            if score < 0.4:
                low_quote.append((line_no, src, ts, round(score, 2), q.group(1)[:70]))
    print(f"source-labelled timestamps checked: {n_ts}; missing: {len(missing_ts)}")
    print(f"source-labelled direct quotes checked: {n_q}; low (<0.4): {len(low_quote)}")
    print(f"quoted classroom-cell lines without same-line A/B citation: {len(missing_label)}")
    for kind, items in (("MISSING TIMESTAMP", missing_ts), ("LOW QUOTE", low_quote), ("MISSING LABEL", missing_label)):
        for item in items[:30]:
            print(kind, item)
    if n_ts == 0:
        print("No A/B-labelled citations were found")
    if n_ts == 0 or missing_ts or low_quote or missing_label:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
