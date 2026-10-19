# Platform Course JSON Output Contract

Emit the confirmed course design as an **importable MindNexus platform course JSON**.
The platform JSON schema authority is `docs/course-json-format.md`; the **08-06 publish gate**
requires every milestone spec to carry `milestone_key` + an `evaluation_template`
(`dimensions` + `core_comment_prompt`). Validate the emit against that gate before handing off.

## 1. Emit Contract

```jsonc
{
  "id": "english_lowercase_slug",       // OPTIONAL for course packages; when absent the platform generates a new course id on import
  "title": "Course title",                  // required
  "description": "Course description",
  "cover_image_url": null,
  "tags": ["AI通识", "Agent"],              // optional multi-value labels (category 列已删除，tags 是唯一分类语义)
  "preparation_note": "开课前请完成…",       // optional ≤500 chars; 课前准备区块说明（工具清单引用平台笔记，导入后在 GUI 配置）
  "sessions": [                             // optional 期次（可选发布信息；不带=纯草稿，导师 GUI 后补）
    {                                       //   带上则发布门禁「≥1 期次」开箱即过（Agent 测试快速通路）
      "title": "第一期",                     // optional; default 第 N 期
      "session_number": 1,                  // optional; default list order 1..N
      "start_date": "2026-11-01T10:00:00Z", // required (期次起止，datetime)
      "end_date": "2026-11-30T18:00:00Z",   // required
      "delivery_mode": "online",            // online=视频会议 / offline=线下
      "meeting_url": "https://…",           // online 时；location 用于 offline
      "max_students": 30,                   // optional
      "session_dates": ["2026-11-05", "2026-11-12"],  // optional 显式上课日期列表（0095 唯一真相源，去重排序，≤400）
      "schedule_start_time": "19:00",       // dates 非空时必填
      "schedule_end_time": "21:00",         // dates 非空时必填且晚于开始
      "schedule_note": "改排期说明（仅成员可见）"   // optional
    }
  ],
  "status": "draft|pending|published",      // default pending（导入恒为 draft）
  "pricing_type": "free|paid",              // default free
  "requires_approval": false,
  "price_cents": 0,                         // paid>0, free forced to 0
  "currency": "CNY",
  "is_referenceable": true,
  "referenceable_cases": "all|selected|none",
  "lessons": [                              // teaching chapters (Markdown; legacy inline form)
    { "title": "...", "content": "...", "order_index": 0 }
  ],
  "chapters": [                             // chapters as package files (preferred for course packages)
    { "title": "...", "chapter_type": "markdown",
      "content_file": "chapters/01-intro.md",   // package-relative md path; alternative to inline markdown_content
      "summary": "...", "order_index": 0 }
  ],
  "assignments": [                          // one core project per course
    {
      "id": "assignment_slug",
      "title": "Project title",
      "description": "Project purpose",
      "input_materials": [],
      "milestone_specs": [                  // ← derived from Project.milestones
        {
          "milestone_key": "goal_define",   // REQUIRED by publish gate; ^[a-z][a-z0-9_]*$
          "title": "Milestone title",
          "description": "Milestone purpose + artifact",
          "rules": ["acceptance rule 1"],   // at least 1; always include: submit AI interaction log/brief + participant analysis/reflection
          "steps": [                        // learner-side execution scaffolding (3-7; optional but recommended)
            { "order_index": 1, "title": "Step title", "description": "What to do",
              "estimated_minutes": 30,      // nullable
              "resources": [                // 0-3 per step
                { "type": "template|example|short_doc|video_link|external",
                  "title": "Resource title", "url": "https://..." },
                { "type": "package_file",   // package-internal file (course package)
                  "title": "In-package template", "file": "resources/templates/x.md" }
              ]
            }
          ],
          "checklist": [                    // ≥1 item; self-check before formal submission
            { "text": "Checklist item", "required": true }
          ],
          "thinking_requirement": {         // optional; structured decision evidence gate
            "require_on_process_draft": false,
            "require_on_formal_submit": true,   // default recommendation for real projects
            "required_fields": ["problem_statement", "key_basis"]
          },
          "guide_file": "guides/milestone-key-1.md",  // optional: milestone detailed process guide (package file)
          "evaluation_template": {          // REQUIRED by publish gate
            "dimensions": [                 // ← derived from Assessment Bundle dimension
              { "key": "dim_key", "title": "Dimension name", "weight": 1.0,
                "levels": [                 // optional; quantified 1-4 for agent pre-scoring
                  {"level": 1, "label": "未达标", "indicator": "checkable indicator"},
                  {"level": 3, "label": "胜任", "indicator": "checkable indicator"}
                ],
                "agent_indicators": ["agent-checkable criterion 1", "agent-checkable criterion 2"]
              },
              { "key": "decision_quality",  // RECOMMENDED thinking-evidence dimension (when thinking_requirement set)
                "title": "思考证据质量", "weight": 0.2,
                "levels": [
                  {"level": 1, "label": "未达标", "indicator": "决策说明缺失或与交付无关（空话/套话）"},
                  {"level": 2, "label": "发展中", "indicator": "有决策说明但与交付弱绑定，未提放弃方向"},
                  {"level": 3, "label": "胜任", "indicator": "核心问题与决策依据清晰，与交付强绑定，有真实放弃记录"},
                  {"level": 4, "label": "优秀", "indicator": "取舍有依据、风险自知，放弃方向具体且反思有洞察"}
                ],
                "agent_indicators": [
                  "problem_statement 是否具体且与本次交付绑定",
                  "key_basis 是否引用真实依据（反馈/约束/原则/案例）而非口号",
                  "alternatives 是否具体并说明放弃原因（防表演性填空）"
                ]
              }
            ],
            "core_comment_prompt": "评价最强能力与主要缺口；若配置了 thinking_requirement，必须同时评价思考证据（决策真实性、与交付的一致性、放弃方向的具体性），不得只看最终效果"
          }
        }
      ],
      "submission_requirements": [          // required deliverables; every milestone also requires AI log + reflection
        { "title": "deliverable", "required": true },
        { "title": "AI interaction log/brief", "required": true },
        { "title": "Participant analysis/reflection", "required": true }
      ],
      "rubric": [                           // weights MUST sum to 1.0
        { "criterion": "dim1", "description": "...", "weight": 0.25 }
      ],
      "is_referenceable": true
    }
  ],
  "practices": [                            // course practices = classroom exercises (项目才是毕业设计)
    {
      "title": "Practice title",
      "instruction": "What to do, how to redo it freely (≤5000 chars)",
      "kind": "experience|training|evidence",     // warm-up / drill / artifact rehearsal
      "submission_mode": "none|reflection|text|link|attachment",
      "chapter_title": "Must exactly match one chapters[].title (anchor)",
      "required": false,                          // practices are for learning; default optional
      "contributes_to_milestone_key": null,       // definition-level hint only, no data binding
      "expected_artifact": "Short description of the practice output",
      "ai_feedback_template": { "focus": "What the AI feedback should check" }
    }
  ]
}
```

