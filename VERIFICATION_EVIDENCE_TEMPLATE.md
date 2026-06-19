# Verification Evidence Template

## Purpose

Use this template after a GitHub Actions or fresh-clone verification run.

## Source

```text
source:
run date:
commit sha:
reviewer:
```

## Command

```bash
python scripts/verify_all.py --report verification-report.json
```

## Expected Marker

```text
RESULT: ELYRIA ADMISSION RUNTIME FULL VERIFY PASS
```

## Output Area

```text
Paste verification output here.
```

## Report Summary

```text
report file: verification-report.json
passed:
unit tests:
digest manifest:
external verifier:
production preflight review mode:
```

## Follow-Up

When evidence is present, update the fresh-clone record and the final verification issue.
