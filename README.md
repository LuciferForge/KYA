# KYA — Know Your Agent

An open standard for AI agent identity, compliance, and auditability.

## What is KYA?

KYA defines a machine-readable **Agent Card** — a JSON document that declares who an AI agent is, what it can do, and how it has been audited. Think of it as a passport for AI agents.

## Why?

- The EU AI Act requires conformity assessments for high-risk AI systems
- Enterprise procurement questionnaires ask "has your AI been audited?"
- Agent frameworks (MCP, LangChain, CrewAI) have no standard identity format
- No one can answer "what does this agent actually do?" in a verifiable way

KYA fills that gap.

## Quick Start

```bash
pip install kya

# Generate a skeleton agent card
kya init --agent-id "your-org/your-agent" --name "My Agent"

# Validate an agent card
kya validate agent-card.kya.json

# Score completeness
kya score agent-card.kya.json
```

## Agent Card Example

```json
{
  "kya_version": "0.1",
  "agent_id": "luciferforge/mcp-security-audit",
  "name": "MCP Security Audit",
  "version": "0.2.0",
  "purpose": "Scans MCP servers for security vulnerabilities...",
  "agent_type": "tool",
  "owner": {
    "name": "LuciferForge",
    "contact": "luciferforge@proton.me"
  },
  "capabilities": {
    "declared": [
      {"name": "mcp_server_connection", "risk_level": "medium", "scope": "Read-only enumeration"}
    ],
    "denied": ["code_execution", "data_exfiltration"]
  },
  "security": {
    "last_audit": {"date": "2026-03-04", "score": 92, "tool": "mcp-security-audit v0.2.0"},
    "injection_tested": true
  },
  "compliance": {
    "frameworks": ["NIST-AI-RMF", "OWASP-LLM-Top-10"],
    "risk_classification": "minimal",
    "human_oversight": "human-above-the-loop"
  }
}
```

## Part of the LuciferForge Agent Safety Suite

| Package | Purpose |
|---------|---------|
| **kya** | Agent identity and compliance standard |
| [mcp-security-audit](https://pypi.org/project/mcp-security-audit/) | Security scanning for MCP servers |
| [ai-injection-guard](https://pypi.org/project/ai-injection-guard/) | Prompt injection detection (22 patterns) |
| [ai-decision-tracer](https://pypi.org/project/ai-decision-tracer/) | Agent decision audit trails |
| [ai-cost-guard](https://pypi.org/project/ai-cost-guard/) | LLM budget enforcement |
| [agent-safety-mcp](https://pypi.org/project/agent-safety-mcp/) | MCP server wrapping all safety tools |

## License

MIT
