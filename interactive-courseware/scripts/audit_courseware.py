#!/usr/bin/env python3
# =============================================================================
#  MindNexus 交互式课件审计器（interactive-courseware 技能的确定性执行臂）
# -----------------------------------------------------------------------------
#  职责：对课件目录（index.html + styles.css + app.js 三件套）或 zip 做静态
#        沙箱兼容审计，输出可复现的违规清单。规则三源冲突时以源码为准：
#    1. 平台硬门禁  backend/app/services/courseware_service.py（上传 422）
#    2. 契约文档    .trellis/spec/backend/courseware-contracts.md
#    3. 作者级要求  本技能 SKILL.md 规则 1-6
#
#  分级：ERROR = 沙箱内必炸或上传必拒；WARN = 高风险模式，人工判断。
#  用法：python3 audit_courseware.py <deck-dir> [<deck-dir> | deck.zip ...]
#  退出码：0 全部通过；1 存在 ERROR；2 用法/IO 错误。
# =============================================================================
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

MAX_FILES = 20
MAX_BYTES = 8 * 1024 * 1024
REQUIRED = ("index.html",)

# 沙箱必炸：直接触达即 ERROR（注释里提到不算——先剥注释再匹配）
DEADLY = re.compile(
    r"\b(?:localStorage|sessionStorage|indexedDB)\s*[.\[]"
    r"|\bdocument\s*\.\s*cookie\b"
    r"|\bwindow\s*\.\s*(?:top|parent)\b"
    r"|\beval\s*\(|\bnew\s+Function\s*\("
    r"|\bimport\s*\(\s*[\"']"          # 动态 import 在内联后无解析基底
)
# 历史写入：必须同行带 try 包裹特征；裸写即 ERROR
HISTORY = re.compile(r"\bhistory\s*\.\s*(pushState|replaceState)\b")
MODULE_SCRIPT = re.compile(r"<script[^>]+type\s*=\s*[\"']module[\"']", re.I)
EXTERNAL = re.compile(r"https?://[^\s\"'<>)]+", re.I)
CDN_HINT = re.compile(r"https?://(?:unpkg|cdn\.|jsdelivr|googleapis|cdnjs|bootcdn|staticfile)", re.I)
TRAVERSAL = re.compile(r"(?:^|/)\.\.(?:/|$)|^[A-Za-z]:[\\/]|^/", re.M)


class Report:
    def __init__(self, name: str) -> None:
        self.name = name
        self.errors: list[str] = []
        self.warns: list[str] = []

    def err(self, m: str) -> None: self.errors.append(m)
    def warn(self, m: str) -> None: self.warns.append(m)

    def dump(self) -> None:
        print(f"\n=== {self.name} ===")
        for m in self.errors:
            print(f"  ERROR  {m}")
        for m in self.warns:
            print(f"  WARN   {m}")
        if not self.errors and not self.warns:
            print("  OK")
        print(f"  -> {len(self.errors)} error(s), {len(self.warns)} warning(s)")
        return None


def _strip_comments(js: str) -> str:
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    return re.sub(r"//[^\n]*", "", js)


def _collect(paths: dict[str, bytes], rep: Report) -> None:
    """静态检查所有文本成员。"""
    for name in sorted(paths):
        if name.endswith((".html", ".css", ".js", ".svg", ".json", ".txt", ".md")):
            try:
                text = paths[name].decode("utf-8")
            except UnicodeDecodeError:
                rep.err(f"{name}: 非 UTF-8 编码")
                continue
            if name.endswith(".js"):
                code = _strip_comments(text)
            else:
                code = text
            for m in DEADLY.finditer(code):
                frag = code[m.start():m.start() + 40].split("\n")[0]
                rep.err(f"{name}: 沙箱必炸 API -> {frag!r}")
            if name.endswith(".js"):
                for m in HISTORY.finditer(code):
                    line = code[:m.start()].count("\n")
                    ctx = code.split("\n")[line].strip()
                    if "try" not in ctx:
                        rep.err(f"{name}: 裸 history.{m.group(1)}（srcdoc 下抛 SecurityError）行 {line + 1}")
            for m in MODULE_SCRIPT.finditer(text):
                rep.err(f"{name}: <script type=\"module\"> 禁用（内联后无模块基底）")
            for m in CDN_HINT.finditer(text):
                rep.err(f"{name}: 外部 CDN 引用 -> {m.group(0)}（零依赖铁律）")
            if name.endswith((".html", ".css")):
                for m in EXTERNAL.finditer(text):
                    url = m.group(0)
                    if url.startswith(("http://www.w3.org/", "https://www.w3.org/")):
                        continue  # SVG 命名空间
                    rep.warn(f"{name}: 绝对外链 {url}（若为字体/图片/脚本即违规）")


def _check_layout(paths: dict[str, bytes], rep: Report) -> None:
    names = list(paths)
    if len(names) > MAX_FILES:
        rep.err(f"文件数 {len(names)} 超上限 {MAX_FILES}")
    total = sum(len(v) for v in paths.values())
    if total > MAX_BYTES:
        rep.err(f"解压总量 {total} 字节超上限 {MAX_BYTES}")
    roots = {n.split("/")[0] for n in names}
    if not any(n == "index.html" or n.endswith("/index.html") for n in names):
        rep.err("缺少 index.html")
    if len(roots) == 1 and not any("/" in n for n in names):
        pass  # 三件套平铺
    for n in names:
        if "__MACOSX/" in n or n.endswith(".DS_Store"):
            rep.warn(f"打包残留: {n}")
        if TRAVERSAL.search(n):
            rep.err(f"非法路径: {n}")


def audit(target: Path) -> Report:
    rep = Report(target.name)
    if target.is_dir():
        paths = {str(p.relative_to(target)): p.read_bytes()
                 for p in sorted(target.rglob("*")) if p.is_file()}
    elif target.is_file() and target.suffix == ".zip":
        with zipfile.ZipFile(target) as zf:
            paths = {
                n: zf.read(n) for n in zf.namelist()
                if n not in ("__MACOSX",) and not n.endswith("/")
            }
    else:
        rep.err("目标不存在或不是课件目录/zip")
        rep.dump()
        return rep
    _check_layout(paths, rep)
    _collect(paths, rep)
    rep.dump()
    return rep


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args:
        print(__doc__)
        return 2
    reps = [audit(Path(a)) for a in args]
    errs = sum(len(r.errors) for r in reps)
    warns = sum(len(r.warns) for r in reps)
    print(f"\n总计：{len(reps)} 个课件，{errs} error(s)，{warns} warning(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
