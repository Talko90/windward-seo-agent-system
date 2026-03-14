# Scroll Story Landing Page — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rebuild index.html as a narrative scroll-story landing page with 6 full-viewport sections: Hero → Why → How → Agent Network (animated SVG) → Results (tabbed dashboard) → CTA.

**Architecture:** Single vanilla HTML file. New story sections (1–4, 6) written from scratch. Existing dashboard content (Performance, Ahrefs, Agent Roster, Keywords, Pipeline, Competitors, Status, Health) preserved verbatim and moved into Section 5 as tabs. IntersectionObserver drives all scroll animations. Pure SVG + CSS for agent network — no external libraries.

**Tech Stack:** HTML5, CSS3 (custom properties, grid, flexbox, keyframe animations), vanilla JS (IntersectionObserver, SVG manipulation). No build step. Open directly in browser to test.

**Reference files:**
- Current dashboard: `index.html` (1222 lines) — sections at lines 525–1112 are preserved in Task 6
- Design doc: `docs/plans/2026-03-14-scroll-story-design.md`

---

## Before You Start

The existing `index.html` has dashboard content we need to preserve. Before touching anything:

```bash
cp index.html index.html.bak
```

Open `index.html.bak` in a browser tab — keep it open as reference throughout.

---

### Task 1: New HTML File — Scaffold, Design Tokens, Base CSS

**File:** `index.html` (full replacement)

**What this produces:** A blank 6-section page with correct colors, typography, layout tokens, and section backgrounds. No content yet — just structure you can scroll through and verify.

**Step 1: Replace the entire file with this scaffold**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Autonomous SEO at Scale — Windward.ai Case Study</title>
<style>

/* ══════════════════════════════════════
   DESIGN TOKENS
══════════════════════════════════════ */
:root {
  --navy:    #0a0f1e;
  --navy-2:  #0f172a;
  --navy-3:  #1e293b;
  --slate-50:  #f8fafc;
  --slate-100: #f1f5f9;
  --slate-200: #e2e8f0;
  --slate-300: #cbd5e1;
  --slate-400: #94a3b8;
  --slate-500: #64748b;
  --slate-600: #475569;
  --slate-700: #334155;
  --slate-800: #1e293b;
  --slate-900: #0f172a;
  --blue:    #2563eb;
  --blue-light: #dbeafe;
  --cyan:    #0891b2;
  --green:   #16a34a;
  --green-light: #dcfce7;
  --purple:  #8b5cf6;
  --purple-light: #f3e8ff;
  --red:     #dc2626;
  --red-light: #fef2f2;
  --orange:  #f59e0b;
  --orange-light: #fff7ed;
  --white:   #ffffff;
  --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  --radius: 8px;
  --shadow: 0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
  --shadow-lg: 0 4px 12px rgba(0,0,0,.08);
}

/* ══════════════════════════════════════
   RESET & BASE
══════════════════════════════════════ */
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--font);
  color: var(--slate-800);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}
a { text-decoration: none; }
ul { list-style: none; }

/* ══════════════════════════════════════
   SCROLL ANIMATION BASE
══════════════════════════════════════ */
.reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
.reveal-delay-1 { transition-delay: 0.1s; }
.reveal-delay-2 { transition-delay: 0.2s; }
.reveal-delay-3 { transition-delay: 0.3s; }
.reveal-delay-4 { transition-delay: 0.4s; }
.reveal-delay-5 { transition-delay: 0.5s; }

