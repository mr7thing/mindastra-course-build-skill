---
name: interactive-courseware
description: |
  Produces zero-dependency interactive courseware (课堂演示课件 / 交互课件 / 演示幻灯)
  for MindNexus courses: an HTML slide deck (index.html + styles.css + app.js) packed
  into a zip and uploaded per-course, published by the facilitator, and rendered on
  the course detail page inside a sandboxed iframe. Use when asked to make course
  slides, interactive courseware, 演示课件, 互动课件, or to package teaching demos
  for an existing course. NOT for course package (course.json) creation — that is
  the goal-oriented-pbl-course skill.
---

# Interactive Courseware Builder（交互式课件制作）

## Mission

Build a self-contained, zero-dependency interactive slide deck that runs in THREE
host environments, the worst of which is authoritative: the platform renders it via
`<iframe srcdoc sandbox>` with an **opaque origin** (no allow-same-origin). Design
for that world; file:// and normal https are then free.

## Golden References（风格与引擎骨架）

`content/course-packages/ai-detective-research/courseware/` (小侦探, 33 页) and
`content/course-packages/ai-creation-studio/courseware/` (小创作家, 34 页) — commits
`709390b7` / `11aea21d`. （以上为 MindNexus 平台主仓库内路径，本仓库不含样例正文。）
They define the visual bar (editorial typography, CSS-variable
palette, inline SVG, emoji props) and the engine skeleton. **Sandbox rules below
override anything in older samples** — never copy verbatim without re-checking §Rules 1-6.

## Rules（硬约束）

1. **零依赖零网络**：no CDN scripts, no external fonts/images/APIs, no build step.
   Everything inline: SVG, emoji, CSS gradients/animation. Must open correctly from
   `file://` AND inside the sandbox iframe offline.
2. **存储全禁**：`localStorage` / `sessionStorage` / `indexedDB` / `document.cookie`
   throw `SecurityError` in the opaque-origin iframe. All state lives in JS variables;
   persistence is explicitly out of scope for courseware.
3. **历史写入必包 try/catch**：`history.pushState/replaceState` throw on
   `about:srcdoc`. Deep links go through `location.hash = "#sNN"` assignment (legal in
   srcdoc, fires `hashchange`) plus a listener; history writes only ever appear wrapped
   in `try { … } catch { /* 宿主不允许写历史 */ }`, and never before the visual state
   update (an exception must never block rendering).
4. **单文件纪律**：exactly three files — `index.html`, `styles.css`, `app.js` — with
   relative refs (`<link href="styles.css">`, `<script src="app.js">` deferred). The
   platform packing inlines them into one HTML and injects a compat shim — i.e. eli5's
   "single self-contained HTML" delivery principle is fulfilled by the pipeline, not by
   hand-inlining. `app.js` is
   ONE IIFE, `"use strict"`, no `<script type="module">`, no `import`/`export`.
5. **zip 硬限**（上传 422 拒绝）：≤20 files, ≤8MB total decompressed, must contain
   `index.html` at root (or single top-level folder), UTF-8, no absolute paths / `..`,
   strip `__MACOSX/` and `.DS_Store`.
6. **不越框**：no `window.top` / `window.parent` / `window.open` / embedder DOM access;
   no `eval` / `new Function`; no autoplaying audio without a user click.

## Engine Skeleton（每次都从这套骨架出发）

- `.slide` sections with stable ids (`s00` cover, `sNN` pages, `s90` end); active one
  toggled via classes; `goTo(i)` clamps, updates progress + pageNo + tabs.
- Deep link: on load read `location.hash` → `goTo(idIndex.get(hash))`; `hashchange`
  listener follows external jumps. hash write inside `goTo` wrapped in try/catch.
- Per-page enter animations: `onEnter` map `slideId → fn`; timers collected in one
  array and cleared on every page switch (replay on re-enter; never leaks).
- Global click delegation: `[data-goto]` / `[data-jump]` navigation,
  `[data-toggle]` reveal, quiz rows, chip selects — one listener, no per-element wiring
  where delegation suffices.
- Keyboard (←/→/Space/Home/End/M overview) + pointer swipe (≥64px) + bottom nav
  (prev/next/menu) — three input paths, one handler each.
- Overview menu built from the DOM (never hardcode page lists twice).

## Content Bar（作者级，不是模板级）

- **受众校准（eli5 技能「Age 15」档——`~/code/skills/eli5/skills/eli5/SKILL.md`，小侦探/小创作家样板的原生维度）**：
  - 类比来源：社交媒体、手机、游戏——学习者已经熟的东西（样板的「文字接龙老虎机」「侦探手电筒」就是这个路数）；
  - 结构律：每页 = 一句话 what → 一个类比 → 细节分层 → 一句 so what（为什么与你有关）；
  - 讲原理前先讲存在理由（purpose before mechanism——没人在乎语法，直到知道它为何存在）；
  - 语言：术语第一次出现立即一句话定义；一句一个想法；对学习者用「你」；非技术受众允许无情简化——80% 准确但能听懂，好过 100% 准确但全程掉队；
  - 语气：轻快但绝不尬——不说教、不俯就、没有「迎合青少年」的油腻劲儿（fellow kids 能量为零）；练习游戏化且即时反馈（答对立刻庆祝、答错给解释不是给分数）。
  - 写完自检：这一页初中生会不会觉得在被上课？会不会觉得在被讨好？
- Every interactive page TEACHES: demo machines (slot/probability bars, chat replays,
  meter builders), judgment quizzes with explanations on answer, construct-by-chips
  exercises with live feedback — never a page that only holds text.
- Chinese UI throughout; every page has a takeaway; end page routes learners to the
  course's real project/milestones.
- Author-grade content only: concrete examples, real dialogues, checkable criteria —
  the same standard as `goal-oriented-pbl-course` rule 16.
- 视觉系统：每课一个主题色（CSS 变量），全部插图/动画为内联 SVG + CSS/原生 JS；
  尊重 `prefers-reduced-motion`（媒体查询下关掉非必要动画）。

## Pipeline（平台通道）

1. Author the three files locally; open `index.html` from `file://` and verify every
   page + interaction works offline.
2. Run the deterministic audit: `python3 scripts/audit_courseware.py <deck-dir|zip>`.
   Zero ERROR required.
3. Zip the folder and upload as **draft**:
   `POST /api/v1/courses/{course_id}/courseware` (multipart `file`; scope
   `courseware:write` on the API-key channel). Draft is replaceable (re-upload wins).
4. Facilitator publishes: `POST /api/v1/courses/{course_id}/courseware/publish`
   (JWT, FACILITATOR only) — snapshot becomes the published version shown on the
   course detail page via `courses.courseware_document_id`; re-publish creates a new
   version. `DELETE` detaches.
5. Verify in the platform iframe (not just file://): deep links, every interaction,
   no console SecurityError.

Full endpoint/state-machine contract: `references/platform-courseware-pipeline.md`.
