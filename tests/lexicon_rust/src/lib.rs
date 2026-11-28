//! Zero-crate freestanding Pure Rust cross-verifier for the Morpheus Standardized
//! Universal Lexicon (`data/lexicon/morpheus_universal_lexicon.json`, MIT License).
//!
//! Independently implements a minimal UTF-8 JSON parser, ASCII whole-phrase
//! boundary matcher, syllable & Flesch-Kincaid Grade engine, Jargon-to-Word Ratio
//! (JWR) gate, and keyed `SplitMix64` / `FNV-1a64` seam cross-checked bit-for-bit
//! against `tests/lexicon_audit.py`.

use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::{Path, PathBuf};

pub const TIER3_BENCHMARK: &str = "Across totally real cubic Fricke-Vogt quaternion algebras, exact Shimura congruence fails via non-congruence quotient covers on the Bruhat-Tits tree. Over real quadratic fields, left-multiplication congruence surpasses the adjoint surjection while Riehm obstructions kill abelian kernels. Complete torsion-free Borel genus-25 Eichler Hecke Brandt matrices exclude the dicyclic Cayley Laplacian spectrum, and Poitou-Odlyzko discriminant bounds close the Hilbert unimodular Mumford frontier.";

pub const TIER2_BENCHMARK: &str = "In our final closure paper, all four totally real cubic moduli fail congruence under exact three-prime CRT determinant checks. On square root thirty-three, both twin orders achieve level four congruence via the Split-Prime Diagonal Sign-Flip, whereas Riehm bounds close square root thirteen. All nine genus-25 Hecke Brandt Matrix tables fail to match the Dicyclic Companion Graph, and Outward-Rounded Interval checks verify the degree-eight bound.";

pub const TIER1_BENCHMARK: &str = "Four open puzzles stayed unsolved until now. First, all four cubic models miss clean clock rules and fold down to a small nine-bridge web. Next, a Split-Mirror Sign Flip unlocks two true twin grids on square root thirty-three, giving eight clean hits across the map. Third, every Grid-Transition Table across all nine giant curves misses our 48-Bridge Companion Network. Finally, a Safe Number Box and Trap Check seal the degree-eight window with zero loose ends.";

pub const NEGATIVE_TRAP1_TEXT: &str = "We checked the FENV bracket with an anti-facade gate, ran a 3-way check across lanes, and inspected a raw ARM64 emitter for drift.";

pub const EXPECTED_XOR_DIGEST: u64 = 0x9f61_5b24_f0df_d1d2;
pub const EXPECTED_SEQ_FNV: u64 = 0x0345_e680_3850_197e;

const FNV_OFFSET: u64 = 0xcbf2_9ce4_8422_2325;
const FNV_PRIME: u64 = 0x0100_0000_01b3;

#[derive(Debug, Clone)]
pub enum JsonVal {
    Null,
    Bool(bool),
    Num(f64),
    Str(String),
    Arr(Vec<JsonVal>),
    Obj(BTreeMap<String, JsonVal>),
}

impl JsonVal {
    fn as_obj(&self) -> Result<&BTreeMap<String, JsonVal>, String> {
        match self {
            JsonVal::Obj(m) => Ok(m),
            _ => Err("expected JSON object".into()),
        }
    }
    fn as_arr(&self) -> Result<&Vec<JsonVal>, String> {
        match self {
            JsonVal::Arr(a) => Ok(a),
            _ => Err("expected JSON array".into()),
        }
    }
    fn as_str(&self) -> Result<&str, String> {
        match self {
            JsonVal::Str(s) => Ok(s.as_str()),
            _ => Err("expected JSON string".into()),
        }
    }
    fn as_f64(&self) -> Result<f64, String> {
        match self {
            JsonVal::Num(n) => Ok(*n),
            _ => Err("expected JSON number".into()),
        }
    }
}

struct JsonParser<'a> {
    bytes: &'a [u8],
    pos: usize,
}

