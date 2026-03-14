# KYA Roadmap — March 2026 → March 2027

*Saved: March 4, 2026*

## The Forcing Function

- **August 2026**: EU AI Act enforcement begins. Agent identity becomes legally required.
- **By December 2026**: MCP servers go from hundreds to tens of thousands.
- **By March 2027**: Multi-agent systems are mainstream. Identity at every hop.

## Evolution: Document → Protocol

| | March 2026 | March 2027 |
|---|---|---|
| **Format** | Static JSON file in a repo | Signed, cryptographically verifiable card (like JWT) |
| **Verification** | `kya validate` CLI | Real-time API verification at runtime |
| **Discovery** | Manual — read the repo | Registry — agents look up other agents' cards automatically |
| **Trust** | "I read the JSON and it looks fine" | Cryptographic chain — card signed by issuer, audit signed by auditor |
| **Integration** | CLI tool | GitHub Action, CI/CD plugin, MCP middleware |
| **Scope** | Single agent | Agent relationship graphs — trust chains, delegation |

## Quarterly Plan

### Q2 2026 (Now → June)
- KYA v0.2 — cryptographic signing for agent cards
- GitHub Action — validate KYA card on every push
- First paying audit clients ($149 flat rate)
- Community contributors start appearing
- Distribution: HN, Reddit, MCP Discord, AI safety communities

### Q3 2026 (July → September)
- KYA Registry v1 — hosted service for agent card registration
- API endpoint: "give me the verified card for agent X"
- EU AI Act enforcement begins — demand spikes
- Pricing: $10/mo per registered agent

### Q4 2026 (October → December)
- Enterprise tier — verification API, bulk registration, audit dashboard
- Formal verification add-on (parked idea becomes premium upsell)
- $500-$5,000/mo enterprise contracts
- First conference talk or published paper citing KYA

### Q1 2027 (January → March)
- KYA becomes a protocol, not just a format
- Real-time agent-to-agent card verification
- Trust chains — transitive trust between verified agents
- LuciferForge = the Let's Encrypt of agent identity

## Revenue Trajectory

| Phase | Revenue Source | Target |
|-------|--------------|--------|
| Now | $149 audits | First client by March 31 |
| Q2 | Audits + GitHub Sponsors | $500-1000/mo |
| Q3 | Registry SaaS ($10/agent/mo) | $2,000-5,000/mo |
| Q4 | Enterprise contracts | $5,000-15,000/mo |
| Q1 2027 | SaaS + Enterprise + Consulting | $15,000-30,000/mo |

## Thinking Shifts

| Today | One Year From Now |
|-------|-------------------|
| "Can I build it alone?" | "Which contributions do we accept?" |
| "Will anyone use this?" | "Which enterprise do we prioritize?" |
| Solo dev shipping code | Standard maintainer with governance |
| Revenue = $0 | Recurring SaaS + enterprise consulting |
| Credibility = PyPI packages | NIST record + enterprise adopters + community |

## The Thesis

Tools get replaced. Infrastructure gets embedded. KYA is infrastructure.

SSL certificates were optional in 2010. By 2018 Chrome marked HTTP as "Not Secure." Agent cards are optional in 2026. By 2028, agent frameworks refuse unverified agents. We wrote that standard.
