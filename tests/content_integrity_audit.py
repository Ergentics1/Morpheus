#!/usr/bin/env python3
"""Morpheus Repository-Wide Content-Integrity Audit Harness (MIT License).

Zero external dependencies (Python 3.12+ standard library only). Enforces
11 deterministic repository-wide integrity gates covering Data Model manifests,
PROVENANCE.md SHA-256 inventories, arXiv bundle hygiene & byte parity, binary
metadata privacy, LaTeX/BibTeX cross-reference integrity, Markdown links,
Lean 4 static trust boundaries, governance ledgers, Code-vs-Data separation,
frozen baseline immutability locks, and cross-paper mathematical seam parity.

Usage:
    python3 tests/content_integrity_audit.py
"""

from __future__ import annotations

import hashlib
import json
import math
import pathlib
import re
import struct
import subprocess
import sys
import tarfile
from typing import Dict, List, Set, Tuple

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Canonical LaTeX papers paired with their arXiv bundles and paper directories.
CANONICAL_PAPERS: List[Tuple[str, str, str, str]] = [
    (
        "Paper #01 (Prime Cadences)",
        "paper/prime-cadences.tex",
        "paper/references.bib",
        "arxiv/prime-cadences-arxiv.tar.gz",
    ),
    (
        "Horizon Synthesis Piece I",
        "papers/horizon_synthesis/piece1_propulsion_hardware/paper/piece1_propulsion_hardware.tex",
        "papers/horizon_synthesis/piece1_propulsion_hardware/paper/references.bib",
        "papers/horizon_synthesis/piece1_propulsion_hardware/arxiv/piece1-propulsion-hardware-arxiv.tar.gz",
    ),
    (
        "Horizon Synthesis Piece II",
        "papers/horizon_synthesis/piece2_smallbody_crtbp/paper/piece2_smallbody_crtbp.tex",
        "papers/horizon_synthesis/piece2_smallbody_crtbp/paper/references.bib",
        "papers/horizon_synthesis/piece2_smallbody_crtbp/arxiv/piece2-smallbody-crtbp-arxiv.tar.gz",
    ),
    (
        "Horizon Synthesis Piece III",
        "papers/horizon_synthesis/piece3_nullcone_tuft_hagedorn/paper/piece3_nullcone_tuft_hagedorn.tex",
        "papers/horizon_synthesis/piece3_nullcone_tuft_hagedorn/paper/references.bib",
        "papers/horizon_synthesis/piece3_nullcone_tuft_hagedorn/arxiv/piece3-nullcone-tuft-hagedorn-arxiv.tar.gz",
    ),
    (
        "Paper PC-II (Triadic Wreath & Nauru)",
        "papers/triadic_wreath_nauru/paper/triadic_wreath_nauru.tex",
        "papers/triadic_wreath_nauru/paper/references.bib",
        "papers/triadic_wreath_nauru/arxiv/triadic-wreath-nauru-arxiv.tar.gz",
    ),
    (
        "Paper PC-III (3-Adic Dic6 & Real-Quadratic Atlas)",
        "papers/triadic_3adic_frontier/paper/triadic_3adic_frontier.tex",
        "papers/triadic_3adic_frontier/paper/references.bib",
        "papers/triadic_3adic_frontier/arxiv/triadic-3adic-frontier-arxiv.tar.gz",
    ),
]

# Rule 5 frozen-baseline waiver for Horizon Synthesis Piece II (v0.4.0 immutable).
FROZEN_UNUSED_BIB_WAIVERS: Dict[str, Set[str]] = {
    "papers/horizon_synthesis/piece2_smallbody_crtbp/paper/references.bib": {"farquhar1973"},
}

