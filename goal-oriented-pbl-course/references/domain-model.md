# Domain Model And Guardrails

Use these terms consistently.

## Canonical Terms

**Course**
: A bounded capability practice built around one core project. It is not primarily a content catalog.

**Mentor / Course Navigator**
: A role inside a course. The platform should not require a permanent global mentor identity.

**Participant**
: A role inside a course. Each participant normally owns an independent project instance.

**Project Contract**
: The confirmed upstream agreement describing the real scenario, participant, capability claim, final deliverable, success evidence, boundaries, and entry baseline.

**Capability Claim**
: A transferable ability the completed project is expected to demonstrate. The final deliverable is its evidence carrier, not the capability itself.

**Mastery**
: Demonstrated capability judged by combined evidence — at least two of: restating in own words, correcting errors, variant questions, implementation, material reorganization, or application to the participant's own project. Knowing or following along is not mastery; stable mastery requires independently modifying, designing, and transferring (see `references/mastery-rubric.md`). In the AI-assisted context, mastery includes reviewing and fixing AI output, not only generating it.

**Project Path**
: A dependency-aware sequence of milestones that builds the final deliverable, validates hypotheses, or reduces risk.

**Milestone**
: A project checkpoint that must produce a concrete artifact. A lesson, reading, discussion, or attendance event is not a milestone by itself.

**Artifact**
: A submit-able, inspect-able output created at a milestone. Every milestone submission bundles the artifact with two mandatory evidence items: an **AI interaction log/brief** and the participant's own **analysis/reflection**.

**AI Interaction Log / Brief**
: The mandatory record of the participant's AI tool usage at a milestone: the prompts used, conversation summaries, and references to generated material that fed the artifact.

**Analysis / Reflection**
: The participant's own written analysis or reflection at a milestone: what the AI contributed, what they judged and changed, what they learned, their **self-calibration** (expected vs. delivered level), and any **anti-patterns** they caught in their own or the AI's work.

**Self-Calibration**
: The participant's prediction of their own capability level for a milestone, compared against the mentor's actual assessment. It is part of the mandatory analysis/reflection and trains accurate self-assessment.

**Anti-Pattern**
: A commonly chosen wrong practice that looks right. Feedback names anti-patterns alongside correct practice; recognizing them is part of mastery.

**AI Tool Usage Guidance**
: The mentor's teaching of how to use AI tools well for the project — choosing tools, decomposing work into prompts, reviewing and overriding AI output, and iterating. It is a required lens of milestone feedback alongside project/industry experience.

**Blocking Coordinate**
: A milestone whose failure invalidates or materially blocks downstream project work. It requires an explicit reason.

**Evidence Gate**
: Binary submission sufficiency: required items, access, format, privacy, and similar prerequisites. It answers whether evaluation can begin.

**Quality Evaluation**
: Evidence-based judgment of capability and artifact quality. It produces levels, evidence citations, a core comment, and revision advice.

**Capability Evidence Matrix**
: Course-level mapping from capability dimensions to observable behaviors, required evidence, and milestone artifacts.

**Milestone Assessment Template**
: The independent evaluation contract for one milestone. It remains aligned to the course-level matrix without sharing a weighted score formula.

**Learning Dependency**
: A knowledge, method, tool, or prior capability gap that must be addressed to complete a milestone artifact.

**Learning Node / Chapter**
: A learning step compiled from confirmed dependencies. It does not automatically contain an exercise or become a milestone.

**Training Module**
: An optional or required exercise requested by the mentor. It may support a project but does not automatically contribute project evidence.

**Spaced Review**
: Optional consolidation cycles (learn-anything style R1/R2/R3/R4 intervals) offered after milestone completion. Review cycles are training modules, never milestones or hard requirements.

**Badge**
: A capability recognition artifact. It replaces completion certificates. It can satisfy a prerequisite when its evidence and level match.

**Equivalent Capability Evidence**
: A work sample or external proof reviewed by the mentor when a participant lacks the expected badge.

**Needs Review**
: A retained downstream artifact whose upstream assumptions changed. It is not deleted or silently regenerated.

## Non-Negotiable Decisions

- One course, one core project.
- Milestones are artifact checkpoints, not chapter exercises.
- Every milestone submission bundles the artifact with an **AI interaction log/brief** and the participant's own **analysis/reflection**; a missing item fails the evidence gate.
- Mentor feedback evaluates both **project/industry experience** and **AI tool usage guidance**; neither lens may be skipped.
- Feedback names **anti-patterns** alongside correct practice, and each analysis/reflection includes the participant's **self-calibration** against the mentor's assessment.
- Every milestone has its own assessment template.
- Course-level capability evidence constrains milestone evaluation direction.
- Evidence gates and quality evaluation remain separate.
- Default evaluation has no total score, average, or weighting requirement.
- The mentor has final design authority, subject to hard safety and evaluability gates.
- AI output is a versioned draft until human confirmation.
- Prerequisites support badge passage and equivalent evidence review.
- Collaborative crews and capability-seat matching belong to the future Jump Gate scope, not the base MVP.

## Source Status

Use these statuses for project-contract fields:

- `confirmed`: directly confirmed by the mentor.
- `inferred`: extracted from sources or inferred by AI.
- `missing`: absent or empty.
- `conflicted`: incompatible claims remain unresolved.

Use these sources:

- `user_answer`
- `source_material`
- `existing_draft`
- `ai_inference`

Do not upgrade `source_material` or `ai_inference` to `confirmed` without human confirmation.
