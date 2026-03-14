![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-orange?logo=anthropic)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

# Autonomous SEO Agent System

An autonomous, multi-agent SEO system built with [Claude Code](https://claude.ai/code) that continuously optimizes organic search presence, AI answer engine visibility, and agent-readiness — with zero manual intervention between weekly runs.

**Live Demo**: [View the SEO Agent Dashboard](https://growthbyagent.com/project/Agentic-SEO/)

> **Case study**: This system was built and deployed for [Windward.ai](https://windward.ai) — a maritime intelligence company. The dashboard shows real pipeline outputs and agent logic. Replace the industry context with your own to deploy it for any business.

---

## What Is This?

Instead of a single AI assistant answering SEO questions, this system uses **8 specialized agents** operating as a coordinated team, each with a defined scope and data contract. A central Orchestrator agent reads proposals from all analysis agents, resolves conflicts, and drives a prioritized action queue for human teams.

The result: a fully automated SEO pipeline that runs on any cadence (daily, twice weekly, or on-demand), generates content briefs and outreach drafts, syncs to Google Sheets, notifies Slack, and continuously learns from results — with no manual steering required.

---

## The 8 Specialized Agents

| Agent | Slash Command | Role |
|-------|--------------|------|
| **Data Agent** | `/seo-data` | Fetches and normalizes GSC, GA4, PageSpeed, and sitemap data. Caches results to reduce redundant API calls. |
| **Keyword Agent** | `/seo-keywords` | Identifies keyword opportunities using Ahrefs MCP + GSC data. Classifies intent, scores by ROI, and maintains the Glossary Backlog. |
| **Technical Agent** | `/seo-technical` | Audits Core Web Vitals, schema markup, sitemap health, and crawl issues. Produces developer-ready fix specs. |
| **GEO/AEO Agent** | `/seo-geo` | Optimizes content for AI answer engines (Google AI Overviews, Perplexity, ChatGPT). Scores pages for AI fitness and identifies FAQ/schema gaps. |
| **Competitor Agent** | `/seo-competitors` | Monitors competitor content, backlink profiles, and SERP positioning. Identifies gaps and content opportunities. |
| **Content Agent** | `/seo-content` | Generates full content drafts, meta descriptions, and optimization briefs. Enforces brand voice and legal compliance. |
| **Link Building Agent** | `/seo-links` | Finds backlink opportunities, drafts outreach emails, and manages the outreach pipeline. Writes complete guest post articles and PR assets. |
| **AI Agent Readiness Agent** | `/seo-agents` | Ensures the site is discoverable and navigable by autonomous AI agents (OpenAI Operator, Anthropic Computer Use, Google Mariner). |

**Supporting commands**: `/seo-plan` (Orchestrator), `/seo-pipeline` (end-to-end runner), `/seo-protocols` (shared protocols), `/seo-review` (QA gate), `/seo-learning` (algorithm update tracker), `/seo-health-check` (system diagnostics).

---

## What Makes This Different

### 1. Fully Autonomous Execution
The pipeline runs unattended on any schedule. From data fetch to Slack notification to Google Sheets sync — no human in the loop between runs. Human review happens asynchronously via Slack and the dashboard.

### 2. Low-Hanging Fruits Protocol
Every agent is programmed to identify "effort=1" wins first — small changes with outsized impact. Example: updating blog post titles that were getting 330K impressions/week at 0.3% CTR because the title tags didn't match searcher intent. Expected result: 10x CTR improvement with a single metadata change.

### 3. Multi-Agent Consensus with Proposal Buffers
Analysis agents write proposals to `data/proposals/` — they never write directly to the master database. The Orchestrator reads all proposals, resolves conflicts, applies the priority scoring formula `(Business Value × Urgency × Confidence) / Effort`, and produces a single reconciled action queue. This prevents agents from overwriting each other's work.

### 4. Cross-Agent Synthesis
The Orchestrator identifies synergies across proposals. Example: the Data Agent flags a trending topic → the Content Agent drafts a hub page → the Link Building Agent has outreach prospects for that topic. The Orchestrator coordinates all three to execute together for maximum impact.

### 5. Zero-Hallucination Architecture
Every quantitative claim in every proposal must include `data_source` and `fetched_at`. Acceptable sources have defined confidence scores: `ahrefs_mcp` (0.95), `gsc_data` (0.90), `web_search` (0.60). If data is unavailable, agents say "Data not available" — never estimate without evidence.

---

## Data Flow

```
GSC / GA4 / Ahrefs MCP / PageSpeed
         ↓
    /seo-data (Data Agent)
    Normalizes + caches raw data
         ↓
    ┌────┴────────────────────────────────────────┐
    ↓         ↓         ↓         ↓         ↓    ↓
/seo-      /seo-     /seo-     /seo-    /seo-  /seo-
keywords  technical   geo    competitors content  links
    ↓         ↓         ↓         ↓         ↓    ↓
    └────────────────────────────────────────────┘
              ↓ (all write to data/proposals/)
         /seo-plan (Orchestrator)
    Validates → Merges → Prioritizes → Updates master/
         ↓
    ┌────┴────────────────────┐
    ↓                         ↓
Google Sheets Dashboard    Slack Notifications
(Action Queue, Calendar,   (Teams notified with
 Metrics, Content Tracker)  task-specific CTAs)
         ↓
    Human Teams
(Content, Dev, Marketing)
    Execute tasks
         ↓
    /seo-learning
    Updates skills.md
    with results
```

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| [Claude Code](https://claude.ai/code) | The CLI that runs the agents |
| [Ahrefs MCP](https://ahrefs.com/mcp) | Remote MCP server for keyword/backlink data (Standard plan: 150K units/month) |
| Google Cloud Project | For GSC API, PageSpeed API, Sheets API |
| Google Search Console | Verified property for your site |
| Google Sheets | Dashboard spreadsheet (clone the template) |
| Slack Webhook | For pipeline notifications (optional but recommended) |

---

## Setup Instructions

### Step 1: Clone and configure

```bash
git clone https://github.com/Talko90/windward-seo-agent-system.git
cd windward-seo-agent-system
cp scripts/.env.example scripts/.env
# Edit scripts/.env with your API keys
```

### Step 2: Set up Google APIs

1. Create a Google Cloud project at [console.cloud.google.com](https://console.cloud.google.com)
2. Enable: **Search Console API**, **PageSpeed Insights API**, **Google Sheets API**, **Google Drive API**
3. Create OAuth 2.0 credentials (Desktop app type)
4. Download `credentials.json` → save to `scripts/credentials.json`
5. Run `python3 scripts/fetch_gsc.py` once to complete OAuth flow (creates `scripts/token.json`)

### Step 3: Set up Google Sheets dashboard

1. Create a new Google Sheet with these tabs: `Action Queue`, `Weekly Metrics`, `Keywords Tracking`, `Team Progress`, `Content Calendar`, `Content Feedback`, `Glossary Backlog`
2. Copy the Spreadsheet ID from the URL
3. Update `YOUR_GOOGLE_SHEETS_ID` in `CLAUDE.md` and all agent files
4. Share the sheet with your Google service account (Editor permission)

### Step 4: Configure Ahrefs MCP

1. Sign up at [ahrefs.com/mcp](https://ahrefs.com/mcp)
2. Add to your `.mcp.json` in the project root:
```json
{
  "mcpServers": {
    "ahrefs": {
      "command": "npx",
      "args": ["-y", "@ahrefs/mcp"]
    }
  }
}
```
3. Run `/mcp` in Claude Code to authenticate

### Step 5: Update CLAUDE.md for your site

Edit `CLAUDE.md` to replace the example context with your site's:
- Domain and industry context
- Competitor list
- Team routing (who handles content, dev, marketing)
- Google Sheets ID
- Slack webhook URL

### Step 6: Run your first pipeline

```bash
# In Claude Code, run:
/seo-health-check   # Verify all systems working
/seo-data           # Fetch baseline data
/seo-plan           # Generate initial action queue
```

### Step 7: Schedule automated runs (macOS)

```bash
# Edit run-seo-pipeline.sh with your PROJECT_DIR and Slack webhook
chmod +x scripts/run-seo-pipeline.sh

# Add to crontab (runs Sunday + Wednesday at 10:00 AM):
crontab -e
# Add: 0 10 * * 0,3 /path/to/your/seo-project/scripts/run-seo-pipeline.sh
```

---

## Project Structure

```
/
├── index.html                    ← Live dashboard (served by GitHub Pages)
├── CLAUDE.md                     ← Agent configuration and architecture rules
├── skills.md                     ← Continuously updated learnings database
├── .claude/
│   └── commands/                 ← One .md file per agent (slash commands)
│       ├── seo-agents.md         ← AI Agent Readiness Agent
│       ├── seo-competitors.md    ← Competitor Analysis Agent
│       ├── seo-content.md        ← Content Optimization Agent
│       ├── seo-data.md           ← Data Utility Agent
│       ├── seo-geo.md            ← GEO/AEO Agent
│       ├── seo-health-check.md   ← System Diagnostics
│       ├── seo-keywords.md       ← Keyword Research Agent
│       ├── seo-learning.md       ← Algorithm Update Tracker
│       ├── seo-links.md          ← Link Building Agent
│       ├── seo-pipeline.md       ← Full Pipeline Runner
│       ├── seo-plan.md           ← Orchestrator (COO Agent)
│       ├── seo-protocols.md      ← Shared Agent Protocols
│       ├── seo-review.md         ← QA & Security Gate
│       └── seo-technical.md      ← Technical Audit Agent
├── scripts/
│   ├── fetch_gsc.py              ← Google Search Console data fetcher
│   ├── fetch_pagespeed.py        ← PageSpeed Insights fetcher
│   ├── run-seo-pipeline.sh       ← Schedulable pipeline runner
│   └── .env.example              ← Environment variable template
└── data/                         ← Gitignored - created at runtime
    ├── raw/                      ← API responses and exports
    ├── master/                   ← Canonical databases (keywords, content, etc.)
    ├── proposals/                ← Agent proposals awaiting orchestration
    ├── drafts/                   ← Content drafts for human review
    └── reports/                  ← Pipeline run reports
```

---

## Key Design Principles

**Hub-and-Spoke with Proposal Buffers**: Analysis agents write ONLY to `data/proposals/`. Only the Orchestrator (`/seo-plan`) writes to `data/master/`. This prevents race conditions and ensures every change is reviewed before becoming canonical.

**Two-Tier Approval**: Content drafts and marketing materials are auto-approved (teams are notified to review async). Live website changes require explicit human approval before an agent acts.

**Token Efficiency**: All detailed context has been moved to skill files and loaded on-demand. `CLAUDE.md` stays lean — it's an architecture document, not a data dump.

**Anti-Hallucination**: The system treats unsourced claims as errors. Every number needs a `data_source`. Agents that can't verify something say so — they don't estimate.

---

## License

MIT License — use this freely for your own SEO projects.

Built by [Tal Cohen](https://github.com/Talko90) using [Claude Code](https://claude.ai/code) by Anthropic.
