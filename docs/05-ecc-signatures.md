# 05 — ECC and signatures

Elliptic-curve challenges combine group arithmetic, serialization, and transcript rules. Validate the group before attacking a signature equation.

## Curve model

For a short Weierstrass curve over a prime field:

```text
y² = x³ + a*x + b mod p
```

Typical public parameters:

- field prime `p`;
- curve coefficients `a,b`;
- base point `G`;
- subgroup order `n`;
- cofactor `h`;
- public key `Q = d*G`.

Validation checklist:

- `p` and `n` have the expected primality/order properties for the challenge;
- discriminant is non-zero modulo `p`;
- `G` and `Q` lie on the curve;
- `n*G` is the point at infinity;
- public keys are not the point at infinity;
- compressed points use the correct prefix and coordinate length;
- verifier performs subgroup or cofactor checks where required.

## ECDSA

For message hash representative `z`, private key `d`, and nonce `k`:

```text
R = k*G
r = x(R) mod n
s = k⁻¹ * (z + r*d) mod n
```

Verification reconstructs a point using `s⁻¹`, `z`, `r`, and the public key.

### Reused nonce

If two signatures use the same `k`, they have the same `r`:

```text
s1 = k⁻¹(z1 + r*d) mod n
s2 = k⁻¹(z2 + r*d) mod n
```

Subtract:

```text
k = (z1-z2) * (s1-s2)⁻¹ mod n
d = (s1*k-z1) * r⁻¹ mod n
```

Every inverse must exist. Proof:

```text
d*G == Q
```

and every supplied signature verifies under `Q`.

### Related or partially leaked nonces

Do not jump directly to a lattice. First write the exact relation:

```text
k_i = known_i + error_i
```

or

```text
k2 = a*k1 + b mod n
```

Then derive dimensions, centered errors, bounds, and scaling. A recovered `d` is valid only if `d*G=Q` and all signatures verify.

## Schnorr-style signatures

A common form is:

```text
R = k*G
e = H(domain || R || Q || message)
s = k + e*d mod n
```

Nonce reuse gives:

```text
d = (s1-s2) * (e1-e2)⁻¹ mod n
```

The exact sign convention varies. Reconstruct it from the verifier. Hash field order, encodings, and domain-separation tags are part of the equation.

## DSA

DSA has the same core nonce-risk pattern as ECDSA but uses a multiplicative subgroup modulo `p`. Verify recovered keys with the challenge's actual DSA equations and parameters.

## Verifier audit

Inspect what the verifier actually enforces:

- bounds `1 <= r,s < n`;
- canonical signature encoding;
- public-key validity and subgroup membership;
- message bytes hashed versus message displayed;
- domain separation and field ordering;
- acceptance of identity/infinity points;
- reduction of attacker-controlled coordinates;
- duplicate/transcript reuse;
- comparison against the intended statement.

Create both positive and negative tests. A verifier that accepts your intended object but also accepts obviously invalid controls may indicate that your model is incomplete.

## ECC proof checklist

- [ ] Points parse exactly and lie on the intended curve.
- [ ] Subgroup/order assumptions are checked.
- [ ] Hash-to-integer and transcript serialization match the verifier.
- [ ] Nonce relation is proven by supplied signatures or source.
- [ ] All modular inverses exist.
- [ ] Recovered private key satisfies `d*G=Q`.
- [ ] Every original signature verifies.
- [ ] Forgery, if relevant, passes the real verifier and negative controls fail.

## Guided practice

1. **Learn:** complete [CryptoHack Elliptic Curves](https://cryptohack.org/courses/elliptic/) before moving into advanced invalid-curve or biased-nonce problems.
2. **Build:** use selected DSA exercises in [Cryptopals Set 6](https://cryptopals.com/sets/6); treat [Set 8](https://cryptopals.com/sets/8) as advanced material.
3. **Check the standard:** use [NIST FIPS 186-5](https://csrc.nist.gov/pubs/fips/186-5/final) for digital signatures and [RFC 6979](https://www.rfc-editor.org/rfc/rfc6979.html) for deterministic DSA/ECDSA nonce generation.
4. **Prove:** validate points and subgroups, require `d*G == Q`, and verify every signature using the exact transcript encoding.

See [Stage 6 of the guided learning path](10-guided-learning-path.md#stage-6--elliptic-curves-and-signatures).
