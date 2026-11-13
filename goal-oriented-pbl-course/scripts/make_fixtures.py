#!/usr/bin/env python3
"""生成 audit_package.py 的最小回归 fixture。

每个 fixture 都是一个能单独跑通审计器的最小课程包，只针对**一条**判据。
基线包（base）本身应当 0 error / 0 warning；各 fixture 在它之上只注入一处缺陷。

用法（通常不需要手工跑，tests/run_tests.sh 会调用）：
    python3 scripts/make_fixtures.py
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"

CHAPTER_BODY = (
    "# 第 1 课：从素材到方向\n\n"
    "这一课先不碰 AI，只做一件事：把你手上的素材摊开看清。\n\n"
    "## 1. 先看素材\n\n"
    "打开课程包里的示例文章，逐段读一遍，标出你认为最有说服力的三处。"
    "读的时候不要急着下结论，也不要先问 AI——这一遍是给你自己的。\n\n"
    "## 2. 写下你的判断\n\n"
    "读完之后，用一句话写下你的判断：这份素材真正在讲什么？"
    "这句话不必漂亮，但必须是**你自己**的话，不能是抄来的形容词。\n\n"
    "## 3. 与 AI 对照\n\n"
    "现在把同样的问题交给 AI，看它给出的方向和你差在哪。"
    "把它说得对的地方留下，说得空的地方划掉，这个删改过程本身就是你的判断依据。\n\n"
    "## 本课产出\n\n"
    "一句你自己的方向判断，以及你从 AI 输出里删掉了什么、为什么删。\n\n"
    "## 为什么先自己写、再问 AI\n\n"
    "顺序反了，你就没有自己的判断可以对照。先写一遍的好处不是让你写得比 AI 好，"
    "而是让你在读到 AI 的答案时，能立刻看出哪里和你不一样。"
    "那个不一样的地方，就是这一课真正要练的东西：你的判断从哪里来。\n\n"
    "## 判断依据怎么写\n\n"
    "依据不是态度词。写「因为这段描述具体讲到了业主每天怎么用这个空间」是依据；"
    "写「因为我觉得这样更好」不是。依据要能让另一个人拿着它去素材里核对，"
    "核对得到，才算成立。\n\n"
    "## 常见误区\n\n"
    "第一个误区是把风格名词当判断，比如只说「现代简约」却不解释它在这个项目里意味着什么。"
    "第二个误区是把 AI 的结论当自己的结论，交上去的东西自己都讲不清依据。"
    "第三个误区是追求完整而堆砌素材用不到的内容——宁可少，但每一句都要有落点。\n"
)

GUIDE_BODY = (
    "# 里程碑指南\n\n"
    "这个里程碑要你把第一课的判断落成一个可以提交的结果。\n\n"
    "## 你要交什么\n\n"
    "一份方向说明，讲清你选了什么、凭什么这么选。判断依据要能指回你在第一课标出的三处素材。\n\n"
    "## 自检\n\n"
    "交之前问自己三个问题：方向是不是我自己的话？依据能不能指回原文？"
    "AI 给的东西我删掉了哪些、为什么删？\n\n"
    "## 如果被卡住\n\n"
    "回到第一课的素材重读一遍，通常卡住是因为素材还没读透，不是方向不够新。"
    "如果重读之后仍然定不下来，把你犹豫的两个方向都写下来，各自列出支持它的"
    "三条素材依据，然后看哪一边的依据更具体。依据更具体的那一边通常就是答案，"
    "因为能被具体指认的东西，才经得起后面的推敲。\n\n"
    "## 交之前最后一遍\n\n"
    "确认你的方向说明里，每一句判断都能在素材里找到落点。"
    "找不到落点的那一句，要么补依据，要么删掉——不要为了显得完整而留下它。\n\n"
    "## 关于 AI 的产出\n\n"
    "AI 给你的方向往往听起来很顺，这种顺滑本身不是证据。判断它有没有用的标准只有一个："
    "它说的东西能不能落到你的素材上。落不到素材上的漂亮话，一律删掉；"
    "能落到素材上但你表达不出来的，留下它的意思，换成你自己的说法。"
    "这个过程慢，但它决定了最后那份东西到底是不是你的。\n"
)


def _base_manifest() -> dict:
    """一个满足全部硬门禁的最小包：2 章 + 1 项目 2 里程碑 + 2 练习。"""
    return {
        "title": "审计器回归样本",
        "description": "仅用于 audit_package.py 回归测试的最小课程包。",
        "status": "draft",
        "pricing_type": "free",
        "chapters": [
            {
                "title": "第 1 课：从素材到方向",
                "chapter_type": "markdown",
                "content_file": "chapters/01-direction.md",
                "summary": "把素材摊开、写下自己的判断，再与 AI 的结论对照，形成可追溯的方向依据。",
                "duration_minutes": 30,
                "order_index": 0,
            },
            {
                "title": "第 2 课：把方向做成结果",
                "chapter_type": "markdown",
                "content_file": "chapters/02-result.md",
                "summary": "把第一课的方向落成可提交的结果，并说明你在过程中删改了什么。",
                "duration_minutes": 30,
                "order_index": 1,
            },
        ],
        "assignments": [
            {
                "title": "方向与结果",
                "description": "选一个方向，做出结果，并说清凭什么这么选。",
                "input_materials": ["示例文章", "示例图片"],
                "milestone_specs": [
                    _milestone(
                        key="direction_pick",
                        title="确定方向",
                        chapter="第 1 课：从素材到方向",
                        guide="guides/direction_pick.md",
                        field_key="direction_statement",
                        field_title="方向说明",
                        field_type="markdown",
                        step_question="你为什么选这个方向？",
                        maps_to="direction_statement",
                    ),
                    _milestone(
                        key="result_delivery",
                        title="交付结果",
                        chapter="第 2 课：把方向做成结果",
                        guide="guides/result_delivery.md",
                        field_key="result_notes",
                        field_title="结果说明",
                        field_type="text",
                        step_question="你的结果说明了什么？",
                        maps_to="result_notes",
                    ),
                ],
                "submission_requirements": [
                    {"title": "AI 互动记录", "required": True},
                    {"title": "个人分析 / 反思", "required": True},
                ],
                "rubric": [
                    {"criterion": "方向清晰", "weight": 0.4},
                    {"criterion": "依据可追溯", "weight": 0.35},
                    {"criterion": "结果完整", "weight": 0.25},
                ],
            }
        ],
        "practices": [
            {
                "title": "练习 1：素材通读",
                "kind": "experience",
                "chapter_title": "第 1 课：从素材到方向",
                "submission_mode": "none",
                "instruction": "通读示例素材，标出三处最有说服力的地方，并说明为什么是这三处。",
                "description": "通读示例素材，标出三处最有说服力的地方。",
            },
            {
                "title": "练习 2：对照 AI",
                "kind": "training",
                "chapter_title": "第 1 课：从素材到方向",
                "submission_mode": "reflection",
                "instruction": "把同样的问题交给 AI，记下它说得空、说得假的地方，写成一段反思。",
                "description": "把同样问题交给 AI，记下它说得空的地方。",
            },
        ],
        "tags": ["回归样本"],
    }


def _milestone(
    *, key: str, title: str, chapter: str, guide: str,
    field_key: str, field_title: str, field_type: str,
    step_question: str, maps_to: str | None,
) -> dict:
    return {
        "milestone_key": key,
        "related_chapter_titles": [chapter],
        "title": title,
        "description": f"{title}：把这一课学到的东西落成一个可提交的结果。",
        "rules": [
            f"{title}的成果必须能指回课程素材，不得编造。",
            "提交时必须附 AI 互动记录与个人分析/反思。",
        ],
        "steps": [
            {
                "order_index": 1,
                "title": "读素材，写下第一判断",
                "description": "打开示例素材通读一遍，先自己写下判断，不查资料也不问 AI。",
                "estimated_minutes": 15,
                "resources": [{"type": "example", "title": "示例素材"}],
                "checklist": [
                    {"text": "已通读素材并标出三处依据", "required": True},
                    {"text": "已用自己的话写下判断", "required": True},
                ],
            },
            {
                "order_index": 2,
                "title": "与 AI 对照后定稿",
                "description": "把同样问题交给 AI，留下说得对的，删掉说得空的，形成最终版本。",
                "estimated_minutes": 15,
                "resources": [{"type": "example", "title": "AI 输出示例"}],
                "checklist": [
                    {"text": "已记录 AI 互动要点", "required": True},
                    {"text": "已写出删改理由", "required": True},
                ],
            },
            {
                "order_index": 3,
                "title": "提交前自检",
                "description": "按里程碑指南逐条自查，确认依据能指回素材、AI 记录与反思齐备。",
                "estimated_minutes": 5,
                "resources": [],
                "checklist": [
                    {"text": "AI 互动记录完整", "required": True},
                    {"text": "个人分析/反思已写", "required": True},
                ],
            },
        ],
        "checklist": [
            {"text": "成果能指回课程素材，没有编造", "required": True},
            {"text": "附上 AI 互动记录", "required": True},
            {"text": "附上个人分析/反思", "required": True},
        ],
        "thinking_requirement": {
            "require_on_formal_submit": False,
            "require_on_process_draft": False,
            "required_fields": [],
        },
        "guide_file": guide,
        "submission_fields": [
            {
                "key": field_key,
                "title": field_title,
                "type": field_type,
                "required": True,
                "guidance": f"{field_title}：说清你为什么这么做，依据要能指回课程素材。",
            }
        ],
        "evaluation_template": {
            "dimensions": [
                {
                    "key": "grounding",
                    "title": "依据是否扎根素材",
                    "weight": 0.5,
                    "agent_indicators": [
                        "判断是否能指回素材里的具体段落或图片？",
                        "有没有出现素材里并不存在的说法？",
                    ],
                    "levels": [
                        {"level": 1, "label": "未达标", "indicator": "判断没有依据，全凭感觉。"},
                        {"level": 2, "label": "及格", "indicator": "有依据但指代含糊。"},
                        {"level": 3, "label": "良好", "indicator": "依据能指回具体段落。"},
                        {"level": 4, "label": "优秀", "indicator": "依据清晰且能说明取舍。"},
                    ],
                },
                {
                    "key": "ai_use",
                    "title": "AI 使用是否有判断",
                    "weight": 0.5,
                    "agent_indicators": [
                        "有没有记录 AI 给了什么、自己改了什么？",
                        "删改理由是否具体？",
                    ],
                    "levels": [
                        {"level": 1, "label": "未达标", "indicator": "直接粘贴 AI 输出。"},
                        {"level": 2, "label": "及格", "indicator": "有少量修改但没写理由。"},
                        {"level": 3, "label": "良好", "indicator": "有删改并写了理由。"},
                        {"level": 4, "label": "优秀", "indicator": "能说明为什么这样改。"},
                    ],
                },
            ],
            "core_comment_prompt": "请评价学员的判断是否扎根素材，以及 AI 使用是否带有自己的取舍；同时评价思考层是否交代了为什么这么选。",
        },
        "interaction": {
            "schema_version": 1,
            "enabled": True,
            "default_mode": "full",
            "steps": [
                {
                    "key": "pick_angle",
                    "question": step_question,
                    "allow_other": True,
                    "ai_guided": False,
                    "maps_to": maps_to,
                },
                {
                    "key": "confirm_final",
                    "question": "定稿前确认：依据能指回素材吗？",
                    "options": [
                        {"id": "yes", "label": "能，已逐条核对"},
                        {"id": "no", "label": "还不能，我要回去补"},
                    ],
                    "allow_other": False,
                    "ai_guided": False,
                },
            ],
            "fallback": {
                "text": "AI 不可用时，按上面两步手工完成：先写下判断并标出依据，再逐条核对后定稿。"
            },
        },
    }


def _write(root: Path, name: str, mutate=None) -> None:
    """把 base 包写到 root/name，可选注入一处缺陷。"""
    dst = root / name
    if dst.exists():
        shutil.rmtree(dst)
    (dst / "chapters").mkdir(parents=True)
    (dst / "guides").mkdir(parents=True)

    (dst / "chapters" / "01-direction.md").write_text(CHAPTER_BODY, encoding="utf-8")
    (dst / "chapters" / "02-result.md").write_text(CHAPTER_BODY, encoding="utf-8")
    (dst / "guides" / "direction_pick.md").write_text(GUIDE_BODY, encoding="utf-8")
    (dst / "guides" / "result_delivery.md").write_text(GUIDE_BODY, encoding="utf-8")

    manifest = _base_manifest()
    if mutate is not None:
        mutate(manifest)
    (dst / "course.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  {name}")


# ---------------------------------------------------------------------------
#  各 fixture 的缺陷注入
# ---------------------------------------------------------------------------
def _dup_mapping(m: dict) -> None:
    """两个 step 映射同一字段 → WARN「多个 step 映射到同一字段」。"""
    steps = m["assignments"][0]["milestone_specs"][0]["interaction"]["steps"]
    steps[1]["maps_to"] = "direction_statement"


def _uncovered_field(m: dict) -> None:
    """可预填类型的字段没有被任何 step 覆盖 → ERROR。"""
    spec = m["assignments"][0]["milestone_specs"][0]
    spec["submission_fields"].append(
        {
            "key": "extra_note",
            "title": "补充说明",
            "type": "text",
            "required": True,
            "guidance": "补充说明你的判断依据。",
        }
    )


def _unprefillable_field(m: dict) -> None:
    """不可预填类型未被覆盖 → WARN（不是 ERROR）。"""
    spec = m["assignments"][0]["milestone_specs"][0]
    spec["submission_fields"].append(
        {
            "key": "asset_upload",
            "title": "上传成品图",
            "type": "asset",
            "required": True,
            "guidance": "上传最终成品图。",
        }
    )


def _prefill_never_no_reason(m: dict) -> None:
    """prefill: never 但缺 prefill_reason → ERROR。"""
    spec = m["assignments"][0]["milestone_specs"][0]
    spec["submission_fields"].append(
        {
            "key": "hand_written",
            "title": "手写栏",
            "type": "text",
            "required": True,
            "prefill": "never",
            "guidance": "这一栏必须手写。",
        }
    )


def _thinking_not_taught(m: dict) -> None:
    """开启决策证据但全包没教那两栏 → WARN。"""
    spec = m["assignments"][0]["milestone_specs"][0]
    spec["thinking_requirement"] = {
        "require_on_formal_submit": True,
        "require_on_process_draft": False,
        "required_fields": ["problem_statement", "key_basis"],
    }
    # 提供 decision_quality 维度，避免先撞 ERROR（本 fixture 只测"没教"这条 WARN）
    spec["evaluation_template"]["dimensions"].append(
        {
            "key": "decision_quality",
            "title": "决策证据质量",
            "weight": 0.0,
            "agent_indicators": ["问题陈述是否讲清了要解决什么？"],
            "levels": [
                {"level": 1, "label": "未达标", "indicator": "没有决策证据。"},
                {"level": 2, "label": "及格", "indicator": "证据不完整。"},
                {"level": 3, "label": "良好", "indicator": "证据完整。"},
                {"level": 4, "label": "优秀", "indicator": "证据清晰且说明取舍。"},
            ],
        }
    )


def _make_zip_bad(path: Path) -> None:
    """zip 多包一层同名顶层目录 → ERROR（契约要求根部即 course.json）。"""
    import zipfile

    src = FIXTURES / "base_clean"
    if not src.is_dir():
        return
    if path.exists():
        path.unlink()
    top = "wrapped"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(src.rglob("*")):
            if f.is_file():
                zf.write(f, f"{top}/{f.relative_to(src).as_posix()}")


def main() -> int:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    print("生成 fixtures：")
    _write(FIXTURES, "base_clean")
    _write(FIXTURES, "dup_mapping", _dup_mapping)
    _write(FIXTURES, "uncovered_field", _uncovered_field)
    _write(FIXTURES, "unprefillable_field", _unprefillable_field)
    _write(FIXTURES, "prefill_never_no_reason", _prefill_never_no_reason)
    _write(FIXTURES, "thinking_not_taught", _thinking_not_taught)
    _make_zip_bad(FIXTURES / "zip_wrapped.zip")
    print("  zip_wrapped.zip")
    print(f"完成，共 7 个 fixture -> {FIXTURES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
