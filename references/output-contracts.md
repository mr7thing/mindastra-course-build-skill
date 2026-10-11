# Structured Output Contracts

Use these contracts when the host environment accepts JSON or when deterministic validation is required. Omit unknown optional data; do not invent confirmation.

> **To emit an importable MindNexus platform course JSON**, read
> `references/platform-course-json.md` (maps these design contracts to the platform
> `course-json-format.md`, including the 08-06 publish gate `milestone_key` +
> `evaluation_template`). Golden example: `content/course_opening_guide.json`.

## Project Contract

Each field uses the same envelope:

```json
{
  "value": "field value",
  "status": "confirmed",
  "source": "user_answer",
  "source_refs": ["message:42"],
  "confidence": null,
  "confirmed_by": "user-id",
  "confirmed_at": "ISO-8601 timestamp"
}
```

Required keys:

```json
{
  "scenario": {},
  "participant_profile": {},
  "current_baseline": {},
  "capability_claim": {},
  "final_deliverable": {},
  "success_evidence": {},
  "authenticity_mode": {},
  "constraints": {},
  "scope": {},
  "entry_baseline": {},
  "entry_proof_options": {}
}
```

Critical fields requiring explicit confirmation:

```text
scenario
participant_profile
capability_claim
final_deliverable
success_evidence
authenticity_mode
constraints
```

## Project Path

```json
{
  "project_title": "Project name",
  "project_purpose": "Capability and real-world purpose",
  "milestones": [
    {
      "milestone_key": "collect_evidence",
      "title": "Build an evidence sample",
      "purpose": "Create analyzable real material",
      "artifact": {
        "type": "evidence_pack",
        "description": "Redacted samples and context notes",
        "contribution": "reduce_risk"
      },
      "steps": [
        {
          "order_index": 1,
          "title": "Collect raw material",
          "description": "Gather accessible samples with context notes",
          "estimated_minutes": 30,
          "resources": [
            {"type": "template", "title": "Sample collection sheet", "url": ""}
          ]
        }
      ],
      "checklist": [
        {"text": "Redact personal information before submitting", "required": true}
      ],
      "thinking_requirement": {
        "require_on_process_draft": false,
        "require_on_formal_submit": true,
        "required_fields": ["problem_statement", "key_basis"]
      },
      "mandatory_submissions": [
        "ai_interaction_log_brief",
        "participant_analysis_reflection"
      ],
      "dependencies": [],
      "blocking": true,
      "blocking_reason": "Diagnosis is invalid without real evidence",
      "evidence_gate": {
        "required_items": [
          "Accessible artifact",
          "AI interaction log/brief",
          "Participant analysis/reflection"
        ],
        "minimum_samples": 2
      },
      "minimum_quality_level": "competent"
    }
  ]
}
```

Allowed contributions:

```text
build_final_deliverable
validate_hypothesis
reduce_risk
```

Allowed capability levels:

```text
not_demonstrated
developing
competent
excellent
```

Allowed resource types:

```text
template
example
short_doc
video_link
external
```

Validation:

- `milestone_key` matches `^[a-z][a-z0-9_]*$` and is unique.
- Every milestone has a non-empty artifact type and description.
- Every milestone lists `ai_interaction_log_brief` and `participant_analysis_reflection` in `mandatory_submissions` (or in `evidence_gate.required_items`).
- The participant's analysis/reflection covers: what the AI contributed, what they judged and changed, their self-calibration (expected vs. delivered level), and any anti-patterns they caught in their own or the AI's work.
- Dependencies reference known keys, do not repeat, do not reference self, and form no cycles.
- `blocking=true` requires a non-empty `blocking_reason`.
- **Process scaffolding (optional per milestone, strongly recommended):** `steps` has 3–7 entries with ascending `order_index`; `checklist` has at least 1 entry; each step carries 0–3 `resources` of an allowed type. Scaffolding is the learner-side "how to do it" — it never replaces `evidence_gate`/`mandatory_submissions` (the acceptance and submission authority).
- **Thinking evidence (optional per milestone):** `thinking_requirement` declares the structured decision-evidence gate: `require_on_process_draft` / `require_on_formal_submit` and a `required_fields` subset of `problem_statement | key_basis`. When required, the matching submission carries a `thinking` object — `problem_statement`, `key_basis`, optional `alternatives[]` (`{title, why_not}`). This is the short **decision layer** ("why this, what was dropped"); it complements the narrative reflection (`ai_interaction_log_brief` + `participant_analysis_reflection`) already mandatory above, never replaces it.

## Assessment Bundle

