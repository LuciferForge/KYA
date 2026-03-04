"""KYA CLI — Know Your Agent command-line interface."""

import argparse
import json
import sys

from .validator import validate, print_result, load_card, compute_completeness_score


def main():
    parser = argparse.ArgumentParser(
        prog="kya",
        description="KYA — Know Your Agent. Validate and score AI agent identity cards.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # validate
    val_parser = subparsers.add_parser("validate", help="Validate an agent card against the KYA schema")
    val_parser.add_argument("card", help="Path to agent card JSON file")
    val_parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    val_parser.add_argument("--json", action="store_true", dest="json_output", help="Output as JSON")

    # score
    score_parser = subparsers.add_parser("score", help="Score an agent card's completeness")
    score_parser.add_argument("card", help="Path to agent card JSON file")

    # init
    init_parser = subparsers.add_parser("init", help="Generate a skeleton agent card")
    init_parser.add_argument("--agent-id", required=True, help="Agent ID (format: owner/agent-name)")
    init_parser.add_argument("--name", required=True, help="Human-readable agent name")
    init_parser.add_argument("-o", "--output", default="agent-card.kya.json", help="Output file path")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "validate":
        result = validate(args.card, strict=args.strict)
        if args.json_output:
            print(json.dumps(result, indent=2))
        else:
            print_result(result)
        sys.exit(0 if result["valid"] else 1)

    elif args.command == "score":
        card = load_card(args.card)
        score = compute_completeness_score(card)
        print(f"Completeness Score: {score}/100")

    elif args.command == "init":
        skeleton = {
            "kya_version": "0.1",
            "agent_id": args.agent_id,
            "name": args.name,
            "version": "0.1.0",
            "purpose": "TODO: Describe what this agent does and why it exists.",
            "agent_type": "tool",
            "owner": {
                "name": "TODO: Your name or organization",
                "contact": "TODO: security@example.com"
            },
            "capabilities": {
                "declared": [
                    {
                        "name": "TODO: capability_name",
                        "description": "TODO: What this capability does",
                        "risk_level": "low",
                        "scope": "TODO: Boundaries of this capability"
                    }
                ],
                "denied": []
            },
            "data_access": {
                "sources": [],
                "destinations": [],
                "pii_handling": "none",
                "retention_policy": "TODO: Define data retention policy"
            },
            "security": {
                "last_audit": None,
                "known_vulnerabilities": [],
                "injection_tested": False
            },
            "compliance": {
                "frameworks": [],
                "risk_classification": "minimal",
                "human_oversight": "human-above-the-loop"
            },
            "behavior": {
                "logging_enabled": False,
                "log_format": "none",
                "max_actions_per_minute": 0,
                "kill_switch": True,
                "escalation_policy": "TODO: Define what happens on unexpected situations"
            },
            "dependencies": [],
            "metadata": {
                "created_at": "TODO: ISO datetime",
                "updated_at": "TODO: ISO datetime",
                "tags": []
            }
        }

        with open(args.output, "w") as f:
            json.dump(skeleton, f, indent=2)
        print(f"Agent card skeleton written to {args.output}")
        print("Fill in the TODO fields, then run: kya validate " + args.output)


if __name__ == "__main__":
    main()
