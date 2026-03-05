"""Tests for KYA signer — Ed25519 signing and verification."""

import json
import copy
import tempfile
from pathlib import Path

import pytest

from kya.signer import canonicalize, generate_keypair, compute_key_id, sign_card, verify_card


SAMPLE_CARD = {
    "kya_version": "0.1",
    "agent_id": "test-org/test-agent",
    "name": "Test Agent",
    "version": "1.0.0",
    "purpose": "A test agent for unit testing the KYA signer module.",
    "owner": {"name": "Test Org", "contact": "test@example.com"},
    "capabilities": {
        "declared": [{"name": "testing", "risk_level": "low"}]
    },
}


@pytest.fixture
def key_dir(tmp_path):
    """Generate a key pair in a temp directory."""
    import kya.signer as s
    original_dir = s.KEY_DIR
    s.KEY_DIR = tmp_path
    priv, pub = generate_keypair("test")
    yield {"dir": tmp_path, "private": priv, "public": pub}
    s.KEY_DIR = original_dir


class TestCanonicalize:
    def test_strips_signature(self):
        card = {**SAMPLE_CARD, "_signature": {"value": "fake"}}
        canonical = canonicalize(card)
        assert b"_signature" not in canonical

    def test_deterministic(self):
        """Same card always produces same canonical bytes."""
        a = canonicalize(SAMPLE_CARD)
        b = canonicalize(SAMPLE_CARD)
        assert a == b

    def test_key_order_irrelevant(self):
        """Reversed key insertion order produces same canonical output."""
        reversed_card = dict(reversed(list(SAMPLE_CARD.items())))
        assert canonicalize(SAMPLE_CARD) == canonicalize(reversed_card)


class TestKeygen:
    def test_creates_key_files(self, key_dir):
        assert key_dir["private"].exists()
        assert key_dir["public"].exists()

    def test_private_key_permissions(self, key_dir):
        mode = key_dir["private"].stat().st_mode & 0o777
        assert mode == 0o600


class TestSignAndVerify:
    def test_sign_produces_signature_block(self, key_dir):
        signed = sign_card(SAMPLE_CARD, str(key_dir["private"]))
        sig = signed["_signature"]
        assert sig["algorithm"] == "ed25519"
        assert len(sig["key_id"]) == 16
        assert sig["public_key"].startswith("-----BEGIN PUBLIC KEY-----")
        assert len(sig["value"]) > 0
        assert "signed_at" in sig

    def test_verify_valid_card(self, key_dir):
        signed = sign_card(SAMPLE_CARD, str(key_dir["private"]))
        result = verify_card(signed)
        assert result["valid"] is True
        assert result["key_id"] == signed["_signature"]["key_id"]

    def test_verify_tampered_card_fails(self, key_dir):
        signed = sign_card(SAMPLE_CARD, str(key_dir["private"]))
        signed["name"] = "TAMPERED"
        result = verify_card(signed)
        assert result["valid"] is False
        assert "tampered" in result["error"].lower()

    def test_verify_unsigned_card(self):
        result = verify_card(SAMPLE_CARD)
        assert result["valid"] is False
        assert "No _signature" in result["error"]

    def test_verify_with_explicit_public_key(self, key_dir):
        signed = sign_card(SAMPLE_CARD, str(key_dir["private"]))
        result = verify_card(signed, public_key_path=str(key_dir["public"]))
        assert result["valid"] is True

    def test_key_id_consistent(self, key_dir):
        """Key ID from keygen matches key ID in signed card."""
        from cryptography.hazmat.primitives import serialization
        pub_key = serialization.load_pem_public_key(key_dir["public"].read_bytes())
        expected_id = compute_key_id(pub_key)
        signed = sign_card(SAMPLE_CARD, str(key_dir["private"]))
        assert signed["_signature"]["key_id"] == expected_id
