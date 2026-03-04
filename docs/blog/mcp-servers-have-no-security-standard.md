# MCP Servers Have No Security Standard — Here's Why That's a Problem

*Published: March 2026 | By LuciferForge*

The Model Context Protocol (MCP) is exploding. Anthropic open-sourced it, and now every AI agent framework is integrating it. MCP servers give LLMs the ability to read files, call APIs, query databases, execute code, and interact with the real world.

But here's the question nobody is asking: **who audits these servers?**

## The Problem

An MCP server is essentially a trust bridge between an LLM and your infrastructure. When you connect Claude, GPT, or any agent to an MCP server, you're granting it capabilities. Some of those capabilities are dangerous:

- **Filesystem access** — read, write, delete files
- **Code execution** — run arbitrary commands on the host
- **Network egress** — send data to external endpoints
- **Credential access** — read environment variables, config files

There is no standard way to declare what an MCP server can do. No standard way to verify those declarations. No standard way to audit whether the server's actual behavior matches its claims.

You install an MCP server. You connect your agent. You hope for the best.

## What a Security Standard Would Look Like

A proper standard for MCP server security would require:

1. **Capability declaration** — Every server declares what it can do, at what risk level, and with what scope. Not in a README. In a machine-readable format that tooling can verify.

2. **Denied capabilities** — Explicit declaration of what the server *cannot* and *will not* do. A filesystem server that declares `"denied": ["code_execution", "network_egress"]` is making a verifiable claim.

3. **Audit history** — When was this server last scanned? What tool was used? What was the score? If the answer is "never," that's information a deployer needs.

4. **Risk classification** — Is this server minimal risk? High risk? Does it handle PII? The EU AI Act requires this classification for AI systems. MCP servers are components of AI systems.

## KYA: An Open Standard for Agent Identity

We built [KYA (Know Your Agent)](https://github.com/LuciferForge/KYA) to solve this. KYA defines a machine-readable **Agent Card** — a JSON document that declares who an AI agent or MCP server is, what it can do, and how it has been audited.

```bash
pip install kya-agent

# Generate an agent card for your MCP server
kya init --agent-id "your-org/your-server" --name "My MCP Server"

# Validate the card
kya validate agent-card.kya.json

# Score completeness
kya score agent-card.kya.json
```

An agent card covers:
- **Identity** — who owns this, how to contact them
- **Capabilities** — what it can do, what it explicitly denies
- **Security** — audit history, injection testing status
- **Compliance** — EU AI Act risk classification, NIST AI RMF mapping
- **Behavior** — logging, rate limits, kill switch

## The Alternative is Trust

Without a standard like KYA, the MCP ecosystem runs on trust. Trust that the server README is accurate. Trust that the developer thought about security. Trust that nobody injected a malicious tool description.

Trust doesn't scale. Standards do.

## Get Started

- **KYA standard**: [github.com/LuciferForge/KYA](https://github.com/LuciferForge/KYA)
- **Install**: `pip install kya-agent`
- **Scan your MCP server**: `pip install mcp-security-audit`
- **Detect prompt injection**: `pip install ai-injection-guard`

---

*LuciferForge builds open-source security tooling for AI agent systems. Contact: luciferforge@proton.me*