impl<'a> JsonParser<'a> {
    fn new(src: &'a str) -> Self {
        Self {
            bytes: src.as_bytes(),
            pos: 0,
        }
    }
    fn skip_ws(&mut self) {
        while self.pos < self.bytes.len() {
            match self.bytes[self.pos] {
                b' ' | b'\t' | b'\r' | b'\n' => self.pos += 1,
                _ => break,
            }
        }
    }
    fn peek(&mut self) -> Option<u8> {
        self.skip_ws();
        self.bytes.get(self.pos).copied()
    }
    fn parse_val(&mut self) -> Result<JsonVal, String> {
        match self.peek() {
            Some(b'{') => self.parse_obj(),
            Some(b'[') => self.parse_arr(),
            Some(b'"') => self.parse_str().map(JsonVal::Str),
            Some(b't') => {
                self.expect_lit(b"true")?;
                Ok(JsonVal::Bool(true))
            }
            Some(b'f') => {
                self.expect_lit(b"false")?;
                Ok(JsonVal::Bool(false))
            }
            Some(b'n') => {
                self.expect_lit(b"null")?;
                Ok(JsonVal::Null)
            }
            Some(b'-' | b'0'..=b'9') => self.parse_num().map(JsonVal::Num),
            other => Err(format!("unexpected JSON token {:?} at {}", other, self.pos)),
        }
    }
    fn expect_lit(&mut self, lit: &[u8]) -> Result<(), String> {
        self.skip_ws();
        if self.bytes.get(self.pos..self.pos + lit.len()) == Some(lit) {
            self.pos += lit.len();
            Ok(())
        } else {
            Err(format!("expected literal at {}", self.pos))
        }
    }
    fn parse_str(&mut self) -> Result<String, String> {
        self.skip_ws();
        if self.bytes.get(self.pos) != Some(&b'"') {
            return Err("expected opening quote".into());
        }
        self.pos += 1;
        let mut out = String::new();
        while self.pos < self.bytes.len() {
            let b = self.bytes[self.pos];
            self.pos += 1;
            if b == b'"' {
                return Ok(out);
            }
            if b == b'\\' {
                if self.pos >= self.bytes.len() {
                    return Err("unterminated escape".into());
                }
                let esc = self.bytes[self.pos];
                self.pos += 1;
                match esc {
                    b'"' => out.push('"'),
                    b'\\' => out.push('\\'),
                    b'/' => out.push('/'),
                    b'b' => out.push('\u{0008}'),
                    b'f' => out.push('\u{000C}'),
                    b'n' => out.push('\n'),
                    b'r' => out.push('\r'),
                    b't' => out.push('\t'),
                    b'u' => {
                        if self.pos + 4 > self.bytes.len() {
                            return Err("short unicode escape".into());
                        }
                        let hex = std::str::from_utf8(&self.bytes[self.pos..self.pos + 4])
                            .map_err(|_| "invalid utf8 in escape")?;
                        let code = u32::from_str_radix(hex, 16).map_err(|_| "invalid hex")?;
                        self.pos += 4;
                        let ch = char::from_u32(code).ok_or("invalid unicode scalar")?;
                        out.push(ch);
                    }
                    _ => return Err(format!("unknown escape \\{}", esc as char)),
                }
            } else {
                // Handle multi-byte UTF-8 safely by taking the full char slice.
                let start = self.pos - 1;
                let rest = std::str::from_utf8(&self.bytes[start..])
                    .map_err(|_| "invalid UTF-8 in JSON string")?;
                let ch = rest.chars().next().ok_or("empty UTF-8 slice")?;
                out.push(ch);
                self.pos = start + ch.len_utf8();
            }
        }
        Err("unterminated JSON string".into())
    }
    fn parse_num(&mut self) -> Result<f64, String> {
        self.skip_ws();
        let start = self.pos;
        while self.pos < self.bytes.len() {
            match self.bytes[self.pos] {
                b'-' | b'+' | b'.' | b'e' | b'E' | b'0'..=b'9' => self.pos += 1,
                _ => break,
            }
        }
        let s = std::str::from_utf8(&self.bytes[start..self.pos]).map_err(|_| "bad num")?;
        s.parse::<f64>().map_err(|e| format!("bad number {}: {}", s, e))
    }
    fn parse_arr(&mut self) -> Result<JsonVal, String> {
        self.skip_ws();
        self.pos += 1; // '['
        let mut items = Vec::new();
        if self.peek() == Some(b']') {
            self.pos += 1;
            return Ok(JsonVal::Arr(items));
        }
        loop {
            items.push(self.parse_val()?);
            match self.peek() {
                Some(b',') => self.pos += 1,
                Some(b']') => {
                    self.pos += 1;
                    return Ok(JsonVal::Arr(items));
                }
                _ => return Err(format!("expected ',' or ']' at {}", self.pos)),
            }
        }
    }
    fn parse_obj(&mut self) -> Result<JsonVal, String> {
        self.skip_ws();
        self.pos += 1; // '{'
        let mut map = BTreeMap::new();
        if self.peek() == Some(b'}') {
            self.pos += 1;
            return Ok(JsonVal::Obj(map));
        }
        loop {
            let k = self.parse_str()?;
            if self.peek() != Some(b':') {
                return Err(format!("expected ':' at {}", self.pos));
            }
            self.pos += 1;
            let v = self.parse_val()?;
            map.insert(k, v);
            match self.peek() {
                Some(b',') => self.pos += 1,
                Some(b'}') => {
                    self.pos += 1;
                    return Ok(JsonVal::Obj(map));
                }
                _ => return Err(format!("expected ',' or '}}' at {}", self.pos)),
            }
        }
    }
}