/* ══════════════════════════════════════
   FLOATING NAV (appears after hero)
══════════════════════════════════════ */
.story-nav {
  position: fixed;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  background: rgba(10, 15, 30, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 40px;
  padding: 8px 16px;
  display: flex;
  gap: 4px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}
.story-nav.visible {
  opacity: 1;
  pointer-events: all;
}
.story-nav a {
  color: rgba(255,255,255,.7);
  font-size: 13px;
  font-weight: 500;
  padding: 6px 14px;
  border-radius: 20px;
  transition: all .15s;
}
.story-nav a:hover, .story-nav a.active {
  background: rgba(255,255,255,.12);
  color: white;
}

/* ══════════════════════════════════════
   SECTION WRAPPERS
══════════════════════════════════════ */
.story-section {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 80px 24px;
}
.story-section.dark { background: var(--navy-2); color: white; }
.story-section.light { background: var(--slate-50); color: var(--slate-900); }
.story-section.white { background: var(--white); color: var(--slate-900); }

.story-inner {
  max-width: 1100px;
  margin: 0 auto;
  width: 100%;
}

.story-eyebrow {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: .08em;
  text-transform: uppercase;
  margin-bottom: 16px;
  opacity: .6;
}
.story-h1 {
  font-size: clamp(36px, 6vw, 64px);
  font-weight: 800;
  letter-spacing: -.03em;
  line-height: 1.1;
  margin-bottom: 20px;
}
.story-h2 {
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 800;
  letter-spacing: -.02em;
  line-height: 1.15;
  margin-bottom: 16px;
}
.story-lead {
  font-size: clamp(15px, 2vw, 18px);
  line-height: 1.7;
  max-width: 640px;
  opacity: .8;
  margin-bottom: 40px;
}

/* ══════════════════════════════════════
   UTILITY
══════════════════════════════════════ */
.badge-pill {
  display: inline-block;
  background: rgba(255,255,255,.1);
  border: 1px solid rgba(255,255,255,.18);
  color: rgba(255,255,255,.85);
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: .06em;
  text-transform: uppercase;
  margin-bottom: 20px;
}
.badge-pill.light {
  background: var(--blue-light);
  border-color: var(--blue);
  color: var(--blue);
}

/* ══════════════════════════════════════
   PLACEHOLDER SECTIONS (filled in later tasks)
══════════════════════════════════════ */
/* Task-specific CSS added below each section */

</style>
</head>
<body>

<!-- FLOATING NAV -->
<nav class="story-nav" id="story-nav">
  <a href="#why">Why</a>
  <a href="#how">How</a>
  <a href="#agents">Agents</a>
  <a href="#results">Results</a>
  <a href="https://github.com/Talko90/windward-seo-agent-system" target="_blank">★ GitHub</a>
</nav>

<!-- S1: HERO -->
<section class="story-section dark" id="hero">
  <div class="story-inner">HERO — Task 2</div>
</section>

<!-- S2: WHY -->
<section class="story-section light" id="why">
  <div class="story-inner">WHY — Task 3</div>
</section>

<!-- S3: HOW -->
<section class="story-section dark" id="how">
  <div class="story-inner">HOW — Task 4</div>
</section>

<!-- S4: AGENTS -->
<section class="story-section light" id="agents">
  <div class="story-inner">AGENTS — Task 5</div>
</section>

<!-- S5: RESULTS -->
<section class="story-section white" id="results">
  <div class="story-inner">RESULTS — Task 6</div>
</section>

<!-- S6: CTA -->
<section class="story-section dark" id="cta">
  <div class="story-inner">CTA — Task 7</div>
</section>

<script>
// ── Scroll reveal ──
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Nav visibility ──
const heroSection = document.getElementById('hero');
const storyNav = document.getElementById('story-nav');
const navObserver = new IntersectionObserver((entries) => {
  storyNav.classList.toggle('visible', !entries[0].isIntersecting);
}, { threshold: 0.1 });
navObserver.observe(heroSection);
</script>
</body>
</html>
```

**Step 2: Verify in browser**

Open `index.html` in a browser. You should see:
- 6 tall sections alternating dark/light/dark/light/white/dark
- Each section has placeholder text identifying the task
- Floating nav is hidden (appears after scrolling past hero)
- Scroll past the hero: nav pill appears at top center

**Step 3: Commit**
```bash
git add index.html
git commit -m "feat: scaffold scroll story page — 6 sections + base CSS"
```

---

### Task 2: Section 1 — Hero

**File:** `index.html` — replace `<!-- S1: HERO -->` section and add CSS

**Step 1: Add hero CSS** inside `<style>` before the closing `</style>`:

```css
/* ══════════════════════════════════════
   S1: HERO
══════════════════════════════════════ */
#hero {
  background: linear-gradient(160deg, #0a0f1e 0%, #0f2040 50%, #0a1628 100%);
  position: relative;
  overflow: hidden;
}
#hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 50% at 70% 50%, rgba(37,99,235,.08) 0%, transparent 70%),
    repeating-linear-gradient(90deg, rgba(255,255,255,.02) 0, rgba(255,255,255,.02) 1px, transparent 1px, transparent 80px),
    repeating-linear-gradient(0deg, rgba(255,255,255,.02) 0, rgba(255,255,255,.02) 1px, transparent 1px, transparent 80px);
  pointer-events: none;
}
.hero-inner { position: relative; z-index: 1; }
.hero-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  max-width: 600px;
  margin-bottom: 40px;
}
.hero-stat-box {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 12px;
  padding: 20px 16px;
  text-align: center;
}
.hero-stat-num {
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -.03em;
  color: white;
  line-height: 1;
}
.hero-stat-label {
  font-size: 11px;
  color: rgba(255,255,255,.5);
  text-transform: uppercase;
  letter-spacing: .07em;
  margin-top: 6px;
}
.hero-scroll-cue {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: rgba(255,255,255,.4);
  cursor: pointer;
  border: none;
  background: none;
  font-family: var(--font);
}
.scroll-arrow {
  width: 32px;
  height: 32px;
  border: 1px solid rgba(255,255,255,.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  animation: bounce 2s infinite;
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(5px); }
}
```

**Step 2: Replace the hero section HTML:**

```html
<!-- S1: HERO -->
<section class="story-section dark" id="hero">
  <div class="story-inner hero-inner">
    <div class="badge-pill reveal">CASE STUDY &mdash; WINDWARD.AI</div>
    <h1 class="story-h1 reveal reveal-delay-1">What if your SEO team<br>never slept?</h1>
    <p class="story-lead reveal reveal-delay-2">
      We replaced a manual SEO workflow with 10 coordinated AI agents.<br>
      They run twice a week, automatically &mdash; finding opportunities, generating content,
      building links, and learning from results. Here&rsquo;s the system.
    </p>
    <div class="hero-stats reveal reveal-delay-3">
      <div class="hero-stat-box">
        <div class="hero-stat-num">10</div>
        <div class="hero-stat-label">AI Agents</div>
      </div>
      <div class="hero-stat-box">
        <div class="hero-stat-num" data-target="163">0</div>
        <div class="hero-stat-label">Tasks Generated</div>
      </div>
      <div class="hero-stat-box">
        <div class="hero-stat-num">2×</div>
        <div class="hero-stat-label">Per Week</div>
      </div>
    </div>
    <button class="hero-scroll-cue reveal reveal-delay-4" onclick="document.getElementById('why').scrollIntoView({behavior:'smooth'})">
      <span class="scroll-arrow">↓</span>
      <span>See how it works</span>
    </button>
  </div>