### 1.1 Optional interaction layer (2026-10-19)

`practices[].interaction` and `assignments[].milestone_specs[].interaction` MAY define a guidance layer.
It never changes `submission_mode`; final artifacts still use the existing mode / `submission_fields`.

```jsonc
"prompts": [                              // optional registry; ref-target for interaction steps
  { "key": "material_diagnosis", "version": 1, "text": "可直接复制的提示词…" }
],
"practices": [
  {
    // … existing practice fields …
    "interaction": {
      "schema_version": 1,
      "enabled": true,
      "default_mode": "guided",           // guided | full
      "steps": [
        {
          "key": "s1",                     // stable id; changing it breaks existing traces
          "question": "先选一个方向",
          "options": [{ "id": "a", "label": "生活方式" }, { "id": "b", "label": "空间叙事" }],
          "allow_other": true,
          "ai_guided": false,
          "prompt": { "ref": "prompt:material_diagnosis@1" }   // or { "text": "..." }
        }
      ],
      "fallback": { "text": "AI 引导暂不可用时的静态说明" },
      "reflection": {
        "enabled": true,
        "fields": [
          { "key": "reflection_result", "type": "single_select", "title": "结果如何？",
            "required": true,
            "options": [{ "value": "good", "label": "好" }, { "value": "bad", "label": "不好" }] }
        ]
      },
      "submission": { "mode": "text", "fields": [] }   // mode ∈ existing five values
    }
  }
]
```

