"""
KYA Validator — Validates agent cards against the KYA schema.

Usage:
    kya validate agent-card.json
    kya validate --strict agent-card.json
    kya score agent-card.json
"""

import json
import sys
from pathlib import Path
from typing import Any

SCHEMA_FILE = Path(__file__).parent / "kya-v0.1.schema.json"

# Completeness weights for scoring
SECTION_WEIGHTS = {
    "kya_version": 5,
    "agent_id": 10,
    "name": 5,
    "version": 5,
    "purpose": 10,
    "agent_type": 5,
    "owner": 10,
    "capabilities": 15,
    "data_access": 10,
    "security": 15,
    "compliance": 10,
    "behavior": 10,
    "dependencies": 3,
    "metadata": 2,
}


def load_schema() -> dict:
    """Load the KYA JSON Schema."""
    if not SCHEMA_FILE.exists():
        print(f"Error: Schema file not found at {SCHEMA_FILE}", file=sys.stderr)
        sys.exit(1)
    with open(SCHEMA_FILE) as f:
        return json.load(f)


def load_card(path: str) -> dict:
    """Load an agent card from a JSON file."""
    card_path = Path(path)
    if not card_path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(card_path) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {path}: {e}", file=sys.stderr)
            sys.exit(1)


def validate_required_fields(card: dict, schema: dict) -> list[str]:
    """Check that all required fields are present."""
    errors = []
    required = schema.get("required", [])
    for field in required:
        if field not in card:
            errors.append(f"Missing required field: '{field}'")
    return errors


def validate_field_types(card: dict, schema: dict) -> list[str]:
    """Basic type validation without full JSON Schema library dependency."""
    errors = []
    properties = schema.get("properties", {})

    for field, value in card.items():
        if field not in properties:
            errors.append(f"Unknown field: '{field}' (not in KYA schema)")
            continue

        field_schema = properties[field]
        expected_type = field_schema.get("type")

        if expected_type == "string" and not isinstance(value, str):
            errors.append(f"Field '{field}' must be a string, got {type(value).__name__}")
        elif expected_type == "object" and not isinstance(value, dict):
            errors.append(f"Field '{field}' must be an object, got {type(value).__name__}")
        elif expected_type == "array" and not isinstance(value, list):
            errors.append(f"Field '{field}' must be an array, got {type(value).__name__}")
        elif expected_type == "integer" and not isinstance(value, int):
            errors.append(f"Field '{field}' must be an integer, got {type(value).__name__}")
        elif expected_type == "boolean" and not isinstance(value, bool):
            errors.append(f"Field '{field}' must be a boolean, got {type(value).__name__}")

        # Validate const
        if "const" in field_schema and value != field_schema["const"]:
            errors.append(f"Field '{field}' must be '{field_schema['const']}', got '{value}'")

        # Validate enum
        if "enum" in field_schema and value not in field_schema["enum"]:
            errors.append(f"Field '{field}' must be one of {field_schema['enum']}, got '{value}'")

        # Validate pattern
        if "pattern" in field_schema and isinstance(value, str):
            import re
            if not re.match(field_schema["pattern"], value):
                errors.append(f"Field '{field}' does not match pattern: {field_schema['pattern']}")

        # Validate minLength
        if "minLength" in field_schema and isinstance(value, str):
            if len(value) < field_schema["minLength"]:
                errors.append(f"Field '{field}' is too short (min {field_schema['minLength']} chars)")

    return errors


def validate_capabilities(card: dict) -> list[str]:
    """Validate the capabilities section has proper structure."""
    errors = []
    caps = card.get("capabilities", {})

    if not isinstance(caps, dict):
        return ["'capabilities' must be an object"]

    declared = caps.get("declared", [])
    if not declared:
        errors.append("No capabilities declared. An agent with no capabilities is suspicious.")
        return errors

    for i, cap in enumerate(declared):
        if not isinstance(cap, dict):
            errors.append(f"capabilities.declared[{i}] must be an object")
            continue
        if "name" not in cap:
            errors.append(f"capabilities.declared[{i}] missing 'name'")
        if "risk_level" not in cap:
            errors.append(f"capabilities.declared[{i}] missing 'risk_level'")
        elif cap["risk_level"] not in ("low", "medium", "high", "critical"):
            errors.append(f"capabilities.declared[{i}].risk_level must be low/medium/high/critical")

    return errors