# Rule 5 cryptographic immutability locks on frozen archived baselines.
FROZEN_BASELINE_SHA256: Dict[str, str] = {
    "paper/prime-cadences.tex": "82465e8f5e4d96dd50e0b4f6214bb2ad66b9347c637689633699f21c15ca4048",
    "paper/prime-cadences.pdf": "86d0ab607f44c4849acecc8cf0d9e38899c707e51ed8f76ae2ac6371a6bb1111",
    "arxiv/prime-cadences-arxiv.tar.gz": "406da9dab04ae99cecd9b97a119db08a7c2eaed5cf034ac0d4eb4ac915f991a8",
    "cleanroom/prime_cadences_resolution/paper.typ": "e8628cb105c0f2e7cad113985b1d16f4d142aba922011c035c251b7616a8f37b",
    "papers/wp030_shape_propulsion/cleanroom/paper.typ": "f2202e9e69861143c44a233e4d403ab266d0c47e0a8dd09ea8afc449e9ea914e",
    "papers/wp031_3d_j2_hil/cleanroom/paper.typ": "2e30d56dbb545fbf323defd9b4d89b118d6db872468a7ef84c1e2e34515427ae",
    "papers/wp032_bennu_3body/cleanroom/paper.typ": "c2fe46dbf0ee42c714926fae71ec9811d95389074e27c5e0c829809b6a9b89dd",
    "papers/wp033_halo_tag_guidance/cleanroom/paper.typ": "0f659f079a459dff2926ce8a81101ecec911a78dc0d302d632e34f6346eb8a47",
    "papers/wp034_null_cone_gravity/cleanroom/paper.typ": "113cf012a95cc52bc2c9565d92d2888e6d1fb8cbb9958df35eb447c6ff7872b3",
    "papers/wp035_tuft_hagedorn_repair/cleanroom/paper.typ": "56152791320c286ff118a0ab6f357b7baf51970015f5c499aca47b8d1ca29fd8",
    "papers/horizon_synthesis/piece1_propulsion_hardware/paper/piece1_propulsion_hardware.pdf": "a2326e8f7b4e6ef09ce6422493ad81221e4c1c4f4d5103caf8eb53df9c3b177b",
    "papers/horizon_synthesis/piece2_smallbody_crtbp/paper/piece2_smallbody_crtbp.pdf": "c604527415860980630e446644e728ebdea3c1b0dcb99fb183b4a658613f66c8",
    "papers/horizon_synthesis/piece3_nullcone_tuft_hagedorn/paper/piece3_nullcone_tuft_hagedorn.pdf": "51cde9d6a7165237fce25565cacfeeb1bbb895782b980a8748a37a5cef8cff64",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_tracked_files() -> List[str]:
    out = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8")
    tracked = {p for p in out.split("\0") if p}
    # Include untracked non-ignored files in tests/ during pre-commit local runs.
    for p in (ROOT / "tests").rglob("*"):
        if p.is_file() and "__pycache__" not in p.parts:
            tracked.add(p.relative_to(ROOT).as_posix())
    return sorted(tracked)


def gate_ci1_manifests() -> Tuple[bool, str]:
    """CI-1: Verify all MANIFEST.sha256 files using repo-root-relative paths."""
    manifests = sorted(ROOT.rglob("MANIFEST.sha256"))
    if len(manifests) < 12:
        return False, f"Expected >= 12 MANIFEST.sha256 files, found {len(manifests)}"
    checked_entries = 0
    errors: List[str] = []
    for mf in manifests:
        rel_mf = mf.relative_to(ROOT).as_posix()
        lines = [ln.strip() for ln in mf.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if not lines:
            errors.append(f"Empty manifest: {rel_mf}")
            continue
        for ln in lines:
            m = re.match(r"^([0-9a-f]{64})\s+\*?(.+)$", ln)
            if not m:
                errors.append(f"Malformed line in {rel_mf}: {ln}")
                continue
            expected_hash, rel_target = m.group(1), m.group(2)
            if rel_target.startswith("/") or ".." in pathlib.Path(rel_target).parts or "/" not in rel_target:
                errors.append(f"Non-repo-root-relative path in {rel_mf}: {rel_target}")
                continue
            target = ROOT / rel_target
            if not target.is_file():
                errors.append(f"Missing target in {rel_mf}: {rel_target}")
                continue
            actual = sha256_file(target)
            if actual != expected_hash:
                errors.append(f"SHA-256 mismatch in {rel_mf} for {rel_target}: got {actual[:12]} != {expected_hash[:12]}")
            checked_entries += 1
    if errors:
        return False, "; ".join(errors[:5]) + (f" (+{len(errors)-5} more)" if len(errors) > 5 else "")
    return True, f"{len(manifests)}/{len(manifests)} manifests ({checked_entries} JSON entries) exact SHA-256 OK"


def gate_ci2_provenance() -> Tuple[bool, str]:
    """CI-2: Verify every Current SHA-256 row in PROVENANCE.md against disk."""
    prov = ROOT / "PROVENANCE.md"
    if not prov.is_file():
        return False, "PROVENANCE.md missing"
    row_rx = re.compile(r"^\|\s*`([^`]+)`\s*\|[^|]+\|\s*`([0-9a-f]{64})`\s*\|")
    rows = 0
    errors: List[str] = []
    for lineno, line in enumerate(prov.read_text(encoding="utf-8").splitlines(), 1):
        m = row_rx.match(line)
        if not m:
            continue
        rel_path, expected = m.group(1), m.group(2)
        rows += 1
        target = ROOT / rel_path
        if not target.is_file():
            errors.append(f"PROVENANCE.md:{lineno} missing file {rel_path}")
            continue
        actual = sha256_file(target)
        if actual != expected:
            errors.append(f"PROVENANCE.md:{lineno} stale SHA-256 for {rel_path} (disk {actual[:12]} != table {expected[:12]})")
    if rows < 150:
        return False, f"Too few PROVENANCE.md inventory rows parsed ({rows})"
    if errors:
        return False, "; ".join(errors[:5]) + (f" (+{len(errors)-5} more)" if len(errors) > 5 else "")
    return True, f"{rows}/{rows} PROVENANCE.md SHA-256 rows match disk"


def gate_ci3_arxiv_bundles() -> Tuple[bool, str]:
    """CI-3: Verify neutral 0/0 tar headers and byte-for-byte paper/ parity on all 5 arXiv bundles."""
    total_members = 0
    errors: List[str] = []
    for label, tex_rel, _bib_rel, tar_rel in CANONICAL_PAPERS:
        tar_path = ROOT / tar_rel
        paper_dir = (ROOT / tex_rel).parent
        if not tar_path.is_file():
            errors.append(f"Missing tarball: {tar_rel}")
            continue
        with tarfile.open(tar_path, "r:gz") as tf:
            members = [m for m in tf.getmembers() if m.isfile()]
            if not members:
                errors.append(f"Empty tarball: {tar_rel}")
                continue
            for m in members:
                total_members += 1
                if m.uid != 0 or m.gid != 0 or m.uname != "" or m.gname != "":
                    errors.append(f"Non-neutral tar header in {tar_rel}: {m.name} ({m.uid}/{m.gid} {m.uname}/{m.gname})")
                disk_file = paper_dir / m.name
                if not disk_file.is_file():
                    errors.append(f"Tar member {m.name} missing in {paper_dir.relative_to(ROOT)}")
                    continue
                ef = tf.extractfile(m)
                assert ef is not None
                if sha256_bytes(ef.read()) != sha256_file(disk_file):
                    errors.append(f"Parity mismatch in {label}: {m.name}")
    if errors:
        return False, "; ".join(errors[:5])
    return True, f"{len(CANONICAL_PAPERS)}/{len(CANONICAL_PAPERS)} arXiv tarballs ({total_members} members) 0/0 headers & byte-exact parity"


def gate_ci4_binary_privacy() -> Tuple[bool, str]:
    """CI-4: Verify zero PNG text metadata chunks and zero local-path leaks in PDFs."""
    # Construct URI prefix dynamically so security.yml does not self-trigger on this script.
    pdf_leak_rx = re.compile(
        rb"(/home/[A-Za-z0-9._-]+/|/Users/[A-Za-z0-9._-]+/|[A-Za-z]:\\Users\\[A-Za-z0-9._-]+\\|"
        + b"file:"
        + b"///)"
    )
    png_count = 0
    pdf_count = 0
    errors: List[str] = []
    for rel in git_tracked_files():
        p = ROOT / rel
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext == ".png":
            png_count += 1
            data = p.read_bytes()
            pos = 8
            while pos + 8 <= len(data):
                length = struct.unpack(">I", data[pos : pos + 4])[0]
                ctype = data[pos + 4 : pos + 8].decode("ascii", errors="replace")
                if ctype in ("tEXt", "iTXt", "zTXt"):
                    errors.append(f"PNG metadata chunk {ctype} in {rel}")
                pos += 12 + length
        elif ext == ".pdf":
            pdf_count += 1
            if pdf_leak_rx.search(p.read_bytes()):
                errors.append(f"Local path leak in PDF {rel}")
    if errors:
        return False, "; ".join(errors[:5])
    return True, f"{png_count} PNGs & {pdf_count} PDFs clean (0 metadata/path leaks)"


def strip_tex_comments(src: str) -> str:
    out_lines = []
    for line in src.splitlines():
        # Strip unescaped % comments.
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                line = line[:i]
                break
            i += 1
        out_lines.append(line)
    return "\n".join(out_lines)


def gate_ci5_latex_bibtex() -> Tuple[bool, str]:
    """CI-5: Verify zero unresolved/duplicate labels and zero broken/unused BibTeX entries across all 5 papers."""
    errors: List[str] = []
    total_labels = 0
    total_cites = 0
    for label, tex_rel, bib_rel, _tar_rel in CANONICAL_PAPERS:
        tex_src = strip_tex_comments((ROOT / tex_rel).read_text(encoding="utf-8"))
        bib_src = (ROOT / bib_rel).read_text(encoding="utf-8")

        raw_labels = re.findall(r"\\label\{([^}]+)\}", tex_src)
        seen_labels: Set[str] = set()
        for lb in raw_labels:
            if lb in seen_labels:
                errors.append(f"{label}: duplicate label {lb}")
            seen_labels.add(lb)
        total_labels += len(seen_labels)

        refs = re.findall(r"\\(?:eq|page)?ref\{([^}]+)\}", tex_src)
        for rf in refs:
            if rf not in seen_labels:
                errors.append(f"{label}: unresolved ref {rf}")

        bib_keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib_src))
        cite_blocks = re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", tex_src)
        cited: Set[str] = set()
        for blk in cite_blocks:
            for k in blk.split(","):
                k = k.strip()
                if k:
                    cited.add(k)
        total_cites += len(cited)

        missing = sorted(cited - bib_keys)
        if missing:
            errors.append(f"{label}: undefined cites {missing}")
        waived = FROZEN_UNUSED_BIB_WAIVERS.get(bib_rel, set())
        unused = sorted((bib_keys - cited) - waived)
        if unused:
            errors.append(f"{label}: unused bib entries {unused}")

    if errors:
        return False, "; ".join(errors[:5])
    return True, f"{len(CANONICAL_PAPERS)}/{len(CANONICAL_PAPERS)} LaTeX/BibTeX papers clean ({total_labels} labels, {total_cites} cited bib keys, 0 unresolved/unused)"


