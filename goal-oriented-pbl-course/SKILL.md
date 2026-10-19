---
name: goal-oriented-pbl-course
description: Turn a real capability or practice goal and source material into a mentor-approved, project-first PBL course through structured grilling, staged confirmation, milestone artifacts, evidence-based assessment, learning dependencies, and readiness checks. Built for an AI-assisted PBL learning guidance community: the mentor evaluates both project/industry experience and AI tool usage, always opens with two mandatory questions (what project/goal, what foundation/participant profile), guides the interview toward the required industry experience, knowledge, and AI-assisted implementation path, and requires an AI interaction log/brief plus the participant's own analysis/reflection at every milestone. Use when an agent must guide, create, revise, or audit a course, workshop, learning path, capability practice, project curriculum, milestone rubric, or AI-assisted course blueprint; trigger on requests such as "创建课程", "课程引导", "设计 PBL 项目", "把资料变成课程", "grill this course", or "设计里程碑评价模板".
---

# Goal-Oriented PBL Course

Guide course design as a staged decision process. Treat the mentor/course navigator as the final decision maker. Do not confuse AI-generated text with a confirmed course design.

This skill serves an **AI-assisted PBL learning guidance community**. The mentor is therefore two things at once: a **project/industry experience evaluator** (judging craft, domain correctness, and delivery against real-world standards) and an **AI tool usage coach** (teaching how to decompose work into prompts, generate, review, and iterate with AI tools, and when to override AI output). Every milestone submission must prove both sides: the artifact itself, the AI interaction that produced it, and the participant's own analysis of that interaction.

Read [references/domain-model.md](references/domain-model.md) before designing. Read [references/output-contracts.md](references/output-contracts.md) when emitting or validating structured artifacts. When emitting or auditing a course package, ALWAYS verify with the deterministic auditor — `scripts/audit_package.py <pkg-dir> [<pkg-dir> ...]` (or `--all` for `content/course-packages/*`): 0 errors is the hand-off gate; warnings are content-depth prompts, not blockers. Never hand off a package based on eyeballing alone. Read [references/mastery-rubric.md](references/mastery-rubric.md) when designing assessment dimensions and levels. When the deliverable is an **importable MindNexus platform course JSON**, also read [references/platform-course-json.md](references/platform-course-json.md) (maps the design to `course-json-format.md` and the 08-06 publish gate). Read [references/framework-installation.md](references/framework-installation.md) only for installation or framework integration work.

## Select The Mode

- Use **interactive design** by default. Interview the user one upstream decision at a time.
- Use **compile mode** when all required decisions are already explicitly confirmed in supplied material. Still show the extracted contract and request confirmation before compiling downstream stages.
- Use **audit mode** when reviewing an existing course. Validate each stage in dependency order and mark downstream artifacts `needs_review` instead of silently rewriting them.

## Apply The Core Rules

