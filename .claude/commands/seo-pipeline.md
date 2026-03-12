# /seo-pipeline - Full End-to-End SEO Workflow

**Purpose**: Runs the complete SEO optimization pipeline from data refresh through content generation without manual intervention.

**Runtime**: 15-20 minutes (automated, unattended)

**Output**: Comprehensive execution report with all findings, task assignments, and any errors encountered.

---

## What This Does

This skill orchestrates the entire SEO workflow automatically:

1. **Data Refresh** - Fetch latest GSC, GA4, sitemap data
2. **Keyword Analysis** - Identify opportunities
3. **Competitor Analysis** - Detect competitive gaps
4. **GEO/AEO Analysis** - Audit AI readiness
5. **Technical Analysis** - Check site health
6. **Link Building** - Discover opportunities, monitor backlinks
7. **AI Agent Readiness** - Audit agent discoverability and navigation
8. **Orchestration** - Merge proposals and prioritize
9. **QA Review** - Validate quality and security
10. **Content Generation** - Create drafts for approved tasks

**Key Benefit**: Eliminates the need to manually run 9 separate commands and monitor for completion.

---

## Shared Protocols

All phases follow CLAUDE.md protocols:
- **Verification**: Follow Rule 2 (Self-Verification Before Reporting) after each phase
- **Error handling**: Follow Rule 3 (Error Handling Protocol) for all failures
- **Slack**: Follow Slack Notification Protocol after each phase completes
- **Sheets sync**: Follow Google Sheets Sync Protocol when updating dashboard

---

## Workflow (Self-Executing)

### Phase 0: COO Pre-Run Assessment (< 1 min)

**The COO evaluates the current state before deciding what to run.**

1. **Check Last Run Metadata** — Read `data/reports/pipeline_health.json` (if exists):
   - When was the last successful run?
   - Which phases succeeded/failed?
   - Any unresolved errors from last run?

2. **Data Freshness Assessment:**
   - Check `data/raw/ahrefs_last_fetch.json` — Ahrefs data age
   - Check `data/raw/gsc_dump.csv` modification date — GSC data age
   - Check `data/raw/ga4_organic.csv` modification date — GA4 data age

3. **Content Feedback Check:**
   - Read Content Feedback sheet tab for new team feedback since last run
   - Flag any "didn't perform well" entries for priority adjustment

4. **API Credit Check:**
   - Call `mcp__ahrefs__subscription-info-limits-and-usage` to verify Ahrefs credits
   - If < 10% remaining, switch to TARGETED run scope

5. **Decide Run Scope:**
   - **FULL** (default): All phases, all agents — for scheduled Sunday/Wednesday runs
   - **TARGETED**: Only data refresh + specific agents with new proposals — when API credits are low or data is mostly fresh
   - **EMERGENCY**: Only the phase(s) addressing an urgent competitive threat — triggered by competitive alerts

6. **Send Slack "Starting" Notification:**
```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":":rocket: *SEO Pipeline Starting*\nScope: [FULL/TARGETED/EMERGENCY]\nAhrefs data age: [X hours]\nGSC data age: [X days]\nLast run: [date] ([status])"}' \
  'YOUR_SLACK_WEBHOOK_URL'
```

---

### Phase 1: Data Refresh (2-3 min)

Execute `/seo-data` agent.

**Key outputs to verify:**
- `data/raw/gsc_dump.csv`
- `data/raw/sitemap_urls.json`
- `data/master/content_index.json` updated with fresh timestamps

**On failure**: Log error, proceed with cached data, flag in final report.

---

### Phase 2: Keyword Research (3-4 min)

Execute `/seo-keywords` agent.

**Key outputs to verify:**
- `data/proposals/keywords_proposal.json` (with `reasoning` field and confidence scores 0.5-1.0)

**On failure**: Log error, continue to next phase.

---

### Phase 3: Competitor Analysis (3-4 min)

Execute `/seo-competitors` agent.

**Key outputs to verify:**
- `data/proposals/competitors_proposal.json` (with `reasoning` field)
- No false alarms (publication dates < 7 days for "new content")

**On failure**: Log error, continue to next phase.

---

### Phase 4: GEO/AEO Analysis (2-3 min)

Execute `/seo-geo` agent.

**Key outputs to verify:**
- `data/proposals/geo_proposal.json` (with AI Fitness scores and schema reasoning)

**On failure**: Log error, continue to next phase.

---

### Phase 5: Technical Audit (2-3 min)

Execute `/seo-technical` agent.

**Key outputs to verify:**
- `data/proposals/technical_proposal.json` (with Core Web Vitals metrics and severity categories)

**On failure**: Log error, continue to next phase.

---

### Phase 6: Link Building Discovery & Monitoring (2-3 min)

Execute `/seo-links` agent (Discovery + Backlink Monitor modes).

**Key outputs to verify:**
- `data/proposals/links_proposal.json` (with priority scores and reasoning)
- Backlink monitoring data included

**On failure**: Log error, continue to Orchestration. Non-blocking.

---

### Phase 7: AI Agent Readiness Audit (2-3 min)

Execute `/seo-agents` agent.

**Key outputs to verify:**
- `data/proposals/agents_proposal.json` (with Agent Readiness Score 0-100)
- Discovery files checked (llms.txt, robots.txt, agents.json)
- Task flow simulations completed (5 scenarios)
- Competitor benchmark included (if not checked < 14 days ago)

**On failure**: Log error, continue to Orchestration. Non-blocking.

---

### Phase 8: Orchestration (1-2 min)

Execute `/seo-plan` agent.