</section>
```

**Step 3: Verify**

Open in browser. The hero should:
- Fill the full viewport with a dark navy gradient + subtle grid pattern
- Show headline, lead text, 3 stat boxes, scroll cue
- Stat box for "Tasks Generated" should animate 0→163 on load
- Scrolling past hero: floating nav appears

> The counter animation JS goes in Task 8. For now the "163" will show as 0 until Task 8.

**Step 4: Commit**
```bash
git add index.html
git commit -m "feat: add hero section — headline, stats, scroll cue"
```

---

### Task 3: Section 2 — Why (Before/After)

**File:** `index.html`

**Step 1: Add Why CSS** inside `<style>`:

```css
/* ══════════════════════════════════════
   S2: WHY
══════════════════════════════════════ */
.why-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  margin-top: 48px;
}
.why-col {
  padding: 32px;
  border-radius: 16px;
}
.why-col.before {
  background: white;
  border: 1px solid var(--slate-200);
}
.why-col.after {
  background: var(--navy-2);
  color: white;
  border: 1px solid rgba(37,99,235,.3);
  box-shadow: 0 0 40px rgba(37,99,235,.08);
}
.why-col-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
  margin-bottom: 20px;
}
.why-col.before .why-col-label { color: var(--slate-400); }
.why-col.after .why-col-label { color: var(--blue); }
.why-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(0,0,0,.06);
  font-size: 14px;
  line-height: 1.5;
}
.why-col.after .why-item { border-bottom-color: rgba(255,255,255,.08); }
.why-item:last-child { border-bottom: none; }
.why-icon {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  flex-shrink: 0;
  margin-top: 1px;
}
.why-col.before .why-icon { background: #fee2e2; color: #991b1b; }
.why-col.after .why-icon { background: rgba(22,163,74,.2); color: #4ade80; }
.why-col.before .why-item-text { color: var(--slate-500); text-decoration: line-through; text-decoration-color: var(--slate-300); }
.why-col.after .why-item-text { color: rgba(255,255,255,.85); }
@media (max-width: 700px) { .why-grid { grid-template-columns: 1fr; } }
```

**Step 2: Replace the Why section HTML:**

```html
<!-- S2: WHY -->
<section class="story-section light" id="why">
  <div class="story-inner">
    <div class="badge-pill light reveal">The Problem</div>
    <h2 class="story-h2 reveal reveal-delay-1">The old way has a<br>bottleneck. It&rsquo;s you.</h2>
    <p class="story-lead reveal reveal-delay-2">
      Traditional SEO requires constant human coordination — a keyword researcher
      talks to a content writer who talks to a dev who talks to a link builder.
      Each handoff loses context. Each week starts from scratch.
    </p>
    <div class="why-grid">
      <div class="why-col before reveal reveal-delay-2">
        <div class="why-col-label">❌ The Old Way</div>
        <div class="why-item"><div class="why-icon">✕</div><span class="why-item-text">Weekly manual keyword research — slow, incomplete, siloed</span></div>
        <div class="why-item"><div class="why-icon">✕</div><span class="why-item-text">SEO tools don't talk to content tools — context lost at every handoff</span></div>
        <div class="why-item"><div class="why-icon">✕</div><span class="why-item-text">Human review bottleneck — insights queue up, opportunities expire</span></div>
        <div class="why-item"><div class="why-icon">✕</div><span class="why-item-text">No cross-channel synthesis — keyword wins don't inform link strategy</span></div>
        <div class="why-item"><div class="why-icon">✕</div><span class="why-item-text">Expensive team coordination for recurring, structured work</span></div>
        <div class="why-item"><div class="why-icon">✕</div><span class="why-item-text">Learning dies with the analyst who leaves</span></div>
      </div>
      <div class="why-col after reveal reveal-delay-3">
        <div class="why-col-label">✓ The New Way</div>
        <div class="why-item"><div class="why-icon">✓</div><span class="why-item-text">10 agents run in parallel every week — no human to schedule</span></div>
        <div class="why-item"><div class="why-icon">✓</div><span class="why-item-text">Data Agent feeds all analysts from one cache — no context loss</span></div>
        <div class="why-item"><div class="why-icon">✓</div><span class="why-item-text">Orchestrator merges proposals instantly — nothing queues</span></div>
        <div class="why-item"><div class="why-icon">✓</div><span class="why-item-text">Cross-agent synthesis: keyword drop triggers content + link update together</span></div>
        <div class="why-item"><div class="why-icon">✓</div><span class="why-item-text">Human review only for live site changes — everything else auto-approved</span></div>
        <div class="why-item"><div class="why-icon">✓</div><span class="why-item-text">Learning accumulates in skills.md — every run the system gets smarter</span></div>
      </div>
    </div>
  </div>
</section>
```

**Step 3: Verify**

Two-column before/after layout. Before column: grayed out with strikethrough text. After column: dark navy with green checkmarks.

**Step 4: Commit**
```bash
git add index.html
git commit -m "feat: add Why section — before/after comparison"
```

---

### Task 4: Section 3 — How It Works (Enhanced Pipeline)

**File:** `index.html`

**Step 1: Add How CSS** inside `<style>`:

```css
/* ══════════════════════════════════════
   S3: HOW IT WORKS
══════════════════════════════════════ */
.pipeline-flow {
  display: flex;
  align-items: flex-start;
  gap: 0;
  margin-top: 48px;
  position: relative;
}
.pipeline-step-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}
.pipeline-step-wrap:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 36px;
  left: calc(50% + 36px);
  right: calc(-50% + 36px);
  height: 2px;
  background: linear-gradient(90deg, rgba(37,99,235,.6), rgba(8,145,178,.3));
}
.pipeline-node {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin-bottom: 16px;
  position: relative;
  z-index: 1;
}
.pipeline-step-num-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--navy-2);
  border: 2px solid var(--blue);
  color: var(--blue);
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}
.pipeline-step-title {
  font-size: 14px;
  font-weight: 700;
  color: white;
  text-align: center;
  margin-bottom: 8px;
}
.pipeline-step-detail {
  font-size: 12px;
  color: rgba(255,255,255,.5);
  text-align: center;
  line-height: 1.5;
  padding: 0 8px;
}
.pipeline-meta {
  margin-top: 48px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.pipeline-meta-item {
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 10px;
  padding: 16px 20px;
}
.pipeline-meta-label {
  font-size: 11px;
  color: rgba(255,255,255,.4);
  text-transform: uppercase;
  letter-spacing: .06em;
  margin-bottom: 4px;
}
.pipeline-meta-value {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255,255,255,.85);
}
@media (max-width: 700px) {
  .pipeline-flow { flex-direction: column; gap: 24px; }
  .pipeline-step-wrap::after { display: none; }
  .pipeline-meta { grid-template-columns: 1fr; }
}
```

**Step 2: Replace the How section HTML:**

```html
<!-- S3: HOW IT WORKS -->
<section class="story-section dark" id="how">
  <div class="story-inner">
    <div class="badge-pill reveal">The System</div>
    <h2 class="story-h2 reveal reveal-delay-1">A fully automated pipeline.<br>No human in the loop between runs.</h2>
    <p class="story-lead reveal reveal-delay-2">
      Every week, the system completes all 5 phases without stopping.
      From raw data to Slack notification in one unattended run.
    </p>

    <div class="pipeline-flow">
      <div class="pipeline-step-wrap reveal reveal-delay-1">
        <div class="pipeline-node" style="background:linear-gradient(135deg,#2563eb,#0891b2)">
          📡<span class="pipeline-step-num-badge">1</span>
        </div>
        <div class="pipeline-step-title">Collect</div>
        <div class="pipeline-step-detail">GSC, GA4, Ahrefs MCP, PageSpeed — all cached for the week</div>
      </div>
      <div class="pipeline-step-wrap reveal reveal-delay-2">
        <div class="pipeline-node" style="background:linear-gradient(135deg,#8b5cf6,#6366f1)">
          🔍<span class="pipeline-step-num-badge">2</span>
        </div>
        <div class="pipeline-step-title">Analyze</div>
        <div class="pipeline-step-detail">8 specialist agents each examine a different angle, writing proposals to a shared buffer</div>
      </div>
      <div class="pipeline-step-wrap reveal reveal-delay-3">
        <div class="pipeline-node" style="background:linear-gradient(135deg,#f59e0b,#d97706)">
          👑<span class="pipeline-step-num-badge">3</span>
        </div>
        <div class="pipeline-step-title">Orchestrate</div>
        <div class="pipeline-step-detail">COO agent reads all proposals, resolves conflicts, scores by impact ÷ effort</div>
      </div>
      <div class="pipeline-step-wrap reveal reveal-delay-4">
        <div class="pipeline-node" style="background:linear-gradient(135deg,#16a34a,#059669)">
          ✍️<span class="pipeline-step-num-badge">4</span>
        </div>
        <div class="pipeline-step-title">Execute</div>
        <div class="pipeline-step-detail">Content drafts auto-generated. Technical changes routed to human teams</div>
      </div>
      <div class="pipeline-step-wrap reveal reveal-delay-5">
        <div class="pipeline-node" style="background:linear-gradient(135deg,#0891b2,#0e7490)">
          📚<span class="pipeline-step-num-badge">5</span>
        </div>
        <div class="pipeline-step-title">Learn</div>
        <div class="pipeline-step-detail">Results measured. System updates its strategy — every run builds on the last</div>
      </div>
    </div>

    <div class="pipeline-meta">
      <div class="pipeline-meta-item reveal reveal-delay-1">
        <div class="pipeline-meta-label">Cadence</div>
        <div class="pipeline-meta-value">Twice weekly via cron (Sun + Wed, 10 AM)</div>
      </div>
      <div class="pipeline-meta-item reveal reveal-delay-2">
        <div class="pipeline-meta-label">Data Sources</div>
        <div class="pipeline-meta-value">Ahrefs MCP · Google Search Console · GA4 · PageSpeed API</div>
      </div>
      <div class="pipeline-meta-item reveal reveal-delay-3">
        <div class="pipeline-meta-label">Human Touchpoints</div>
        <div class="pipeline-meta-value">Live site changes only — everything else auto-approved</div>
      </div>
    </div>
  </div>