def validate_security(card: dict) -> list[str]:
    """Validate the security section."""
    warnings = []
    security = card.get("security", {})

    if not security:
        warnings.append("No security section. Agent has never been audited.")
        return warnings

    audit = security.get("last_audit", {})
    if not audit:
        warnings.append("No audit history. Consider running mcp-security-audit.")

    if not security.get("injection_tested"):
        warnings.append("Agent has not been tested for prompt injection attacks.")

    return warnings


def compute_completeness_score(card: dict) -> int:
    """Score 0-100 based on how complete the agent card is."""
    total_weight = sum(SECTION_WEIGHTS.values())
    earned = 0

    for section, weight in SECTION_WEIGHTS.items():
        value = card.get(section)
        if value is None:
            continue

        if isinstance(value, str) and len(value) > 0:
            earned += weight
        elif isinstance(value, dict) and len(value) > 0:
            # Partial credit based on sub-field completeness
            if section == "capabilities":
                declared = value.get("declared", [])
                if declared:
                    earned += weight
                else:
                    earned += weight * 0.3
            elif section == "security":
                if value.get("last_audit"):
                    earned += weight
                else:
                    earned += weight * 0.3
            else:
                earned += weight
        elif isinstance(value, list) and len(value) > 0:
            earned += weight
        elif isinstance(value, bool):
            earned += weight
        elif isinstance(value, (int, float)):
            earned += weight

    return round((earned / total_weight) * 100)


def check_signature(card: dict) -> dict:
    """Check signature status of a card. Returns status dict."""
    sig = card.get("_signature")
    if not sig:
        return {"status": "unsigned"}

    try:
        from .signer import verify_card
        result = verify_card(card)
        if result["valid"]:
            return {
                "status": "verified",
                "key_id": result["key_id"],
                "signed_at": result["signed_at"],
            }
        else:
            return {"status": "invalid", "error": result["error"]}
    except ImportError:
        return {"status": "unverified", "note": "Install kya-agent[signing] to verify signatures"}


def validate(card_path: str, strict: bool = False) -> dict:
    """Run full validation on an agent card. Returns result dict."""
    schema = load_schema()
    card = load_card(card_path)

    errors = []
    warnings = []

    # Required fields — skip _signature from unknown field check
    errors.extend(validate_required_fields(card, schema))

    # Type validation
    type_errors = validate_field_types(card, schema)
    # Filter out _signature "unknown field" errors since it's valid via patternProperties
    type_errors = [e for e in type_errors if "'_signature'" not in e]
    if strict:
        errors.extend(type_errors)
    else:
        warnings.extend(type_errors)

    # Capabilities
    cap_issues = validate_capabilities(card)
    errors.extend([i for i in cap_issues if "missing" in i.lower()])
    warnings.extend([i for i in cap_issues if "missing" not in i.lower()])

    # Security
    warnings.extend(validate_security(card))

    # Completeness score
    score = compute_completeness_score(card)

    # Signature check
    sig_status = check_signature(card)

    return {
        "valid": len(errors) == 0,
        "score": score,
        "errors": errors,
        "warnings": warnings,
        "agent_id": card.get("agent_id", "unknown"),
        "agent_name": card.get("name", "unknown"),
        "signature": sig_status,
    }


def print_result(result: dict) -> None:
    """Pretty-print validation results."""
    status = "PASS" if result["valid"] else "FAIL"
    print(f"\nKYA Validation: {status}")
    print(f"Agent: {result['agent_name']} ({result['agent_id']})")
    print(f"Completeness Score: {result['score']}/100")

    # Signature status
    sig = result.get("signature", {})
    sig_status = sig.get("status", "unsigned")
    if sig_status == "verified":
        print(f"Signature: VERIFIED (key: {sig['key_id']}, signed: {sig['signed_at']})")
    elif sig_status == "invalid":
        print(f"Signature: INVALID — {sig.get('error', 'unknown error')}")
    elif sig_status == "unverified":
        print(f"Signature: PRESENT (install kya-agent[signing] to verify)")
    else:
        print(f"Signature: UNSIGNED")

    if result["errors"]:
        print(f"\nErrors ({len(result['errors'])}):")
        for e in result["errors"]:
            print(f"  [x] {e}")

    if result["warnings"]:
        print(f"\nWarnings ({len(result['warnings'])}):")
        for w in result["warnings"]:
            print(f"  [!] {w}")

    if not result["errors"] and not result["warnings"]:
        print("\nNo issues found. Agent card is complete and well-formed.")

    print()
