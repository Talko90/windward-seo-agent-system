# Portfolio Polish Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the dashboard into a process-first portfolio showcase that impresses marketing leaders — without changing data, agent cards, or section content.

**Architecture:** Five targeted edits to `index.html` + one README cleanup. No new files, no structural rewrites. Each task is a self-contained string replacement.

**Tech Stack:** Vanilla HTML/CSS/JS (no build step). Edit in-place. Test by opening `index.html` in a browser.

---

## Before You Start

You'll need your GitHub username for Task 5. Search `README.md` for `USERNAME` — it appears 3 times and needs to be replaced with your actual handle (e.g. `talcohen`).

---

### Task 1: Hero — Rework Badge, Headline, Description, and Stats

**File:** `index.html` lines 392–440

**What to change:**

Replace the entire hero inner content between `<div class="container hero-inner">` and its closing `</div></section>`.

**Step 1: Replace the hero-badge text**

Old:
```html
<div class="hero-badge">WINDWARD.AI &mdash; SEO OPERATIONS</div>
```

New:
```html
<div class="hero-badge">CASE STUDY &mdash; WINDWARD.AI</div>
```

**Step 2: Replace the h1**

Old:
```html
<h1>Autonomous SEO Agent System</h1>
```

New:
```html
<h1>Autonomous SEO at Scale</h1>
```

**Step 3: Replace the hero description**

Old:
```html
<p class="hero-desc">10 AI agents work around the clock to find keyword opportunities, analyze competitors, audit technical health, and create content &mdash; all orchestrated automatically.</p>
```

New:
```html
<p class="hero-desc">A live implementation: 10 AI agents replacing the traditional SEO team at Windward.ai, a maritime intelligence company. Built by Tal Cohen &mdash; from data collection to prioritized action queue, fully automated.</p>
```

**Step 4: Replace both stat rows with a single row of 3 process-story stats**

Old (lines 398–431 — both `.hero-stats` and `.hero-stats-row2` divs):
```html
    <div class="hero-stats">
      <div class="hero-stat">
        <div class="hero-stat-value" data-target="4348">0</div>
        <div class="hero-stat-label">Weekly Sessions</div>
        <span class="hero-stat-change change-up">&uarr; GA4 Mar 11</span>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-value" data-target="15">0</div>
        <div class="hero-stat-label">Conversions (7d)</div>
        <span class="hero-stat-change change-up">Mar 5–11</span>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-value" data-target="4881">0</div>
        <div class="hero-stat-label">Search Clicks (7d)</div>
        <span class="hero-stat-change change-up">1.05M impressions</span>
      </div>
    </div>
    <div class="hero-stats-row2">
      <div class="hero-stat">
        <div class="hero-stat-value" data-target="64">0</div>
        <div class="hero-stat-label">Domain Rating</div>
        <span class="hero-stat-change change-up">27,810 org traffic/mo</span>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-value" data-target="1993">0</div>
        <div class="hero-stat-label">Referring Domains</div>
        <span class="hero-stat-change change-up">15,990 backlinks</span>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-value" data-target="163">0</div>
        <div class="hero-stat-label">Active Tasks</div>
        <span class="hero-stat-change change-up">115 approved</span>
      </div>
    </div>
```

New (single row, 3 stats that tell the process story):
```html
    <div class="hero-stats">
      <div class="hero-stat">
        <div class="hero-stat-value">10</div>
        <div class="hero-stat-label">AI Agents</div>
        <span class="hero-stat-change change-up">coordinated team</span>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-value" data-target="163">0</div>
        <div class="hero-stat-label">Active Tasks Generated</div>
        <span class="hero-stat-change change-up">115 approved</span>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-value" data-target="27810">0</div>
        <div class="hero-stat-label">Organic Traffic / mo</div>
        <span class="hero-stat-change change-up">Ahrefs &bull; illustrative</span>
      </div>
    </div>
```

**Step 5: Remove the Ahrefs data strip and simplify hero-meta**

Old (lines 432–438):
```html
    <div style="margin-top:16px;padding:12px 16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:var(--radius);display:flex;gap:24px;flex-wrap:wrap;font-size:13px;color:rgba(255,255,255,.8)">
      <span><strong style="color:rgba(255,255,255,.95)">Ahrefs Organic Traffic:</strong> 27,810/mo</span>
      <span><strong style="color:rgba(255,255,255,.95)">Keywords:</strong> 3,464</span>
      <span><strong style="color:rgba(255,255,255,.95)">DR:</strong> 64 (stable)</span>
      <span><strong style="color:rgba(255,255,255,.95)">Backlinks:</strong> 15,990</span>
    </div>
    <div class="hero-meta">Last updated: March 12, 2026 &bull; Data: GSC (Mar 2–9) + GA4 (Mar 11) + Ahrefs (147,100 units remaining) &bull; Pipeline Run v5.1: 7 new tasks, 163 total &bull; Tech health: 68/100 &bull; AI readiness: 59/100</div>
```