pub fn parse_json(src: &str) -> Result<JsonVal, String> {
    let mut p = JsonParser::new(src);
    let v = p.parse_val()?;
    p.skip_ws();
    if p.pos != p.bytes.len() {
        return Err(format!("trailing JSON bytes at {}", p.pos));
    }
    Ok(v)
}

#[derive(Debug, Clone)]
pub struct Concept {
    pub id: String,
    pub discipline: String,
    pub tier1_plain: String,
    pub tier2_canonical: String,
    pub deprecated_aliases: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct Registry {
    pub atelier_jwr_ceiling_pct: f64,
    pub atelier_fk_grade_min: f64,
    pub atelier_fk_grade_max: f64,
    pub prng_seed: u64,
    pub expected_disciplines: BTreeMap<String, usize>,
    pub scoped_symbol_count: usize,
    pub tier3_markers: BTreeSet<String>,
    pub concepts: Vec<Concept>,
}

#[derive(Debug, Clone)]
pub struct AuditReport {
    pub words: usize,
    pub sentences: usize,
    pub syllables: usize,
    pub fk_grade: f64,
    pub jargon_words: usize,
    pub jwr_pct: f64,
    pub deprecated_hits: usize,
}

pub fn repo_root() -> PathBuf {
    // CARGO_MANIFEST_DIR is `<repo>/tests/lexicon_rust`.
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .and_then(Path::parent)
        .expect("tests/lexicon_rust must live under <repo>/tests/")
        .to_path_buf()
}

pub fn load_registry(path: &Path) -> Result<Registry, String> {
    let src = fs::read_to_string(path).map_err(|e| format!("read {}: {}", path.display(), e))?;
    let root = parse_json(&src)?;
    let obj = root.as_obj()?;
    let policy = obj.get("policy").ok_or("missing policy")?.as_obj()?;
    let atelier_jwr_ceiling_pct = policy
        .get("atelier_jwr_ceiling_pct")
        .ok_or("missing ceiling")?
        .as_f64()?;
    let atelier_fk_grade_min = policy
        .get("atelier_fk_grade_min")
        .ok_or("missing fk_min")?
        .as_f64()?;
    let atelier_fk_grade_max = policy
        .get("atelier_fk_grade_max")
        .ok_or("missing fk_max")?
        .as_f64()?;
    let seed_hex = policy
        .get("prng_seed_hex")
        .ok_or("missing prng_seed_hex")?
        .as_str()?;
    let prng_seed = u64::from_str_radix(seed_hex.trim_start_matches("0x"), 16)
        .map_err(|_| "invalid prng_seed_hex")?;

    let mut expected_disciplines = BTreeMap::new();
    for d in obj.get("disciplines").ok_or("missing disciplines")?.as_arr()? {
        let dm = d.as_obj()?;
        let id = dm.get("id").ok_or("missing disc id")?.as_str()?.to_string();
        let cnt = dm
            .get("expected_count")
            .ok_or("missing expected_count")?
            .as_f64()? as usize;
        expected_disciplines.insert(id, cnt);
    }

    let scoped_symbol_count = obj
        .get("scoped_symbols")
        .ok_or("missing scoped_symbols")?
        .as_arr()?
        .len();

    let mut tier3_markers = BTreeSet::new();
    for m in obj
        .get("tier3_jargon_markers")
        .ok_or("missing tier3_jargon_markers")?
        .as_arr()?
    {
        tier3_markers.insert(m.as_str()?.to_ascii_lowercase());
    }

    let mut concepts = Vec::new();
    for c in obj.get("concepts").ok_or("missing concepts")?.as_arr()? {
        let cm = c.as_obj()?;
        let mut aliases = Vec::new();
        for a in cm
            .get("deprecated_aliases")
            .ok_or("missing deprecated_aliases")?
            .as_arr()?
        {
            aliases.push(a.as_str()?.to_string());
        }
        concepts.push(Concept {
            id: cm.get("id").ok_or("missing id")?.as_str()?.to_string(),
            discipline: cm
                .get("discipline")
                .ok_or("missing discipline")?
                .as_str()?
                .to_string(),
            tier1_plain: cm
                .get("tier1_plain")
                .ok_or("missing tier1_plain")?
                .as_str()?
                .to_string(),
            tier2_canonical: cm
                .get("tier2_canonical")
                .ok_or("missing tier2_canonical")?
                .as_str()?
                .to_string(),
            deprecated_aliases: aliases,
        });
    }

    Ok(Registry {
        atelier_jwr_ceiling_pct,
        atelier_fk_grade_min,
        atelier_fk_grade_max,
        prng_seed,
        expected_disciplines,
        scoped_symbol_count,
        tier3_markers,
        concepts,
    })
}

pub fn splitmix64_next(state: &mut u64) -> u64 {
    *state = state.wrapping_add(0x9e37_79b9_7f4a_7c15);
    let mut z = *state;
    z = (z ^ (z >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
    z ^ (z >> 31)
}

pub fn fnv1a64_bytes(data: &[u8], mut h: u64) -> u64 {
    for &b in data {
        h ^= b as u64;
        h = h.wrapping_mul(FNV_PRIME);
    }
    h
}

pub fn normalize_ws_lower(text: &str) -> String {
    text.to_lowercase()
        .split_whitespace()
        .collect::<Vec<_>>()
        .join(" ")
}

pub fn extract_ascii_words(text: &str) -> Vec<String> {
    let mut out = Vec::new();
    let mut cur = String::new();
    for b in text.bytes() {
        if b.is_ascii_alphabetic() {
            cur.push(b as char);
        } else if !cur.is_empty() {
            out.push(std::mem::take(&mut cur));
        }
    }
    if !cur.is_empty() {
        out.push(cur);
    }
    out
}

pub fn count_sentences(text: &str) -> usize {
    let mut count = 0usize;
    let mut prev_term = false;
    for ch in text.chars() {
        if matches!(ch, '.' | '!' | '?') {
            if !prev_term {
                count += 1;
            }
            prev_term = true;
        } else {
            prev_term = false;
        }
    }
    count.max(1)
}

pub fn count_syllables(word: &str) -> usize {
    let lower = word.to_ascii_lowercase();
    let mut s = lower.as_str();
    if s.len() <= 3 {
        return 1;
    }
    if s.ends_with('e') && !s.ends_with("le") {
        s = &s[..s.len() - 1];
    }
    let mut groups = 0usize;
    let mut in_vowel = false;
    for b in s.bytes() {
        let is_v = matches!(b, b'a' | b'e' | b'i' | b'o' | b'u' | b'y');
        if is_v {
            if !in_vowel {
                groups += 1;
            }
            in_vowel = true;
        } else {
            in_vowel = false;
        }
    }
    groups.max(1)
}

pub fn count_whole_phrase_hits(norm_text: &str, phrase: &str) -> usize {
    let np = normalize_ws_lower(phrase);
    if np.is_empty() {
        return 0;
    }
    let tb = norm_text.as_bytes();
    let pb = np.as_bytes();
    if pb.len() > tb.len() {
        return 0;
    }
    let mut hits = 0usize;
    let mut i = 0usize;
    while i + pb.len() <= tb.len() {
        if &tb[i..i + pb.len()] == pb {
            let left_ok = i == 0 || !tb[i - 1].is_ascii_alphanumeric();
            let right_ok =
                i + pb.len() == tb.len() || !tb[i + pb.len()].is_ascii_alphanumeric();
            if left_ok && right_ok {
                hits += 1;
                i += pb.len();
                continue;
            }
        }
        i += 1;
    }
    hits
}

pub fn audit_text(text: &str, reg: &Registry, register: &str) -> Result<AuditReport, String> {
    if register != "research" && register != "atelier" {
        return Err(format!("unknown register: {}", register));
    }
    let words_list = extract_ascii_words(text);
    if words_list.is_empty() {
        return Err("empty or non-alphabetic input text".into());
    }
    let sentences = count_sentences(text);
    let syllables: usize = words_list.iter().map(|w| count_syllables(w)).sum();
    let total_words = words_list.len();
    let fk_grade =
        0.39 * (total_words as f64 / sentences as f64) + 11.8 * (syllables as f64 / total_words as f64)
            - 15.59;

    let norm_text = normalize_ws_lower(text);
    let mut deprecated_hits = 0usize;
    for c in &reg.concepts {
        for a in &c.deprecated_aliases {
            deprecated_hits += count_whole_phrase_hits(&norm_text, a);
        }
    }

    let jargon_words = words_list
        .iter()
        .filter(|w| reg.tier3_markers.contains(&w.to_ascii_lowercase()))
        .count();
    let jwr_pct = 100.0 * (jargon_words as f64) / (total_words as f64);

    Ok(AuditReport {
        words: total_words,
        sentences,
        syllables,
        fk_grade,
        jargon_words,
        jwr_pct,
        deprecated_hits,
    })
}

pub fn compute_splitmix_seam(reg: &Registry) -> Result<(u64, u64), String> {
    let n = reg.concepts.len();
    let mut per_hashes = Vec::with_capacity(n);
    for c in &reg.concepts {
        let payload = format!(
            "{}|{}|{}|{}",
            c.id,
            c.tier1_plain,
            c.tier2_canonical,
            c.deprecated_aliases.len()
        );
        per_hashes.push(fnv1a64_bytes(payload.as_bytes(), FNV_OFFSET));
    }

    let xor_forward = per_hashes.iter().fold(0u64, |acc, &h| acc ^ h);

    let mut state = reg.prng_seed;
    let mut order: Vec<usize> = (0..n).collect();
    for i in (1..n).rev() {
        let r = splitmix64_next(&mut state);
        let j = (r as usize) % (i + 1);
        order.swap(i, j);
    }

    let mut xor_shuffled = 0u64;
    let mut seq_fnv = FNV_OFFSET;
    for idx in order {
        let h = per_hashes[idx];
        xor_shuffled ^= h;
        seq_fnv = fnv1a64_bytes(&h.to_le_bytes(), seq_fnv);
    }
    if xor_forward != xor_shuffled {
        return Err("order-invariant XOR digest mismatch".into());
    }
    Ok((xor_forward, seq_fnv))
}

pub fn verify_all_six_gates() -> Result<String, String> {
    let root = repo_root();
    let reg = load_registry(&root.join("data/lexicon/morpheus_universal_lexicon.json"))?;

    // Gate L1: Registry integrity & strict Tier-1/Tier-3 separation.
    let mut ids = BTreeSet::new();
    let mut aliases = BTreeSet::new();
    let mut tier2 = BTreeSet::new();
    let mut disc_counts: BTreeMap<String, usize> = BTreeMap::new();
    for c in &reg.concepts {
        if !ids.insert(c.id.clone()) {
            return Err(format!("L1 duplicate id {}", c.id));
        }
        *disc_counts.entry(c.discipline.clone()).or_insert(0) += 1;
        for w in extract_ascii_words(&c.tier1_plain) {
            if reg.tier3_markers.contains(&w.to_ascii_lowercase()) {
                return Err(format!("L1 Tier-1 jargon overlap in {}: {}", c.id, w));
            }
        }
        tier2.insert(normalize_ws_lower(&c.tier2_canonical));
        if c.deprecated_aliases.len() < 2 {
            return Err(format!("L1 concept {} has < 2 aliases", c.id));
        }
        for a in &c.deprecated_aliases {
            if !aliases.insert(normalize_ws_lower(a)) {
                return Err(format!("L1 duplicate alias {}", a));
            }
        }
    }
    if disc_counts != reg.expected_disciplines || reg.concepts.len() != 60 || aliases.len() < 120 || reg.scoped_symbol_count != 6 {
        return Err("L1 unexpected registry counts".into());
    }
    if aliases.iter().any(|a| tier2.contains(a)) {
        return Err("L1 alias collides with Tier-2 canonical term".into());
    }

    // Gate L2: Live PC-IV manuscript & GFM mirror compliance (0 deprecated aliases).
    for rel in [
        "papers/arithmetic_frontiers_closure/paper/arithmetic_frontiers_closure.tex",
        "papers/arithmetic_frontiers_closure/arithmetic_frontiers_closure.md",
    ] {
        let txt = fs::read_to_string(root.join(rel)).map_err(|e| format!("read {}: {}", rel, e))?;
        let rep = audit_text(&txt, &reg, "research")?;
        if rep.deprecated_hits != 0 {
            return Err(format!("L2 {} has {} deprecated aliases", rel, rep.deprecated_hits));
        }
    }

    // Gate L3: Negative Trap 1 (4 injected deprecated aliases).
    let trap1 = audit_text(NEGATIVE_TRAP1_TEXT, &reg, "research")?;
    if trap1.deprecated_hits != 4 {
        return Err(format!("L3 expected 4 deprecated hits, got {}", trap1.deprecated_hits));
    }

    // Gate L4 & L5: Negative Trap 2 & Positive Readability Funnel.
    let t3 = audit_text(TIER3_BENCHMARK, &reg, "atelier")?;
    let t2 = audit_text(TIER2_BENCHMARK, &reg, "research")?;
    let t1 = audit_text(TIER1_BENCHMARK, &reg, "atelier")?;
    if t3.jwr_pct <= reg.atelier_jwr_ceiling_pct || t3.jwr_pct < 20.0 {
        return Err(format!("L4 Tier-3 JWR {:.2}% too low", t3.jwr_pct));
    }
    if t2.deprecated_hits != 0 || t1.deprecated_hits != 0 {
        return Err("L5 unexpected deprecated hits on T2/T1".into());
    }
    if !(t3.jwr_pct > t2.jwr_pct && t2.jwr_pct > t1.jwr_pct && t1.jwr_pct <= reg.atelier_jwr_ceiling_pct) {
        return Err(format!("L5 non-monotone JWR funnel {:.2}% -> {:.2}% -> {:.2}%", t3.jwr_pct, t2.jwr_pct, t1.jwr_pct));
    }
    if !(reg.atelier_fk_grade_min <= t1.fk_grade && t1.fk_grade <= reg.atelier_fk_grade_max) {
        return Err(format!("L5 Tier-1 FK {:.2} out of bounds", t1.fk_grade));
    }

    // Gate L6: Bit-exact SplitMix64 seam parity + 4 fault guards + 60/60 Tier-1 strict check.
    let (xor_d, seq_fnv) = compute_splitmix_seam(&reg)?;
    if xor_d != EXPECTED_XOR_DIGEST || seq_fnv != EXPECTED_SEQ_FNV {
        return Err(format!(
            "L6 SplitMix64 seam mismatch: xor=0x{:016x} fnv=0x{:016x}",
            xor_d, seq_fnv
        ));
    }
    let mut faults = 0usize;
    if audit_text("   12345 !!! ", &reg, "research").is_err() {
        faults += 1;
    }
    if audit_text("Valid prose.", &reg, "bogus_register").is_err() {
        faults += 1;
    }
    if load_registry(&root.join("data/lexicon/does_not_exist.json")).is_err() {
        faults += 1;
    }
    if audit_text("", &reg, "atelier").is_err() {
        faults += 1;
    }
    if faults != 4 {
        return Err(format!("L6 expected 4 faults caught, got {}", faults));
    }
    for c in &reg.concepts {
        let rep = audit_text(&format!("{}.", c.tier1_plain), &reg, "atelier")?;
        if rep.deprecated_hits != 0 || rep.jwr_pct > 0.0 {
            return Err(format!("L6 Tier-1 entry {} failed atelier check", c.id));
        }
    }

    Ok(format!(
        "Rust Lexicon Audit: 6/6 gates PASS ({} concepts, {} alias traps, PC-IV 0 aliases, JWR {:.1}%->{:.1}%->{:.1}%, FK={:.2}, xor=0x{:016x}, fnv=0x{:016x})",
        reg.concepts.len(),
        aliases.len(),
        t3.jwr_pct,
        t2.jwr_pct,
        t1.jwr_pct,
        t1.fk_grade,
        xor_d,
        seq_fnv
    ))
}
