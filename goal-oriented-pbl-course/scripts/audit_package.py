#!/usr/bin/env python3
# =============================================================================
#  MindNexus 课程包审计器（goal-oriented-pbl-course 技能的确定性执行臂）
# -----------------------------------------------------------------------------
#  职责：把一个课程包目录（course.json + chapters/ + guides/ + resources/）
#        按三层规则打分，输出可复现的违规清单。
#
#  规则三源（冲突时以源码为准）：
#    1. 平台硬门禁  backend/app/services/course_package_service.py（导入 422）
#                   backend/app/services/course_publication_service.py（发布 422）
#                   backend/app/routers/courses.py:705（rubric 权重和）
#    2. 契约文档    .trellis/spec/backend/course-package-import-contracts.md
#                   .trellis/spec/backend/pbl-process-scaffolding-contracts.md
#    3. 作者级要求  SKILL.md 规则 3/13/14/15/16 + references/platform-course-json.md §3
#
#  分级：ERROR = 导入/发布失败或规则 16 判定为"模板级填充"，必须修；
#        WARN  = 内容深度不足，人工判断。
#
#  用法：python3 audit_package.py <pkg-dir> [<pkg-dir> ...]
#        python3 audit_package.py --all   # 扫 content/course-packages/*
#  退出码：0 全部通过；1 存在 ERROR；2 用法/IO 错误。
# =============================================================================

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
#  常量：契约里的枚举与正则
# ---------------------------------------------------------------------------
SLUG = re.compile(r"^[a-z][a-z0-9_]*$")
PRACTICE_KINDS = {"experience", "training", "evidence"}
SUBMISSION_MODES = {"none", "reflection", "text", "link", "attachment"}
RESOURCE_TYPES = {"template", "example", "short_doc", "video_link", "external", "package_file"}
THINKING_FIELDS = {"problem_statement", "key_basis"}
EPS = 0.011  # 浮点权重容差（0.25*4 / 0.3+0.4+0.3 均需落在 1.0±EPS）
MIN_CHAPTER_CHARS = 600  # 作者级章节正文下限（WARN）


class Report:
    """违规收集器：ERROR/WARN 分桶，按包聚合。"""

    def __init__(self, name: str) -> None:
        self.name = name
        self.errors: list[str] = []
        self.warns: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warns.append(msg)

    def dump(self) -> None:
        print(f"\n=== {self.name} ===")
        for m in self.errors:
            print(f"  ERROR  {m}")
        for m in self.warns:
            print(f"  WARN   {m}")
        if not self.errors and not self.warns:
            print("  OK")
        print(f"  -> {len(self.errors)} error(s), {len(self.warns)} warning(s)")


