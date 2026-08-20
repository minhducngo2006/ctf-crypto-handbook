# 06 — Hashes, MACs, checksums, and PRNGs

These challenges are often about framing and state rather than “breaking” the primitive. Reproduce the exact bytes before analyzing the construction.

## Hash intake

Write the full preimage framing:

```text
domain_tag || length(user) || user || separator || timestamp || payload
```

Record:

- hash algorithm and output length;
- raw digest versus hex/Base64 text;
- field order and separators;
- length encodings and endian order;
- Unicode normalization and text encoding;
- truncation;
- secret position: prefix, suffix, or HMAC key;
- whether two contexts share one domain.

One invisible delimiter can invalidate an otherwise correct derivation.

## Length extension

Merkle–Damgård hashes can permit extension of a construction shaped like:

```text
MAC = H(secret_prefix || message)
```

This does **not** apply to HMAC, secret-suffix MACs in the same way, sponge hashes such as SHA-3, or constructions with different framing.

Preconditions:

- exact vulnerable construction evidenced;
- hash family supports the state continuation model;
- secret length known or uniquely bounded by challenge evidence;
- forged serialized message includes the original hash padding exactly;
- real verifier recomputes the vulnerable form.

Proof requires local reproduction of the original digest and verifier acceptance of the extended message. Do not sweep secret lengths against a remote service.

## HMAC

HMAC is not `H(key || message)`:

```text
H((K' XOR opad) || H((K' XOR ipad) || message))
```

Correctly used HMAC resists ordinary length extension. CTF weaknesses usually lie in key handling, comparison, truncation, parsing, or using different messages on the two sides—not in the HMAC construction itself.

## CRC and linear checksums

CRC and many custom checksums are linear over GF(2), but parameters matter:

- polynomial;
- initial value;
- reflected input/output;
- final XOR;
- byte/bit order;
- included message range.

First reproduce every known checksum. Then derive the requested correction algebraically and validate it with an independent implementation.

## MAC construction traps

Audit:

- raw CBC-MAC used on variable-length messages;
- omitted length/domain binding;
- tag truncation;
- non-constant-time comparison only when the challenge explicitly supplies a safe local model;
- encrypt-and-MAC field disagreements;
- parsing ambiguity between signed and consumed bytes.

Do not perform blind remote timing or tag-candidate loops.

## PRNG workflow

1. Identify the recurrence from source or strongly evidenced output structure.
2. Determine output timing: before or after the state update.
3. Determine truncation, tempering, byte order, and skipped outputs.
4. Count unknown state variables and independent observations.
5. Solve using algebra, GF(2), or one justified SMT model.
6. Reproduce the **entire** observed sequence.
7. Predict a held-out value.

## Linear congruential generator

```text
x[i+1] = a*x[i] + c mod m
```

If `m` is known and full consecutive states are observed, differences can eliminate `c`:

```text
d1 = x1-x0
d2 = x2-x1
a*d1 ≡ d2 mod m
```

An inverse for `d1` exists only when `gcd(d1,m)=1`; otherwise solve the linear congruence with all consistency conditions. Recover `c`, then reproduce every output.

## MT19937 and tempered generators

Full outputs may reveal enough state because tempering is invertible. Before reconstructing:

- confirm generator variant and word size;
- confirm outputs are complete words, not truncated;
- preserve output order;
- account for skipped draws;
- distinguish direct outputs from floats or range-reduced values.

A cloned state must replay the complete observed sequence before predicting anything.

## Truncated-output models

Truncation turns simple state recovery into a constraint problem. Write:

```text
observed_i = truncate(output(state_i))
state_(i+1) = transition(state_i)
```

Use Z3, GF(2), or lattices only when the equations and bounds support them. Do not enumerate seeds unless the challenge explicitly provides a small, justified seed domain and local testing is part of the intended task.

## Proof checklist

- [ ] Framing reproduced byte-for-byte.
- [ ] All known hashes/tags/checksums match.
- [ ] PRNG recurrence and output timing match source/transcript.
- [ ] Recovered state reproduces all observations.
- [ ] At least one held-out value is predicted correctly.
- [ ] No conclusion relies solely on a readable output.

## Guided practice

1. **Learn:** use [CryptoHack Hash Functions](https://cryptohack.org/challenges/hashes/) to connect pre-image, second-preimage, collision, and length-extension concepts to challenges.
2. **Build:** use [Cryptopals Set 3](https://cryptopals.com/sets/3) for MT19937 and [Set 4](https://cryptopals.com/sets/4) for controlled MAC and length-extension exercises.
3. **Check the construction:** consult [NIST FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) for SHA definitions and [RFC 2104](https://www.rfc-editor.org/rfc/rfc2104.html) for HMAC.
4. **Prove:** reproduce all known digests/outputs, predict a held-out value, and include negative MAC tests.

See [Stage 4 of the guided learning path](10-guided-learning-path.md#stage-4--hashes-macs-and-generators).
