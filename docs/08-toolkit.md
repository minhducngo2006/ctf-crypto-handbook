# 08 — Toolkit and environment

Choose a tool because the equations require it—not because the challenge contains a familiar keyword.

## Minimal Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

| Tool | Best use | Do not use it for |
|---|---|---|
| Python standard library | Parsing, integers, GCD, modular exponentiation, byte transforms | Approximate large-number roots |
| PyCryptodome | Exact AES/RSA primitives, padding, local round trips | Choosing an attack automatically |
| SymPy | Exact integer roots, symbolic algebra, number-theory helpers | Blind generic factoring |
| SageMath | Finite fields, elliptic curves, polynomial rings, lattices | Unexplained “run every attack” scripts |
| Z3 | One explicitly derived constraint system | Seed/key enumeration without a model |
| fpylll/Sage LLL | Bounded lattice models with justified scaling | Trial-and-error basis sweeping |
| OpenSSL | Inspecting standard keys/certificates and format conversion | Executing or trusting unknown key material |
| CyberChef | Manual encoding inspection and quick transforms | Reproducible final solvers |

## Safe artifact inspection

```bash
rg --files
file path/to/artifact
xxd -g 1 -l 128 path/to/artifact
sha256sum path/to/artifact
openssl pkey -pubin -in public.pem -text -noout
```

Never send private challenge artifacts to public web tools unless the event rules explicitly permit it.

## Solver layout

```text
challenge-dir/
├── challenge.py          # original, unchanged
├── output.txt            # original, unchanged
├── solve.py              # deterministic solver
├── solve_log.md          # evidence and proof trail
└── evidence/             # generated, non-secret intermediate results
```

The reusable handbook templates are intentionally generic. Copy them into the actual challenge directory rather than placing challenge secrets in this repository.

## Dependency hygiene

- Inspect challenge-supplied `requirements.txt`, lock files, and install scripts.
- Use a disposable virtual environment or container.
- Avoid `sudo pip install`.
- Do not run setup hooks from unknown packages on your main machine.
- Keep package caches and generated files inside the challenge workspace when possible.
- Record versions only when a result depends on library behavior.

## Determinism rules

- Fix seeds for algorithms with randomized internals.
- Use exact integer/rational/finite-field arithmetic.
- Assert dimensions, lengths, and ranges.
- Sort unordered inputs before processing.
- Save the one successful parameter set with its derivation; do not hide sweeps.
- Capture actual solver output in the write-up.

## Command discipline

A useful command should produce one of:

- a new fact;
- a falsified hypothesis;
- a verified equation;
- a reproducible artifact;
- a clear blocker.

Pause after repeated commands that provide none of these. More tooling does not compensate for an undefined model.

## Recommended workflow by scale

| Task | Preferred form |
|---|---|
| One conversion or GCD | Python REPL, then copy the confirmed result into the solver |
| Multi-step derivation | `solve.py` with `parse/derive/verify` |
| Finite fields/ECC/lattices | `solve.sage` with explicit ring/group construction |
| Constraint system | One Z3 model with named equations and assertions |
| Repeatable proof | Standalone script plus captured output |

## Before sharing a solver

- [ ] Remove tokens, cookies, hostnames, and unrelated personal data.
- [ ] Replace event-only network steps with saved transcripts when permitted.
- [ ] Keep challenge author attribution.
- [ ] Include dependencies and exact run command.
- [ ] Ensure failure paths are explicit.
- [ ] Verify the solver from a clean environment.
