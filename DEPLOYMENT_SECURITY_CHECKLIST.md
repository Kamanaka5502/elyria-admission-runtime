# Deployment Security Checklist

This checklist separates implemented review controls from deployment-dependent controls.

| Area | Status | Notes |
|---|---|---|
| Auth | implemented for review | production identity remains deployment-dependent |
| RBAC | implemented for review | role permissions are test-covered |
| Tenant isolation | implemented for review | production tenancy requires customer approval |
| Runtime signing | implemented for review | production custody is deployment-dependent |
| Receipt persistence | implemented for review | enterprise database selection is customer-dependent |
| Audit chain | implemented for review | retention policy is customer-dependent |
| Replay review | implemented for review | abuse controls are deployment-dependent |
| Proof packet handling | implemented for review | data classification is customer-dependent |
| Evidence privacy | required before production | sanitize public examples |
| CORS | required before production | restrict by deployment origin |
| Rate limits | required before production | set at gateway or app layer |
| Backup / restore | customer-dependent | define retention and recovery controls |
| Incident response | customer-dependent | align with customer security operations |
| External review | external-review-dependent | required where buyer or regulation requires it |

## Boundary

Do not treat this checklist as production approval.
