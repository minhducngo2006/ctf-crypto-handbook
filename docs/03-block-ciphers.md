# 03 — Block ciphers

Do not begin with an attack name. First establish the block size, mode, padding, IV/nonce/tag serialization, and exact parser behavior.

## Mode recognition

| Observation | Possible explanation | Required confirmation |
|---|---|---|
| Repeated plaintext blocks produce repeated ciphertext blocks | ECB | Same key and exact repeated blocks; no chaining |
| Ciphertext is IV plus block-aligned data | CBC or another IV-based mode | Source or exact recurrence |
| Ciphertext length equals plaintext length | CTR/stream-like mode | Counter/nonce construction |
| Nonce and authentication tag are present | GCM/EAX/CCM or custom AEAD | Tag length, associated data, verification order |
| One changed ciphertext block affects two decrypted blocks | CBC | Controlled local comparison |

The same length pattern can fit multiple modes. Source code or a round-trip test is stronger than visual classification.

## ECB

ECB encrypts each block independently:

```text
C[i] = E_K(P[i])
```

Its main evidence is equality leakage: identical plaintext blocks under the same key produce identical ciphertext blocks. Verify exact block alignment before drawing conclusions from repeated hex substrings.

## CBC

Encryption and decryption:

```text
C[0] = IV
C[i] = E_K(P[i] XOR C[i-1])
P[i] = D_K(C[i]) XOR C[i-1]
```

### Deterministic bit transform

To change a known plaintext block `P[i]` into a chosen block `P'[i]`, modify the previous ciphertext block:

```text
delta = P[i] XOR P'[i]
C'[i-1] = C[i-1] XOR delta
```

This also corrupts the previous decrypted block. A valid CTF use must account for parser structure, padding, and authentication. It will fail against correctly verified authenticated encryption.

Proof:

1. Perform the change against a local copy of the challenge construction.
2. Assert the targeted block equals the desired bytes.
3. Confirm every parser field that must remain valid.
4. Include a negative test with a wrong delta.

## CTR

CTR turns a block cipher into a stream construction:

```text
KS[i] = E_K(nonce || counter_i)
C[i] = P[i] XOR KS[i]
```

Reusing the same `(key, nonce, counter sequence)` gives:

```text
C1 XOR C2 = P1 XOR P2
```

Before applying this relation, prove that the entire counter block construction is reused—not merely that a displayed nonce is equal.

Check:

- nonce prefix/suffix position;
- counter width and endian order;
- initial counter value;
- whether the counter resets per message;
- whether part of the nonce is hidden or random.

## GCM and other AEAD modes

AEAD protects both confidentiality and integrity when used correctly. CTF weaknesses usually come from implementation errors such as:

- nonce reuse under one key;
- omitted or incorrectly verified tags;
- truncated tags combined with a challenge-supported model;
- disagreement about associated-data framing;
- using decrypted data before authentication succeeds.

Do not treat GCM as “CTR plus a tag” and modify ciphertext blindly. Reconstruct the exact nonce, associated data, ciphertext, and tag inputs first. A forgery claim requires the real verifier to accept it.

## Padding

PKCS#7 for block size `B` appends `k` bytes, each equal to `k`, where `1 <= k <= B`.

```python
from Crypto.Util.Padding import pad, unpad

padded = pad(message, 16)
assert unpad(padded, 16) == message
```

Common parser mistakes:

- removing padding before checking its full pattern;
- accepting zero-length padding;
- confusing zero padding with PKCS#7;
- decoding UTF-8 before unpadding;
- losing an entire padding block when plaintext is block-aligned.

## Verification template

```python
ciphertext = encrypt(key, iv_or_nonce, plaintext, aad)
assert ciphertext == supplied_ciphertext

recovered = decrypt_and_verify(key, iv_or_nonce, ciphertext, tag, aad)
assert recovered == plaintext
```

## Failure diagnosis

| Symptom | Likely first check |
|---|---|
| First block wrong, later blocks correct | IV parsing |
| Every block wrong but stable | key, mode, endian/counter construction |
| Plaintext correct except end | padding or original length |
| Targeted CBC block correct but parser rejects | damaged preceding block, padding, or MAC |
| CTR recovery shifts after one block | counter width/start/endian |
| Local decryption works but service rejects | tag/AAD/framing mismatch |

## Guided practice

1. **Learn:** follow [CryptoHack Symmetric Cryptography](https://cryptohack.org/courses/symmetric/) to separate AES from its modes and common misuse.
2. **Build:** implement and test the relevant exercises in [Cryptopals Set 2](https://cryptopals.com/sets/2), then use [Set 3](https://cryptopals.com/sets/3) for CTR and harder mode behavior.
3. **Check definitions:** use [NIST SP 800-38A](https://csrc.nist.gov/pubs/sp/800/38/a/final) for ECB/CBC/CFB/OFB/CTR and [NIST IR 8459](https://csrc.nist.gov/pubs/ir/8459/final) for the newer review of the SP 800-38 series.
4. **Prove:** require local round trips, exact parser behavior, and negative tests for a changed IV, nonce, tag, padding byte, or AAD field.

See [Stage 3 of the guided learning path](10-guided-learning-path.md#stage-3--aes-and-block-cipher-modes).