New:
```html
    <div class="hero-meta">Built with Claude Code &bull; Runs twice weekly via cron &bull; Illustrative data &bull; Framework available on GitHub</div>
```

**Step 6: Open `index.html` in a browser and verify** the hero looks clean — badge says "CASE STUDY", headline is "Autonomous SEO at Scale", 3 stats display, no duplicate data strip.

**Step 7: Commit**
```bash
git add index.html
git commit -m "feat: rework hero for process-first portfolio narrative"
```

---

### Task 2: Add Case Study Disclaimer Banner

**File:** `index.html` — insert between line 440 (`</section>` closing hero) and line 442 (`<nav class="sticky-nav">`)

**What to change:**

**Step 1: Add CSS for the banner** — insert inside `<style>` before the closing `</style>` tag (before line 388):

```css
/* ─── Case Study Banner ─── */
.case-study-banner {
  background: #fffbeb;
  border-bottom: 1px solid #fde68a;
  padding: 10px 0;
  font-size: 13px;
  color: #78350f;
  text-align: center;
}
.case-study-banner a { color: #92400e; font-weight: 600; }
.case-study-banner a:hover { text-decoration: underline; }
```

**Step 2: Add the banner HTML** between `</section>` (hero close) and `<nav class="sticky-nav">`:

```html
<!-- ═══════════════ CASE STUDY BANNER ═══════════════ -->
<div class="case-study-banner">
  <div class="container">
    &#8505;&#65039; Case Study &bull; Data is illustrative, based on real methodology applied to Windward.ai (maritime intelligence) &bull; Built by <a href="https://growthbyagent.com" target="_blank">Tal Cohen</a> &bull; <a href="https://growthbyagent.com" target="_blank">growthbyagent.com</a>
  </div>
</div>
```

**Step 3: Verify** — the banner should appear as a warm amber/yellow strip between hero and the nav tabs.

**Step 4: Commit**
```bash
git add index.html
git commit -m "feat: add case study disclaimer banner below hero"
```

---

### Task 3: Move "How It Works" to First Nav Position and First Section

This is the most structural change. It's two sub-steps: reorder the nav link, then move the section's DOM position.

**File:** `index.html`

**Step 1: Reorder nav links** — in the `<nav class="sticky-nav">` block (lines 442–457):

Old:
```html
      <a href="#performance" class="nav-link active">Performance</a>
      <a href="#ahrefs" class="nav-link">Ahrefs</a>
      <a href="#agents" class="nav-link">Agent Roster</a>
      <a href="#keywords" class="nav-link">Keywords</a>
      <a href="#pipeline" class="nav-link">Task Pipeline</a>
      <a href="#competitors" class="nav-link">Competitors</a>
      <a href="#status" class="nav-link">Status</a>
      <a href="#health" class="nav-link">System Health</a>
      <a href="#how" class="nav-link">How It Works</a>
```

New (move "How It Works" first, change `active` to it):
```html
      <a href="#how" class="nav-link active">How It Works</a>
      <a href="#performance" class="nav-link">Performance</a>
      <a href="#ahrefs" class="nav-link">Ahrefs</a>
      <a href="#agents" class="nav-link">Agent Roster</a>
      <a href="#keywords" class="nav-link">Keywords</a>
      <a href="#pipeline" class="nav-link">Task Pipeline</a>
      <a href="#competitors" class="nav-link">Competitors</a>
      <a href="#status" class="nav-link">Status</a>
      <a href="#health" class="nav-link">System Health</a>
```

**Step 2: Move the "How It Works" section block in the DOM**

The "How It Works" block is currently lines 1047–1102:
```
<!-- ═══════════════ HOW IT WORKS ═══════════════ -->
<section class="section" id="how">
  ...
</section>
```

It needs to be the **first section** inside `<div class="container">` (line 459), before `<!-- ═══════════════ PERFORMANCE TRENDS ═══════════════ -->`.

The move:
- **Cut** the entire `<!-- ═══════════════ HOW IT WORKS ═══════════════ -->` block (from `<!-- ═══` comment through `</section>`)
- **Paste** it immediately after `<div class="container">` on line 459

After the move, the order inside `<div class="container">` should be:
1. How It Works (`id="how"`)
2. Performance Trends (`id="performance"`)
3. Ahrefs Intelligence (`id="ahrefs"`)
4. Agent Roster (`id="agents"`)
5. ... rest unchanged

**Step 3: Verify** — open in browser, scroll from top. First section after the nav should be "How It Works" with the 5-step pipeline diagram. "Performance Trends" should come second.

**Step 4: Commit**
```bash
git add index.html
git commit -m "feat: promote How It Works to first section for process-first narrative"
```

---

### Task 4: Replace Footer with GitHub/Deploy CTA

**File:** `index.html` lines 1106–1111

**What to change:**