Validation: `schema_version=1`; `enabled` boolean; step `key` unique; option `id` unique; `ai_guided`
boolean; each `prompt` has non-empty `text` or a `prompt:<key>@<version>` ref resolvable in `prompts[]`;
`reflection.fields[].type` ∈ `single_select|confirm|textarea` (single_select needs non-empty options);
`submission.mode` ∈ five values; `fields[].generation` ∈ `text|image|audio|video`.

## 2. Mapping From Design Contracts

| Skill contract (design) | Platform course JSON |
|---|---|
| `Project.project_title/purpose` | `assignments[].title/description` |
| `Project.milestones[].milestone_key/title/purpose/artifact` | `milestone_specs[].milestone_key/title/description` (+ `rules` from `artifact.quality`/`evidence_gate`) |
| `Project.milestones[].mandatory_submissions` (`ai_interaction_log_brief`, `participant_analysis_reflection`) | `milestone_specs[].rules` + `assignments[].submission_requirements[]` (always `required: true`) |
| `Project.milestones[].steps` | `milestone_specs[].steps` (learner-side execution scaffolding; 3–7 steps, 0–3 resources each) |
| `Project.milestones[].checklist` | `milestone_specs[].checklist` (≥1 self-check item before formal submission) |
| `Project.milestones[].thinking_requirement` | `milestone_specs[].thinking_requirement` (optional structured decision-evidence gate) |
| `Assessment Bundle.capability_matrix.dimensions[].dimension_key/name` | `evaluation_template.dimensions[]` + `rubric[].criterion` |
| `Assessment Bundle.milestone_templates[].core_comment_prompt` | `evaluation_template.core_comment_prompt` |
| `final_deliverable` / `success_evidence` | `submission_requirements[]` |
| training modules / classroom exercises / spaced-review drills | `practices[]` (never milestones; never part of the evaluation chain) |
| learning nodes / source coverage | `lessons[]` chapters |
| knowledge / engineering-method / tool-usage content | `lessons[]` chapters (group by kind) |

`steps`/`checklist`/`resources` are **learner-side scaffolding**: they tell the participant *how* to work
through a milestone and what to self-check before submitting. They never replace `rules` (acceptance
criteria) or `submission_requirements` (AI interaction log/brief + participant analysis/reflection are
always `required: true`). The evaluation and submission authority is unchanged.

`thinking_requirement` is the **decision-evidence gate**: when `require_on_process_draft` /
`require_on_formal_submit` is true, the matching submission must carry a structured
`thinking` object (`problem_statement`, `key_basis`, optional `alternatives[]` of
`{title, why_not}`). It complements — never replaces — the narrative reflection
(AI log/brief + analysis) already mandatory via `submission_requirements`:
thinking is the short decision layer ("why this, what was dropped"), reflection is the
narrative layer ("what was done, what AI contributed").

Group `lessons[]` by three kinds: **knowledge** (concepts), **engineering method** (how-to), and
**tool usage** (how to use each tool). A complete course has project milestones (the PBL path)
plus teaching chapters of these kinds; if a kind is absent, state why.