def strip_md_code(src: str) -> str:
    # Remove fenced code blocks and inline code spans.
    src = re.sub(r"```.*?```", "", src, flags=re.S)
    src = re.sub(r"`[^`\n]+`", "", src)
    return src


def gate_ci6_markdown_links() -> Tuple[bool, str]:
    """CI-6: Verify every relative link across all tracked Markdown files resolves on disk."""
    md_files = [rel for rel in git_tracked_files() if rel.endswith(".md")]
    link_rx = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    checked_links = 0
    errors: List[str] = []
    for rel in md_files:
        md_path = ROOT / rel
        text = strip_md_code(md_path.read_text(encoding="utf-8"))
        for raw_target in link_rx.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            checked_links += 1
            resolved = (md_path.parent / path_part).resolve()
            if not resolved.exists():
                errors.append(f"{rel}: broken link -> {target}")
    if errors:
        return False, "; ".join(errors[:5]) + (f" (+{len(errors)-5} more)" if len(errors) > 5 else "")
    return True, f"{len(md_files)} Markdown files, {checked_links} relative links resolved (0 broken)"


def strip_lean_comments(src: str) -> str:
    # Remove /- ... -/ nested block comments and -- line comments.
    out: List[str] = []
    i, n, depth = 0, len(src), 0
    while i < n:
        if depth == 0 and src[i : i + 2] == "--":
            j = src.find("\n", i)
            i = n if j == -1 else j
            continue
        if src[i : i + 2] == "/-":
            depth += 1
            i += 2
            continue
        if depth > 0 and src[i : i + 2] == "-/":
            depth -= 1
            i += 2
            continue
        if depth == 0:
            out.append(src[i])
        i += 1
    return "".join(out)


