# Security and privacy

[简体中文](SECURITY.md) · [English home](README.en.md)

This repository distributes public methods and fictional exercises. Keep credentials in local environment settings or the client's authentication system, never in skills, examples, screenshots, commit messages or review inputs.

The initial public package used an explicit file allowlist and a fresh public Git history. For updates, inspect content, filenames, nested configuration, URL query parameters and commit authors. `.gitignore` does not remove tracked files or earlier commits.

`scripts/privacy_scan.py` is a heuristic preflight for common tokens, private keys, credential assignments, signed URLs, personal paths, email addresses and high-entropy candidates. It does not prove the absence of all sensitive information. Use `--deny-file` with a local-only private list for names, accounts, voice IDs and project identifiers. Keep that list outside the repository.

The scanner reports categories, files and line numbers, never matched values. Manually inspect all files intended for publication too. If a real key is exposed, revoke or rotate it before addressing history. Deleting the latest file does not retract a leaked credential.

For a security problem, first prepare a local reproduction without secrets. Submit only through GitHub private vulnerability reporting if enabled for this repository. If unavailable, wait for a private channel rather than posting sensitive samples publicly. Never send credentials to maintainers.