</section>
```

**Step 3: Verify**

5-step horizontal pipeline with colored circles and connecting lines. 3 meta cards below. Steps animate in on scroll.

**Step 4: Commit**
```bash
git add index.html
git commit -m "feat: add How It Works section — enhanced pipeline diagram"
```

---

### Task 5: Section 4 — Agent Network (Animated SVG)

This is the most complex section. The SVG hub-and-spoke diagram uses pure CSS `stroke-dashoffset` animation to create a "data pulse" effect on connecting lines.

**File:** `index.html`

**Step 1: Add Agent Network CSS** inside `<style>`:

```css
/* ══════════════════════════════════════
   S4: AGENT NETWORK
══════════════════════════════════════ */
.agent-network-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 48px;
  gap: 48px;
}
.agent-svg-wrap {
  width: 100%;
  max-width: 600px;
}
.agent-svg-wrap svg {
  width: 100%;
  height: auto;
  overflow: visible;
}

/* Agent node circles */
.agent-node-circle {
  cursor: pointer;
  transition: transform 0.2s ease;
  transform-origin: center;
  transform-box: fill-box;
}
.agent-node-circle:hover { transform: scale(1.1); }

/* Connecting lines with pulse animation */
@keyframes dash-flow {
  from { stroke-dashoffset: 40; }
  to { stroke-dashoffset: 0; }
}
.agent-line {
  stroke-dasharray: 6 4;
  animation: dash-flow 1.2s linear infinite;
  opacity: 0.5;
}

/* Staggered appearance */
.agent-node { opacity: 0; transition: opacity 0.5s ease; }
.agent-network-wrap.animate .agent-node { opacity: 1; }
.agent-network-wrap.animate .agent-node:nth-child(1) { transition-delay: 0.0s; }
.agent-network-wrap.animate .agent-node:nth-child(2) { transition-delay: 0.1s; }
.agent-network-wrap.animate .agent-node:nth-child(3) { transition-delay: 0.2s; }
.agent-network-wrap.animate .agent-node:nth-child(4) { transition-delay: 0.3s; }
.agent-network-wrap.animate .agent-node:nth-child(5) { transition-delay: 0.4s; }
.agent-network-wrap.animate .agent-node:nth-child(6) { transition-delay: 0.5s; }
.agent-network-wrap.animate .agent-node:nth-child(7) { transition-delay: 0.6s; }
.agent-network-wrap.animate .agent-node:nth-child(8) { transition-delay: 0.7s; }
.agent-network-wrap.animate .agent-node:nth-child(9) { transition-delay: 0.8s; }
.agent-network-wrap.animate .agent-node:nth-child(10) { transition-delay: 0.9s; }