def gate_ci7_lean_static_trust() -> Tuple[bool, str]:
    """CI-7: Verify all 9 Lean 4.36.0 projects contain zero sorry/admit/native_decide/unsafe/axiom."""
    lakefiles = sorted(ROOT.rglob("lakefile.toml"))
    if len(lakefiles) < 9:
        return False, f"Expected >= 9 Lean projects, found {len(lakefiles)}"
    forbidden = re.compile(r"\b(sorry|admit|native_decide|unsafe|axiom)\b")
    lean_files_checked = 0
    theorem_count = 0
    errors: List[str] = []
    for lf in lakefiles:
        proj = lf.parent
        tc_path = proj / "lean-toolchain"
        if not tc_path.is_file():
            errors.append(f"Missing lean-toolchain in {proj.relative_to(ROOT)}")
        else:
            tc = tc_path.read_text(encoding="utf-8").strip()
            if tc != "leanprover/lean4:v4.36.0":
                errors.append(f"Toolchain drift in {proj.relative_to(ROOT)}: {tc}")
        for lean_file in sorted(proj.rglob("*.lean")):
            if ".lake" in lean_file.parts:
                continue
            lean_files_checked += 1
            code = strip_lean_comments(lean_file.read_text(encoding="utf-8"))
            theorem_count += len(re.findall(r"^\s*theorem\s+", code, flags=re.M))
            for m in forbidden.finditer(code):
                # Allow string literals inside IO.println diagnostic messages.
                line_start = code.rfind("\n", 0, m.start()) + 1
                line_end = code.find("\n", m.end())
                line = code[line_start : (len(code) if line_end == -1 else line_end)]
                if '"' in line and line.count('"') >= 2:
                    stripped_str = re.sub(r'"[^"]*"', "", line)
                    if not forbidden.search(stripped_str):
                        continue
                errors.append(f"Forbidden token '{m.group(1)}' in {lean_file.relative_to(ROOT)}: {line.strip()}")
    if errors:
        return False, "; ".join(errors[:5])
    return True, f"{len(lakefiles)} Lean 4.36.0 projects ({lean_files_checked} files, {theorem_count} theorems, 0 forbidden tokens)"


