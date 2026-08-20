#!/usr/bin/env python3
"""Safe toy RSA example demonstrating derivation plus proof.

The parameters are intentionally tiny and are not suitable for real security.
"""

from math import gcd


def main() -> None:
    p, q = 61, 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    assert gcd(e, phi) == 1

    d = pow(e, -1, phi)
    assert (e * d) % phi == 1
    assert p * q == n

    message = 65
    ciphertext = pow(message, e, n)
    recovered = pow(ciphertext, d, n)

    assert recovered == message
    assert pow(recovered, e, n) == ciphertext

    print(f"n={n} e={e} d={d}")
    print(f"ciphertext={ciphertext} recovered={recovered}")
    print("verification=PASS")


if __name__ == "__main__":
    main()