Do NOT carry `weight`, total-score, or average-score fields into `evaluation_template.dimensions`
(the publish gate expects a plain `{key,title,weight}` shape; total-score is forbidden by
`output-contracts.md` §Assessment). Rubric weights are the only numeric weights emitted.

## 3. Validation Gate (before hand-off)

**Deterministic auditor (mandatory):** run `goal-oriented-pbl-course/scripts/audit_package.py <pkg-dir>` — it encodes every check below plus rule 3/15/16 hard gates (submission_requirements AI-log/reflection items, checklist AI/reflection items, `guide_file` existence, steps 3-7 with real descriptions, practice enums/anchors). Exit code 0 = hand-off allowed; any ERROR blocks hand-off.

- `id`/`title` present; `lessons` and `assignments` arrays valid.
- Exactly one core `assignment` (one project per course).
- `rubric` weights sum to `1.0` (platform rejects otherwise with `422`).
- Every `milestone_spec` has a unique `milestone_key` AND an `evaluation_template` with
  non-empty `dimensions` + `core_comment_prompt` (publish gate `_validate_framework`).
- Every milestone's `submission_requirements` includes the **AI interaction log/brief** and the
  participant's **analysis/reflection** as `required: true` deliverables.
- ≥2 milestones, ≥3 rubric criteria.
- When `steps` is present: 3–7 entries with ascending `order_index`; when `checklist` is present:
  ≥1 entry. These fields are optional scaffolding — an absent `steps`/`checklist` must not break
  import or the publish gate (the platform treats them as opaque JSON in `deliverable_spec`).
- `thinking_requirement` is optional and opaque to import/publish; `required_fields` entries must be
  a subset of `problem_statement | key_basis` (MVP).
- When `practices` is present: every `kind` ∈ `experience|training|evidence`, every
  `submission_mode` ∈ `none|reflection|text|link|attachment`, every `chapter_title` exactly matches
  one `chapters[].title` (unresolved anchors import as unlinked practices — a quality failure),
  `contributes_to_milestone_key` (when set) matches a real `milestone_key`, and no practice carries
  an `id` (packages with platform ids are rejected with 422).
- **Author-grade content (rule 16):** semantic milestone keys (no `m_xxxx` hex slugs); every step has
  a concrete `description` + `estimated_minutes`; dimension `key`s match `^[a-z][a-z0-9_]*$` (titles may
  stay in the course language); `agent_indicators` are concrete checkable questions, never
  "`<title>`是否达成" templates; chapters carry `summary` + `duration_minutes`; in a course package,
  chapter bodies are `chapters/*.md` via `content_file` (inline `markdown_content` is a legacy fallback,
  not package style).

## 4. Golden Reference

`content/course_opening_guide.json` is a passing, importable example (imports via
`POST /api/v1/courses/import`). Use it as the shape reference when emitting a new course.
`content/course-packages/westlake-ip-card-design/` is a passing **course package** example
(directory + zip, imports via `POST /api/v1/courses/import-package`).

## 5. Course Package Layout (directory + zip)

When source material includes files (chapter notes, examples, templates, images, css/js,
detailed process guides), emit a **course package** instead of a single inline JSON —
structure identical to `course.json` above plus package files:

```
<course-package>/                     # zip root or content/course-packages/<slug>/
├── course.json                       # manifest (this contract; chapters use content_file)
├── chapters/*.md                     # chapter notes referenced by chapters[].content_file
├── guides/*.md                       # milestone process guides referenced by milestone_specs[].guide_file
└── resources/**                      # images / examples / templates referenced by resources[].file (package_file)
```

