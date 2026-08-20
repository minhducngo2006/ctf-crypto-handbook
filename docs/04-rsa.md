# 04 — RSA decision tree

RSA CTFs are usually broken by parameters, relations, padding, leakage, or implementation faults—not by factoring an arbitrary strong modulus.

## Baseline model

```text
n = p*q
phi = (p-1)(q-1)
d = e⁻¹ mod phi
c = m^e mod n
m = c^d mod n
```

Sanity checks:

```python
assert n > 1 and e > 1
assert 0 <= c < n
assert 0 <= m < n
assert pow(m, e, n) == c
```

If padding is used, raw `m` is an encoded message representative; parsing it is a separate verified stage.

## Intake checklist

- Bit lengths of `n`, `e`, and `c`.
- Number of moduli and ciphertexts.
- Whether plaintexts are equal, related, or only share a format.
- Whether exponents differ for the same modulus.
- Whether primes, CRT values, bits, or approximate values leak.
- Whether signatures/decryptions include a faulty result.
- Exact bytes-to-integer and padding construction.

## Route 1: shared factor among supplied moduli

For each pair of supplied moduli:

```text
g = gcd(n1,n2)
```

If `1 < g < n1`, then `g` is a shared factor. This is a bounded deterministic test across challenge-provided values, not generic factoring.

Proof:

```python
assert n1 % g == 0 and n2 % g == 0
assert g * (n1 // g) == n1
assert g * (n2 // g) == n2
```

## Route 2: exact low-exponent root

If the encoded message is small enough that `m^e < n`, modular reduction never occurs and `c = m^e` over the integers.

Test:

```python
from sympy import integer_nthroot

m, exact = integer_nthroot(c, e)
assert exact and m**e == c
assert pow(m, e, n) == c
```

Do not add arbitrary multiples `c + k*n` without a challenge-derived bound or equation.

## Route 3: broadcast / CRT relation

The same unpadded message encrypted with the same small exponent under enough pairwise-coprime moduli can be reconstructed with CRT:

```text
c_i = m^e mod n_i
```

After CRT produces `M ≡ m^e mod product(n_i)`, take an exact `e`-th root only if the combined modulus bound guarantees no wraparound.

Proof:

- every `pow(m,e,n_i) == c_i`;
- CRT residues all match;
- recovered root is exact;
- decoded message round-trips to the same integer.

## Route 4: common modulus

If the same message uses one modulus and exponents `e1,e2` with `gcd(e1,e2)=1`, find Bézout coefficients:

```text
a*e1 + b*e2 = 1
m = c1^a * c2^b mod n
```

Negative exponents require modular inverses, which must exist. Verify with both ciphertext equations.

## Route 5: related messages

If the source proves an affine relation such as:

```text
m2 = a*m1 + b mod n
```

the ciphertext polynomials may share a root. Build the exact polynomial relation in the correct ring and verify the recovered message against every ciphertext. Do not infer related-message structure only from similar decoded prefixes.

## Route 6: artifact-supported weak private parameters

Examples include:

- unusually small private exponent `d`;
- primes intentionally close together;
- leaked high/low bits of a prime or `d`;
- partial CRT components;
- linear relations between factors.

Each route requires evidence and an explicit bound. Use continued fractions, Fermat-style difference of squares, Coppersmith, or lattices only after the supplied parameters satisfy that technique's model.

Factor proof is always:

```python
assert p > 1 and q > 1 and p*q == n
```

## Route 7: CRT fault

A faulty RSA signature or decryption may be correct modulo one prime and wrong modulo the other. Depending on the exact operation, a GCD such as:

```text
gcd(s_good - s_faulty, n)
```

or a verifier-derived difference can expose a factor. Derive the expression from the challenge implementation rather than memorizing one formula.

Verify the fault relation modulo both recovered primes.

## Padding and encoding

PKCS#1 v1.5, OAEP, and custom padding change the message representative. Common mistakes:

- treating padded integer bytes as raw flag bytes;
- dropping a leading zero required by encoding;
- assuming deterministic encryption where randomized padding is used;
- applying textbook RSA attacks when the source uses correct randomized padding;
- decoding before checking the padding structure.

## RSA proof checklist

- [ ] All public integers parsed exactly.
- [ ] Attack precondition derived from supplied evidence.
- [ ] Any factor satisfies `p*q=n`.
- [ ] Any inverse exists and is verified.
- [ ] Recovered `m` satisfies every ciphertext congruence.
- [ ] Padding/serialization is parsed separately.
- [ ] Final bytes round-trip to the same integer.
