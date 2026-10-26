import pytest

from consequence_twin.signing import (
    DEMO_KEY_ID,
    SIGNATURE_ALG,
    SigningConfig,
    SigningError,
    SigningMode,
    sign_receipt_fields,
    verify_signed_receipt,
)


def base_receipt(**overrides):
    receipt = {
        "receipt_id": "RCT-001",
        "movement_id": "MOVE-001",
        "tenant_id": "tenant-a",
        "verdict": "ADMIT",
        "input_hash": "input-hash",
        "evidence_hash": "evidence-hash",
        "policy_pack_hash": "policy-hash",
        "engine_version": "0.8.1",
    }
    receipt.update(overrides)
    return receipt


def test_signing_adds_key_id_algorithm_and_signature():
    config = SigningConfig(
        mode=SigningMode.FILE_KEY,
        key_id="file-key-1",
        secret="secret-a",
        production_mode=False,
    )
    signed = sign_receipt_fields(base_receipt(), config)
    assert signed["key_id"] == "file-key-1"
    assert signed["signature_alg"] == SIGNATURE_ALG
    assert signed["signature"]
    assert verify_signed_receipt(signed, config) is True


def test_tampered_receipt_fails_verification():
    config = SigningConfig(
        mode=SigningMode.FILE_KEY,
        key_id="file-key-1",
        secret="secret-a",
        production_mode=False,
    )
    signed = sign_receipt_fields(base_receipt(), config)
    tampered = dict(signed)
    tampered["verdict"] = "REFUSE"
    assert verify_signed_receipt(tampered, config) is False


def test_wrong_key_fails_verification():
    signer = SigningConfig(
        mode=SigningMode.FILE_KEY,
        key_id="file-key-1",
        secret="secret-a",
        production_mode=False,
    )
    wrong = SigningConfig(
        mode=SigningMode.FILE_KEY,
        key_id="file-key-1",
        secret="secret-b",
        production_mode=False,
    )
    signed = sign_receipt_fields(base_receipt(), signer)
    assert verify_signed_receipt(signed, wrong) is False


def test_missing_key_fails_closed():
    config = SigningConfig(
        mode=SigningMode.FILE_KEY,
        key_id="file-key-1",
        secret=None,
        production_mode=False,
    )
    with pytest.raises(SigningError):
        sign_receipt_fields(base_receipt(), config)


def test_demo_key_cannot_be_used_in_production_mode():
    config = SigningConfig(
        mode=SigningMode.LOCAL_DEMO_HMAC,
        key_id=DEMO_KEY_ID,
        secret="demo-secret",
        production_mode=True,
    )
    with pytest.raises(SigningError):
        sign_receipt_fields(base_receipt(), config)


def test_unimplemented_kms_stub_fails_closed():
    config = SigningConfig(
        mode=SigningMode.KMS_STUB,
        key_id="kms-stub-key-1",
        secret=None,
        production_mode=False,
    )
    with pytest.raises(SigningError, match="not a cryptographic signer"):
        sign_receipt_fields(base_receipt(), config)


def test_unimplemented_external_adapter_fails_closed():
    config = SigningConfig(
        mode=SigningMode.EXTERNAL_SIGNING_ADAPTER,
        key_id="external-key-1",
        secret=None,
        production_mode=False,
    )
    with pytest.raises(SigningError, match="not configured with a real signer"):
        sign_receipt_fields(base_receipt(), config)