def _load(pkg: Path) -> tuple[dict, Report] | None:
    """读取 manifest；失败直接返回终局报告。"""
    rep = Report(pkg.name)
    mf = pkg / "course.json"
    if not mf.is_file():
        rep.err("缺少 course.json（manifest）")
        rep.dump()
        return None
    try:
        data = json.loads(mf.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        rep.err(f"course.json 不是有效 JSON: {e}")
        rep.dump()
        return None
    return data, rep


# ---------------------------------------------------------------------------
#  1. 平台绑定数据：课程包是离线内容资产，任何 id 都是污染
# ---------------------------------------------------------------------------
def audit_ids(m: dict, rep: Report) -> None:
    if m.get("id"):
        rep.err("manifest 含平台 id（导入会生成全新课程草稿，须移除 `id`）")
    for i, a in enumerate(m.get("assignments") or []):
        if a.get("id"):
            rep.err(f"assignments[{i}] 含平台 id（须移除）")
    for i, p in enumerate(m.get("practices") or []):
        if p.get("id"):
            rep.err(f"practices[{i}] 含平台 id（须移除）")


# ---------------------------------------------------------------------------
#  2. 章节：包内必须文件化（规则 14/16），且携带 summary + duration_minutes
# ---------------------------------------------------------------------------
def audit_chapters(m: dict, pkg: Path, rep: Report) -> list[str]:
    chapters = m.get("chapters") or []
    if not chapters:
        lessons = m.get("lessons") or []
        rep.err(f"无 chapters（仅 lessons={len(lessons)}）；课程包必须用 chapters[].content_file")
        return []
    titles: list[str] = []
    for i, c in enumerate(chapters):
        tag = f"chapters[{i}] {c.get('title') or '<无标题>'}"
        if not c.get("title"):
            rep.err(f"chapters[{i}] 缺少 title")
        titles.append(c.get("title") or "")
        cf = c.get("content_file")
        if c.get("markdown_content"):
            rep.err(f"{tag}: 内联 markdown_content（包内章节必须外化为 chapters/*.md）")
        if not cf:
            rep.err(f"{tag}: 缺少 content_file")
        else:
            f = pkg / cf
            if not f.is_file():
                rep.err(f"{tag}: content_file 不存在 -> {cf}")
            else:
                body = f.read_text(encoding="utf-8")
                if len(body.strip()) < MIN_CHAPTER_CHARS:
                    rep.warn(f"{tag}: 正文仅 {len(body.strip())} 字符（<{MIN_CHAPTER_CHARS}，疑似占位）")
        if not c.get("summary"):
            rep.err(f"{tag}: 缺少 summary（规则 16）")
        dm = c.get("duration_minutes")
        if not isinstance(dm, int) or dm <= 0:
            rep.err(f"{tag}: duration_minutes 必须为正整数（当前 {dm!r}）")
        if not isinstance(c.get("order_index"), int):
            rep.err(f"{tag}: order_index 必须为整数")
    dup = {t for t in titles if t and titles.count(t) > 1}
    if dup:
        rep.err(f"章节标题重复（练习锚点会歧义）: {sorted(dup)}")
    oi = [c.get("order_index") for c in chapters]
    if oi != sorted(oi):
        rep.err(f"chapters order_index 非升序: {oi}")
    return [t for t in titles if t]


# ---------------------------------------------------------------------------
#  3. 评价维度：语义 key + 完整 levels + 具体 agent_indicators（规则 13/16）
# ---------------------------------------------------------------------------
def audit_dimensions(spec: dict, idx: int, rep: Report) -> None:
    tpl = spec.get("evaluation_template") or {}
    dims = tpl.get("dimensions") or []
    tag = f"milestone[{idx}] {spec.get('milestone_key') or '?'}"
    if not dims:
        rep.err(f"{tag}: evaluation_template.dimensions 为空（发布门禁 422）")
        return
    if not tpl.get("core_comment_prompt"):
        rep.err(f"{tag}: 缺少 core_comment_prompt（发布门禁 422）")
    wsum = sum(d.get("weight") or 0 for d in dims if isinstance(d.get("weight"), (int, float)))
    if abs(wsum - 1.0) > EPS:
        rep.err(f"{tag}: dimensions weight 和={round(wsum, 4)}，须为 1.0")
    keys = [d.get("key") for d in dims]
    for d in dims:
        k = d.get("key")
        dtag = f"{tag} dim[{k}]"
        if not k or not d.get("title"):
            rep.err(f"{tag}: 维度缺少 key/title")
            continue
        if not SLUG.match(k):
            rep.err(f"{dtag}: key 不符合 ^[a-z][a-z0-9_]*$（须为语义英文 slug）")
        if keys.count(k) > 1:
            rep.err(f"{dtag}: key 重复")
        lv = d.get("levels")
        if lv is not None:
            nums = sorted(x.get("level") for x in lv if isinstance(x, dict))
            if nums != [1, 2, 3, 4]:
                rep.err(f"{dtag}: levels 必须恰为 1-4 完整集（当前 {nums}）")
            for x in lv or []:
                if not isinstance(x, dict) or not x.get("label") or not x.get("indicator"):
                    rep.err(f"{dtag}: levels 每项需含 label/indicator")
                    break
        ai = d.get("agent_indicators")
        if not isinstance(ai, list) or not ai or not all(isinstance(x, str) and x.strip() for x in ai):
            rep.err(f"{dtag}: agent_indicators 需为非空字符串数组")
            continue
        for s in ai:
            if s.endswith("是否达成") or s.startswith(("未满足：", "部分满足：", "完整满足：", "超出预期：")):
                rep.err(f"{dtag}: agent_indicator 是模板残渣 -> 「{s}」（须为可检查的具体问题）")
    # 思考证据契约：配了 thinking_requirement 就必须能评"想没想"
    tr = spec.get("thinking_requirement") or {}
    if tr.get("require_on_formal_submit") or tr.get("require_on_process_draft"):
        if "decision_quality" not in keys:
            rep.err(f"{tag}: 配置了 thinking_requirement 却缺 decision_quality 维度")
        prompt = tpl.get("core_comment_prompt") or ""
        if "思考" not in prompt:
            rep.err(f"{tag}: core_comment_prompt 未要求评价思考层")
        bad = set(tr.get("required_fields") or []) - THINKING_FIELDS
        if bad:
            rep.err(f"{tag}: thinking_requirement.required_fields 越界 {sorted(bad)}")


# ---------------------------------------------------------------------------
#  4. 过程脚手架：steps/checklist/resources（契约 §2 + 规则 16）
# ---------------------------------------------------------------------------
def audit_scaffold(spec: dict, idx: int, pkg: Path, rep: Report) -> None:
    tag = f"milestone[{idx}] {spec.get('milestone_key') or '?'}"
    steps = spec.get("steps") or []
    if not (3 <= len(steps) <= 7):
        rep.err(f"{tag}: steps 数量={len(steps)}，须 3-7")
    oi = [s.get("order_index") for s in steps]
    if oi != sorted(oi) or oi != list(range(1, len(steps) + 1)):
        rep.err(f"{tag}: steps order_index 须为 1..n 升序（当前 {oi}）")
    for s in steps:
        stag = f"{tag} step{s.get('order_index')}"
        desc = (s.get("description") or "").strip()
        if len(desc) < 12:
            rep.err(f"{stag} 「{s.get('title')}」: description 缺失或空泛（{len(desc)} 字符）")
        elif desc == (s.get("title") or "").strip():
            rep.err(f"{stag}: description 只是复述 title")
        em = s.get("estimated_minutes")
        if not isinstance(em, int) or em <= 0:
            rep.err(f"{stag}: estimated_minutes 须为正整数（当前 {em!r}）")
        res = s.get("resources") or []
        if len(res) > 3:
            rep.err(f"{stag}: resources={len(res)}，上限 3")
        for r in res:
            if r.get("type") not in RESOURCE_TYPES:
                rep.err(f"{stag}: resource type 非法 {r.get('type')!r}")
            if not r.get("title"):
                rep.err(f"{stag}: resource 缺 title")
            if r.get("type") == "package_file":
                rel = r.get("file")
                if not rel or not (pkg / rel).is_file():
                    rep.err(f"{stag}: package_file 缺失 -> {rel}")
            elif r.get("type") == "external" and not r.get("url"):
                rep.err(f"{stag}: external resource 缺 url")
    cl = spec.get("checklist") or []
    if not cl:
        rep.err(f"{tag}: checklist 为空（至少 1 项自检）")
    joined = " ".join(x.get("text", "") for x in cl if isinstance(x, dict))
    if "AI" not in joined:
        rep.err(f"{tag}: checklist 未含 AI 互动记录项（规则 3 硬门）")
    if "反思" not in joined:
        rep.err(f"{tag}: checklist 未含个人分析/反思项（规则 3 硬门）")
    if not spec.get("guide_file"):
        rep.err(f"{tag}: 缺少 guide_file")
    else:
        gf = pkg / spec["guide_file"]
        if not gf.is_file():
            rep.err(f"{tag}: guide_file 不存在 -> {spec['guide_file']}")
        elif len(gf.read_text(encoding='utf-8').strip()) < 400:
            rep.warn(f"{tag}: guide_file 仅 {len(gf.read_text(encoding='utf-8').strip())} 字符")


# ---------------------------------------------------------------------------
#  5. 项目/练习：一课一毕业项目 + 练习是课堂练习（规则 15）
# ---------------------------------------------------------------------------
def audit_assignment(m: dict, pkg: Path, rep: Report) -> list[str]:
    asg = m.get("assignments") or []
    if len(asg) != 1:
        rep.err(f"assignments 数量={len(asg)}，发布门禁要求恰为 1 个核心项目")
        return []
    a = asg[0]
    specs = a.get("milestone_specs") or []
    if len(specs) < 2:
        rep.err(f"里程碑数量={len(specs)}，须 ≥2")
    keys = [s.get("milestone_key") for s in specs]
    for i, s in enumerate(specs):
        k = s.get("milestone_key")
        if not k:
            rep.err(f"milestone[{i}] 缺少 milestone_key")
        elif not SLUG.match(k):
            rep.err(f"milestone[{i}] milestone_key 「{k}」 不符合 ^[a-z][a-z0-9_]*$")
        elif re.match(r"^m[0-9a-f]{4,}$", k):
            rep.err(f"milestone[{i}] milestone_key 「{k}」 是十六进制残渣，须语义化")
        if keys.count(k) > 1:
            rep.err(f"milestone[{i}] milestone_key 重复: {k}")
        if not s.get("title") or not s.get("description"):
            rep.err(f"milestone[{i}] {k}: 缺少 title/description")
        if not (s.get("rules") or []):
            rep.err(f"milestone[{i}] {k}: rules 为空（至少 1 条验收规则）")
        audit_dimensions(s, i, rep)
        audit_scaffold(s, i, pkg, rep)
    rub = a.get("rubric") or []
    if len(rub) < 3:
        rep.err(f"rubric 条目={len(rub)}，须 ≥3")
    rw = sum(r.get("weight") or 0 for r in rub)
    if abs(rw - 1.0) > EPS:
        rep.err(f"rubric weight 和={round(rw, 4)}，须为 1.0（平台 422）")
    sr = a.get("submission_requirements") or []
    if not sr:
        rep.err("submission_requirements 为空")
    for r in sr:
        if r.get("required") is not True:
            rep.err(f"submission_requirements「{r.get('title')}」required 须为 true")
    srt = " ".join(r.get("title", "") for r in sr)
    if "AI" not in srt:
        rep.err("submission_requirements 未含 AI 互动记录（规则 3 硬门）")
    if "反思" not in srt:
        rep.err("submission_requirements 未含个人分析/反思（规则 3 硬门）")
    return [k for k in keys if k]


def audit_practices(m: dict, chapter_titles: list[str], milestone_keys: list[str], rep: Report) -> None:
    prs = m.get("practices") or []
    if not prs:
        rep.warn("无 practices（规则 15：标准课程应含课堂练习）")
        return
    for i, p in enumerate(prs):
        tag = f"practices[{i}] {p.get('title') or '<无标题>'}"
        if p.get("kind") not in PRACTICE_KINDS:
            rep.err(f"{tag}: kind 非法 {p.get('kind')!r}")
        if p.get("submission_mode") not in SUBMISSION_MODES:
            rep.err(f"{tag}: submission_mode 非法 {p.get('submission_mode')!r}")
        ct = p.get("chapter_title")
        if not ct:
            rep.err(f"{tag}: 缺少 chapter_title 锚点")
        elif ct not in chapter_titles:
            rep.err(f"{tag}: chapter_title「{ct}」未匹配任何章节标题")
        ck = p.get("contributes_to_milestone_key")
        if ck and ck not in milestone_keys:
            rep.err(f"{tag}: contributes_to_milestone_key「{ck}」不是真实 milestone_key")
        if not (p.get("instruction") or "").strip():
            rep.err(f"{tag}: 缺少 instruction")
        if p.get("kind") == "evidence" and not p.get("expected_artifact"):
            rep.warn(f"{tag}: evidence 型练习建议给出 expected_artifact")
        fb = p.get("ai_feedback_template")
        if fb is not None and not (isinstance(fb, dict) and fb.get("focus")):
            rep.err(f"{tag}: ai_feedback_template 须为 {{focus: ...}} 或 null")


# ---------------------------------------------------------------------------
#  5.5 可选发布信息：tags / preparation_note / sessions（2026-10 导入扩展）
# ---------------------------------------------------------------------------
DELIVERY_MODES = {"online", "offline"}
MAX_SESSION_DATES = 400


def audit_extras(m: dict, rep: Report) -> None:
    tags = m.get("tags")
    if tags is not None:
        if not isinstance(tags, list) or not all(isinstance(t, str) and t.strip() for t in tags):
            rep.err("tags 须为非空字符串数组")
    note = m.get("preparation_note")
    if note is not None and (not isinstance(note, str) or len(note) > 500):
        rep.err(f"preparation_note 须为 ≤500 字符的字符串（当前 {len(note or '')} 字符）")
    if m.get("category") is not None:
        rep.err("manifest 含 category——该字段已废弃（列已删除），请改用 tags")
    for i, s in enumerate(m.get("sessions") or []):
        tag = f"sessions[{i}]"
        if s.get("id"):
            rep.warn(f"{tag}: 携带 id 会被忽略（平台生成期次 id）")
        if not s.get("start_date") or not s.get("end_date"):
            rep.err(f"{tag}: 缺少 start_date/end_date")
        if s.get("delivery_mode") not in (None, "online", "offline"):
            rep.err(f"{tag}: delivery_mode 非法 {s.get('delivery_mode')!r}（仅 online/offline）")
        dates = s.get("session_dates") or []
        if len(dates) > MAX_SESSION_DATES:
            rep.err(f"{tag}: session_dates 超上限 {MAX_SESSION_DATES}")
        if dates and not (s.get("schedule_start_time") and s.get("schedule_end_time")):
            rep.err(f"{tag}: 带了 session_dates 必须同时给 schedule_start_time/schedule_end_time")
        if (s.get("meeting_url") and s.get("delivery_mode") != "online") or (
            s.get("location") and s.get("delivery_mode") != "offline"
        ):
            rep.warn(f"{tag}: meeting_url/location 与 delivery_mode 不匹配")


# ---------------------------------------------------------------------------
#  入口
# ---------------------------------------------------------------------------
def audit(pkg: Path) -> Report:
    loaded = _load(pkg)
    if loaded is None:
        return Report(pkg.name)
    m, rep = loaded
    if not m.get("title"):
        rep.err("manifest 缺少 title")
    audit_ids(m, rep)
    titles = audit_chapters(m, pkg, rep)
    keys = audit_assignment(m, pkg, rep)
    audit_practices(m, titles, keys, rep)
    audit_extras(m, rep)
    rep.dump()
    return rep


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args == ["--all"]:
        root = Path(__file__).resolve().parents[3] / "content" / "course-packages"
        pkgs = sorted(p for p in root.iterdir() if (p / "course.json").is_file())
    else:
        pkgs = [Path(a) for a in args]
    reps = [audit(p) for p in pkgs]
    errs = sum(len(r.errors) for r in reps)
    warns = sum(len(r.warns) for r in reps)
    print(f"\n总计：{len(reps)} 个课程包，{errs} error(s)，{warns} warning(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