/* Agent grid below SVG */
.agent-list-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  width: 100%;
  max-width: 800px;
}
.agent-list-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: 10px;
  box-shadow: var(--shadow);
  transition: border-color .15s;
}
.agent-list-item:hover { border-color: var(--blue); }
.agent-list-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}
.agent-list-name { font-size: 13px; font-weight: 600; color: var(--slate-800); }
.agent-list-role { font-size: 12px; color: var(--slate-500); line-height: 1.4; }
@media (max-width: 600px) { .agent-list-grid { grid-template-columns: 1fr; } }
```

**Step 2: Replace the Agents section HTML:**

The SVG uses a 600×560 viewBox. Orchestrator at center (300, 280). Data Agent in the inner ring (300, 140). 8 specialist agents in the outer ring at evenly spaced angles.

**Agent positions** (outer ring, r=210 from center 300,280):
- Keyword: (300+210×sin(0°), 280-210×cos(0°)) = (300, 70)
- Technical: (300+210×sin(45°), 280-210×cos(45°)) = (449, 131)
- GEO: (300+210×sin(90°), 280-210×cos(90°)) = (510, 280)
- Competitors: (300+210×sin(135°), 280-210×cos(135°)) = (449, 429)
- Content: (300+210×sin(180°), 280-210×cos(180°)) = (300, 490)
- Links: (300+210×sin(225°), 280-210×cos(225°)) = (151, 429)
- AI-Ready: (300+210×sin(270°), 280-210×cos(270°)) = (90, 280)
- Learning: (300+210×sin(315°), 280-210×cos(315°)) = (151, 131)

```html
<!-- S4: AGENT NETWORK -->
<section class="story-section light" id="agents">
  <div class="story-inner">
    <div class="badge-pill light reveal">The Team</div>
    <h2 class="story-h2 reveal reveal-delay-1">10 agents.<br>One coordinated team.</h2>
    <p class="story-lead reveal reveal-delay-2">
      Each agent has a defined scope and data contract. No agent overwrites another&rsquo;s work.
      The Orchestrator is the only one with write access to the master database &mdash;
      every other agent writes to a proposals buffer first.
    </p>

    <div class="agent-network-wrap" id="agent-network">
      <div class="agent-svg-wrap reveal reveal-delay-2">
        <svg viewBox="0 0 600 560" xmlns="http://www.w3.org/2000/svg" aria-label="Agent network diagram">
          <defs>
            <!-- Gradient for orchestrator -->
            <radialGradient id="orchestrator-grad" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#3b82f6"/>
              <stop offset="100%" stop-color="#1d4ed8"/>
            </radialGradient>
            <!-- Gradient for data agent -->
            <radialGradient id="data-grad" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#8b5cf6"/>
              <stop offset="100%" stop-color="#6d28d9"/>
            </radialGradient>
          </defs>

          <!-- ── Outer ring connecting lines (from specialist agents to orchestrator) ── -->
          <!-- These lines animate with data-flowing-outward feel -->
          <!-- Keyword → Orchestrator -->
          <line class="agent-line" x1="300" y1="92" x2="300" y2="240" stroke="#2563eb" stroke-width="1.5"/>
          <!-- Technical → Orchestrator -->
          <line class="agent-line" x1="437" y1="152" x2="336" y2="252" stroke="#0891b2" stroke-width="1.5" style="animation-delay:.15s"/>
          <!-- GEO → Orchestrator -->
          <line class="agent-line" x1="497" y1="280" x2="356" y2="280" stroke="#8b5cf6" stroke-width="1.5" style="animation-delay:.3s"/>
          <!-- Competitors → Orchestrator -->
          <line class="agent-line" x1="437" y1="408" x2="336" y2="308" stroke="#f59e0b" stroke-width="1.5" style="animation-delay:.45s"/>
          <!-- Content → Orchestrator -->
          <line class="agent-line" x1="300" y1="468" x2="300" y2="320" stroke="#16a34a" stroke-width="1.5" style="animation-delay:.6s"/>
          <!-- Links → Orchestrator -->
          <line class="agent-line" x1="163" y1="408" x2="264" y2="308" stroke="#ec4899" stroke-width="1.5" style="animation-delay:.75s"/>
          <!-- AI Ready → Orchestrator -->
          <line class="agent-line" x1="103" y1="280" x2="244" y2="280" stroke="#0891b2" stroke-width="1.5" style="animation-delay:.9s"/>
          <!-- Learning → Orchestrator -->
          <line class="agent-line" x1="163" y1="152" x2="264" y2="252" stroke="#64748b" stroke-width="1.5" style="animation-delay:1.05s"/>

          <!-- Data Agent → Orchestrator (inner ring line) -->
          <line class="agent-line" x1="300" y1="158" x2="300" y2="240" stroke="#8b5cf6" stroke-width="2" style="animation-delay:.05s"/>

          <!-- ── Outer ring: Data agent feeds all specialists ── -->
          <!-- Data → Keyword -->
          <line x1="300" y1="140" x2="300" y2="92" stroke="#8b5cf6" stroke-width="1" stroke-dasharray="3 3" opacity=".25"/>
          <line x1="300" y1="140" x2="437" y2="130" stroke="#8b5cf6" stroke-width="1" stroke-dasharray="3 3" opacity=".15"/>
          <line x1="300" y1="140" x2="497" y2="260" stroke="#8b5cf6" stroke-width="1" stroke-dasharray="3 3" opacity=".15"/>
          <line x1="300" y1="140" x2="163" y2="130" stroke="#8b5cf6" stroke-width="1" stroke-dasharray="3 3" opacity=".15"/>

          <!-- ── ORCHESTRATOR (center) ── -->
          <g class="agent-node" id="node-orchestrator">
            <circle cx="300" cy="280" r="54" fill="url(#orchestrator-grad)" opacity=".15"/>
            <circle cx="300" cy="280" r="44" fill="url(#orchestrator-grad)"/>
            <text x="300" y="272" text-anchor="middle" font-size="22">👑</text>
            <text x="300" y="292" text-anchor="middle" fill="white" font-size="9" font-weight="700" letter-spacing=".05em">ORCHESTRATOR</text>
          </g>

          <!-- ── DATA AGENT (inner ring) ── -->
          <g class="agent-node" id="node-data">
            <circle cx="300" cy="140" r="28" fill="url(#data-grad)"/>
            <text x="300" y="134" text-anchor="middle" font-size="14">📡</text>
            <text x="300" y="150" text-anchor="middle" fill="white" font-size="8" font-weight="600">DATA</text>
          </g>

          <!-- ── SPECIALIST AGENTS (outer ring) ── -->
          <!-- Keyword (top) -->
          <g class="agent-node">
            <circle cx="300" cy="62" r="24" fill="#2563eb"/>
            <text x="300" y="56" text-anchor="middle" font-size="13">🔍</text>
            <text x="300" y="70" text-anchor="middle" fill="white" font-size="7" font-weight="600">KEYWORD</text>
          </g>
          <!-- Technical (top-right) -->
          <g class="agent-node">
            <circle cx="448" cy="122" r="24" fill="#0891b2"/>
            <text x="448" y="116" text-anchor="middle" font-size="13">⚡</text>
            <text x="448" y="130" text-anchor="middle" fill="white" font-size="7" font-weight="600">TECHNICAL</text>
          </g>
          <!-- GEO/AEO (right) -->
          <g class="agent-node">
            <circle cx="508" cy="280" r="24" fill="#8b5cf6"/>
            <text x="508" y="274" text-anchor="middle" font-size="13">🤖</text>
            <text x="508" y="288" text-anchor="middle" fill="white" font-size="7" font-weight="600">GEO/AEO</text>
          </g>
          <!-- Competitors (bottom-right) -->
          <g class="agent-node">
            <circle cx="448" cy="438" r="24" fill="#f59e0b"/>
            <text x="448" y="432" text-anchor="middle" font-size="13">🎯</text>
            <text x="448" y="446" text-anchor="middle" fill="white" font-size="7" font-weight="600">COMPETITORS</text>
          </g>
          <!-- Content (bottom) -->
          <g class="agent-node">
            <circle cx="300" cy="498" r="24" fill="#16a34a"/>
            <text x="300" y="492" text-anchor="middle" font-size="13">✍️</text>
            <text x="300" y="506" text-anchor="middle" fill="white" font-size="7" font-weight="600">CONTENT</text>
          </g>
          <!-- Links (bottom-left) -->
          <g class="agent-node">
            <circle cx="152" cy="438" r="24" fill="#ec4899"/>
            <text x="152" y="432" text-anchor="middle" font-size="13">🔗</text>
            <text x="152" y="446" text-anchor="middle" fill="white" font-size="7" font-weight="600">LINKS</text>
          </g>
          <!-- AI Readiness (left) -->
          <g class="agent-node">
            <circle cx="92" cy="280" r="24" fill="#0891b2"/>
            <text x="92" y="274" text-anchor="middle" font-size="13">🤖</text>
            <text x="92" y="288" text-anchor="middle" fill="white" font-size="7" font-weight="600">AI-READY</text>
          </g>
          <!-- Learning (top-left) -->
          <g class="agent-node">
            <circle cx="152" cy="122" r="24" fill="#64748b"/>
            <text x="152" y="116" text-anchor="middle" font-size="13">📚</text>
            <text x="152" y="130" text-anchor="middle" fill="white" font-size="7" font-weight="600">LEARNING</text>
          </g>
        </svg>
      </div>

      <!-- Agent list grid -->
      <div class="agent-list-grid reveal reveal-delay-3">
        <div class="agent-list-item">
          <div class="agent-list-icon" style="background:#ede9fe">📡</div>
          <div><div class="agent-list-name">Data Agent</div><div class="agent-list-role">Fetches GSC, GA4, PageSpeed, Ahrefs — caches for all agents</div></div>
        </div>
        <div class="agent-list-item">
          <div class="agent-list-icon" style="background:#dbeafe">🔍</div>
          <div><div class="agent-list-name">Keyword Agent</div><div class="agent-list-role">ROI-scores opportunities, maintains glossary backlog</div></div>
        </div>
        <div class="agent-list-item">
          <div class="agent-list-icon" style="background:#cffafe">⚡</div>
          <div><div class="agent-list-name">Technical Agent</div><div class="agent-list-role">Audits Core Web Vitals, schema, crawl errors, 404s</div></div>
        </div>
        <div class="agent-list-item">
          <div class="agent-list-icon" style="background:#f3e8ff">🤖</div>
          <div><div class="agent-list-name">GEO / AEO Agent</div><div class="agent-list-role">Optimizes for Google AI Overviews, ChatGPT, Perplexity</div></div>
        </div>
        <div class="agent-list-item">
          <div class="agent-list-icon" style="background:#fef9c3">🎯</div>
          <div><div class="agent-list-name">Competitor Agent</div><div class="agent-list-role">Monitors SERP movements, content gaps, backlink changes</div></div>
        </div>
        <div class="agent-list-item">
          <div class="agent-list-icon" style="background:#dcfce7">✍️</div>
          <div><div class="agent-list-name">Content Agent</div><div class="agent-list-role">Generates drafts, meta descriptions, optimization briefs</div></div>
        </div>
        <div class="agent-list-item">
          <div class="agent-list-icon" style="background:#fce7f3">🔗</div>
          <div><div class="agent-list-name">Link Building Agent</div><div class="agent-list-role">Finds opportunities, drafts outreach, writes guest posts</div></div>
        </div>
        <div class="agent-list-item">
          <div class="agent-list-icon" style="background:#f1f5f9">👑</div>
          <div><div class="agent-list-name">Orchestrator (COO)</div><div class="agent-list-role">Merges proposals, resolves conflicts, drives action queue</div></div>
        </div>
      </div>
    </div>
  </div>
