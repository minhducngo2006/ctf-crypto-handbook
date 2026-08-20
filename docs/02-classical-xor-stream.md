# 02 — Classical ciphers, XOR, and stream constructions

This family rewards alignment and invariants. Avoid candidate scoring until the challenge supplies a justified key space or crib; prefer direct transforms and exact relations.

## Classical cipher intake

Record:

- exact alphabet and whether case is preserved;
- treatment of spaces, digits, punctuation, and non-ASCII symbols;
- grouping or transposition width;
- known prefix, suffix, or flag format;
- whether the implementation transforms characters or raw bytes.

### Caesar and affine forms

Caesar:

```text
E(x) = x + k mod m
D(y) = y - k mod m
```

Affine:

```text
E(x) = a*x + b mod m
D(y) = a⁻¹*(y-b) mod m
```

The affine multiplier must satisfy `gcd(a,m)=1`. Verify by encrypting the full recovered plaintext and comparing every symbol.

### Transposition

Transposition preserves symbol counts. Use provided grid dimensions, route hints, or source code to reconstruct the permutation. Do not guess widths solely by visual appeal.

## Single-byte and repeating XOR

Fundamental relation:

```text
C = P XOR K
K = C XOR P
P = C XOR K
```

If a known plaintext segment is evidenced:

```python
keystream = bytes(c ^ p for c, p in zip(cipher_segment, known_plaintext))
```

For a repeating key of length `L`, bytes with the same index modulo `L` share a key byte. Establish `L` from source, explicit hints, repeated structure, or a justified statistical model—never accept the first printable candidate as proof.

Verification:

```python
assert xor_repeat(recovered_plaintext, key) == ciphertext
```

## Two-time pad / keystream reuse

If two messages use the same stream:

```text
C1 = P1 XOR K
C2 = P2 XOR K
C1 XOR C2 = P1 XOR P2
```

This removes the keystream but does not automatically reveal either plaintext. A valid recovery needs challenge-supported structure, a known segment, or enough equations to determine the messages uniquely.

Once one plaintext segment is known, derive only the matching keystream segment and verify it against all ciphertexts at those positions.

## Known-plaintext alignment

For every crib, document:

- why the text is expected;
- the exact byte encoding;
- the tested offset;
- the predicted keystream or counterpart bytes;
- a held-out position that the model must predict.

Do not slide a crib across every offset against a remote service. Local alignment tests are appropriate only when the artifact itself supports the model.

## LFSR and linear recurrences

An LFSR is linear over GF(2). A typical recurrence is:

```text
s[i+n] = c0*s[i] + c1*s[i+1] + ... + c(n-1)*s[i+n-1]  over GF(2)
```

Workflow:

1. Extract output bits in the correct order.
2. Confirm whether output occurs before or after the state update.
3. Build the linear system from the observed recurrence.
4. Solve for state/taps using exact GF(2) arithmetic.
5. Reproduce the complete observed sequence.
6. Predict a held-out bit or byte.

Bit order is a frequent trap: MSB-first and LSB-first streams can look like unrelated failures.

## Stream cipher checklist

- [ ] Nonce length and location known.
- [ ] Counter start and endian order known.
- [ ] Keystream reuse proven, not assumed.
- [ ] Plaintext/ciphertext alignment exact.
- [ ] Every derived keystream byte explained by known data or equations.
- [ ] Re-encryption reproduces all observed ciphertext bytes.

## Common false positives

- Printable text produced by one of many unproved keys.
- English scoring that ignores binary or structured plaintext.
- Repeating-key length chosen only because it gives a nice output.
- A known flag prefix applied at an arbitrary offset.
- LFSR state that predicts training bits but fails held-out output.

## Guided practice

1. **Learn:** use [CryptoHack Introduction](https://cryptohack.org/courses/intro/) to review encoding and XOR properties.
2. **Build:** complete the conversion and XOR progression in [Cryptopals Set 1](https://cryptopals.com/sets/1) with local tests.
3. **Prove:** reapply the recovered key or keystream and require an exact match with every supplied ciphertext byte.

Do not use English scoring as the only verifier. See [Stage 1 of the guided learning path](10-guided-learning-path.md#stage-1--encoding-xor-and-classical-structure).
