#!/usr/bin/env python3
"""Evidence-first Crypto CTF solver template.

Copy this file into an authorized challenge directory. Keep parsing, derivation,
and verification separate. Delete unused helpers rather than hiding assumptions.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from math import gcd
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "output.txt"


def b2i(data: bytes, byteorder: str = "big") -> int:
    return int.from_bytes(data, byteorder)


def i2b(value: int, length: int | None = None, byteorder: str = "big") -> bytes:
    if value < 0:
        raise ValueError("negative values need an explicit signed encoding")
    if length is None:
        length = max(1, (value.bit_length() + 7) // 8)
    return value.to_bytes(length, byteorder)


def xor_bytes(*parts: bytes) -> bytes:
    if not parts:
        raise ValueError("at least one byte string is required")
    if len({len(part) for part in parts}) != 1:
        raise ValueError("all byte strings must have equal length")
    return bytes(reduce(int.__xor__, values) for values in zip(*parts))


def egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return abs(a), 1 if a >= 0 else -1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def modinv(a: int, modulus: int) -> int:
    if modulus <= 1:
        raise ValueError("modulus must be greater than one")
    g, x, _ = egcd(a % modulus, modulus)
    if g != 1:
        raise ValueError(f"inverse does not exist: gcd={g}")
    inverse = x % modulus
    assert (a * inverse) % modulus == 1
    return inverse


def crt_pair(a1: int, n1: int, a2: int, n2: int) -> tuple[int, int]:
    """Generalized CRT for two consistent congruences."""
    if n1 <= 0 or n2 <= 0:
        raise ValueError("moduli must be positive")
    g = gcd(n1, n2)
    delta = a2 - a1
    if delta % g:
        raise ValueError("inconsistent congruences")
    left, right = n1 // g, n2 // g
    step = (delta // g) * modinv(left, right) % right
    modulus = n1 * right
    value = (a1 + n1 * step) % modulus
    assert value % n1 == a1 % n1
    assert value % n2 == a2 % n2
    return value, modulus


def crt(equations: Iterable[tuple[int, int]]) -> tuple[int, int]:
    equations = list(equations)
    if not equations:
        raise ValueError("at least one congruence is required")
    value, modulus = equations[0]
    for residue, next_modulus in equations[1:]:
        value, modulus = crt_pair(value, modulus, residue, next_modulus)
    return value, modulus


@dataclass(frozen=True)
class PublicData:
    # Replace with fields observed in the supplied artifact.
    raw: bytes


@dataclass(frozen=True)
class DerivedData:
    # Replace with the uniquely derived secret/message/state.
    recovered: bytes


def parse(path: Path) -> PublicData:
    """Parse the artifact exactly; preserve byte-level information."""
    raw = path.read_bytes()
    if not raw:
        raise ValueError(f"empty input: {path}")
    return PublicData(raw=raw)


def derive(public: PublicData) -> DerivedData:
    """Implement one evidence-backed derivation.

    Replace this explicit blocker only after writing the equations and
    falsifiable hypothesis in solve_log.md.
    """
    raise NotImplementedError("derive() requires a challenge-specific model")


def verify(public: PublicData, derived: DerivedData) -> None:
    """Assert every original equation, bound, and round-trip property."""
    if not derived.recovered:
        raise ValueError("recovered result is empty")
    # Add challenge-specific inverse/held-out/verifier assertions here.


def main() -> None:
    public = parse(INPUT)
    derived = derive(public)
    verify(public, derived)
    print(derived.recovered.decode("utf-8", errors="strict"))


if __name__ == "__main__":
    main()
