DEMO_ASSESSMENTS = [
    {
        "movement_id": "MOVE-001",
        "source_node": "ai.recommendation",
        "target_node": "operator.approval",
        "authority_present": True,
        "authority_scope_valid": True,
        "standing_active": True,
        "evidence_present": True,
        "evidence_sufficient": True,
        "custody_preserved": True,
        "refusal_condition_active": False,
        "revalidation_required": False,
        "receipt_available": True,
        "replay_available": True,
        "evidence_items": [
            {
                "evidence_id": "DEMO-EVIDENCE-001",
                "evidence_type": "policy_record",
                "source_system": "demo.registry",
                "custody_owner": "demo.operator",
                "hash_reference": "sha256:demo-fixture-reference",
                "required": True,
                "status": "accepted",
                "notes": "Sanitized fixture demonstrating the required structured-evidence shape; not authenticated production evidence."
            }
        ],
        "notes": "Clean admitted movement with a structured demo evidence fixture."
    },
    {
        "movement_id": "MOVE-002",
        "source_node": "evidence.check",
        "target_node": "payment.release",
        "authority_present": True,
        "authority_scope_valid": True,
        "standing_active": True,
        "evidence_present": False,
        "evidence_sufficient": False,
        "custody_preserved": False,
        "refusal_condition_active": False,
        "revalidation_required": False,
        "receipt_available": False,
        "replay_available": False,
        "notes": "Black path: movement can attempt to bind without evidence, receipt, or replay."
    },
    {
        "movement_id": "MOVE-003",
        "source_node": "unscoped.override",
        "target_node": "customer.escalation",
        "authority_present": False,
        "authority_scope_valid": False,
        "standing_active": False,
        "evidence_present": True,
        "evidence_sufficient": True,
        "custody_preserved": True,
        "refusal_condition_active": True,
        "revalidation_required": False,
        "receipt_available": True,
        "replay_available": True,
        "notes": "Hard refused movement."
    }
]