</section>
```

**Step 3: Add SVG scroll trigger JS** in the `<script>` block at the bottom of the file:

```js
// ── Agent network: trigger animation on scroll ──
const agentNetwork = document.getElementById('agent-network');
const agentObserver = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    agentNetwork.classList.add('animate');
  }
}, { threshold: 0.3 });
agentObserver.observe(agentNetwork);
```

**Step 4: Verify**

Scroll to the Agents section. The SVG diagram should:
- Show a hub-and-spoke layout with Orchestrator at center
- Have animated dashed lines "flowing" from outer agents to the center
- Agent nodes appear one by one as you scroll in (staggered opacity transition)
- Below the SVG: 8 agent cards in a 2-column grid

**Step 5: Commit**
```bash
git add index.html
git commit -m "feat: add Agent Network section — animated SVG hub-and-spoke diagram"
```

---

### Task 6: Section 5 — Results (Tabbed Dashboard)

Preserve ALL existing dashboard HTML. The content from the current dashboard becomes tabs in this section.

**File:** `index.html`

**Important:** Have `index.html.bak` open to copy from. The sections you need are at these lines in the backup:
- Performance Trends: lines 525–594
- Ahrefs Intelligence: lines 595–714
- Agent Roster: lines 715–802
- Keyword Rankings: lines 803–862
- Task Pipeline: lines 863–924
- Competitors: lines 925–1016
- What's Working / Issues: lines 1017–1054
- System Health: lines 1055–1112

**Step 1: Add Results CSS** inside `<style>`:

```css
/* ══════════════════════════════════════
   S5: RESULTS
══════════════════════════════════════ */
.results-intro {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}
.sample-data-badge {
  background: #fffbeb;
  border: 1px solid #fde68a;
  color: #78350f;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 12px;
}
.results-tabs {
  position: sticky;
  top: 0;
  background: white;
  z-index: 50;
  border-bottom: 2px solid var(--slate-200);
  margin-bottom: 32px;
  display: flex;
  gap: 0;
  overflow-x: auto;
  scrollbar-width: none;
}
.results-tabs::-webkit-scrollbar { display: none; }
.rtab-btn {
  padding: 12px 20px;
  font-size: 13px;
  font-weight: 500;
  color: var(--slate-500);
  cursor: pointer;
  border: none;
  background: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  white-space: nowrap;
  font-family: var(--font);
  transition: all .15s;
}
.rtab-btn:hover { color: var(--slate-700); }
.rtab-btn.active { color: var(--blue); border-bottom-color: var(--blue); font-weight: 600; }
.rtab-panel { display: none; }
.rtab-panel.active { display: block; }

