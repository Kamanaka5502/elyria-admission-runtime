import subprocess
import sys

from scripts.generate_digest_manifest import build_manifest, write_manifest
from scripts.verify_digest_manifest import DigestVerificationError, verify_manifest


def test_build_manifest_records_sha256_and_size(tmp_path):
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    artifact = bundle / "artifact.txt"
    artifact.write_text("elyria\n", encoding="utf-8")

    manifest = build_manifest(bundle)

    assert manifest["manifest_type"] == "elyria_admission_runtime_digest_manifest"
    assert manifest["artifacts"][0]["path"] == "artifact.txt"
    assert manifest["artifacts"][0]["size_bytes"] == len("elyria\n".encode())
    assert len(manifest["artifacts"][0]["sha256"]) == 64


def test_verify_manifest_passes_for_current_artifact(tmp_path):
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "artifact.txt").write_text("elyria\n", encoding="utf-8")
    write_manifest(bundle)

    result = verify_manifest(bundle)

    assert result["valid"] is True
    assert result["artifact_count"] == 1


def test_verify_manifest_detects_digest_difference(tmp_path):
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    artifact = bundle / "artifact.txt"
    artifact.write_text("elyria\n", encoding="utf-8")
    write_manifest(bundle)
    artifact.write_text("elyria two\n", encoding="utf-8")

    try:
        verify_manifest(bundle)
    except DigestVerificationError as exc:
        assert "sha256 mismatch" in str(exc) or "size mismatch" in str(exc)
    else:
        raise AssertionError("digest verification should detect mismatch")


def test_verify_digest_script_returns_pass(tmp_path):
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "artifact.txt").write_text("elyria\n", encoding="utf-8")
    write_manifest(bundle)

    result = subprocess.run(
        [sys.executable, "scripts/verify_digest_manifest.py", str(bundle)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "DIGEST MANIFEST PASS" in result.stdout