Rules:
- A course package is an **offline content asset**: it carries format + content only. Import **creates a new course draft** — pure insert, no update/overwrite/delete. Platform ids (`id`, assignment ids, practice ids) are generated by the import backend; **a package carrying any platform id is rejected with a clear message** (MVP has no revision/update semantics).
- `content_file` / `guide_file` / `resources[].file` are package-relative paths; the file MUST exist in the package (missing → import 422).
- Markdown relative references inside `chapters/*.md` / `guides/*.md` (images, media, files) are auto-collected as package assets and rewritten to `/api/v1/assets/{id}/raw`. Resolution is **markdown-standard**: relative to the referencing file's directory first (`./images/x.png` from `chapters/01.md` → `chapters/images/x.png`), with package-root-relative paths as fallback; `./x` and `x` deduplicate to one asset. Unresolvable refs stay as-is (external links allowed).
- **Media writing contract**: `![alt](path)` renders as `<img>` — images only. Audio/video MUST be written as HTML tags (`<video controls src="media/clip.mp4"></video>`, `<audio controls src="media/narr.mp3"></audio>`); they are collected, uploaded, and sanitized the same way (allowed: `.mp4` `.mp3`).
- `thinking_requirement` / `steps` / `checklist` ride along inside `milestone_specs` exactly as in single JSON; the import pipeline treats them as opaque JSON (no package files needed).
- Optional publish info rides in the manifest root: `tags` / `preparation_note` / `sessions[]` (see §1). All are optional — a bare manifest imports as a pure draft with zero publish info. `sessions[]` is validated on import (dates without schedule times → 422 Chinese error). The preparation **tool checklist** references platform note documents and can therefore NOT live in a package — configure it post-import via GUI (`课程管理 → 课前准备`) or `PUT /api/v1/courses/{id}/preparations`.
- Publication gates (all verified server-side at publish): ≥1 期次, capacity > 0, mentor accepted + owner/navigator dual confirm, evaluation framework complete (1 core project, ≥2 milestones with evaluation templates). A package carrying `sessions[]` clears the 期次 gate on import.
- Zip: one `course.json` at package root (a nested folder containing it is auto-detected); absolute paths and `..` escapes are rejected.
- Platform entry points: single JSON → `POST /api/v1/courses/import`; package zip → `POST /api/v1/courses/import-package`. Full design: `docs/COURSE_PACKAGE_IMPORT_DESIGN.md`.

## 6. Agent Import Guide（AI Agent 调用契约）

两个导入端点都已接入 API Key 通道（`require_scopes`），Agent 可免 JWT 全流程建课：

| 通道 | 端点 | scope | 载荷 |
|---|---|---|---|
| 单 JSON | `POST /api/v1/courses/import` | `course:import` | JSON body（§1 形状） |
| 课程包 zip | `POST /api/v1/courses/import-package` | `course:import` | multipart `file=<zip>`（≤200MB） |

- 鉴权：`Authorization: Bearer mnk_...`（API Key）。key 只能调用 scope 白名单内端点；`course:import` 覆盖两导入端点 + 课程导出（key 属主同时须为课组成员）。
- 成功：`201 {"course": {"id": "course_…", …}, "message": "课程已导入为草稿…"}`。**拿 `course.id` 做后续一切操作**（期次/课件/发布）。
- 失败：`422 {"detail": "<中文提示>"}`（zip 损坏/引用缺失/平台 id/期次校验失败）；`403`（key 越权/带平台课程 id）。
- Agent 建课最小闭环（按序）：
  1. 导入课程包（manifest 建议携带 `sessions[]` + `capacity`）→ 201 取 `course.id`；
  2. 导入/上传课件 zip → `POST /api/v1/courses/{id}/courseware`（scope `courseware:write`；上传即草稿）→ `POST …/courseware/publish`（仅 FACILITATOR）；
  3. 课前准备工具清单（可选）：`PUT /api/v1/courses/{id}/preparations` `{"note": "…", "items": [{"document_id": "doc_…", "order_index": 0}]}`；
  4. 发布流程需 creator/导师双确认（GUI 或对应 command 端点），Agent 导入后以草稿态交付人工确认发布。
- 课件制作规范另见本仓库姊妹技能 [`../interactive-courseware/SKILL.md`](../interactive-courseware/SKILL.md)。
