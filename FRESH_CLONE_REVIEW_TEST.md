# Fresh Clone Review Test

## Purpose

This file records the clean-machine review path for Elyria Admission Runtime.

## Commands

```bash
git clone https://github.com/Kamanaka5502/elyria-admission-runtime.git
cd elyria-admission-runtime
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pytest
python scripts/generate_digest_manifest.py review-bundle/latest
python scripts/verify_digest_manifest.py review-bundle/latest
python external_verifier/verify_bundle.py review-bundle/latest
python scripts/production_preflight.py --mode review
```

## Expected Output

```text
pytest PASS
digest manifest PASS
RESULT: ELYRIA ADMISSION RUNTIME VERIFIER PASS
PRODUCTION PREFLIGHT REVIEW MODE PASS
```

## Evidence Status

Fresh-clone terminal evidence has not yet been pasted here.

This file is a review procedure until fresh-clone output is recorded.
