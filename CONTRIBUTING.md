# Contributing

Contributions should make the handbook more precise, reproducible, or easier to verify.

## Good contributions

- Correct an equation, boundary condition, serialization rule, or misleading claim.
- Add a safe toy example with fixed inputs and automatic self-checks.
- Add an independent verification method for an existing derivation.
- Improve a decision tree, checklist, or failure-diagnosis section.
- Clarify the difference between a fact, inference, hypothesis, and proof.

## Do not submit

- Active event flags or challenge secrets.
- Real credentials, tokens, cookies, private keys, or personal data.
- Unattributed copies of challenge statements, binaries, or write-ups.
- Attack-all wrappers, credential guessing, wordlists, or unexplained brute force.
- Instructions that broaden testing beyond an authorized CTF or lab.

## Style

1. State the evidence that justifies a technique.
2. Write the exact equation or parser behavior.
3. Provide one deterministic test and its expected result.
4. Explain how to independently verify success.
5. Keep examples intentionally small and self-contained.

Before opening a change, run:

```bash
python -m compileall templates examples
python examples/toy_rsa_roundtrip.py
```
