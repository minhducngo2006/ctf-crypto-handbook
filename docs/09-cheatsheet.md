# 09 — Crypto CTF field cheatsheet

Use this page during a challenge. Follow links to the full chapter before implementing an unfamiliar technique.

## First 10 questions

1. What are the exact input bytes?
2. What encoding and byte order are used?
3. Which values are public, secret, random, or reused?
4. What are their exact lengths and bounds?
5. What equations does the source compute?
6. Where does modular reduction occur?
7. What is padded, hashed, truncated, or serialized?
8. What evidence supports the suspected weakness?
9. What single test would falsify that model?
10. How will the recovered result be independently verified?

## Core Python

```python
from math import gcd

x = int.from_bytes(blob, "big")
blob = x.to_bytes(max(1, (x.bit_length() + 7) // 8), "big")
inv = pow(a, -1, modulus)          # only after gcd(a, modulus) == 1
y = pow(base, exponent, modulus)
g = gcd(a, b)
```

## Core equations

### XOR reuse

```text
C1 XOR C2 = P1 XOR P2
K = C XOR P
```

### CBC targeted delta

```text
C'[i-1] = C[i-1] XOR P[i] XOR P'[i]
```

### RSA

```text
c = m^e mod n
d = e⁻¹ mod phi(n)
m = c^d mod n
```

### ECDSA nonce reuse

```text
k = (z1-z2) * (s1-s2)⁻¹ mod n
d = (s1*k-z1) * r⁻¹ mod n
```

### LCG

```text
x[i+1] = a*x[i] + c mod m
```

### LWE

```text
b = A*s + e mod q
```

## Attack preconditions

| Technique | Required evidence | Required proof |
|---|---|---|
| RSA exact root | `m^e < n` or exact-root model | `root^e == c` and re-encryption |
| RSA shared prime | Multiple supplied moduli | factors multiply back to each modulus |
| RSA common modulus | Same `n,m`, coprime exponents | both ciphertext equations match |
| RSA broadcast | Same unpadded `m,e`, enough coprime moduli | every residue and exact root match |
| CTR/two-time pad | Same full keystream segment | re-encryption of all known bytes |
| CBC transform | Known target block and parser layout | local decrypt/parser acceptance |
| ECDSA nonce reuse | Same commitment/`r` from same nonce | `d*G=Q`, all signatures verify |
| Length extension | Vulnerable secret-prefix hash construction | original digest and forged verifier match |
| PRNG state recovery | Known recurrence and enough outputs | entire sequence replay plus held-out prediction |
| Lattice/HNP/LWE | Exact small-error equations and bounds | all equations and error bounds pass |
| ZKP verifier flaw | Missing constraint/binding evidenced in code | real verifier accepts; negative controls fail |

## “Almost correct” diagnosis

| Symptom | Check first |
|---|---|
| Output shifted by bytes | offset, prefix, IV/nonce placement |
| Correct text missing first zero | fixed-length integer conversion |
| Correct blocks except first | IV parsing |
| Correct message except end | padding and original length |
| ECC points rejected | endian, compression prefix, curve/subgroup |
| Signature math fails | hash-to-integer and sign convention |
| Lattice gives close values | centered residues, transpose, scaling |
| PRNG predicts some outputs | skipped draws, truncation, output timing |
| Local forgery works, service rejects | framing, tag/AAD, verifier mismatch |

## Stop conditions

- Same error three times.
- Two failed tests of the same model.
- Around eight commands without a new fact.
- Next step is blind brute force, wordlist use, or remote candidate spraying.
- Evidence points to another category rather than crypto.

## Final proof

```text
[ ] parse exact
[ ] equations exact
[ ] preconditions proven
[ ] derivation deterministic
[ ] inverse/second verifier passes
[ ] all samples and bounds pass
[ ] final format correct
[ ] no unrelated secrets exposed
```
