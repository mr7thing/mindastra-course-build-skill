# mindastra-course-build-skill

Mindastra 课程建设技能集：把真实目标与手头资料，变成**可导入平台、可交付教学**的课程资产。

本仓库是 [Mindastra](https://mindastra.space)) 课程建设类技能的官方发布仓库，每个技能采用可移植的 Agent Skills 布局（`SKILL.md` + references + scripts），可在 Claude Code、Codex、OpenClaw 等任何兼容 Agent Skills 的工具中离线使用。

## 技能一览

| 技能 | 用途 |
|---|---|
| [`goal-oriented-pbl-course`](goal-oriented-pbl-course/) | 目标导向 PBL 建课：资料 → 课程契约 → 里程碑 → 课程资料包（`course.json` + 章节 + 指南 + 附件） |
| [`interactive-courseware`](interactive-courseware/) | 交互课件：零依赖 HTML 幻灯（zip），上传课程后在沙箱 iframe 内播放 |

两者分工明确：建课技能产出课程结构与资料包；课件技能为已有课程制作课堂演示交互课件。

## 安装

```bash
git clone https://github.com/mr7thing/mindastra-course-build-skill.git
cd mindastra-course-build-skill

# 安装单个技能（各技能自包含安装器，按需选择）
./goal-oriented-pbl-course/scripts/install-skill.sh claude-global
./interactive-courseware/scripts/install-skill.sh claude-global
# 目标亦可换：codex-global / openclaw-workspace / all-global / custom <dir>
```

安装器以符号链接把**技能目录本身**接入各框架的技能发现目录，不复制文件、不产生漂移。

| 目标 | 发现目录 |
|---|---|
| `claude-global` / `claude-project` | `~/.claude/skills/` / `<project>/.claude/skills/` |
| `codex-global` / `codex-project` | `~/.codex/skills/` / `<project>/.agents/skills/` |
| `openclaw-global` / `openclaw-workspace` | `~/.openclaw/skills/` / `~/.openclaw/workspace/skills/` |
| `all-global` | 以上全局位一次装齐 |
| `custom <dir>` | 任意 Agent Skills 兼容目录 |

## 快速上手（建课技能）

安装后对 Agent 说：

```text
用 goal-oriented-pbl-course 把这份资料变成一门课程：<资料路径或粘贴内容>
```

技能会从两个必答问题开始，逐阶段向你确认；确认完毕后在工作目录产出 `course-design/` 与课程资料包，最后运行审计脚本：

```bash
python3 goal-oriented-pbl-course/scripts/audit_package.py <课程资料包目录>
```

退出码 0 = 可交付；ERROR 必须修复，WARNING 只是内容深度提示。

## 导入 MindNexus 平台

课程资料包可通过平台导入为课程草稿：

- **GUI**：登录平台 → 课程管理 → 导入课程包
- **API**：`POST /api/v1/courses/import-package`（JWT 鉴权）

导入即创建新课程草稿（纯新增，不改既有数据）；发布前需在课程管理中配置至少 1 个期次。

完整的图文使用笔记（从安装到发布全流程）见平台技能页：<https://mindastra.space/skills>

## 目录结构

```text
├── goal-oriented-pbl-course/           # PBL 建课技能
│   ├── SKILL.md                        #   工作流、规则、模式
│   ├── references/                     #   领域模型 / 产物契约 / 评价矩阵 / 平台 JSON
│   ├── scripts/
│   │   ├── audit_package.py            #   确定性审计器（交付门禁）
│   │   └── install-skill.sh            #   跨框架安装器
│   └── agents/openai.yaml              #   Codex 适配元数据
└── interactive-courseware/             # 交互课件技能
    ├── SKILL.md                        #   沙箱硬约束、引擎骨架、页式规范
    ├── references/                     #   平台课件管线契约
    └── scripts/
        └── audit_courseware.py         #   课件规范审计器
```

## License

[MIT](LICENSE)
