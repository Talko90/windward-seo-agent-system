# CLAUDE.md

Autonomous SEO agent system for Windward.ai (maritime intelligence). Optimizes for SEO, GEO (AI Overviews), AEO (featured snippets), and AI Agent Readiness.

## Goals

1. Increase organic traffic from search engines and LLMs
2. Improve Windward visibility for maritime intelligence keywords
3. Achieve AI citation/mention in answer engines

## Domain Context

Windward.ai: maritime domain awareness, sanctions compliance, dark fleet detection, AIS data, vessel tracking, deceptive shipping practices, maritime security.

## Architecture: Hub-and-Spoke with Proposal Buffers

**Analysis agents write ONLY to `data/proposals/`**
**Only `/seo-plan` (Orchestrator) writes to `data/master/`**

### Proposal Format

All proposals MUST include a `"reasoning"` field per recommendation:
```json
{"reasoning": {"data_basis": "...", "alternatives_considered": "...", "confidence_rationale": "...", "expected_impact": "..."}}
```

### Task Lifecycle

`pending → approved → in_progress → completed`

### Two-Tier Approval

**Auto-Approved** (status: "approved"):
- Content drafts, content updates, analysis outputs, outreach drafts, guest posts, PR assets
- Anything assigned to `content-team` or `marketing-team`

**Requires Manual Approval** (status: "pending"):
- Live website changes (dev-external, yael-webmaster), schema, technical fixes, URL changes

### Persona System

Each task has a `"persona"` field: `"commercial"` | `"government"` | `"both"`
Persona files in `data/context/`. Must be read by `/seo-content` before drafting.

### Reference Documents