/* Preserve all existing dashboard styles */
.container { max-width: 1120px; margin: 0 auto; padding: 0 24px; }
.section { margin-top: 48px; }
.section-title { font-size: 22px; font-weight: 700; color: var(--slate-900); margin-bottom: 6px; }
.section-subtitle { font-size: 14px; color: var(--slate-500); margin-bottom: 20px; }
.card { background: white; border: 1px solid var(--slate-200); border-radius: var(--radius); padding: 20px; box-shadow: var(--shadow); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.card-title { font-size: 15px; font-weight: 600; }
```

> **Important**: Also copy ALL the existing CSS from `index.html.bak` (lines 10–413) — the chart bars, agent grid, keyword table, badges, pipeline styles, competitor grid, health cards, etc. Paste it all into the `<style>` block. Do NOT delete any of it.

**Step 2: Replace the Results section HTML:**

```html
<!-- S5: RESULTS -->
<section class="story-section white" id="results">
  <div class="story-inner">
    <div class="badge-pill light reveal">Live Output</div>
    <div class="results-intro reveal reveal-delay-1">
      <div>
        <h2 class="story-h2">7 pipeline runs later.</h2>
        <p style="color:var(--slate-500);font-size:15px;margin-top:8px">This is the actual output — tracked, prioritized, and acted on.</p>
      </div>
      <div class="sample-data-badge">
        ℹ️ Illustrative data — based on real methodology applied to Windward.ai
      </div>
    </div>

    <div class="results-tabs" id="results-tabs">
      <button class="rtab-btn active" data-tab="perf">Performance</button>
      <button class="rtab-btn" data-tab="agents">Agent Roster</button>
      <button class="rtab-btn" data-tab="keywords">Keywords</button>
      <button class="rtab-btn" data-tab="pipeline">Task Pipeline</button>
      <button class="rtab-btn" data-tab="competitors">Competitors</button>
      <button class="rtab-btn" data-tab="health">System Health</button>
    </div>

    <div class="rtab-panel active" id="rtab-perf">
      <!-- PASTE Performance Trends + Ahrefs Intelligence sections from index.html.bak lines 525–714 here -->
      <!-- Remove the outer <section class="section" id="performance"> and <section class="section" id="ahrefs"> wrappers, keep inner content -->
    </div>
    <div class="rtab-panel" id="rtab-agents">
      <!-- PASTE Agent Roster section from lines 715–802 (keep inner content, remove outer section wrapper) -->
    </div>
    <div class="rtab-panel" id="rtab-keywords">
      <!-- PASTE Keyword Rankings from lines 803–862 -->
    </div>
    <div class="rtab-panel" id="rtab-pipeline">
      <!-- PASTE Task Pipeline from lines 863–924 -->
    </div>
    <div class="rtab-panel" id="rtab-competitors">
      <!-- PASTE Competitors + What's Working/Issues from lines 925–1054 -->
    </div>
    <div class="rtab-panel" id="rtab-health">
      <!-- PASTE System Health from lines 1055–1112 -->
    </div>
  </div>
</section>
```

**Step 3: Add tab switching JS** in the `<script>` block:

```js
// ── Results tab switching ──
document.querySelectorAll('.rtab-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.rtab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.rtab-panel').forEach(p => p.classList.remove('active'));
    this.classList.add('active');
    document.getElementById('rtab-' + this.dataset.tab).classList.add('active');
  });
});
```

**Step 4: Verify**

Scroll to Results. Should see:
- Headline "7 pipeline runs later." + sample data badge
- 6 sticky tabs (Performance, Agent Roster, Keywords, Task Pipeline, Competitors, System Health)
- Default tab shows Performance content
- Clicking tabs switches content correctly

**Step 5: Commit**
```bash
git add index.html
git commit -m "feat: add Results section — tabbed dashboard with preserved data"
```

---

### Task 7: Section 6 — CTA Footer

**File:** `index.html`

**Step 1: Add CTA CSS** inside `<style>`:

```css
/* ══════════════════════════════════════
   S6: CTA
══════════════════════════════════════ */
#cta {
  background: linear-gradient(160deg, #0a0f1e 0%, #0f2040 100%);
  text-align: center;
  min-height: auto;
  padding: 80px 24px;
}
.cta-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 32px;
}
.cta-btn {
  display: inline-block;
  padding: 14px 28px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity .15s, transform .15s;
  border: none;
  font-family: var(--font);
  text-decoration: none;
}
.cta-btn:hover { opacity: .88; transform: translateY(-1px); }
.cta-btn-primary { background: white; color: #0f172a; }
.cta-btn-secondary {
  background: rgba(255,255,255,.1);
  color: white;
  border: 1px solid rgba(255,255,255,.2);
}
.cta-footer-attr {
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid rgba(255,255,255,.08);
  font-size: 12px;
  color: rgba(255,255,255,.3);
}
```

**Step 2: Replace the CTA section HTML:**

```html
<!-- S6: CTA -->
<section class="story-section dark" id="cta">
  <div class="story-inner" style="text-align:center">
    <div class="badge-pill reveal">Open Source</div>
    <h2 class="story-h2 reveal reveal-delay-1">Deploy this for your own site.</h2>
    <p class="story-lead reveal reveal-delay-2" style="margin:0 auto 0">
      The full system &mdash; agents, scripts, dashboard &mdash; is open-source and MIT licensed.
      Replace the Windward context with your domain. Run your first pipeline in an afternoon.
    </p>
    <div class="cta-buttons reveal reveal-delay-3">
      <a href="https://github.com/Talko90/windward-seo-agent-system" target="_blank" class="cta-btn cta-btn-primary">★ Star on GitHub</a>
      <a href="https://growthbyagent.com" target="_blank" class="cta-btn cta-btn-secondary">growthbyagent.com</a>
    </div>
    <div class="cta-footer-attr reveal reveal-delay-4">
      Built by <a href="https://growthbyagent.com" target="_blank" style="color:rgba(255,255,255,.5)">Tal Cohen</a>
      using <a href="https://claude.ai/code" target="_blank" style="color:rgba(255,255,255,.5)">Claude Code</a>
      by Anthropic &bull; MIT License
    </div>
  </div>
</section>
```

**Step 3: Commit**
```bash
git add index.html
git commit -m "feat: add CTA footer section"
```

---

### Task 8: JavaScript — Counters, Scroll Reveal, Nav Active State

**File:** `index.html` — complete the `<script>` block

Replace the placeholder script with the full JS:

```html
<script>
// ── Scroll reveal ──
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Animated counters ──
function animateCounter(el, target, duration) {
  const startTime = performance.now();
  function update(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(target * eased).toLocaleString();
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      if (!el.dataset.animated) {
        el.dataset.animated = 'true';
        animateCounter(el, parseInt(el.dataset.target), 1200);
      }
    }
  });
}, { threshold: 0.5 });
document.querySelectorAll('[data-target]').forEach(el => counterObserver.observe(el));

