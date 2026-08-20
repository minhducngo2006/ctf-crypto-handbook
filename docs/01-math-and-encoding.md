# 01 — Math and encoding foundations

Most failed Crypto CTF solves are parser failures disguised as math failures. Establish the byte model before applying number theory.

## Bytes and integers

Python:

```python
def b2i(data: bytes, byteorder: str = "big") -> int:
    return int.from_bytes(data, byteorder)

def i2b(value: int, length: int | None = None, byteorder: str = "big") -> bytes:
    if value < 0:
        raise ValueError("negative integers need an explicit signed encoding")
    if length is None:
        length = max(1, (value.bit_length() + 7) // 8)
    return value.to_bytes(length, byteorder)
```

Always ask:

- Is byte order big-endian or little-endian?
- Is the length fixed or minimal?
- Are leading `00` bytes meaningful?
- Is the integer signed?
- Was the value reduced modulo another number?

Round-trip test:

```python
assert i2b(b2i(blob), len(blob)) == blob
```

## Hex and Base64

```python
import base64

raw = bytes.fromhex(hex_text.strip())
assert raw.hex() == hex_text.strip().lower()

raw = base64.b64decode(b64_text, validate=True)
assert base64.b64encode(raw).decode() == b64_text
```

Do not repeatedly decode text simply because the next layer is printable. Record every transform and its justification.

## GCD and modular inverse

For integers `a` and `m`, an inverse `a⁻¹ mod m` exists exactly when `gcd(a,m)=1`.

```python
from math import gcd

assert gcd(a, m) == 1
inv = pow(a, -1, m)
assert (a * inv) % m == 1
```

Extended Euclid gives coefficients `x,y` such that:

```text
a*x + b*y = gcd(a,b)
```

This is central to common-modulus RSA, CRT, and linear congruences.

## Linear congruences

Solve:

```text
a*x ≡ b (mod m)
```

Let `g = gcd(a,m)`:

- no solution if `g` does not divide `b`;
- `g` residue classes if it does;
- a unique class modulo `m` only when `g=1`.

Do not call `pow(a,-1,m)` until invertibility is proven.

## Chinese Remainder Theorem

For pairwise-coprime moduli:

```text
x ≡ a1 (mod n1)
x ≡ a2 (mod n2)
...
```

there is one solution modulo `N = n1*n2*...`.

Verification is simple and mandatory:

```python
for residue, modulus in equations:
    assert x % modulus == residue % modulus
```

If moduli are not coprime, use generalized CRT and first check consistency modulo each pairwise GCD.

## Exact integer roots

Floating-point roots are unsafe for cryptography-sized integers. Use an exact routine that returns both root and exactness.

With SymPy:

```python
from sympy import integer_nthroot

root, exact = integer_nthroot(value, exponent)
assert exact
assert root**exponent == value
```

An approximate root that decodes to readable bytes is not proof.

## Centered modular representatives

For error or lattice problems, values modulo `q` are often interpreted in `(-q/2, q/2]`:

```python
def centered(x: int, q: int) -> int:
    x %= q
    return x - q if x > q // 2 else x
```

Using `[0,q)` when the equations assume centered errors can make a correct model look inconsistent.

## XOR as GF(2) addition

For bytes or bit vectors:

```text
x XOR x = 0
x XOR 0 = x
a XOR b XOR b = a
```

```python
def xor_bytes(*parts: bytes) -> bytes:
    if not parts or len({len(p) for p in parts}) != 1:
        raise ValueError("all inputs must have equal length")
    return bytes(v for v in map(lambda t: __import__('functools').reduce(int.__xor__, t), zip(*parts)))
```

For production solver code, prefer the clearer utility in `templates/solve.py`.

## Parsing failure checklist

When output is shifted, nearly correct, or library-dependent, verify:

- [ ] leading zero bytes;
- [ ] integer byte length;
- [ ] endian order;
- [ ] signed versus unsigned conversion;
- [ ] hex/Base64 padding;
- [ ] block boundaries;
- [ ] IV, nonce, and tag placement;
- [ ] PKCS#7 padding rules;
- [ ] point compression prefix and coordinate length;
- [ ] signature encoding: raw pair, ASN.1 DER, or JSON;
- [ ] hash field order and separators;
- [ ] modulo reduction and centered representatives.