def gate_ci8_governance_ledgers() -> Tuple[bool, str]:
    """CI-8: Verify NEGATIVES.md ID uniqueness, CHANGELOG.md ordering, and CITATION.cff fields."""
    errors: List[str] = []

    # NEGATIVES.md unique table IDs
    neg_text = (ROOT / "NEGATIVES.md").read_text(encoding="utf-8")
    ids = re.findall(r"^\|\s*\*\*(NEG-[MEW]\d+)\*\*\s*\|", neg_text, flags=re.M)
    seen: Set[str] = set()
    for nid in ids:
        if nid in seen:
            errors.append(f"Duplicate NEGATIVE ID: {nid}")
        seen.add(nid)
    if len(ids) < 60:
        errors.append(f"Unexpectedly few NEGATIVE IDs parsed: {len(ids)}")

    # CHANGELOG.md structure
    ch_text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if "## [Unreleased]" not in ch_text:
        errors.append("CHANGELOG.md missing ## [Unreleased]")
    vers = re.findall(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})$", ch_text, flags=re.M)
    if len(vers) != len({v for v, _ in vers}):
        errors.append("Duplicate release version in CHANGELOG.md")
    semver_tuples = [tuple(int(x) for x in v.split(".")) for v, _ in vers]
    if semver_tuples != sorted(semver_tuples, reverse=True):
        errors.append(f"CHANGELOG.md versions not strictly descending: {[v for v, _ in vers]}")

    # CITATION.cff required keys
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    for key in ("cff-version:", "title:", "version:", "date-released:"):
        if not re.search(rf"^{re.escape(key)}", cff, flags=re.M):
            errors.append(f"CITATION.cff missing {key}")

    if errors:
        return False, "; ".join(errors[:5])
    return True, f"NEGATIVES.md ({len(ids)} unique IDs), CHANGELOG.md ({len(vers)} ordered releases), CITATION.cff OK"