```json
{
  "capability_matrix": {
    "dimensions": [
      {
        "dimension_key": "evidence_reasoning",
        "name": "Evidence reasoning",
        "observable_behaviors": ["Separates observation, interpretation, and hypothesis"],
        "required_evidence": ["Redacted sample", "Coding table"],
        "milestone_keys": ["collect_evidence", "diagnose_bias"],
        "minimum_level": "competent",
        "levels": [
          {"level": 1, "label": "未达标", "indicator": "Observation and interpretation are mixed"},
          {"level": 2, "label": "发展中", "indicator": "Evidence exists but traceability is partial"},
          {"level": 3, "label": "胜任", "indicator": "Evidence supports a traceable distinction"},
          {"level": 4, "label": "优秀", "indicator": "Multiple hypotheses and limitations compared"}
        ],
        "agent_indicators": ["Does the artifact separate observation from interpretation?", "Is each claim cited to evidence?"]
      }
    ],
    "final_synthesis_rules": ["The final artifact cites evidence from all blocking milestones"]
  },
  "milestone_templates": [
    {
      "milestone_key": "collect_evidence",
      "evidence_gate": {
        "required_items": [
          "Accessible artifact",
          "AI interaction log/brief",
          "Participant analysis/reflection"
        ],
        "format_rules": ["Use Markdown"],
        "access_rules": [],
        "privacy_rules": ["Redact personal information"]
      },
      "dimensions": [
        {
          "dimension_key": "evidence_reasoning",
          "stage_indicators": {
            "not_demonstrated": "No usable evidence",
            "developing": "Evidence exists but observation and interpretation are mixed",
            "competent": "Evidence supports a traceable distinction",
            "excellent": "Multiple hypotheses and evidence limitations are compared"
          },
          "evidence_prompts": ["Quote exact evidence from the artifact"]
        }
      ],
      "artifact_quality_criteria": ["Evidence is traceable to the conclusion"],
      "core_comment_prompt": "State the strongest demonstrated capability and its material limitation; when thinking_requirement is set, also judge the decision evidence (authenticity, alignment with the artifact, concreteness of abandoned directions)",
      "revision_prompt": "Give the next concrete revision action"
    }
  ]
}
```

Validation:

- Capability dimension keys are unique.
- Every dimension has observable behavior, required evidence, milestone mappings, and a minimum level.
- Every project milestone has exactly one template; no unknown milestone keys exist.
- Template dimension keys exist in the matrix.
- Every matrix dimension appears in at least one milestone template.
- Each evidence gate has at least one required item; every evidence gate must require the **AI interaction log/brief** and the participant's **analysis/reflection** alongside the artifact.
- Each assessment dimension has all four non-empty level indicators and at least one evidence prompt.
- Dimension indicators are grounded in combined evidence: at least two of restating in own words, correcting errors, variant questions, implementation, material reorganization, or project application (see `references/mastery-rubric.md`).
- Each template has artifact quality criteria, a core comment prompt, and a revision prompt.
- Reject extra `weight`, total-score, or average-score fields unless the mentor explicitly enables a separate numeric reporting mode. Numeric reporting must not determine badge issuance automatically.
- **Thinking-evidence dimension (when `thinking_requirement` is set on the milestone):** the template MUST include a `decision_quality`-style dimension whose level indicators and `evidence_prompts` judge the structured thinking layer — `problem_statement` (specific, bound to this delivery), `key_basis` (real basis: feedback/constraint/principle/case, not slogans), `alternatives` (concrete abandoned directions with reasons). AI pre-scoring and the mentor review both score it; the core comment must address it (authenticity, alignment with the artifact), so the platform can tell "did the work" from "thought about it".

## Learning Dependency

```json
{
  "dependency_key": "conversation_coding_method",
  "capability_gap": "Cannot reliably separate observation from interpretation",
  "milestone_keys": ["diagnose_bias"],
  "application_evidence": "The coding table separates facts, interpretations, and hypotheses",
  "content_priority": "required",
  "chapter_refs": []
}
```

Allowed priorities: `required`, `recommended`, `optional`.

## Source Coverage Decision

```json
{
  "source_id": "source-id",
  "source_fragment": "section:3",
  "classification": "method",
  "decision": "use",
  "target_refs": ["milestone:diagnose_bias"],
  "rationale": "Directly supports the diagnostic artifact",
  "requires_explicit_confirmation": false,
  "status": "confirmed"
}
```

Allowed decisions: `use`, `adapt`, `omit`, `supplement`.

## Readiness Report

```json
{
  "ready": false,
  "hard_blockers": [
    {
      "code": "ai_log_missing",
      "target_ref": "milestone:diagnose_bias",
      "message": "The milestone submission has no AI interaction log/brief"
    },
    {
      "code": "reflection_missing",
      "target_ref": "milestone:diagnose_bias",
      "message": "The milestone submission has no participant analysis/reflection"
    }
  ],
  "quality_warnings": [],
  "overrides": [],
  "revision_no": 7
}
```

Never allow an override for a hard blocker. A warning override requires actor, timestamp, and reason.

Readiness hard-blocker codes include: `contract_incomplete`, `artifact_missing`, `ai_log_missing`, `reflection_missing`, `dependency_invalid`, `assessment_missing`, `evidence_unmapped`, and unresolved privacy/safety/copyright/authenticity issues.
