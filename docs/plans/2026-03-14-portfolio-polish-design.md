# Portfolio Polish Design — Dashboard for Marketing Leaders

**Date**: 2026-03-14
**Status**: Approved
**Goal**: Transform the Windward SEO Agent System dashboard into a compelling portfolio showcase for marketing leaders, using a process-first narrative.

---

## Context

This project is being shared publicly on GitHub and hosted on growthbyagent.com / Vercel as a case study of AI-driven growth. Target audience: marketing leaders (CMOs, VPs of Growth, SEO directors). Desired takeaway: "AI agents can replace/augment a traditional SEO team with better coordination and zero hallucination."

**Constraints**: Illustrative data only (no real Windward metrics), hybrid branding (Windward as real case + reusable framework positioning).

---

## Approved Design (Approach A — Light Polish)

### Change 1: Hero Rework

**File**: `index.html` — `.hero` section
**Current**: Generic title + 6 raw KPI stat boxes
**New**:
- Add "Case Study" badge next to the title
- New headline: "Autonomous SEO at Scale"
- New sub: "A live implementation: 10 AI agents replacing the traditional SEO team at Windward.ai — a maritime intelligence company."
- Reduce KPI boxes from 6 to 3 (most story-relevant: Organic Traffic, AI Fitness Score, Agents Running)

### Change 2: Sample Data Disclaimer Banner

**File**: `index.html` — between hero and sticky nav
**New element**: Thin info bar
Content: `ℹ️ Case Study Showcase · Data shown is illustrative, based on real methodology applied to Windward.ai · Built by Tal Cohen · growthbyagent.com`

### Change 3: Reorder Nav — "How It Works" to Section 1

**File**: `index.html` — sticky nav + section order
**Current order**: Performance, Ahrefs, Agent Roster, Keywords, Task Pipeline, Competitors, Status, System Health, How It Works
**New order**: How It Works, Performance, Ahrefs, Agent Roster, Keywords, Task Pipeline, Competitors, Status, System Health
The "How It Works" section HTML block is also moved earlier in the DOM.

### Change 4: GitHub/Deploy CTA Footer

**File**: `index.html` — new section before `</body>`
**New section**:
- Headline: "Deploy this for your own site"
- 2 CTAs: Star on GitHub | Read the setup guide
- Attribution: Built with Claude Code · growthbyagent.com

### Change 5: README Cleanup

**File**: `README.md`
- Replace `USERNAME` placeholder with actual GitHub username (to be provided)
- Update live dashboard URL once deployed

---

## Non-Changes (Intentional)

- Dashboard data values: left as-is (illustrative, clearly labeled)
- All 10 agent cards: kept as-is (impressive on their own)
- Section content: no rewrites of individual sections
- CLAUDE.md: no changes (operational config, not portfolio-facing)
- Agent skill files: no changes
