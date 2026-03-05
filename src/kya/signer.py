"""KYA Signer — Ed25519 signing and verification for agent cards."""

import json
import hashlib
import datetime
from pathlib import Path
from typing import Optional

KEY_DIR = Path.home() / ".kya" / "keys"


def _check_crypto():
    """Raise ImportError with install instructions if cryptography not available."""
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        return True
    except ImportError:
        raise ImportError(
            "Signing requires the 'cryptography' package.\n"
            "Install with: pip install kya-agent[signing]"
        )


def canonicalize(card: dict) -> bytes:
    """Produce canonical JSON bytes for signing.

    Strips _signature field, sorts keys recursively,
    uses compact separators, ASCII-only encoding.
    """
    card_copy = {k: v for k, v in card.items() if k != "_signature"}
    return json.dumps(
        card_copy, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def generate_keypair(name: str = "default") -> tuple[Path, Path]:
    """Generate Ed25519 key pair, save to ~/.kya/keys/."""
    _check_crypto()
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization

    KEY_DIR.mkdir(parents=True, exist_ok=True)

    private_key = Ed25519PrivateKey.generate()

    priv_path = KEY_DIR / f"{name}.key"
    pub_path = KEY_DIR / f"{name}.pub"

    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    priv_path.write_bytes(priv_bytes)
    priv_path.chmod(0o600)

    pub_bytes = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    pub_path.write_bytes(pub_bytes)

    return priv_path, pub_path


def compute_key_id(public_key) -> str:
    """SHA-256 fingerprint of raw public key bytes, truncated to 16 hex chars."""
    from cryptography.hazmat.primitives import serialization
    raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return hashlib.sha256(raw).hexdigest()[:16]


def sign_card(card: dict, private_key_path: str) -> dict:
    """Sign a card dict, return new dict with _signature embedded."""
    _check_crypto()
    import base64
    from cryptography.hazmat.primitives import serialization

    key_path = Path(private_key_path)
    private_key = serialization.load_pem_private_key(
        key_path.read_bytes(), password=None
    )

    canonical = canonicalize(card)
    signature = private_key.sign(canonical)

    public_key = private_key.public_key()
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii").strip()

    signed_card = {k: v for k, v in card.items() if k != "_signature"}
    signed_card["_signature"] = {
        "algorithm": "ed25519",
        "key_id": compute_key_id(public_key),
        "public_key": pub_pem,
        "signed_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "value": base64.b64encode(signature).decode("ascii"),
    }

    return signed_card


def verify_card(card: dict, public_key_path: Optional[str] = None) -> dict:
    """Verify a signed card. Returns result dict."""
    _check_crypto()
    import base64
    from cryptography.hazmat.primitives import serialization
    from cryptography.exceptions import InvalidSignature

    sig_block = card.get("_signature")
    if not sig_block:
        return {"valid": False, "error": "No _signature field found in card"}

    if public_key_path:
        pub_key = serialization.load_pem_public_key(
            Path(public_key_path).read_bytes()
        )
    elif "public_key" in sig_block:
        pub_key = serialization.load_pem_public_key(
            sig_block["public_key"].encode("ascii")
        )
    else:
        return {"valid": False, "error": "No public key available for verification"}

    canonical = canonicalize(card)
    sig_bytes = base64.b64decode(sig_block["value"])

    try:
        pub_key.verify(sig_bytes, canonical)
        return {
            "valid": True,
            "key_id": sig_block.get("key_id", "unknown"),
            "signed_at": sig_block.get("signed_at", "unknown"),
            "algorithm": sig_block.get("algorithm", "unknown"),
        }
    except InvalidSignature:
        return {"valid": False, "error": "Signature verification failed — card may have been tampered with"}
