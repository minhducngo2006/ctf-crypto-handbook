# 07 — Lattices, LWE, and proof verifiers

These techniques are model-sensitive. LLL is not an “attack button”; a basis is meaningful only when every coordinate, bound, and scaling factor comes from the challenge equations.

## When a lattice is justified

Typical evidence:

- modular equations with small unknown errors;
- partial nonce/key bits;
- approximate common divisors;
- small polynomial roots modulo a known modulus;
- knapsack/subset-sum structure with challenge-supported density;
- LWE samples `b = A*s + e mod q` with bounded `e`.

Before building a basis, write:

- exact equations;
- modulus or field;
- unknown vector;
- dimension;
- centered error convention;
- numerical bound for every small value;
- desired short/close vector;
- scaling that makes coordinate magnitudes comparable.

## LLL workflow

1. Normalize all modular representatives.
2. Derive a lattice whose target vector corresponds to the unknowns.
3. Explain each row and column in a comment or notebook cell.
4. Derive scaling from explicit bounds—not trial-and-error sweeps.
5. Run LLL/CVP once for the justified model.
6. Decode candidate values.
7. Substitute them into every original equation and check bounds.

If the result fails, diagnose the model: sign, transpose, centered reduction, dimension, or scaling. Do not keep sweeping parameters until readable text appears.

## Hidden Number Problem pattern

Signature leakage often yields a relation resembling:

```text
a_i * secret + b_i ≡ small_i (mod q)
```

The exact `a_i`, `b_i`, sign, and error bound depend on the signature equation and leakage direction. Derive them algebraically from the source. Verify a recovered signing key by reconstructing the public key and checking every signature.

## LWE intake

Canonical form:

```text
b = A*s + e mod q
```

Record:

- matrix dimensions;
- secret distribution;
- error distribution and bound;
- modulus `q`;
- row/column orientation;
- encoding of negative errors;
- number of samples;
- whether samples are exact, rounded, or truncated.

Proof:

```text
centered(b - A*s mod q) == e
```

and every recovered error lies within the stated bound.

## Polynomial and small-root models

For a polynomial relation `f(x) ≡ 0 mod N` with a bounded root, document:

- ring and modulus;
- polynomial coefficients and degree;
- exact root bound;
- whether the root is univariate or multivariate;
- why the theoretical precondition is plausible for supplied parameters.

Verify by evaluating the original polynomial and decoding the root through the original serialization.

## ZKP/proof-verifier audit

Do not focus only on the prover's claim. Follow data into constraints enforced by the verifier.

Audit layers:

1. **Statement binding** — Are all public values included in the transcript/challenge?
2. **Witness constraints** — Does the circuit prove the intended relation or a weaker one?
3. **Canonical encoding** — Can the same value have multiple serialized forms?
4. **Group validation** — Are points on-curve, in-subgroup, and non-identity?
5. **Fiat–Shamir transcript** — Domain tag, field order, lengths, and encodings exact?
6. **Challenge range** — Is the hash reduced correctly and bound to all commitments?
7. **Input validation** — Are attacker-controlled values reduced or accepted unchecked?
8. **Reuse** — Are commitments, challenges, or transcripts repeated?
9. **Comparison target** — Does the verifier compare against the intended statement?

## Positive and negative controls

A convincing verifier test suite includes:

- one known-valid proof that passes;
- the crafted proof that passes for the derived reason;
- a one-byte or one-field mutation that fails;
- an invalid group element that fails when validation is expected;
- a changed public statement that fails if binding is correct.

## Final proof checklist

- [ ] Every basis/constraint coordinate explained.
- [ ] Bounds derived from the challenge.
- [ ] Centered representatives used consistently.
- [ ] Recovered values satisfy all original equations.
- [ ] Recovered errors satisfy all bounds.
- [ ] Real verifier or exact local copy accepts the result.
- [ ] Negative controls fail.

## Guided practice

### Lattices

1. **Learn:** follow the progressive vector, Gram–Schmidt, reduction, and cryptanalysis challenges in [CryptoHack Lattices](https://cryptohack.org/challenges/post-quantum/).
2. **Build:** create one tiny LLL or closest-vector example where every basis coordinate and scale comes from a written bound.
3. **Prove:** substitute the result into every original equation and test every error bound.

### Zero-knowledge proofs

1. **Learn:** use [CryptoHack Zero-Knowledge Proofs](https://cryptohack.org/challenges/zkp/) to study statement/witness relations, completeness, soundness, transcript reuse, and Fiat–Shamir binding.
2. **Build:** write a small local verifier with one valid transcript and at least two invalid controls.
3. **Prove:** require the intended statement to pass while a changed statement, response, or group element fails.

Continue with [Stages 7–8 of the guided learning path](10-guided-learning-path.md#stage-7--lattices-and-bounded-error-models).
