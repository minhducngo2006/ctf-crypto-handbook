# 10 — Guided learning path

This path turns the handbook into a course without turning it into a link dump. Each stage follows the same loop:

```text
learn one idea → implement the smallest useful primitive → solve selected challenges → prove your result
```

## How the sources are used

| Source | Best role | How to use it here |
|---|---|---|
| [CryptoHack Courses](https://cryptohack.org/courses/) | Guided explanation and short interactive challenges | Learn a concept, then reproduce it in a local script without copying a solution |
| [Cryptopals](https://cryptopals.com/) | Programming-heavy exercises that build and then break constructions | Treat each set as a project; keep tests for every primitive you implement |
| [NIST Cryptographic Standards and Guidelines](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines) | Precise definitions, approved constructions, and current standards context | Consult after the concept is clear; use it to check names, inputs, and security conditions |
| [RFC Editor](https://www.rfc-editor.org/) | Protocol and format specifications such as PKCS #1 and HMAC | Read only the sections needed to reproduce the exact encoding or algorithm |

CryptoHack and Cryptopals teach by doing. NIST publications and RFCs are references, not beginner tutorials. Reading a standard too early often hides the main idea under implementation detail.

## Progress rule

Do not mark a stage complete because a challenge accepted a flag. Keep these three outputs:

1. a small implementation or parser;
2. a `solve_log.md` entry explaining the relevant equation;
3. a test that would fail if your model were wrong.

Move forward when you can explain the result without reading someone else's solve script.

## Stage 0 — Build the workbench

**Goal:** manipulate bytes safely and keep challenge work reproducible.

Read:

- [Handbook 00 — Evidence-first workflow](00-evidence-first-workflow.md)
- [Handbook 08 — Toolkit](08-toolkit.md)
- [CryptoHack Introduction](https://cryptohack.org/courses/intro/)

Build:

- hex, Base64, bytes, and integer conversion helpers;
- equal-length and repeating-key XOR helpers;
- a solver skeleton with `parse`, `derive`, and `verify` stages.

Exit check:

```text
bytes → integer → bytes returns the original fixed-length value
hex → bytes → Base64 matches a trusted test vector
xor(xor(message, key), key) == message
```

## Stage 1 — Encoding, XOR, and classical structure

**Goal:** see byte alignment and invariants before reaching for statistics.

Read and practice:

- [Handbook 01 — Math and encoding](01-math-and-encoding.md)
- [Handbook 02 — Classical, XOR, and streams](02-classical-xor-stream.md)
- [CryptoHack Introduction](https://cryptohack.org/courses/intro/) for encoding and XOR
- [Cryptopals Set 1](https://cryptopals.com/sets/1) for conversion, XOR, repeating-key XOR, and ECB recognition

Suggested checkpoint:

- implement Cryptopals 1–5 with tests;
- complete the CryptoHack introduction course;
- for one XOR challenge, document why the key length or known plaintext is justified.

Exit check: re-encryption reproduces every supplied ciphertext byte. Printable output alone does not pass.

## Stage 2 — Modular arithmetic

**Goal:** become comfortable with the arithmetic underneath RSA, Diffie–Hellman, signatures, and many CTF constructions.

Read and practice:

- [CryptoHack Modular Arithmetic](https://cryptohack.org/courses/modular/)
- [CryptoHack Mathematics challenges](https://cryptohack.org/challenges/maths/)
- [Handbook 01 — Math and encoding](01-math-and-encoding.md)

Build:

- extended Euclid and verified modular inverse;
- generalized CRT for consistent, non-coprime congruences;
- exact integer root wrapper;
- centered modular representative helper.

Exit check:

- every inverse satisfies `(a * inverse) % modulus == 1`;
- every CRT result satisfies all original congruences;
- an integer root is accepted only when raising it returns the original value.

## Stage 3 — AES and block-cipher modes

**Goal:** separate the block cipher from the mode, padding, nonce/IV rules, and authentication.

Read:

- [CryptoHack Symmetric Cryptography](https://cryptohack.org/courses/symmetric/)
- [Handbook 03 — Block ciphers](03-block-ciphers.md)
- [NIST SP 800-38A](https://csrc.nist.gov/pubs/sp/800/38/a/final) for the definitions of ECB, CBC, CFB, OFB, and CTR
- [NIST IR 8459](https://csrc.nist.gov/pubs/ir/8459/final) for the modern review of the SP 800-38 series and implementation concerns

Practice:

- [Cryptopals Set 2](https://cryptopals.com/sets/2): PKCS#7, CBC, mode recognition, and controlled block transformations;
- [Cryptopals Set 3](https://cryptopals.com/sets/3): CTR and more advanced block-mode exercises.

Build:

- local ECB, CBC, and CTR round trips using a trusted AES primitive;
- strict PKCS#7 validation;
- a block visualizer that prints offsets and repeated blocks.

Exit check: changing one IV, nonce, counter, tag, padding byte, or AAD field produces the effect predicted by your exact mode equation.

> SP 800-38A defines confidentiality-only modes. Do not interpret a successful CBC or CTR round trip as proof of integrity or safe real-world protocol design.

## Stage 4 — Hashes, MACs, and generators

**Goal:** distinguish a hash, keyed hash, HMAC, checksum, and stateful generator by construction rather than by output length.

Read:

- [CryptoHack Hash Functions](https://cryptohack.org/challenges/hashes/)
- [Handbook 06 — Hashes, MACs, and PRNGs](06-hash-mac-prng.md)
- [NIST FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) for the Secure Hash Standard
- [RFC 2104](https://www.rfc-editor.org/rfc/rfc2104.html) for the HMAC construction

Practice:

- [Cryptopals Set 3](https://cryptopals.com/sets/3) for MT19937 state and output exercises;
- [Cryptopals Set 4](https://cryptopals.com/sets/4) for message authentication and controlled length-extension exercises.

Build:

- an exact message-framing logger that prints each hashed field and its byte length;
- one LCG state-recovery toy example;
- an MT19937 replay test using complete local outputs;
- HMAC test vectors with both positive and negative cases.

Exit check: all known digests or outputs match, a held-out output is predicted, and HMAC is not confused with `H(key || message)`.

## Stage 5 — RSA and public-key relations

**Goal:** identify broken assumptions around RSA rather than attempting to factor arbitrary moduli.

Read:

- [CryptoHack Public-Key Cryptography](https://cryptohack.org/courses/public-key/)
- [Handbook 04 — RSA](04-rsa.md)
- [RFC 8017: PKCS #1 v2.2](https://www.rfc-editor.org/rfc/rfc8017.html) for RSA primitives and encoding schemes

Practice:

- [Cryptopals Set 5](https://cryptopals.com/sets/5) for implementation, Diffie–Hellman, RSA, and broadcast relations;
- selected local exercises from [Cryptopals Set 6](https://cryptopals.com/sets/6) after you can explain the padding and oracle model.

Build:

- textbook RSA round trip with intentionally small toy parameters;
- shared-prime GCD check across supplied moduli;
- exact low-exponent root test;
- CRT broadcast reconstruction with complete congruence verification.

Exit check: recovered factors multiply to `n`, recovered messages satisfy every ciphertext congruence, and encoded messages are parsed separately from raw RSA arithmetic.

## Stage 6 — Elliptic curves and signatures

**Goal:** understand group validation and signature transcript equations before attempting nonce or verifier attacks.

Read:

- [CryptoHack Elliptic Curves](https://cryptohack.org/courses/elliptic/)
- [Handbook 05 — ECC and signatures](05-ecc-signatures.md)
- [NIST FIPS 186-5](https://csrc.nist.gov/pubs/fips/186-5/final) for current digital-signature definitions and requirements
- [RFC 6979](https://www.rfc-editor.org/rfc/rfc6979.html) for deterministic DSA/ECDSA nonce generation

Practice:

- CryptoHack's elliptic-curve course before advanced attack categories;
- selected [Cryptopals Set 6](https://cryptopals.com/sets/6) exercises for DSA nonce relations;
- [Cryptopals Set 8](https://cryptopals.com/sets/8) only after basic curve arithmetic and subgroup checks are comfortable.

Build:

- point-addition and scalar-multiplication tests on a tiny toy curve;
- point-on-curve and subgroup validation;
- a local repeated-nonce ECDSA demonstration with public-key verification.

Exit check: a recovered signing key satisfies `d*G == Q` and every supplied signature verifies under the exact transcript encoding.

## Stage 7 — Lattices and bounded-error models

**Goal:** construct a lattice from an equation and bound—not from an attack recipe.

Read and practice:

- [CryptoHack Lattices](https://cryptohack.org/challenges/post-quantum/)
- [Handbook 07 — Lattices, LWE, and proof verifiers](07-lattices-lwe-zkp.md)

Build:

- Gram–Schmidt and nearest-plane toy examples;
- a small LLL demonstration where every basis coordinate is explained;
- an LWE verification function for `centered(b - A*s mod q)`.

Exit check: every recovered value satisfies the original modular equations and every error lies inside the stated bound. A vector that merely “looks short” does not pass.

## Stage 8 — Zero-knowledge proof verifiers

**Goal:** follow the statement, witness, commitments, challenge, and response into the constraints actually enforced.

Read and practice:

- [CryptoHack Zero-Knowledge Proofs](https://cryptohack.org/challenges/zkp/)
- the verifier-audit section of [Handbook 07](07-lattices-lwe-zkp.md)

Learn these concepts in order:

1. statement and witness;
2. completeness, soundness, and zero knowledge;
3. transcript structure;
4. commitment reuse and special soundness;
5. Fiat–Shamir transcript binding;
6. group/input validation;
7. positive and negative verifier tests.

Exit check: the real verifier accepts the intended proof, rejects a mutated proof, and binds the proof to the intended public statement.

## Capstone routine

For a new Crypto CTF challenge:

1. classify only from observed evidence;
2. read the matching handbook chapter;
3. choose at most one learning reference for a missing concept;
4. return to the challenge and write its exact equations;
5. implement the smallest solver;
6. save actual output and independent proof;
7. write a short explanation in your own words.

This prevents “tutorial hopping”—spending hours consuming material without converting it into a solver or a verified result.

## Source-maintenance note

The links in this chapter point to source pages rather than copied lesson text. Standards can be revised and challenge catalogs can grow. Check the publication page's status, planning notes, and errata before treating a specification as current implementation guidance.

Last reviewed: 2026-08-20.
