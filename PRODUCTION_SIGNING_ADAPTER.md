# Production Signing Adapter

Phase 1 adds a signing adapter boundary for Elyria Admission Runtime.

Supported modes:

```text
local_demo_hmac
file_key
kms_stub
external_signing_adapter
```

The receipt record identifies the signing mode, key identifier, signature algorithm, and signature.

Production posture:

```text
Demo signing is for review only.
Production signing requires a non-demo adapter and customer-approved key custody.
```

Implemented proof file:

```text
tests/test_signing_adapter.py
```