**Step 1: Add footer CSS** — insert inside `<style>` before `</style>`:

```css
/* ─── CTA Footer ─── */
.cta-footer {
  margin-top: 64px;
  background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
  color: white;
  padding: 48px 0;
  text-align: center;
}
.cta-footer h2 {
  font-size: 26px; font-weight: 800; letter-spacing: -.5px; margin-bottom: 10px;
}
.cta-footer p {
  font-size: 15px; color: rgba(255,255,255,.65); margin-bottom: 28px; max-width: 480px; margin-left: auto; margin-right: auto;
}
.cta-buttons { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
.cta-btn {
  display: inline-block; padding: 12px 24px; border-radius: 8px;
  font-size: 14px; font-weight: 600; text-decoration: none; transition: opacity .15s;
}
.cta-btn:hover { opacity: .88; }
.cta-btn-primary { background: white; color: #0f172a; }
.cta-btn-secondary { background: rgba(255,255,255,.12); color: white; border: 1px solid rgba(255,255,255,.2); }
.cta-footer-meta {
  margin-top: 28px; font-size: 12px; color: rgba(255,255,255,.35);
}
.footer-simple {
  padding: 16px 0; text-align: center; font-size: 12px; color: var(--slate-400);
  border-top: 1px solid var(--slate-200);
}
```

**Step 2: Replace the old footer** with the new CTA section + minimal attribution footer:

Old:
```html
<!-- ═══════════════ FOOTER ═══════════════ -->
<div class="footer">
  <div class="container">
    Windward.ai SEO Agent System &bull; Built with Claude Code &bull; Dashboard generated March 12, 2026
  </div>
</div>
```

New:
```html
<!-- ═══════════════ CTA FOOTER ═══════════════ -->
<div class="cta-footer">
  <div class="container">
    <h2>Deploy This for Your Own Site</h2>
    <p>The full system — agents, scripts, and dashboard — is open-source. Clone it, replace the Windward context with your domain, and run your first pipeline in an afternoon.</p>
    <div class="cta-buttons">
      <a href="https://github.com/YOUR_GITHUB_USERNAME/windward-seo-agent-system" target="_blank" class="cta-btn cta-btn-primary">&#9733; Star on GitHub</a>
      <a href="https://growthbyagent.com" target="_blank" class="cta-btn cta-btn-secondary">growthbyagent.com</a>
    </div>
    <div class="cta-footer-meta">Built with Claude Code by Anthropic &bull; MIT License &bull; Open source</div>
  </div>
</div>
<div class="footer-simple">
  <div class="container">Windward.ai SEO Agent System &bull; Case Study Dashboard &bull; Illustrative data</div>
</div>
```

> **Note:** Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username before committing.

**Step 3: Remove old `.footer` CSS** if it exists (search for `.footer {` in the `<style>` block and delete it to avoid conflicts).

**Step 4: Verify** — scroll to the bottom of the page. Should see a dark CTA section with two buttons and a simple attribution line below it.

**Step 5: Commit**
```bash
git add index.html
git commit -m "feat: add GitHub/deploy CTA footer"
```

---

### Task 5: README — Fix USERNAME Placeholders

**File:** `README.md`

**Step 1: Find all USERNAME instances**
```bash
grep -n "USERNAME" README.md
```
Expected: 3 matches (lines ~8, ~112, ~234)

**Step 2: Replace each instance with your GitHub username**

Line ~8:
```
**Live Dashboard**: [View the SEO Agent Dashboard](https://USERNAME.github.io/windward-seo-agent-system/)
```
→ Replace `USERNAME` with your actual GitHub handle.

Line ~112:
```
git clone https://github.com/USERNAME/windward-seo-agent-system.git
```
→ Replace `USERNAME`.

Line ~234:
```
Built by [Tal Cohen](https://github.com/USERNAME) using [Claude Code](https://claude.ai/code) by Anthropic.
```
→ Replace `USERNAME`.

**Step 3: Update the Live Dashboard URL** on line 8 if you're using Vercel instead of GitHub Pages — replace the URL with your actual hosted URL.

**Step 4: Commit**
```bash
git add README.md
git commit -m "docs: fix USERNAME placeholders and live dashboard URL"
```

---

## Final Verification Checklist

Open `index.html` in a browser and walk through:

- [ ] Hero badge says "CASE STUDY — WINDWARD.AI"
- [ ] Headline is "Autonomous SEO at Scale"
- [ ] 3 hero stats: 10 AI Agents, 163 Active Tasks, 27,810 Organic Traffic
- [ ] Amber disclaimer banner visible between hero and nav
- [ ] First nav item is "How It Works" (active/highlighted)
- [ ] First section after scrolling past nav is the 5-step pipeline diagram
- [ ] Dark CTA footer at bottom with GitHub and growthbyagent.com links
- [ ] README has no "USERNAME" strings

```bash
grep -n "USERNAME" README.md index.html
# Expected: no output
```
