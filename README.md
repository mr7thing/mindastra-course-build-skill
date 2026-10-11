# mindastra-course-build-skill

把一个真实的能力目标 + 手头资料，变成一门**导师签收、项目先行**的 PBL 课程（含可导入 MindNexus 平台的课程资料包）。

本仓库是 [Mindastra](https://mindnexus.multii.cn) 课程建设技能的官方发布仓库，采用可移植的 Agent Skills 布局（`SKILL.md` + references + scripts），可在 Claude Code、Codex、OpenClaw 等任何兼容 Agent Skills 的工具中离线使用。

## 它做什么

你提供：一个真实项目/能力目标 + 任意形式的资料（笔记、文档、示例、链接）。

技能引导 AI 完成：

1. **两个必答问题开场** —— 要做什么项目？学员是什么基础？
2. **逐项拷问式访谈** —— 一轮一问，确认课程契约 11 项要素
3. **分阶段编译** —— 项目路径（里程碑）→ 能力评价矩阵 → 学习依赖 → 章节内容
4. **产出课程资料包** —— `course.json` + 章节 Markdown + 里程碑指南 + 附件的标准目录/zip
5. **确定性审计** —— `audit_package.py` 逐条硬门禁校验，0 错误才可交付

每个里程碑强制携带：作品本身 + **AI 交互日志** + 学员自己的**分析反思**——这是本技能区别于"AI 帮你水一门课"的核心设计。

## 安装

```bash
git clone https://github.com/mr7thing/mindastra-course-build-skill.git
cd mindastra-course-build-skill
./scripts/install-skill.sh claude-global   # 或 codex-global / openclaw-workspace / all-global
```

安装器以符号链接接入各框架的技能发现目录，不复制文件、不产生漂移。

| 目标 | 发现目录 |
|---|---|
| `claude-global` / `claude-project` | `~/.claude/skills/` / `<project>/.claude/skills/` |
| `codex-global` / `codex-project` | `~/.codex/skills/` / `<project>/.agents/skills/` |
| `openclaw-global` / `openclaw-workspace` | `~/.openclaw/skills/` / `~/.openclaw/workspace/skills/` |
| `all-global` | 以上全局位一次装齐 |
| `custom <dir>` | 任意 Agent Skills 兼容目录 |

## 快速上手

安装后对 Agent 说：

```text
用 goal-oriented-pbl-course 把这份资料变成一门课程：<资料路径或粘贴内容>
```

技能会从两个必答问题开始，逐阶段向你确认；确认完毕后在工作目录产出 `course-design/` 与课程资料包，最后运行审计脚本：

```bash
python3 scripts/audit_package.py <课程资料包目录>
```

退出码 0 = 可交付；ERROR 必须修复，WARNING 只是内容深度提示。

## 导入 MindNexus 平台

课程资料包可通过平台导入为课程草稿：

- **GUI**：登录平台 → 课程管理 → 导入课程包
- **API**：`POST /api/v1/courses/import-package`（JWT 鉴权）

导入即创建新课程草稿（纯新增，不改既有数据）；发布前需在课程管理中配置至少 1 个期次。

完整的图文使用笔记（从安装到发布全流程）见平台技能页：<https://mindnexus.multii.cn/skills>

## 目录结构

```text
├── SKILL.md                          # 技能主文件：工作流、规则、模式
├── references/
│   ├── domain-model.md               # 领域模型：设计前必读
│   ├── output-contracts.md           # 结构化产物契约
│   ├── mastery-rubric.md             # 能力评价维度与等级
│   ├── platform-course-json.md       # 平台课程 JSON / 资料包契约
│   └── framework-installation.md     # 各框架安装与调用细节
├── scripts/
│   ├── audit_package.py              # 确定性审计器（交付门禁）
│   └── install-skill.sh              # 跨框架安装器
└── agents/
    └── openai.yaml                   # Codex 适配元数据
```

## License

[MIT](LICENSE)
