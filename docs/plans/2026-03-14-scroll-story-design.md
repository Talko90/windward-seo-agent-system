# Scroll Story Landing Page — Design Document

**Date**: 2026-03-14
**Status**: Approved
**Goal**: Rebuild index.html as a narrative-driven scroll-story landing page that takes marketing leaders through Why → How → Agents → Results, with the existing dashboard data embedded as the proof section.

---

## Design Decisions

- **Format**: Full scroll story, full-viewport sections, dark/light alternating backgrounds
- **Build**: Full rebuild of index.html (not additive). Existing dashboard data sections preserved and moved into Section 5 (Results).
- **Agent section**: Animated hub-and-spoke SVG flow diagram (scroll-triggered, hover interactions)
- **Results section**: Existing dashboard tabs embedded inline — not a separate page
- **Tech**: Vanilla HTML/CSS/JS, no build step, IntersectionObserver for scroll animations, SVG for agent diagram
- **Audience**: Marketing leaders (CMOs, VPs Growth, SEO directors)
- **Tone**: "Here's a real system I built" — confident, specific, not salesy

---

## Page Structure

### Section 1 — HERO (dark, full viewport, `#000d1a`)
- **Badge**: CASE STUDY · WINDWARD.AI
- **Headline**: "What if your SEO team never slept?"
- **Sub**: "We replaced a manual SEO workflow with 10 coordinated AI agents. They run twice a week, automatically — finding opportunities, generating content, building links, and learning from results. Here's the system."
- **3 animated counters**: `10 AI Agents` | `163 Tasks Generated` | `Runs 2×/Week`
- **Scroll cue**: animated arrow pointing down
- **No nav**: story starts uninterrupted

### Section 2 — WHY (light, `#f8fafc`)
- **Headline**: "The old way has a bottleneck. It's you."
- **Layout**: Two columns — Before vs After
- **Before** (left, grayed): Manual keyword research, weekly human review, siloed tools (keyword tool ≠ content tool ≠ link tool), slow feedback loop, expensive team coordination
- **After** (right, colored): 10 agents running in parallel, cross-agent synthesis (keywords → content → links coordinated), continuous execution, data-backed every step
- **Visual**: Simple icon rows with strikethrough/checkmark treatment

### Section 3 — HOW IT WORKS (dark, `#0f172a`)
- **Headline**: "A fully automated pipeline. No human in the loop between runs."
- **Content**: Enhanced 5-step pipeline flow (existing steps, expanded with real specifics)
  - Step 1 Collect: GSC + GA4 + Ahrefs + PageSpeed → cached for all agents
  - Step 2 Analyze: 6 specialist agents run in parallel, each write proposals to a buffer
  - Step 3 Orchestrate: COO agent reads all proposals, resolves conflicts, scores by impact formula
  - Step 4 Execute: Content drafts auto-generated. Technical + website changes → human teams
  - Step 5 Learn: Results measured each run, strategies updated in skills.md
- **Visual**: Horizontal stepper with icons, animated on scroll (fade-in per step)

### Section 4 — AGENT NETWORK (light, `#f8fafc`)
- **Headline**: "10 agents. One coordinated team."
- **Sub**: "Each agent has a defined scope and data contract. No agent overwrites another's work. The Orchestrator is the only one with write access to the master database."
- **Visual**: Animated SVG hub-and-spoke diagram
  - Center: Orchestrator (COO) — crown icon, large circle
  - Inner ring: Data Agent — feeds all others
  - Outer ring: 8 specialist agents (Keyword, Technical, GEO, Competitors, Content, Links, AI-Readiness, Learning)
  - Animated arrows: pulse effect showing data flow direction (agents → Orchestrator)
  - Scroll-triggered: agents appear one by one (staggered fade-in)
  - Hover: agent card expands showing role + inputs + outputs
- **Below diagram**: compact 2-column grid with agent name + one-sentence role

### Section 5 — RESULTS: Live Dashboard (white, `#ffffff`)
- **Intro headline**: "7 pipeline runs later."
- **Sub**: "This is the actual output — keywords tracked, tasks prioritized, competitors monitored. Sample data based on real methodology."
- **Sample data badge**: amber disclaimer strip (same as current)
- **Content**: The existing dashboard sections in a tabbed interface
  - Tab 1: Performance (traffic charts, Ahrefs metrics)
  - Tab 2: Agent Roster (agent grid with status)
  - Tab 3: Keywords (keyword table with filters)
  - Tab 4: Task Pipeline (action queue, stacked bars)
  - Tab 5: Competitors (competitor cards)
- **Sticky tab nav**: tabs stick to top as user scrolls through results

### Section 6 — CTA (dark, `#0f172a`)
- **Headline**: "Deploy this for your own site"
- **Sub**: "The full system — agents, scripts, and dashboard — is open-source. Replace the Windward context with your domain, and run your first pipeline in an afternoon."
- **Buttons**: ★ Star on GitHub | growthbyagent.com
- **Footer line**: Built with Claude Code · MIT License · Open source

---

## Technical Specifications

### Animations
- **Scroll-triggered**: IntersectionObserver (threshold: 0.2) — fade-in + translateY(20px → 0)
- **Counters**: Animate from 0 to target on first viewport entry (same JS as current)
- **Agent SVG**: Staggered appearance (150ms delay per agent), then continuous pulse on arrows
- **Step diagram**: Each step fades in sequentially as section enters viewport

### Agent Network SVG
- Pure SVG + CSS animations (no external library)
- Viewbox: 600×600, responsive with `viewBox` + `width: 100%`
- Orchestrator: center circle, r=60, dark fill
- 8 outer agents: r=40, arranged in circle, r_orbit=220
- Connecting lines with animated `stroke-dashoffset` for pulse effect
- Hover: SVG foreignObject or CSS tooltip showing agent details

### Navigation
- No top nav initially (hero is full screen)
- After scrolling past hero: fixed pill-style nav appears (Why | How | Agents | Results | GitHub)
- Smooth scroll on click

### Preserved from Current Dashboard
All existing HTML for these sections is kept verbatim, moved into Section 5 tabs:
- Performance Trends charts
- Ahrefs Intelligence metrics
- Agent Roster grid
- Keyword Rankings table + filters
- Task Pipeline (stacked bars + action queue)
- Competitor Landscape cards
- Current Status + System Health

### Removed from Current Dashboard
- The standalone sticky nav (replaced by the scroll story nav)
- The hero section (replaced by Section 1)
- The "How It Works" section (replaced by Section 3 — enhanced)
- The current footer (replaced by Section 6 CTA)

---

## Color System
- Dark sections: `#0f172a` (navy) background, white text
- Light sections: `#f8fafc` (slate-50) background, dark text
- Accent: `#2563eb` (blue) for CTAs and highlights
- Agent diagram colors: each agent gets a distinct accent color matching existing badge system

---

## Files Changed
- `index.html` — full rewrite
- `public/project/Agentic-SEO/index.html` in growthbyagent repo — sync after

---

## Non-Goals
- No external JS libraries (keep it vanilla)
- No server-side rendering
- No real-time data fetching
- No dark mode toggle
