# Morpheus Data Model (`data/`)

Immutable, schema-typed, SHA-256-checksummed research outputs (**CC BY 4.0**).

> **Non-conflation rule:** Executable code in `swiftpp/`, `lean/`, and `rust/` (MIT License) never reads files from `data/` as proof of verification; it recomputes from first principles and writes validated records here only via explicit CLI export flags.

## Verification

Check integrity of all Data Model artifacts against the manifest:

```bash
sha256sum -c data/MANIFEST.sha256
sha256sum -c data/lexicon/MANIFEST.sha256
```

## Layout

- `calibrations/` — Rung-1 distributional calibration and RCT outputs conforming to [`CALIBRATIONS.md`](../CALIBRATIONS.md) (`schema_version: "1.0.0"`).
- `lexicon/` — Morpheus Standardized Universal Lexicon (`morpheus_universal_lexicon.json`, `60` three-tier ISO 704 concepts, `120` deprecated-alias traps, `6` scoped symbols, SHA-256 manifested) enforced by CI Gate `CI-12` ([`../LEXICON.md`](../LEXICON.md)).
- `MANIFEST.sha256` — SHA-256 checksums for every immutable record in `data/`.