// ── Floating nav: show after hero ──
const heroSection = document.getElementById('hero');
const storyNav = document.getElementById('story-nav');
const navObserver = new IntersectionObserver((entries) => {
  storyNav.classList.toggle('visible', !entries[0].isIntersecting);
}, { threshold: 0.1 });
navObserver.observe(heroSection);

// ── Floating nav: active section highlight ──
const navSections = ['why', 'how', 'agents', 'results'];
const navLinks = document.querySelectorAll('.story-nav a[href^="#"]');
const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navLinks.forEach(l => l.classList.remove('active'));
      const link = document.querySelector(`.story-nav a[href="#${entry.target.id}"]`);
      if (link) link.classList.add('active');
    }
  });
}, { threshold: 0.4 });
navSections.forEach(id => {
  const el = document.getElementById(id);
  if (el) sectionObserver.observe(el);
});

// ── Agent network: trigger on scroll ──
const agentNetwork = document.getElementById('agent-network');
if (agentNetwork) {
  const agentObserver = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) agentNetwork.classList.add('animate');
  }, { threshold: 0.3 });
  agentObserver.observe(agentNetwork);
}

// ── Results tab switching ──
document.querySelectorAll('.rtab-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.rtab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.rtab-panel').forEach(p => p.classList.remove('active'));
    this.classList.add('active');
    document.getElementById('rtab-' + this.dataset.tab).classList.add('active');
  });
});

// ── Existing dashboard JS: tabs, expand, keyword filter ──
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    const parent = this.closest('.card');
    parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    parent.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    this.classList.add('active');
    document.getElementById('tab-' + this.dataset.tab).classList.add('active');
  });
});
function toggleExpand(btn) {
  btn.classList.toggle('open');
  btn.nextElementSibling.classList.toggle('open');
}
document.querySelectorAll('.kw-filter-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.kw-filter-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const cluster = this.dataset.cluster;
    document.querySelectorAll('.kw-table tbody tr').forEach(row => {
      row.style.display = (cluster === 'all' || row.dataset.cluster === cluster) ? '' : 'none';
    });
  });
});
</script>
```

**Step 2: Verify all JS works**
- Hero counter (163) animates on load
- Floating nav appears after scrolling past hero
- Nav links highlight the current section
- Agent nodes appear one-by-one on scroll into agents section
- Results tabs switch correctly
- Existing keyword filter + expand still work inside Results tabs

**Step 3: Commit**
```bash
git add index.html
git commit -m "feat: complete JS — counters, scroll reveal, nav, agent animation, tabs"
```

---

### Task 9: Sync to growthbyagent + Push Both Repos

**Step 1: Copy updated index.html to Personal Website**
```bash
cp /Users/talcohen/Downloads/SEO-Public/index.html \
   "/Users/talcohen/Personal Website/public/project/Agentic-SEO/index.html"
```

**Step 2: Push SEO-Public**
```bash
cd /Users/talcohen/Downloads/SEO-Public
git push
```

**Step 3: Push growthbyagent**
```bash
cd "/Users/talcohen/Personal Website"
git add public/project/Agentic-SEO/index.html
git commit -m "feat: update Agentic-SEO dashboard — scroll story redesign"
git push
```

**Step 4: Verify live**
- Wait ~2 min for Vercel to deploy
- Open https://growthbyagent.com/project/Agentic-SEO/
- Walk through all 6 sections
- Confirm floating nav, agent diagram, tab switching all work in production

---

## Final Checklist

- [ ] Hero: full viewport, dark gradient, 3 stats, scroll cue, counter animates
- [ ] Why: two-column before/after, strikethrough on left, green checks on right
- [ ] How: 5-step pipeline with connecting lines, 3 meta cards, reveals on scroll
- [ ] Agents: SVG hub-and-spoke, animated pulse lines, agents appear on scroll, 8-item grid below
- [ ] Results: 6 tabs (Performance, Agents, Keywords, Pipeline, Competitors, Health), tabs sticky at top of section
- [ ] CTA: dark, GitHub + growthbyagent.com buttons, attribution footer
- [ ] Floating nav: hidden until past hero, active state tracks current section
- [ ] Mobile responsive: check at 375px width — stacked columns, pipeline wraps vertically
- [ ] No Google Fonts dependency (system fonts only)
- [ ] Both repos pushed, Vercel deployed
