# Policy Packs

Policy packs map a customer review corridor into runtime admission requirements.

A policy pack defines:

```text
policy_pack_id
version
allowed_movement_types
allowed_authority_scopes
required_evidence
custody_required
review rules
replay rules
no-bind rules
```

Runtime expectation:

```text
Each governed decision identifies the policy pack hash.
```

Implemented proof file:

```text
tests/test_policy_pack.py
```
