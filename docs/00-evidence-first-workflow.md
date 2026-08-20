# 00 — Evidence-first workflow

Use this chapter for every Crypto CTF, regardless of primitive. It prevents the most common failure mode: selecting an attack from a keyword before reconstructing what the challenge actually computes.

## The loop

```text
scope → preserve → parse → model → hypothesize → derive → verify → document
```

## 1. Confirm scope and preserve evidence

- Work only with the supplied challenge directory and explicitly authorized service.
- Save original files unchanged. Put generated outputs in clearly named files.
- Record hashes for important binary artifacts when accidental modification is possible.
- Treat source, archives, notebooks, and dependencies as untrusted input.
- Do not execute an unknown file merely because its extension looks familiar.

Recommended first commands:

```bash
rg --files
file -- *
sha256sum challenge.py output.txt
sed -n '1,240p' challenge.py
```

Inspect the primary source or transcript before reading peripheral files.

## 2. Build an exact inventory

Write down only observable values:

| Field | Questions |
|---|---|
| Encoding | Hex, Base64, decimal integer, raw bytes, JSON, PEM, custom alphabet? |
| Length | Exact byte/bit/block length? Leading zeroes preserved? |
| Public values | Modulus, exponent, curve, point, nonce, IV, tag, signature? |
| Unknowns | Key, message, state, nonce, factors, error vector? |
| Bounds | Message size, prime size, error magnitude, timestamp range? |
| Reuse | Same key, modulus, IV, nonce, commitment, prefix, or state? |
| Verification | Local checker, decryption routine, signature verifier, flag format? |

Avoid words such as “probably AES-CBC” in the FACT section. A block length of 16 bytes is a fact; an AES-CBC classification is a hypothesis until the source or behavior supports it.

## 3. Reconstruct the scheme

Translate the implementation into explicit stages:

```text
message bytes
  → padding/framing
  → bytes-to-integer or block split
  → mathematical/cryptographic operation
  → truncation/serialization
  → printed transcript
```

For every stage, capture:

- input type and length;
- output type and length;
- endianness;
- modular reduction;
- padding or delimiter rules;
- truncation, slicing, or dropped leading zeroes;
- hash domain and field order.

Create a tiny parser that reproduces the public input. Do not begin cryptanalysis while the parser is “almost right.”

## 4. Separate claims

Use four labels in `solve_log.md`:

- **FACT** — directly observed and reproducible.
- **INFERENCE** — follows logically from facts.
- **HYPOTHESIS** — predicts an observation and has one falsifiable test.
- **BLOCKER** — missing evidence or a method outside scope.

Example:

```text
FACT: c is 127 bytes and n is a 1024-bit integer.
INFERENCE: c is in the valid RSA ciphertext range 0 <= c < n.
H1: plaintext is small enough that m^3 < n.
TEST: compute the exact integer cube root and require root^3 == c.
PROOF: re-encrypt recovered m with pow(m, 3, n) and compare with c.
```

## 5. Select one justified family

Choose the first test with the strongest direct evidence and cheapest independent verifier. Good tests produce a binary result:

- exact root or not;
- GCD is 1 or exposes a supplied shared factor;
- recurrence reproduces every output or it does not;
- forged transcript passes the real verifier or it does not.

Do not run generic attack collections “to see what works.” They obscure why a result is valid and often create false positives.

## 6. Implement the smallest solver

Use three stages:

```python
public = parse(INPUT)
secret = derive(public)
verify(public, secret)
```

Requirements:

- assert every assumption;
- fail loudly on ambiguous parsing;
- use exact integer/field arithmetic;
- keep one source of truth for constants;
- print the final answer only after verification;
- use a fixed seed when an algorithm contains randomized internals.

## 7. Verify independently

Prefer at least two of these:

1. inverse operation: encrypt, sign, hash, or step the recurrence again;
2. substitution into all original equations;
3. held-out transcript or output;
4. second implementation using a different library or direct arithmetic;
5. real local verifier with positive and negative cases;
6. in-scope remote acceptance of one uniquely derived answer.

## 8. Know when to stop or pivot

Pause the current route when:

- roughly eight commands produce no new fact;
- the same error appears three times;
- two tests falsify the same model;
- the next action would be brute force or blind remote probing;
- evidence shows the dominant task is reverse engineering, forensics, web, or pwn rather than cryptanalysis.

Record the blocker before switching paths. A clean rejection of a model is progress.

## Final handoff checklist

- [ ] Original artifacts preserved.
- [ ] Public values and encodings documented.
- [ ] Exact equations written.
- [ ] Attack choice tied to evidence.
- [ ] One complete solver saved.
- [ ] Solver output recorded.
- [ ] Independent verification passed.
- [ ] Flag format validated.
- [ ] No unrelated secrets included.