**Key outputs to verify:**
- `data/master/action_queue.json` updated with new tasks
- All proposals read and merged (including links and agents proposals)
- `data/master/outreach_pipeline.json` and `backlink_monitor.json` updated
- False positive validation applied
- Task assignments made (content-team, yael-webmaster, dev-external, marketing-team)
- Team task reports generated in `data/reports/`
- Dashboard synced via Google Sheets Sync Protocol

**CRITICAL**: If orchestration fails completely, STOP pipeline and report error to user immediately.

---

### Phase 9: QA Review (1-2 min)

Execute `/seo-review` agent.

**Key outputs to verify:**
- Review report saved to `data/reports/qa_review_[timestamp].json`
- Security scan completed (customer names, IMO numbers, credentials)

**QA Gate Logic:**
- **BLOCKING issues found** - STOP pipeline, do NOT proceed to Phase 10
- **WARNING issues found** - Flag in report, proceed to Phase 10
- **PASS** - Proceed to Phase 10

**On failure**: Log error but continue to Phase 10 (manual review preferred over stopping).

---

### Phase 10: Content Generation (2-3 min)

Execute `/seo-content` agent. Only processes tasks with `status: "approved"`.

**Key outputs to verify:**
- All approved tasks processed
- Draft files saved to `data/drafts/ACT-XXX-*.md`
- Schema notes saved separately for dev-external
- Task statuses updated in `action_queue.json`

**On failure**: Log error for each failed task, continue processing remaining tasks.

---

### Phase 11: Dashboard Regeneration (< 1 min)

**MANDATORY**: Regenerate the local HTML dashboard with data from all phases.

The `/seo-plan` step (Phase 8) handles this as its Step 10. Verify:
- `docs/seo-agents-dashboard.html` was updated
- File size > 20KB
- Timestamp in footer matches today's date

**On failure**: Log error, include in final report. Non-blocking.

---

### Phase 12: COO Post-Run Review (< 1 min)

**The COO reviews results and prepares for the next run.**

1. **Compare to Previous Run:**
   - Read `data/reports/pipeline_health.json` for last run's metrics
   - Compare: task count, phase completion rate, error count
   - Flag improvements or regressions

2. **Action Effectiveness Review:**
   - Check `data/master/completed_actions_history.json` for tasks completed 2+ weeks ago
   - Cross-reference with `data/reports/weekly_metrics.json` — did metrics improve?
   - For each completed action: tag as `"effective"`, `"neutral"`, or `"ineffective"`
   - Update `skills.md` with winning patterns and failed approaches

3. **Content Performance Tracking:**
   - Use cached `data/raw/ahrefs_keywords.json` from Phase 1 (`/seo-data`) — do NOT re-fetch from Ahrefs (saves ~550 units)
   - Check if recently published content appears in the cached keyword list
   - Compare actual performance vs expected (from action_queue's `expected_outcome`)
   - Flag content that underperformed expectations for re-optimization

4. **Ahrefs Budget Report:**
   - Call `mcp__ahrefs__subscription-info-limits-and-usage` (free, 0 units)
   - Log: `units_usage_workspace`, `units_limit_workspace`, % remaining
   - Compare to `data/raw/ahrefs_last_fetch.json` → calculate units consumed this run
   - Include in pipeline health and Slack notification

5. **Save Run Metadata** — Write to `data/reports/pipeline_health.json`:
```json
{
  "runs": [
    {
      "run_date": "2026-03-08T10:00:00Z",
      "scope": "FULL",
      "phases_total": 13,
      "phases_succeeded": 12,
      "phases_failed": 1,
      "failed_phases": ["Phase 5: Technical Audit"],
      "tasks_queued": 11,
      "drafts_generated": 5,
      "slack_notifications_sent": 8,
      "duration_minutes": 18,
      "ahrefs_units_used_this_run": 4200,
      "ahrefs_units_remaining": 143000,
      "ahrefs_units_limit": 150000,
      "errors": ["PageSpeed API timeout"]
    }
  ]
}
```
Keep last 20 runs. Flag anomalies after 5+ runs (e.g., duration 2x average, error rate increase).

5. **Send COO Summary Slack Notification** — Final comprehensive message with:
   - Pipeline status (COMPLETED / WITH WARNINGS / FAILED)
   - Key metrics trend (plain English)
   - Tasks queued per team
   - Any competitive alerts
   - Next scheduled run date

---

## Final Report Generation

After all phases complete (or fail), generate a report with these sections:

1. **Phase Status Summary** - Each phase with status (SUCCESS/WARNING/FAILED) and emoji
2. **Key Outputs** - Action Queue task count, Content Drafts count, Top 3 priorities with ACT IDs and scores
3. **Warnings & Errors** - All issues from all phases
4. **Next Steps** - Actionable items per team (content-team, yael-webmaster, dev-external)
5. **Files Updated** - All master DB files, reports, and drafts created/updated
6. **Slack Notifications** - Count of notifications sent
7. **Pipeline Status** - COMPLETED / COMPLETED WITH WARNINGS / FAILED
8. **QA Notes** - Any warnings to review before publishing drafts

---

## Usage

```bash
/seo-pipeline
```

**When to run**: Monday mornings (weekly), after major site changes, before quarterly reporting.

**What happens**: All 10 phases run automatically with real-time progress updates, self-verification, and Slack notifications. No manual monitoring needed.

---

## Pre-Run Checklist

1. All agent skills present in `.claude/commands/`
2. MCP servers configured (Google Sheets)
3. Slack webhook verified
4. Each phase tested independently (first run only)

## Notes

- **Runtime**: 15-20 min typical. Investigate if exceeding 30 min.
- **Learning**: Each run improves via `skills.md` updates.
- **Manual Override**: Interrupt and resume from last completed phase if needed.
- **Success Target** (after 3-5 runs): 95%+ phase completion rate, 8+ Slack notifications per run, 3-8 content drafts per run.