def gate_ci9_code_data_separation() -> Tuple[bool, str]:
    """CI-9: Verify zero data blobs live inside maintained Code Model directories (Rule 2)."""
    data_exts = {".json", ".csv", ".tsv", ".parquet", ".pkl", ".npy", ".npz"}
    build_config_allowlist = {"lake-manifest.json"}
    code_roots = ("lean/", "rust/", "swiftpp/", "ergentics/", "tests/")
    errors: List[str] = []
    scanned = 0
    for rel in git_tracked_files():
        is_maintained_code = rel.startswith(code_roots) or bool(
            re.match(r"^papers/.+/(code|cpp|lean|rust)/", rel)
        )
        if not is_maintained_code:
            continue
        scanned += 1
        p = pathlib.Path(rel)
        if p.name in build_config_allowlist:
            continue
        if p.suffix.lower() in data_exts:
            errors.append(f"Data blob inside Code Model directory: {rel}")
    if errors:
        return False, "; ".join(errors[:5])
    return True, f"{scanned} maintained Code Model files checked (0 stray data blobs)"


def gate_ci10_frozen_baselines() -> Tuple[bool, str]:
    """CI-10: Verify cryptographic SHA-256 locks on all frozen baseline anchors (Rule 5)."""
    errors: List[str] = []
    for rel, expected in FROZEN_BASELINE_SHA256.items():
        p = ROOT / rel
        if not p.is_file():
            errors.append(f"Frozen anchor missing: {rel}")
            continue
        actual = sha256_file(p)
        if actual != expected:
            errors.append(f"Frozen anchor modified: {rel} ({actual[:12]} != {expected[:12]})")
    if errors:
        return False, "; ".join(errors[:5])
    return True, f"{len(FROZEN_BASELINE_SHA256)}/{len(FROZEN_BASELINE_SHA256)} frozen baseline anchors intact"


