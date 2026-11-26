# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ergentics, LLC -- [GB] Round-1 reconciliation tooling
"""Build the Round-1 reconciled editions (papers/<slug>/paper/) and [GB] dossiers.

The frozen cleanroom/paper.typ is copied line for line; [GB] notes are inserted
as boxed callouts between [E] lines. No [E] line is edited or removed.
Usage (from the repository root):  python3 reconciliation/horizon_round1/build_r1.py
"""
import os, shutil, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from r1_items import PAPERS, ORDER, DATE
from r1_specs import SPECS

COLORS = {"CONFIRMED": "#15803d", "CONFIRMED-IN-SUBSTANCE": "#4d7c0f", "PARTIAL": "#b45309",
          "DISPUTED": "#b91c1c", "UNVERIFIABLE": "#525252", "SPEC-NEEDED": "#1d4ed8", "NEW": "#7e22ce"}
VORDER = list(COLORS)

def tstr(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

def macros(wp):
    cols = ", ".join(f'"{k}": rgb("{v}")' for k, v in COLORS.items())
    return f'''
// ---- [GB] Round-1 reconciliation layer (inserted; [E] lines above and below are unchanged) ----
#let gb-col = ({cols})
#let gbnote(id, verdict, title, body) = block(width: 100%, breakable: true, above: 6pt, below: 6pt,
  inset: (x: 8pt, y: 5.5pt), fill: rgb("#fffaf3"), radius: 1.5pt,
  stroke: (left: 2.2pt + gb-col.at(verdict, default: luma(120))))[
  #set par(first-line-indent: 0pt, hanging-indent: 0pt, justify: true, leading: 0.5em)
  #set text(size: 8.3pt)
  #text(weight: "bold", fill: gb-col.at(verdict, default: luma(80)))[Reconciliation #id · #verdict] — #emph(title) \\
  #body
]
#block(width: 100%, inset: (x: 10pt, y: 7pt), fill: rgb("#f5f3ff"), stroke: 0.6pt + rgb("#7e22ce"), radius: 2pt)[
  #set par(first-line-indent: 0pt, justify: true, leading: 0.5em)
  #set text(size: 8.4pt)
  #text(weight: "bold")[Reconciled edition — Round 1 ({DATE}).]
  #{tstr("The text of Working Paper " + wp + " below is the frozen clean-room manuscript, unchanged. Boxed notes are Grok Bot ([GB]) Round-1 verdicts on the Gemini 4 Neon ([G4N]) Cycle-1 catches and on new [GB] items. Claims that rest on the internal Swift++ corpus are left exactly as written and marked UNVERIFIABLE. Corrections are proposed, not applied in the text; the author decides. A ledger of all verdicts is at the end.")}
]
// ---- end [GB] layer header ----
'''

def note(it):
    return f'#gbnote({tstr(it["id"])}, {tstr(it["verdict"])}, {tstr(it["title"])}, {tstr(it["text"])})\n'

def ledger(items, wp):
    rows = "".join(f'  {tstr(i["id"])}, {tstr(i["title"])}, text(fill: gb-col.at({tstr(i["verdict"])}), weight: "bold", {tstr(i["verdict"])}),\n' for i in items)
    c = collections.Counter(i["verdict"] for i in items)
    counts = ", ".join(f"{k} {c[k]}" for k in VORDER if c[k])
    return f'''
// ---- [GB] Round-1 ledger (inserted) ----
#heading(numbering: none)[Reconciliation Ledger (Grok Bot, Round 1)]
#block[
#set par(first-line-indent: 0pt, hanging-indent: 0pt)
#set text(size: 8pt)
#table(columns: (auto, 1fr, auto), inset: 4pt, stroke: 0.4pt + luma(170),
  table.header([*ID*], [*Item*], [*Verdict*]),
{rows})
#text(size: 8pt)[#{tstr("Totals: " + counts + ". Full evidence, reproduction commands and run specs: reconciliation/GROKBOT_WP" + wp + "_ROUND1.md in this paper's folder.")}]
]
// ---- end [GB] ledger ----
'''

def is_heading(l):
    s = l.lstrip()
    return (s.startswith("=") and not s.startswith("==>")) or s.startswith("#heading(")

def refs_index(lines):
    for k in range(len(lines) - 1, -1, -1):
        if "References" in lines[k] and (is_heading(lines[k]) or lines[k].startswith("#text(")):
            j = k
            while j > 0 and (lines[j-1].strip() == "" or lines[j-1].startswith("//") or lines[j-1].startswith("#v(") or lines[j-1].startswith("#line(")):
                j -= 1
            return j
    raise SystemExit("no References heading")

def build_paper(root, slug):
    P = PAPERS[slug]; base = os.path.join(root, "papers", slug)
    src = open(os.path.join(base, "cleanroom", "paper.typ"), encoding="utf-8").read().split("\n")
    items = P["items"]
    after = collections.defaultdict(list); before_refs = []
    heads = [k for k, l in enumerate(src) if is_heading(l)]
    for it in items:
        if it["anchor"] == "@refs":
            before_refs.append(it); continue
        hits = [k for k in heads if it["anchor"] in src[k]]
        if len(hits) != 1:
            raise SystemExit(f"{slug}: anchor {it['anchor']!r} matched {len(hits)} headings")
        after[hits[0]].append(it)
    first = next(k for k in heads if src[k].lstrip().startswith("= "))
    ri = refs_index(src)
    out = []
    for k, l in enumerate(src):
        if k == first:
            out.append(macros(P["wp"]))
        if k == ri:
            out += [note(i) for i in before_refs]
            out.append(ledger(items, P["wp"]))
        out.append(l)
        if k in after:
            out += [note(i) for i in after[k]]
    if src[0].startswith("//"):
        out.insert(0, "// [GB] Round-1 reconciled edition: clean-room [E] text unchanged, with inserted reconciliation notes.")
    pd = os.path.join(base, "paper"); os.makedirs(pd, exist_ok=True)
    open(os.path.join(pd, "paper.typ"), "w", encoding="utf-8").write("\n".join(out))
    fsrc = os.path.join(base, "cleanroom", "figures")
    if os.path.isdir(fsrc):
        shutil.copytree(fsrc, os.path.join(pd, "figures"), dirs_exist_ok=True)
    for f in os.listdir(os.path.join(base, "cleanroom")):
        if f.lower().endswith((".svg", ".png", ".jpg", ".pdf")):
            shutil.copy2(os.path.join(base, "cleanroom", f), os.path.join(pd, f))
    # sanity: every [E] line survives in order
    it = iter(out)
    assert all(any(l == o for o in it) for l in src), "an [E] line was lost"
    return pd

def md_table(items):
    s = "| ID | Item | Verdict | Placed under |\n| :--- | :--- | :--- | :--- |\n"
    for i in items:
        where = "end of paper (before References)" if i["anchor"] == "@refs" else f"§ “{i['anchor']}”"
        s += f"| `{i['id']}` | {i['title']} | **{i['verdict']}** | {where} |\n"
    return s

def build_dossier(root, slug):
    P = PAPERS[slug]; items = P["items"]
    c = collections.Counter(i["verdict"] for i in items)
    counts = " · ".join(f"{k} {c[k]}" for k in VORDER if c[k])
    scripts = "\n".join(f"python3 reconciliation/horizon_round1/code/{s}" for s in P["scripts"])
    body = [f"# Grok Bot (`[GB]`) Round-1 Reconciliation — Working Paper {P['wp']}",
            "", f"*{P['short']}* · Round 1 · {DATE} · Method: ADPIE, as in the Morpheus v0.2.0 and round-2/3 reconciliations.", "",
            "## Scope and rules", "",
            "- Inputs: the frozen `cleanroom/` manuscript and the `[G4N]` Cycle-1 dossier in this folder. `[GB]` checks were written from scratch, without reading `[G4N]` code or data; `[G4N]`'s verifiers were then re-run separately.",
            "- The reconciled edition is [`../paper/paper.typ`](../paper/paper.typ) → [`../paper/paper.pdf`](../paper/paper.pdf): every `[E]` line is kept verbatim and in order; verdicts are inserted as boxed notes. Corrections are proposed, not applied.",
            "- Claims attributed to the Ergentics internal model / Swift++ corpus are never altered. Where they can't be checked from this repository they are marked **UNVERIFIABLE**.",
            "", f"**Verdict totals:** {counts}", "", "## Verdict table", "", md_table(items), "## Evidence", ""]
    for i in items:
        body += [f"### `{i['id']}` — {i['title']} · **{i['verdict']}**", "", i["text"], ""]
    if SPECS.get(slug, "").strip():
        body += ["## Run spec requested from the author", "", SPECS[slug].strip(), ""]
    body += ["## Reproduce (from the repository root)", "", "```bash", scripts,
             f"python3 papers/{slug}/code/*.py   # [G4N] plane 1",
             f"lake -d papers/{slug}/lean build   # [G4N] plane 2 (Lean 4.36.0)",
             f"cargo test --manifest-path papers/{slug}/rust/Cargo.toml   # [G4N] plane 3",
             f"typst compile papers/{slug}/paper/paper.typ", "```", ""]
    d = os.path.join(root, "papers", slug, "reconciliation"); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"GROKBOT_WP{P['wp']}_ROUND1.md")
    open(p, "w", encoding="utf-8").write("\n".join(body))
    return p

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    which = sys.argv[2:] or ORDER
    for slug in which:
        print(build_paper(root, slug)); print(build_dossier(root, slug))