| Document | Location |
|----------|----------|
| Content Priorities | [Google Doc](https://docs.google.com/document/d/YOUR_GOOGLE_DOC_ID_CONTENT_PRIORITIES/edit) |
| Content Feedback | Dashboard > "Content Feedback" tab |
| Content Calendar | Dashboard > "Content Calendar" tab |
| Glossary Backlog | Dashboard > "Glossary Backlog" tab |

Config: `data/context/reference_docs.json`. Read script: `python3 scripts/read_from_drive.py <doc_id>`

### Data Flow

```
/seo-data → raw data → Analysis Agents → proposals/ → /seo-plan → master/ → /seo-content → drafts → Human Teams → skills.md
```

## Execution Rules (CRITICAL)

### Rule 1: Pipeline Completion

**Complete ALL phases of your workflow without stopping mid-execution.**

- Analysis agents: Complete all analysis → write proposal → verify file exists → send Slack → report
- `/seo-plan`: Read ALL proposals → validate → merge → update master → generate reports → sync Sheets → send Slack → archive proposals
- `/seo-content`: Process ALL approved tasks → generate ALL drafts → save files → send Slack
- `/seo-links`: Complete ALL phases → write proposal → save ALL drafts → send Slack

**Golden Rule: If your job involves multiple items, process ALL of them before reporting completion.**

### Rule 2: Self-Verification

Before reporting "task complete," verify:
- All output files exist and are non-empty
- Slack notification sent successfully (response contains "ok")
- No critical errors were silently swallowed
- User knows what was done and what (if anything) failed

### Rule 3: Error Handling

1. Log error to `data/reports/[agent]_errors.log`
2. Retry transient errors (network: 3x with 5s wait; rate limit: 60s then once)
3. Continue workflow — don't let one failure block the pipeline
4. Report all successes, warnings, and failures at end. Never fail silently.

### Rule 4: Data Citation (Zero Hallucinations)

Every quantitative claim MUST include `data_source` and `fetched_at`. Acceptable sources:
- `ahrefs_mcp` (0.95) | `gsc_data` (0.90) | `ga4_data` (0.90) | `web_fetch` (0.80) | `web_search` (0.60) | `calculated` (show formula)

If data unavailable, say "Data not available" — never estimate without basis.

### Rule 5: Anti-Hallucination (ZERO TOLERANCE)

Every number must be traceable. Forbidden: "estimated ~X" without data, traffic projections without historical basis, "competitor likely has..." without data. If unverifiable: `"verified": false`, confidence max 0.5.

### Rule 6: Ahrefs API Unit Budget (CRITICAL)

**Plan: Standard (150,000 units/month, 25 rows max per request). Remote MCP server only (OAuth).**
The local `@ahrefs/mcp` npm package is deprecated and removed. If 403 "Insufficient plan" error occurs, re-authenticate via `/mcp` command or contact Ahrefs support.

| Premium Field | Extra Cost | Avoid Unless Needed |
|---|---|---|
| `volume` | 10 units/row | Use only for final keyword lists |
| `keyword_difficulty` | 10 units/row | Use only for top candidates |
| `sum_traffic` | 10 units/row | Use only for top pages |
| `sum_paid_traffic` | 10 units/row | Almost never needed |

**Minimum 50 units per API call** (even for 1 row). Max 25 rows per request. Budget: ~6,200-8,600 units/run (~17 runs/month).

**Budget guards:** < 20K remaining → ABORT | < 50K → MINIMAL mode | > 50K → FULL mode

**Key rules:** Use `select` for needed columns only. Use `limit` max 25. Cache reuse across agents. Per-agent budgets in `/seo-protocols`.

## Master Database Files

| File | Purpose | Updated By |
|------|---------|------------|
| `keywords_db.json` | Master keyword database | /seo-plan |
| `content_index.json` | All Windward pages indexed | /seo-data, /seo-plan |
| `entity_graph.json` | Knowledge Graph entity mappings | /seo-plan |
| `competitors_db.json` | Competitor tracking | /seo-plan |
| `action_queue.json` | Prioritized task queue | /seo-plan |
| `performance_history.json` | Historical metrics | /seo-plan |
| `outreach_pipeline.json` | Link building outreach tracking | /seo-plan |
| `backlink_monitor.json` | Backlink profile monitoring | /seo-plan |
| `agent_readiness.json` | AI agent readiness scores | /seo-plan |

## Priority Scoring

```
Score = (Business Value × Urgency × Confidence) / Effort
Business Value (1-100) | Urgency: 2.0x drop, 1.5x competitor, 1.0x normal | Confidence (0.5-1.0) | Effort: 1-3
```

## Data Sources

### Ahrefs MCP (PRIMARY — MANDATORY for keyword, backlink, competitor data)

| Priority | Source | Confidence |
|----------|--------|------------|
| 1 | **Ahrefs MCP** — volume, KD, DR, backlinks, competitors, SERP | 0.95 |
| 2 | Google Search Console — clicks, impressions, CTR, position | 0.90 |
| 3 | Google Analytics 4 — sessions, conversions, bounce rate | 0.90 |
| 4 (fallback) | WebSearch — ONLY when Ahrefs unavailable, tag as "unverified" | 0.60 |

If Ahrefs unavailable: state it, lower confidence by 0.3, tag `"unverified"`.

### SEO Dashboard (Google Sheets)

**Spreadsheet**: [Windward SEO Dashboard](https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEETS_ID/edit)

| Tab | Updated By |
|-----|------------|
| Action Queue | `/seo-plan` |
| Weekly Metrics | `/seo-data` |
| Keywords Tracking | `/seo-keywords` |
| Team Progress | `/seo-plan` |
| Content Calendar | `/seo-plan`, `/seo-content` |
| Content Feedback | Team (manual) |
| Glossary Backlog | `/seo-keywords`, `/seo-content` |

## Slack

**Webhook:** `YOUR_SLACK_WEBHOOK_URL`
**Method:** curl via Bash tool (NOT MCP). Send Block Kit JSON. Verify response contains "ok".
**Details:** See `/seo-plan` skill → "Slack Notification Details" section for templates and per-agent content.

## Security

1. **Never hardcode credentials** — use env vars or secure file refs
2. **Never log sensitive data** — no customer names, non-public IMOs, credentials in any output
3. **Validate external URLs** — use reputable sources (IMO.org, OFAC.gov, Lloyd's List)
4. **Sanitize outputs** — no absolute file paths, internal emails, or system details in public content
5. **Data classification**: Public (published news, regulations) | Internal (analytics, GSC data) | Confidential (customer names, non-public IMOs, credentials — NEVER in any output)
6. **Content rule**: Use aggregated stats ("1,400+ vessels" not "1,427 vessels")

See `docs/SECURITY-GUIDELINES.md` for full framework, checklists, incident response.

## Shared Agent Protocols

**All protocols moved to `/seo-protocols` skill for token efficiency.** Includes: Google Sheets Sync, Google Drive Upload, Content Existence Check, Dashboard Regeneration, Slack Notification, Reference Document Loading, Style Guide Compliance, Low-Hanging Fruits, and Ahrefs budget per-agent.

## Cross-References

Detailed content has been moved to skill files and docs/ for token efficiency:

| Topic | Location |
|-------|----------|
| Team roster, task routing, content calendar, agent roster, Slack templates, weekly workflow | `/seo-plan` skill |
| Technical glossary, glossary workflow, legal checklist, approved data points, draft workflow | `/seo-content` skill |
| Seasonal content opportunities | `/seo-keywords` skill |
| MCP configuration, troubleshooting | `/seo-health-check` skill |
| SEO/GEO/AEO best practices, content security checklist | `/seo-review` skill |
| Gemini token optimization, delegation points | `/seo-data` skill |
| Shared protocols, low-hanging fruits, per-agent budgets | `/seo-protocols` skill |
| Monthly review, scoring calibration | `/seo-learning` skill |
| Full security framework, incident response, compliance | `docs/SECURITY-GUIDELINES.md` |
| MCP setup reference | `docs/MCP-SETUP-REFERENCE.md` |
| Troubleshooting guide | `docs/TROUBLESHOOTING.md` |

---

**End of CLAUDE.md**