def gate_ci11_cross_paper_seam_parity() -> Tuple[bool, str]:
    """CI-11: Verify cross-paper mathematical invariants across Data Model JSONs and Lean axiom audits."""
    errors: List[str] = []
    checks = 0

    def load_json(rel: str) -> dict:
        p = ROOT / rel
        if not p.is_file():
            errors.append(f"Missing calibration JSON: {rel}")
            return {}
        return json.loads(p.read_text(encoding="utf-8"))

    p1 = load_json("data/calibrations/theorem_d_pincer_swiftpp.json")
    p2 = load_json("papers/triadic_wreath_nauru/data/triadic_nauru_calibration.json")
    p3 = load_json("papers/triadic_3adic_frontier/data/triadic_3adic_calibration.json")
    w30 = load_json("papers/wp030_shape_propulsion/data/wp030_g4n_cycle1_calibration.json")
    w33 = load_json("papers/wp033_halo_tag_guidance/data/wp033_g4n_cycle1_calibration.json")
    w35 = load_json("papers/wp035_tuft_hagedorn_repair/data/wp035_g4n_cycle1_calibration.json")
    hs1 = load_json("papers/horizon_synthesis/piece1_propulsion_hardware/data/piece1_calibration.json")
    hs2 = load_json("papers/horizon_synthesis/piece2_smallbody_crtbp/data/piece2_calibration.json")
    hs3 = load_json("papers/horizon_synthesis/piece3_nullcone_tuft_hagedorn/data/piece3_calibration.json")
    if errors:
        return False, "; ".join(errors[:5])

    # 1. Paper #01 <-> PC-III Poitou-Odlyzko (6, 16, 1, 2) margin & FENV bracket
    p1_margin = p1["three_pincer_results"]["deg6_u16_h1_margin"]
    w616 = p3["F8_poitou_odlyzko_audit"]["witness_6_16_1_2"]
    p3_gap = w616["gap"]
    p3_diff = w616["exp_LB_GL128"] - w616["UB_6_16"]
    if not (
        math.isclose(p1_margin, p3_gap, rel_tol=0.0, abs_tol=1e-12)
        and math.isclose(p3_diff, p3_gap, rel_tol=0.0, abs_tol=1e-12)
        and 0.013629809157 <= p1_margin <= 0.013629809162
    ):
        errors.append(f"Paper#01<->PC-III Poitou (6,16,1,2) mismatch: {p1_margin} vs {p3_gap}")
    checks += 1

    # 2. PC-II <-> PC-III shared arithmetic graph & Shimura invariants
    if p2["D3_nauru_weil"]["prime_cadences_even"] != p3["F1_rational_nauru_and_errata"]["nauru_pi_6_to_24"]:
        errors.append("PC-II<->PC-III Nauru pi_Y(6..24) cadence mismatch")
    checks += 1

    if not (p2["D5_lame_fricke_vogt"]["aut_order"] == p3["F1_rational_nauru_and_errata"]["aut_Y_order"] == 144):
        errors.append("PC-II<->PC-III |Aut(Y)| != 144")
    checks += 1

    p2_tplr = p2["D1_non_fusion"]["T_PLR"]
    p3_tplr = p3["F1_rational_nauru_and_errata"]["tplr_group"]
    if (p2_tplr["order"], p2_tplr["commutator_order"], p2_tplr["abelianization_order"]) != (
        p3_tplr["order"],
        p3_tplr["commutator_order"],
        p3_tplr["abelianization_order"],
    ) or p3_tplr["order"] != 144:
        errors.append("PC-II<->PC-III <T,P,L,R> invariant mismatch")
    checks += 1

    f2 = p3["F2_nauru_metric_gonality"]
    if not (p2["D4_tropical"]["gonality"] == f2["star_scramble_h"] == f2["star_scramble_e"] == 6):
        errors.append("PC-II<->PC-III Nauru gonality != 6")
    checks += 1

    d9 = p2["D9_dic6_3adic"]
    f5 = p3["F5_dic6_cayley_spectrum_gonality"]
    if not (
        d9["divisorial_gonality"] == f5["scramble_S4"]["hitting_number"] == f5["scramble_S4"]["egg_cut_number"] == 8
        and d9["aut_order"] == f5["aut_Z_order"] == 96
        and d9["connected_4reg_cayley"] == f5["connected_cayley_count"] == 18
        and d9["strict_ramanujan_4reg_cayley"] == f5["ramanujan_class_size"] == 12
        and d9["weak_ramanujan_4reg_cayley"] == f5["ramanujan_class_size"] + f5["boundary_class_size"] == 18
        and d9["involutions"] == f5["involution_count"] == 43
    ):
        errors.append("PC-II<->PC-III Dic_6 Cayley/gonality/involution mismatch")
    checks += 1

    d12 = p2["D12_3adic_shimura_manin"]
    f7 = p3["F7_genus25_borel_census"]
    p2_curves = {(c["D"], c["N"], c["e2"], c["e3"]) for c in d12["all_19_results"]}
    p3_curves = {(c["D"], c["N"], c["e2"], c["e3"]) for c in f7["curves"]}
    if not (
        d12["total_genus25_pairs"] == f7["total_curves"] == 19
        and d12["torsion_free_pairs"] == f7["torsion_free_count"] == 9
        and d12["survivors"] == f7["pc2_thm73_manin_T3_survivors"] == 0
        and p2_curves == p3_curves
    ):
        errors.append("PC-II<->PC-III genus-25 Borel census mismatch")
    checks += 1

    # 3. PC-III schema 1.1.0 R1/P1 cross-language SplitMix64 digest seam
    p3_r1 = p3.get("R1_runtime_guards_and_fault_injection", {})
    p3_p1 = p3.get("P1_keyed_prng_rct_and_seam_replay", {})
    if not (
        p3.get("schema_version") == "1.1.0"
        and p3_r1.get("pass") is True
        and p3_r1.get("faults_injected") == 6
        and p3_r1.get("faults_rejected") == 6
        and p3_r1.get("laplacian_rank_Y") == 23
        and p3_r1.get("laplacian_rank_Z") == 23
        and p3_p1.get("pass") is True
        and p3_p1.get("order_invariant_replay") is True
        and p3_p1.get("xor_order_invariant_digest") == "0x8aee1bed32dffe97"
        and p3_p1.get("rct_splitmix64_digest") == "0x76597d8f13155b2c"
    ):
        errors.append("PC-III schema 1.1.0 R1/P1 cross-language SplitMix64 seam contract failed")
    checks += 1

    # 4. WP 030-035 <-> Horizon Synthesis headline invariant seams
    wp_hs_pairs = [
        (
            "Thm G1 (WP030<->HS1)",
            w30["checks"]["D3_equilateral_hopf_and_T_shape_divergence"]["t_ratio_q0p95"],
            hs1["results"]["D2"]["g1_ke_q95"],
        ),
        (
            "Thm G3 (WP033<->HS2)",
            w33["checks"]["D1_k11_c149_and_theorem_g3"]["didymos_y_exact_resonance_L_m"],
            hs2["results"]["D4"]["didymos_L_y_star_m"],
        ),
        (
            "NEG-W22 (WP035<->HS3)",
            w35["results"]["D1_trackA_spectral_zeta_eq65_and_neg_w22"]["metrics"]["neg_w22_s3_true_ratio"],
            hs3["results"]["D4"]["S3_true_ratio"],
        ),
        (
            "Thm G6 (WP035<->HS3)",
            w35["results"]["D4_theorem_g6_hagedorn_equivalence_breaking"]["metrics"]["hagedorn_regimes"][
                "chandrasekaran_clock"
            ]["canonical_gamma_rms_disp"],
            hs3["results"]["D5_P1"]["theorem_g6_exact"]["chandrasekaran_257_90"]["gamma_sigma_over_mean"],
        ),
    ]
    for label, a_val, b_val in wp_hs_pairs:
        if not math.isclose(a_val, b_val, rel_tol=0.0, abs_tol=1e-12):
            errors.append(f"{label} mismatch: {a_val} vs {b_val}")
        checks += 1

    # 5. Lean 4.36.0 #print axioms coverage guard across all 9 projects
    lakefiles = sorted(ROOT.rglob("lakefile.toml"))
    ax_total = 0
    for lf in lakefiles:
        proj = lf.parent
        c = 0
        for lean_file in sorted(proj.rglob("*.lean")):
            if ".lake" in lean_file.parts:
                continue
            code = strip_lean_comments(lean_file.read_text(encoding="utf-8"))
            c += len(re.findall(r"^\s*#print\s+axioms\b", code, flags=re.M))
        if c < 7:
            errors.append(f"Lean project {proj.relative_to(ROOT)} has only {c} #print axioms audits")
        ax_total += c
    if ax_total < 149:
        errors.append(f"Expected >= 149 total #print axioms audits across 9 Lean projects, found {ax_total}")
    checks += 1

    if errors:
        return False, "; ".join(errors[:5])
    return True, f"{checks} cross-paper seams verified (Paper#01<->PC-II<->PC-III, WP030-035<->HS, {ax_total} Lean #print axioms)"