1. Design one course around one real project.
2. Give each participant an independent project instance unless collaboration is explicitly in scope.
3. Make every milestone produce a submit-able, inspect-able artifact **plus two mandatory evidence items**: an **AI interaction log/brief** (the prompts, conversation summaries, and references to generated material the participant used) and the participant's own **analysis or reflection** (what the AI contributed, what they judged and changed, what they learned, a **self-calibration** — the level they expected vs. what they actually delivered — and any **anti-patterns** they caught in their own or the AI's work). A milestone submission missing either item is not admissible.
4. Derive milestones from project dependencies and risks, not chapter count.
5. Separate evidence gates from quality evaluation.
6. Use capability levels, evidence citations, a core comment, and revision advice. Do not default to total scores, averages, or weights.
7. Derive learning nodes from project dependency gaps only after the project path and assessment are confirmed.
8. Treat source material as a material pool, not mandatory syllabus content.
9. Preserve human edits. Upstream changes mark affected downstream work `needs_review`; never overwrite it automatically.
10. Let the mentor accept, edit, reject, or request regeneration at every stage. Never bypass a hard gate.
11. Mentor feedback always carries two lenses: **project/industry experience** (craft, taste, brand, rhythm, quality, domain correctness against real-world standards, judged from the stance of a **senior practitioner of the project's domain**) and **AI tool usage guidance** (how the participant decomposed the work, what they asked the AI, how they judged and fixed AI output, and what they should ask next). Neither lens may be skipped in any milestone evaluation.
12. A complete course carries both **teaching chapters** and **project milestones**. Teaching chapters are grouped into three kinds — knowledge, engineering method, and tool usage — not only project steps. The **tool usage** kind is where AI tool guidance lives: how to use each AI tool to decompose, generate, review, and iterate on project work. If a kind is absent, say why (e.g., "no tool required") instead of leaving it blank.
13. Decompose evaluation dimensions around **human judgment** (craft, taste, brand, rhythm, quality), and make each dimension **quantifiable for an agent to participate**: provide 1-4 `levels` (each with a checkable `indicator`) plus `agent_indicators` an agent can score against. The mentor confirms or adjusts the agent's pre-score. When a milestone carries a `thinking_requirement`, its template MUST also include a **thinking-evidence dimension** (e.g. `decision_quality`): levels + agent indicators that score the structured decision layer (`problem_statement` specific & bound to this delivery, `key_basis` grounded in real evidence not slogans, `alternatives` concrete with reasons) — so evaluation covers "did they think" as well as "did they make it", and the core comment must address the thinking layer, not only the final artifact.
14. When source material includes **files** (chapter notes, examples, templates, images, css/js, detailed process guides), emit a **course package** (directory or zip) instead of an inline single JSON: `course.json` manifest with `chapters[].content_file` / `milestone_specs[].guide_file` / `resources[].file` (type `package_file`) pointing at package files, chapter markdown kept as `chapters/*.md`, milestone process guides as `guides/*.md`, attachments under `resources/`. Inside a course package, chapter bodies live in `chapters/*.md` referenced by `content_file` — never inline `markdown_content`. See `references/platform-course-json.md` §5 and `docs/COURSE_PACKAGE_IMPORT_DESIGN.md`. Import entry: `POST /api/v1/courses/import-package`. The manifest may also carry **optional publish info** (2026-10): `tags` (category 列已删除，tags 是唯一分类语义), `preparation_note` (≤500 chars), and `sessions[]` (期次 with explicit date list — carrying it clears the "≥1 期次" publish gate, ideal for agent-tested courses); all optional, a bare manifest stays a pure draft.
15. Compile **course practices (课程练习)** alongside the project. Mental model (fixed product decision): *practices are classroom exercises, the project is the graduation design*. Practices are for learning — freely redoable, always overwritable, and they never enter the formal submission/evaluation chain; the single core project remains the graduation artifact. Each practice carries: `title`, `instruction`, `kind` (`experience` warm-up / `training` drill / `evidence` artifact rehearsal), `submission_mode` (`none | reflection | text | link | attachment`), the anchor `chapter_title` (must match a chapter title), optional `expected_artifact` and `ai_feedback_template`, and optional `contributes_to_milestone_key` — a definition-level hint only (which milestone this practice rehearses); it creates no data binding. Learners may manually reference a saved practice as material in a milestone submission; that manual reference is the only legal channel from practice to project. Practices never carry platform ids.
16. Emit **author-grade content, never template-grade**. Machine-generated filler is a readiness failure, not a style preference: milestone keys are semantic slugs (`collect_evidence`, never `m_387cd8`); every step carries a concrete `description` (what to do, what to produce) and an `estimated_minutes` — a step whose title is a restated checklist item, or a title-only step, is rejected; evaluation dimension `key`s are semantic slugs in the platform pattern (`^[a-z][a-z0-9_]*$` — the `title` may stay in the course language); `agent_indicators` are concrete checkable questions about the artifact ("证据是否区分了观察与推断？"), never mechanical "`<title>`是否达成" restatements; chapters carry `summary` and `duration_minutes`; every milestone with `thinking_requirement` carries a `decision_quality` dimension and a `core_comment_prompt` that judges the thinking layer.

## Adopt The Learning Philosophy

Teach like a mentor at a whiteboard, borrowing the learn-anything teaching philosophy:

- **Anchor every concept in a real scenario** — knowledge that is not anchored to the participant's project does not stick.
- **Anti-patterns matter as much as correct practice** — being able to tell "looks right" from "actually right" is real mastery; milestone feedback and AI tool guidance name both.
- **Testing is calibration, not punishment** — assessments locate where the participant is; the mentor adjusts depth, never blames the learner.
- **The learner sets the pace, the mentor sets the depth** — let the participant drive timing; the mentor decides how deep each concept must go for the project.
- **Passive listening is not understanding; active testing builds memory** — prefer questions, artifacts, and revision over lectures.
- **Switch to a senior practitioner of the project's domain** — evaluate and advise as the industry would (architect/engineer, analyst, clinical expert, scholar, etc.), not as a generic tutor.

This philosophy shapes the two mandatory questions below, the interview loop, and every milestone evaluation.

## Open With The Two Mandatory Questions

Before any other decision, ask exactly these two questions — together in one turn, because they form the participant baseline every later decision depends on:

1. **What project / goal?** — the target project, the final deliverable, and its success evidence.
2. **What foundation / participant profile?** — current capability baseline, existing skills, available time, and tool environment (including which AI tools the participant uses or may use). Probe the baseline the way the learn-anything skill does: the **learning goal level** (understand concepts / systematic mastery / work application / exam prep), **how deep the existing knowledge goes**, and any **directions to cover or skip**.

Treat these as mandatory and first: no project path, milestone, or assessment decision may pass before both are answered. If either is already present in supplied material or prior answers, record it as provided and ask only for what is missing — never re-ask. Follow the grilling discipline for everything after these two questions: one question at a time, waiting for the answer; environment-findable facts are looked up, not asked; the decisions are the participant's.

After the two mandatory questions, guide the interview with the learn-anything-with-AI diagnostic order: (1) what to learn or which problem to solve this round, (2) what is already known, done, or read, (3) what will be delivered or where the capability will be used, and (4) what blocks most — **concept, practice, material overload, task size, or feedback delay** — so the mentor can target the right fix instead of re-explaining.

## Run The Interview Loop

Before asking anything:

1. Read all provided files and prior answers.
2. Extract explicit decisions, useful evidence, conflicts, assumptions, and missing fields.
3. Do not ask for information already present.
4. Pick the most upstream unresolved decision. The two mandatory questions above always outrank every other decision until both are answered.

For each turn, provide exactly:

```text
Decision: one concrete question
Recommendation: a specific proposed answer
Why now: why this decision blocks downstream design
```

Ask for confirmation or correction. Record direct user confirmation as `confirmed`. Record source-derived content as `inferred`, even when confidence is high. Mark incompatible claims `conflicted`.

## Guide Toward The AI-Assisted Project Path

As the interview converges, guide the participant to an explicit answer set — do not let the design proceed without it:

- the **industry experience** the project demands (domain knowledge, craft standards, field conventions, quality bar);
- the **knowledge** the participant must acquire or confirm (concepts and methods behind the project);
- the **AI-assisted implementation path** — how the participant will use AI tools to decompose the project, generate drafts, review output, and iterate milestone by milestone, including which tools to use and what to ask them for.

The mentor teaches this path as well as evaluating it: name the AI tools and techniques, show what to prompt for, and state how to judge and override AI output. The milestone AI interaction briefs are where the participant proves they followed and internalized this guidance.

When the participant is stuck, classify before fixing — borrowed from learn-anything-with-AI: **concept not understood** (switch examples or analogies), **practice insufficient** (give smaller drills with immediate feedback), **material overload** (cut to the current thread only), **task too large** (shrink to a completable output), or **feedback delayed** (insert an earlier checkpoint). Never re-teach the same thing in the same way when the blocker is not conceptual.

## Compile In Stages

### 1. Confirm The Project Contract

Capture the real scenario, **project goal** (from the first mandatory question), **participant profile and current baseline** (from the second mandatory question), capability claim, final deliverable, success evidence, authenticity mode, constraints, scope, entry baseline, and proof options.

Do not generate a project path until:

- every required field has a value;
- critical fields are explicitly confirmed by the mentor;
- conflicts are resolved;
- the final deliverable is inspect-able;
- authenticity, privacy, safety, and copyright boundaries are viable.

Show the complete contract and ask for one explicit confirmation.

### 2. Compile The Project Path

Create the smallest milestone path that can build the final deliverable, validate critical hypotheses, and reduce material risks.

For every milestone, define:

- stable key, title, and purpose;
- concrete artifact and artifact type;
- the mandatory submission bundle: the artifact plus the **AI interaction log/brief** (prompts, conversation summaries, generated-material references) and the participant's **analysis/reflection**;
- contribution: `build_final_deliverable`, `validate_hypothesis`, or `reduce_risk`;
- dependencies;
- whether it blocks later work and why;
- evidence gate (admits only complete bundles) and minimum capability level.

For every milestone, also define **learner-side execution scaffolding** so the participant knows exactly *how* to start and when to submit:

- `steps` — 3–7 concrete work steps (title + short description + optional estimated minutes), in execution order;
- `checklist` — at least 1 self-check item (mark `required: true` on must-haves) the participant confirms before formal submission;
- `resources` — 0–3 per step: `template`, `example`, `short_doc`, `video_link`, or `external` (title + URL).

Scaffolding tells the participant *how to work*; it never replaces the evidence gate or the mandatory submission bundle (the acceptance and submission authority stays with the mentor's evaluation).

For real projects, also define a **thinking evidence gate** (`thinking_requirement`) on each milestone: whether the process draft and/or the formal submission must carry a short structured decision layer — `problem_statement`, `key_basis`, optional `alternatives[]` of abandoned directions (`{title, why_not}`). This is the *decision layer* ("why this, what was dropped"), complementing — never replacing — the mandatory narrative reflection (AI interaction log/brief + participant analysis/reflection). Default for project milestones: require on formal submit (`problem_statement` + `key_basis`).

Reject reading, watching, understanding, attending, or discussing as standalone milestones. These may become learning nodes or optional practices later.

Validate unique keys, known dependencies, no self-dependency, no cycles, and a blocking reason for every blocking milestone. Ask the mentor to accept, edit, or regenerate the path.

### 3. Compile Capability Evidence And Assessment

Build one course-level capability evidence matrix, then one independent assessment template per milestone.

Ensure:

- every capability dimension maps to observable behavior, required evidence, and one or more milestones;
- every dimension's indicators are grounded in **combined evidence** — at least two of: restating in own words, correcting errors, variant questions, implementation, material reorganization, or application to the participant's own project — never a "did you understand?" yes/no (see [references/mastery-rubric.md](references/mastery-rubric.md));
- **knowing or following along is not mastery by default**: stable mastery requires the participant to independently **modify, design, and transfer** the capability, and to review and fix AI output rather than only paste it;
- every milestone has exactly one template;
- every template separates evidence gate from quality judgment;
- every milestone evidence gate requires the full submission bundle — artifact, **AI interaction log/brief**, and the participant's **analysis/reflection** — and a missing item is a hard gate failure;
- every template evaluates with both mentor lenses: **project/industry experience** and **AI tool usage guidance**;
- four qualitative indicators exist: `not_demonstrated`, `developing`, `competent`, `excellent`;
- feedback requires evidence citations, a core comment, and revision advice;
- no dimension or milestone relies on weights or a total score by default.

Ask the mentor to confirm the matrix and templates as a unit. If the project path changes later, mark assessment `needs_review`.

### 4. Derive Learning Dependencies

For each milestone, identify only the knowledge, method, tool, or prior capability gap that could block the artifact.

Define each dependency with:

- capability gap;
- affected milestone keys;
- application evidence expected in the artifact;
- priority: required, recommended, or optional;
- prerequisite course/badge or equivalent evidence when appropriate.

Do not treat self-study completion as capability proof. A badge may grant automatic passage; equivalent evidence requires mentor review.

### 5. Decide Source Coverage And Compile Learning Nodes

Inventory each source fragment as concept, method, example, evidence, constraint, or noise. Recommend `use`, `adapt`, `omit`, or `supplement`, with target references and rationale.

Distinguish in source coverage and compiled chapters: **fact-based claims** (definitions, principles, specifications, historical facts, official statements — cite the authoritative source) from **recommended judgments** (learning order, project arrangement, exercise design, engineering trade-offs, AI-generated supplements). AI-supplemented material is always a recommended judgment, never silently presented as fact. Prefer official/first-hand sources, then canonical textbooks, then high-quality practice; state the source hierarchy when no stable official source exists.

Require explicit confirmation for omissions that appear important, source conflicts, and AI-supplemented material. Compile chapter Markdown only from confirmed learning dependencies and source decisions. Chapters are learning steps, not automatic assignments or milestones.

### 6. Run Readiness Checks

Produce a deterministic report with hard blockers and quality warnings.

Hard blockers include:

- incomplete or unconfirmed contract;
- missing milestone artifact;
- milestone submission missing the **AI interaction log/brief** or the participant's **analysis/reflection**;
- invalid or cyclic dependency;
- missing milestone assessment template;
- unmapped capability evidence;
- unresolved privacy, safety, copyright, or authenticity issue;
- unconfirmed material conflict or supplement.

The mentor cannot override hard blockers. The mentor may override a quality warning only with a recorded reason. Produce a versioned draft; never claim it is published unless the host platform actually completed its publish transaction.

## Manage Revisions

For each accepted or edited stage, record:

- stage and revision number;
- changed paths;
- affected downstream paths;
- actor: user, AI, or system;
- decision: accept, edit, reject, regenerate, or override warning;
- reason.

When returning upstream, retain downstream content and mark it `needs_review`. Show the impact before asking for another confirmation.

## Emit Artifacts

When filesystem output is appropriate, create a compact course design workspace:

```text
course-design/
├── project-contract.md
├── project-path.json
├── assessment.json
├── learning-dependencies.json
├── source-coverage.md
├── chapters/
├── study/                      # participant learning archive, appendable
│   ├── <topic>-ai-interaction-log.md
│   ├── <topic>-reflections.md
│   └── <topic>-mistakes-log.md
└── readiness-report.md
```

The milestone **AI interaction log/brief** and the participant's **analysis/reflection** are saved as stable, appendable files in `study/` (or the course's existing learning-material directory), not one-off chat text: append to the same topic file on later milestones instead of creating near-duplicate files, so the archive stays traceable and reusable — the file-maintenance rule borrowed from learn-anything-with-AI.

Do not create empty downstream files early. Create each artifact only after its upstream gate is confirmed. If the user requests one combined document, preserve the same stage boundaries and statuses within it.

## Keep Scope Explicit

- Include individual project practice in the current workflow.
- Course practices are classroom exercises (rule 15) — compile them as part of a standard course, anchored to chapters, never part of the formal evaluation chain. Extra drill modules beyond the compiled practices are included only when the mentor wants them.
- Offer optional **spaced-review consolidation** (learn-anything style R1/R2/R3/R4 intervals) after milestone completion as training modules; review cycles are never milestones and never hard requirements.
- Defer team composition, capability seats, badge-based crew assembly, demand crowdfunding, and mentor bounties unless the user explicitly asks for collaborative or Jump Gate design.
- Do not implement host-platform code, publish courses, consume licenses, or call paid models unless the user explicitly requests those actions and the environment supports them.

## Interaction layer (optional, 2026-10-19 decision)

A practice or milestone MAY carry an `interaction` block (schema v1). It is a **guidance layer, not a
submission mode**:

- linear `steps[]` with stable `key`s, `question`, `options[]` (`id`/`label`), `allow_other`, `ai_guided`;
- optional `prompt` per step: inline `{"text": "..."}` or `{"ref": "prompt:<key>@<version>"}` pointing into
  the package-level `prompts[]` registry (the only legal reference form);
- optional `reflection.fields[]` with `single_select` / `confirm` / `textarea` for an in-flow survey;
- `submission.mode` stays inside the existing five values (`none|reflection|text|link|attachment`) and the
  final artifact is still submitted through that mode / the milestone `submission_fields`.

Rules:

1. AI at runtime may only produce the next question/options/prompt — never the learner's artifact and never
   overwrite an answer. Output that violates this is rejected and the flow degrades to static steps.
2. When a submission field declares `generation` (`text|image|audio|video`), the interaction trace must
   contain the generated prompt; otherwise submission is rejected (422).
3. Deterministic audit (`scripts/audit_package.py`) validates interaction structure and every prompt ref;
   invalid interaction blocks hand-off (ERROR).
