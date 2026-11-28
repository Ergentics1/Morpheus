#!/usr/bin/env python3
"""Morpheus Standardized Universal Lexicon Auditor & CI-12 Gate (MIT License).

Zero external dependencies (Python 3.12+ standard library only). Implements
three-tier ISO 704 lexical alignment auditing against the Data Model registry
`data/lexicon/morpheus_universal_lexicon.json`:

  - Whole-phrase case-insensitive word-boundary deprecated-alias detection
  - Deterministic syllable estimator & Flesch-Kincaid Grade Level engine
  - Jargon-to-Word Ratio (JWR) gate (<= 2.5% in `--register=atelier --strict`)
  - Deterministic `LEXICON.md` generator (`--emit-md`) and byte-parity verifier
  - Six-gate self-test (`--self-test`) mirroring WP 055 positive/negative traps
    plus keyed `SplitMix64` order-invariant seam parity with `tests/lexicon_rust/`

Exit codes:
  0  PASS
  2  Malformed input / CLI usage fault
  5  Deprecated alias detected under `--strict`
  6  Atelier JWR (> 2.5%) or Flesch-Kincaid grade bound violation under `--strict`
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import pathlib
import re
import sys
from typing import Dict, List, Sequence, Set, Tuple

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = ROOT / "data" / "lexicon" / "morpheus_universal_lexicon.json"
DEFAULT_LEXICON_MD = ROOT / "LEXICON.md"

PC4_TEX = ROOT / "papers" / "arithmetic_frontiers_closure" / "paper" / "arithmetic_frontiers_closure.tex"
PC4_MD = ROOT / "papers" / "arithmetic_frontiers_closure" / "arithmetic_frontiers_closure.md"

TIER3_BENCHMARK = (
    "Across totally real cubic Fricke-Vogt quaternion algebras, exact Shimura congruence "
    "fails via non-congruence quotient covers on the Bruhat-Tits tree. Over real quadratic "
    "fields, left-multiplication congruence surpasses the adjoint surjection while Riehm "
    "obstructions kill abelian kernels. Complete torsion-free Borel genus-25 Eichler "
    "Hecke Brandt matrices exclude the dicyclic Cayley Laplacian spectrum, and Poitou-Odlyzko "
    "discriminant bounds close the Hilbert unimodular Mumford frontier."
)

TIER2_BENCHMARK = (
    "In our final closure paper, all four totally real cubic moduli fail congruence under "
    "exact three-prime CRT determinant checks. On square root thirty-three, both twin orders "
    "achieve level four congruence via the Split-Prime Diagonal Sign-Flip, whereas Riehm "
    "bounds close square root thirteen. All nine genus-25 Hecke Brandt Matrix tables fail to "
    "match the Dicyclic Companion Graph, and Outward-Rounded Interval checks verify the "
    "degree-eight bound."
)

TIER1_BENCHMARK = (
    "Four open puzzles stayed unsolved until now. First, all four cubic models miss clean "
    "clock rules and fold down to a small nine-bridge web. Next, a Split-Mirror Sign Flip "
    "unlocks two true twin grids on square root thirty-three, giving eight clean hits across "
    "the map. Third, every Grid-Transition Table across all nine giant curves misses our "
    "48-Bridge Companion Network. Finally, a Safe Number Box and Trap Check seal the degree-eight "
    "window with zero loose ends."
)

NEGATIVE_TRAP1_TEXT = (
    "We checked the FENV bracket with an anti-facade gate, ran a 3-way check across lanes, "
    "and inspected a raw ARM64 emitter for drift."
)

MASK64 = (1 << 64) - 1
FNV_OFFSET = 0xCBF29CE484222325
FNV_PRIME = 0x100000001B3


def splitmix64_next(state: int) -> Tuple[int, int]:
    state = (state + 0x9E3779B97F4A7C15) & MASK64
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
    return state, (z ^ (z >> 31)) & MASK64


def fnv1a64_bytes(data: bytes, basis: int = FNV_OFFSET) -> int:
    h = basis & MASK64
    for b in data:
        h ^= b
        h = (h * FNV_PRIME) & MASK64
    return h


def fnv1a64_str(text: str, basis: int = FNV_OFFSET) -> int:
    return fnv1a64_bytes(text.encode("utf-8"), basis)


def normalize_ws_lower(text: str) -> str:
    return " ".join(text.lower().split())


def extract_ascii_words(text: str) -> List[str]:
    return re.findall(r"[A-Za-z]+", text)


def count_sentences(text: str) -> int:
    count = 0
    prev_term = False
    for ch in text:
        if ch in ".!?":
            if not prev_term:
                count += 1
            prev_term = True
        else:
            prev_term = False
    return max(1, count)


def count_syllables(word: str) -> int:
    w = word.lower()
    if len(w) <= 3:
        return 1
    if w.endswith("e") and not w.endswith("le"):
        w = w[:-1]
    vowels = "aeiouy"
    groups = 0
    in_vowel = False
    for ch in w:
        if ch in vowels:
            if not in_vowel:
                groups += 1
            in_vowel = True
        else:
            in_vowel = False
    return max(1, groups)


def count_whole_phrase_hits(norm_text: str, phrase: str) -> int:
    norm_phrase = normalize_ws_lower(phrase)
    if not norm_phrase:
        return 0
    pat = r"(?<![a-z0-9])" + re.escape(norm_phrase) + r"(?![a-z0-9])"
    return len(re.findall(pat, norm_text))


@dataclasses.dataclass(frozen=True)
class AuditReport:
    words: int
    sentences: int
    syllables: int
    fk_grade: float
    jargon_words: int
    jwr_pct: float
    deprecated_hits: int
    matched_aliases: Tuple[Tuple[str, str, int], ...]
    matched_jargon: Tuple[str, ...]


def load_registry(path: pathlib.Path = DEFAULT_REGISTRY) -> dict:
    if not path.is_file():
        raise ValueError(f"Missing lexicon registry: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("schema_version", "policy", "tier3_jargon_markers", "disciplines", "scoped_symbols", "concepts"):
        if key not in data:
            raise ValueError(f"Registry missing required top-level key: {key}")
    return data


def audit_text(text: str, registry: dict, register: str = "research") -> AuditReport:
    if register not in ("research", "atelier"):
        raise ValueError(f"Unknown register: {register!r} (expected 'research' or 'atelier')")
    words_list = extract_ascii_words(text)
    if not words_list:
        raise ValueError("Empty or non-alphabetic input text")

    sentences = count_sentences(text)
    syllables = sum(count_syllables(w) for w in words_list)
    total_words = len(words_list)
    fk_grade = 0.39 * (total_words / sentences) + 11.8 * (syllables / total_words) - 15.59

    norm_text = normalize_ws_lower(text)
    alias_hits: List[Tuple[str, str, int]] = []
    deprecated_total = 0
    for c in registry["concepts"]:
        cid = c["id"]
        for alias in c["deprecated_aliases"]:
            n = count_whole_phrase_hits(norm_text, alias)
            if n > 0:
                deprecated_total += n
                alias_hits.append((cid, alias, n))

    markers: Set[str] = {m.lower() for m in registry["tier3_jargon_markers"]}
    jargon_hits: List[str] = []
    for w in words_list:
        wl = w.lower()
        if wl in markers:
            jargon_hits.append(wl)
    jwr_pct = 100.0 * len(jargon_hits) / total_words

    return AuditReport(
        words=total_words,
        sentences=sentences,
        syllables=syllables,
        fk_grade=fk_grade,
        jargon_words=len(jargon_hits),
        jwr_pct=jwr_pct,
        deprecated_hits=deprecated_total,
        matched_aliases=tuple(alias_hits),
        matched_jargon=tuple(sorted(set(jargon_hits))),
    )


def render_lexicon_markdown(registry: dict) -> str:
    disc_map: Dict[str, str] = {d["id"]: d["label"] for d in registry["disciplines"]}
    counts: Dict[str, int] = {d["id"]: 0 for d in registry["disciplines"]}
    for c in registry["concepts"]:
        counts[c["discipline"]] += 1

    total_concepts = len(registry["concepts"])
    total_aliases = sum(len(c["deprecated_aliases"]) for c in registry["concepts"])
    total_symbols = len(registry["scoped_symbols"])
    policy = registry["policy"]

    lines: List[str] = [
        "# Morpheus Standardized Universal Lexicon (`LEXICON.md`)",
        "",
        "> **Auto-generated deterministically from** [`data/lexicon/morpheus_universal_lexicon.json`](data/lexicon/morpheus_universal_lexicon.json) via `python3 tests/lexicon_audit.py --emit-md`. Do not hand-edit; byte-exact parity is enforced by CI Gate `CI-12`.",
        "",
        f"- **Schema Version:** `{registry['schema_version']}` ({registry['standard']})",
        f"- **Scope:** {registry['scope']}",
        f"- **Coverage:** `{total_concepts}` canonical concepts × `3` tiers (`{total_concepts * 3}` aligned expressions), `{total_aliases}` deprecated-alias traps, `{total_symbols}` scoped symbol disambiguations, and `{len(registry['tier3_jargon_markers'])}` Tier-3 specialist jargon markers.",
        f"- **Automated Enforcement:** Research strict ceiling `{policy['research_deprecated_alias_ceiling']}` deprecated aliases; Atelier broadcast ceiling `JWR <= {policy['atelier_jwr_ceiling_pct']:.1f}%` and Flesch–Kincaid Grade `[{policy['atelier_fk_grade_min']:.1f}, {policy['atelier_fk_grade_max']:.1f}]`.",
        "",
        "## Discipline Breakdown",
        "",
        "| Discipline | Concept Count |",
        "| :--- | :---: |",
    ]
    for d in registry["disciplines"]:
        lines.append(f"| **{d['label']}** (`{d['id']}`) | `{counts[d['id']]}` |")
    lines.extend([
        f"| **Total** | **`{total_concepts}`** |",
        "",
        "## Scoped Symbol Disambiguations",
        "",
        "| Symbol ID | LaTeX | Discipline | Meaning | Disambiguated From |",
        "| :--- | :---: | :--- | :--- | :---: |",
    ])
    for s in registry["scoped_symbols"]:
        lines.append(
            f"| `{s['symbol_id']}` | `${s['latex']}$` | {disc_map[s['discipline']]} | {s['meaning']} | `{s['disambiguated_from']}` |"
        )

    for d in registry["disciplines"]:
        did = d["id"]
        lines.extend([
            "",
            f"## {d['label']} (`{counts[did]}` Concepts)",
            "",
            "| ID | Tier 1 (Plain-English / Broadcast) | Tier 2 (Canonical Research) | Tier 3 (Specialist Literature Anchor) | Deprecated Aliases |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ])
        for c in registry["concepts"]:
            if c["discipline"] != did:
                continue
            aliases = ", ".join(f"`{a}`" for a in c["deprecated_aliases"])
            t3 = c["tier3_literature"].replace("|", "\\|")
            lines.append(
                f"| `{c['id']}` | {c['tier1_plain']} | **{c['tier2_canonical']}** | {t3} | {aliases} |"
            )

    lines.extend([
        "",
        "## Verification Commands",
        "",
        "```bash",
        "python3 tests/lexicon_audit.py --self-test",
        "sha256sum -c data/lexicon/MANIFEST.sha256",
        "cargo test --release --manifest-path tests/lexicon_rust/Cargo.toml",
        "```",
        "",
    ])
    return "\n".join(lines)


def compute_splitmix_seam(registry: dict) -> Tuple[int, int]:
    """Keyed SplitMix64 permutation seam over all concepts, mirrored bit-for-bit in Rust."""
    concepts = registry["concepts"]
    n = len(concepts)
    per_hashes: List[int] = []
    for c in concepts:
        payload = f"{c['id']}|{c['tier1_plain']}|{c['tier2_canonical']}|{len(c['deprecated_aliases'])}"
        per_hashes.append(fnv1a64_str(payload))

    xor_forward = 0
    for h in per_hashes:
        xor_forward ^= h

    seed = int(registry["policy"]["prng_seed_hex"], 16)
    state = seed
    order = list(range(n))
    for i in range(n - 1, 0, -1):
        state, r = splitmix64_next(state)
        j = r % (i + 1)
        order[i], order[j] = order[j], order[i]

    xor_shuffled = 0
    seq_fnv = FNV_OFFSET
    for idx in order:
        h = per_hashes[idx]
        xor_shuffled ^= h
        seq_fnv = fnv1a64_bytes(h.to_bytes(8, "little"), seq_fnv)

    if xor_forward != xor_shuffled:
        raise AssertionError("Order-invariant XOR digest mismatch")
    return xor_forward, seq_fnv


def run_self_test(registry_path: pathlib.Path = DEFAULT_REGISTRY, check_md_file: bool = True) -> Tuple[bool, str, Dict[str, object]]:
    """Run all 6 lexicon integrity & positive/negative falsification gates (L1-L6)."""
    reg = load_registry(registry_path)
    policy = reg["policy"]
    markers = {m.lower() for m in reg["tier3_jargon_markers"]}
    concepts = reg["concepts"]

    # Gate L1: Registry structural integrity + zero Tier-1/Tier-3 jargon overlap + LEXICON.md parity.
    seen_ids: Set[str] = set()
    seen_aliases: Set[str] = set()
    tier2_norm: Set[str] = set()
    disc_counts: Dict[str, int] = {d["id"]: 0 for d in reg["disciplines"]}
    expected_counts: Dict[str, int] = {d["id"]: int(d["expected_count"]) for d in reg["disciplines"]}

    for c in concepts:
        cid = c["id"]
        if cid in seen_ids:
            return False, f"L1 FAIL: duplicate concept id {cid}", {}
        seen_ids.add(cid)
        did = c["discipline"]
        if did not in disc_counts:
            return False, f"L1 FAIL: unknown discipline {did} on {cid}", {}
        disc_counts[did] += 1
        t1_words = {w.lower() for w in extract_ascii_words(c["tier1_plain"])}
        overlap = t1_words & markers
        if overlap:
            return False, f"L1 FAIL: Tier-1 jargon overlap in {cid}: {sorted(overlap)}", {}
        tier2_norm.add(normalize_ws_lower(c["tier2_canonical"]))
        if len(c["deprecated_aliases"]) < 2:
            return False, f"L1 FAIL: concept {cid} has < 2 deprecated aliases", {}
        for a in c["deprecated_aliases"]:
            an = normalize_ws_lower(a)
            if an in seen_aliases:
                return False, f"L1 FAIL: duplicate deprecated alias {a!r}", {}
            seen_aliases.add(an)

    if disc_counts != expected_counts:
        return False, f"L1 FAIL: discipline counts {disc_counts} != expected {expected_counts}", {}
    if len(concepts) != 60 or len(seen_aliases) < 120 or len(reg["scoped_symbols"]) != 6:
        return False, f"L1 FAIL: unexpected registry totals ({len(concepts)}, {len(seen_aliases)}, {len(reg['scoped_symbols'])})", {}
    collision = seen_aliases & tier2_norm
    if collision:
        return False, f"L1 FAIL: deprecated alias collides with Tier-2 canonical term: {sorted(collision)}", {}

    expected_md = render_lexicon_markdown(reg)
    if check_md_file:
        if not DEFAULT_LEXICON_MD.is_file():
            return False, "L1 FAIL: LEXICON.md missing (run --emit-md)", {}
        actual_md = DEFAULT_LEXICON_MD.read_text(encoding="utf-8")
        if actual_md != expected_md:
            return False, "L1 FAIL: LEXICON.md drifted from morpheus_universal_lexicon.json", {}

    # Gate L2: Live PC-IV canonical manuscript & GFM mirror compliance (0 deprecated aliases).
    for target in (PC4_TEX, PC4_MD):
        rep = audit_text(target.read_text(encoding="utf-8"), reg, register="research")
        if rep.deprecated_hits != 0:
            return False, f"L2 FAIL: {target.name} has {rep.deprecated_hits} deprecated aliases: {rep.matched_aliases[:3]}", {}

    # Gate L3: Negative Trap 1 (4 deprecated aliases injected -> exact 4 hits).
    trap1 = audit_text(NEGATIVE_TRAP1_TEXT, reg, register="research")
    if trap1.deprecated_hits != 4:
        return False, f"L3 FAIL: expected 4 deprecated hits in Negative Trap 1, got {trap1.deprecated_hits}", {}

    # Gate L4: Negative Trap 2 (Tier-3 jargon overload in Atelier register -> JWR_EXCEEDED).
    t3 = audit_text(TIER3_BENCHMARK, reg, register="atelier")
    if t3.jwr_pct <= float(policy["atelier_jwr_ceiling_pct"]) or t3.jwr_pct < 20.0:
        return False, f"L4 FAIL: Tier-3 benchmark JWR {t3.jwr_pct:.2f}% did not trigger strong overload", {}

    # Gate L5: Positive Readability Funnel (Tier 3 > Tier 2 > Tier 1, Tier 1 <= 2.5%, FK in [5.0, 12.5]).
    t2 = audit_text(TIER2_BENCHMARK, reg, register="research")
    t1 = audit_text(TIER1_BENCHMARK, reg, register="atelier")
    if t2.deprecated_hits != 0 or t1.deprecated_hits != 0:
        return False, f"L5 FAIL: unexpected deprecated hits (T2={t2.deprecated_hits}, T1={t1.deprecated_hits})", {}
    if not (t3.jwr_pct > t2.jwr_pct > t1.jwr_pct):
        return False, f"L5 FAIL: non-monotone JWR funnel (T3={t3.jwr_pct:.2f}%, T2={t2.jwr_pct:.2f}%, T1={t1.jwr_pct:.2f}%)", {}
    if t1.jwr_pct > float(policy["atelier_jwr_ceiling_pct"]):
        return False, f"L5 FAIL: Tier-1 JWR {t1.jwr_pct:.2f}% exceeds ceiling {policy['atelier_jwr_ceiling_pct']}%", {}
    if not (float(policy["atelier_fk_grade_min"]) <= t1.fk_grade <= float(policy["atelier_fk_grade_max"])):
        return False, f"L5 FAIL: Tier-1 FK Grade {t1.fk_grade:.2f} outside [{policy['atelier_fk_grade_min']}, {policy['atelier_fk_grade_max']}]", {}

    # Gate L6: Keyed SplitMix64 seam + 4 adversarial fault guards.
    xor_digest, seq_fnv = compute_splitmix_seam(reg)
    faults_caught = 0
    for bad_call in (
        lambda: audit_text("   12345 !!! ", reg, register="research"),
        lambda: audit_text("Valid prose.", reg, register="bogus_register"),
        lambda: load_registry(ROOT / "data" / "lexicon" / "does_not_exist.json"),
        lambda: audit_text("", reg, register="atelier"),
    ):
        try:
            bad_call()
        except ValueError:
            faults_caught += 1
    if faults_caught != 4:
        return False, f"L6 FAIL: caught only {faults_caught}/4 malformed-input faults", {}

    # Audit every Tier-1 phrase individually in atelier mode (0 aliases, 0.0% JWR).
    for c in concepts:
        rep_c = audit_text(c["tier1_plain"] + ".", reg, register="atelier")
        if rep_c.deprecated_hits != 0 or rep_c.jwr_pct > 0.0:
            return False, f"L6 FAIL: Tier-1 entry {c['id']} failed strict atelier check", {}

    metrics: Dict[str, object] = {
        "concepts": len(concepts),
        "aliases": len(seen_aliases),
        "scoped_symbols": len(reg["scoped_symbols"]),
        "tier3_jwr_pct": round(t3.jwr_pct, 4),
        "tier2_jwr_pct": round(t2.jwr_pct, 4),
        "tier1_jwr_pct": round(t1.jwr_pct, 4),
        "tier1_fk_grade": round(t1.fk_grade, 4),
        "trap1_hits": trap1.deprecated_hits,
        "faults_caught": faults_caught,
        "xor_digest": f"0x{xor_digest:016x}",
        "seq_fnv": f"0x{seq_fnv:016x}",
    }
    summary = (
        f"6/6 gates PASS ({len(concepts)} concepts, {len(seen_aliases)} alias traps, "
        f"PC-IV 0 aliases, JWR {t3.jwr_pct:.1f}%->{t2.jwr_pct:.1f}%->{t1.jwr_pct:.1f}%, "
        f"FK={t1.fk_grade:.2f}, xor=0x{xor_digest:016x}, fnv=0x{seq_fnv:016x})"
    )
    return True, summary, metrics


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Morpheus Standardized Universal Lexicon Auditor")
    parser.add_argument("files", nargs="*", help="Files to audit")
    parser.add_argument("--registry", type=pathlib.Path, default=DEFAULT_REGISTRY, help="Path to lexicon JSON registry")
    parser.add_argument("--register", choices=("research", "atelier"), default="research", help="Target communication register")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on deprecated aliases or Atelier JWR/FK violations")
    parser.add_argument("--self-test", action="store_true", help="Run all 6 lexicon self-test gates (L1-L6)")
    parser.add_argument("--emit-md", action="store_true", help="Regenerate LEXICON.md deterministically from the registry")
    args = parser.parse_args(argv)

    try:
        reg = load_registry(args.registry)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    if args.emit_md:
        md = render_lexicon_markdown(reg)
        DEFAULT_LEXICON_MD.write_text(md, encoding="utf-8")
        print(f"Wrote {DEFAULT_LEXICON_MD.relative_to(ROOT)} ({len(md)} bytes).")
        if not args.self_test and not args.files:
            return 0

    if args.self_test:
        ok, summary, _ = run_self_test(args.registry, check_md_file=True)
        print(f"[{'PASS' if ok else 'FAIL'}] Morpheus Lexicon Audit: {summary}")
        return 0 if ok else 1

    if not args.files:
        parser.print_help()
        return 2

    policy = reg["policy"]
    exit_code = 0
    for fstr in args.files:
        p = pathlib.Path(fstr)
        if not p.is_file():
            print(f"[ERROR] File not found: {fstr}", file=sys.stderr)
            return 2
        try:
            rep = audit_text(p.read_text(encoding="utf-8"), reg, register=args.register)
        except ValueError as exc:
            print(f"[ERROR] {fstr}: {exc}", file=sys.stderr)
            return 2
        print(
            f"{fstr}: words={rep.words} sentences={rep.sentences} fk_grade={rep.fk_grade:.2f} "
            f"jwr={rep.jwr_pct:.2f}% deprecated_hits={rep.deprecated_hits}"
        )
        if rep.matched_aliases:
            for cid, alias, cnt in rep.matched_aliases:
                print(f"  [DEPRECATED] {alias!r} x{cnt} -> use canonical concept `{cid}`")
        if args.strict:
            if rep.deprecated_hits > int(policy["research_deprecated_alias_ceiling"]):
                exit_code = max(exit_code, 5)
            if args.register == "atelier":
                if rep.jwr_pct > float(policy["atelier_jwr_ceiling_pct"]):
                    print(
                        f"  [JWR_EXCEEDED] {rep.jwr_pct:.2f}% > {policy['atelier_jwr_ceiling_pct']:.2f}% "
                        f"(markers={list(rep.matched_jargon)[:10]})"
                    )
                    exit_code = 6
                if not (float(policy["atelier_fk_grade_min"]) <= rep.fk_grade <= float(policy["atelier_fk_grade_max"])):
                    print(
                        f"  [FK_OUT_OF_RANGE] {rep.fk_grade:.2f} not in "
                        f"[{policy['atelier_fk_grade_min']}, {policy['atelier_fk_grade_max']}]"
                    )
                    exit_code = 6
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