def main() -> int:
    gates = [
        ("CI-1", "Data Model MANIFEST.sha256", gate_ci1_manifests),
        ("CI-2", "PROVENANCE.md SHA-256 inventory", gate_ci2_provenance),
        ("CI-3", "arXiv bundles 0/0 headers & parity", gate_ci3_arxiv_bundles),
        ("CI-4", "PNG/PDF metadata privacy", gate_ci4_binary_privacy),
        ("CI-5", "LaTeX/BibTeX cross-references", gate_ci5_latex_bibtex),
        ("CI-6", "Markdown relative link integrity", gate_ci6_markdown_links),
        ("CI-7", "Lean 4.36.0 static trust boundary", gate_ci7_lean_static_trust),
        ("CI-8", "Governance ledgers consistency", gate_ci8_governance_ledgers),
        ("CI-9", "Code-vs-Data Model separation", gate_ci9_code_data_separation),
        ("CI-10", "Frozen baseline SHA-256 locks", gate_ci10_frozen_baselines),
        ("CI-11", "Cross-paper mathematical seam parity", gate_ci11_cross_paper_seam_parity),
    ]
    passed = 0
    print("Running Morpheus 11-gate repository-wide content-integrity audit...")
    for gid, title, fn in gates:
        ok, detail = fn()
        tag = "PASS" if ok else "FAIL"
        print(f"  [{tag}] {gid} ({title}): {detail}")
        if ok:
            passed += 1
    print(f"Summary: {passed}/{len(gates)} content-integrity gates PASS.")
    return 0 if passed == len(gates) else 1


if __name__ == "__main__":
    sys.exit(main())
