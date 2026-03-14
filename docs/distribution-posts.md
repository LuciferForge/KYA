# KYA Distribution Posts

## 1. Hacker News "Show HN" Post

**Title:** Show HN: KYA – Open identity standard for MCP servers

**Body:**

We shipped an open standard for declaring what AI agents (specifically MCP servers) actually do—and proving they're trustworthy to use.

The problem: MCP (Model Context Protocol) is becoming the standard way to connect AI with external tools. But there's no way to know what a server really does, what it accesses, or whether it's been audited. You install it. Hope. That's it.

KYA (Know Your Agent) solves this with a single declarative JSON schema that MCP servers can implement:
- What the server does (plain text, not guessing from code)
- What resources/APIs it touches
- Who audited it and when
- Compliance status (EU AI Act, SOC2, etc.)

It's MIT licensed. We've built reference implementations for 6 common agent safety patterns. Installation: `pip install kya-agent`

The spec is here: https://github.com/LuciferForge/KYA

Real-world use: AI teams now have a machine-readable way to ask "is this agent safe to run?" before execution.

We also offer optional professional audits ($149 flat rate), but the standard itself is completely open and free.

Would love feedback on whether this solves the security visibility problem you're seeing in production MCP deployments.


---

## 2. Reddit r/artificial or r/MachineLearning Post

**Title:** Making AI agents transparent: KYA open standard for compliance and auditing

**Body:**

If you're deploying AI agents in regulated environments (finance, healthcare, EU), you've hit this wall: regulators ask "who built this agent, what does it do, has it been audited?" and you have no structured way to answer.

We built KYA (Know Your Agent) to fix this: an open standard for declaring agent identity, capabilities, and compliance status.

**What it does:**
- Standardizes how agents declare what they do (no more reverse-engineering code)
- Tracks audit status across frameworks (Anthropic, OpenAI, Ollama, custom)
- Connects to EU AI Act categories automatically
- Machine-readable, so compliance tools can actually verify things

**Why this matters:**
- Regulators need proof of auditing. KYA makes it verifiable.
- Teams deploying agents need confidence in what they're using.
- Open source—MIT licensed—so it's not a vendor lock-in.

**Get started:** `pip install kya-agent` then check the docs at https://github.com/LuciferForge/KYA

We've also published a response to NIST-2025-0035 on AI agent security, which covers how identity standards fit into the bigger compliance picture.

If you're dealing with compliance questions around agents, this might save you weeks of documentation work. If you're building agents, it positions you better with customers and regulators.


---

## 3. Reddit r/opensource Post

**Title:** Released: KYA – Open standard for AI agent identity (MIT, 6 packages, fills a gap in agent security tooling)

**Body:**

KYA (Know Your Agent) is an open standard for declaring AI agent identity, capabilities, and compliance status.

**Why it exists:**
AI agents are becoming production infrastructure (Claude integrations, OpenAI plugins, MCP servers, custom LLM tools). But there's no open, standardized way to say what an agent does, what it can access, or whether it's been audited. We built KYA to fill that gap.

**What's in the repo:**
- Core spec (JSON schema) for agent identity
- 6 Python packages covering audit logging, compliance tracking, identity declaration, and verification
- Reference implementations
- Open source (MIT license)

**Install:** `pip install kya-agent`

**Repo:** https://github.com/LuciferForge/KYA

**The pitch:** If you're building agent tooling, security libraries, or compliance software, this is a standardization effort worth contributing to. If you're deploying agents, it gives you a way to verify what you're running.

We're also running an optional audit service for teams that need formal verification, but the standard and all tooling are completely free and open.

Looking for contributors and feedback from the agent security community. This is early—PRs, issues, and thoughts welcome.


---

## 4. MCP Discord / AI Agent Community Post

**Title:** KYA – Identity standard for MCP servers (and other agents)

**Body:**

Hey folks,

We just shipped KYA (Know Your Agent)—a lightweight open standard for declaring what your MCP server actually does.

**The problem you probably have:** You've built an MCP server. It's solid. But when people ask "what does this do, what can it access, has it been audited?" you're explaining it in prose or pointing them at code.

**What KYA does:**
- Single JSON config your server declares once
- Automatic identity verification
- Compliance tracking (EU AI Act, SOC2, etc.)
- Machine-readable so AI tooling can actually understand it

**For MCP devs:**
```
pip install kya-agent
```

Then add identity to your server. Docs here: https://github.com/LuciferForge/KYA

We've also built tooling to verify identities and track audits, so downstream teams can actually trust what they're deploying.

This is MIT—fully open. If you've been frustrated by the lack of agent security standards, come contribute or just use it.

(We do offer professional audits if you want formal verification, but the standard is free.)

Any questions or thoughts on what agent identity should look like?

