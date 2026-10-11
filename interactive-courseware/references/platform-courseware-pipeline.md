# Platform Courseware Pipeline（通道契约参考）

> 真相源：`.trellis/spec/backend/courseware-contracts.md` +
> `backend/app/services/courseware_service.py` + `backend/app/routers/courses/publish.py`。
> 冲突时以源码为准（2026-10 版本）。

## 1. 端点面

| 动作 | 端点 | 权限 | 说明 |
|---|---|---|---|
| 上传草稿 | `POST /api/v1/courses/{course_id}/courseware` | JWT 课程成员 / API Key scope `courseware:write` | multipart `file=<zip>`；上传即创建草稿课件（draft_document） |
| 发布 | `POST /api/v1/courses/{course_id}/courseware/publish` | 仅 JWT，FACILITATOR 角色 | 草稿固化为发布版本；`courses.courseware_document_id` 指向发布文档 |
| 查询 | `GET /api/v1/courses/{course_id}/courseware` | 课程成员 | 返回 `CoursewareMeta`（draft/published 状态与版本号） |
| 删除 | `DELETE /api/v1/courses/{course_id}/courseware` | 课程成员 | 清草稿；发布中则解除 `courseware_document_id` 指针 |

- 成功响应：`200/201 {"draft": {...}, "published": {...}, "published_version": n}` 形状以 `CoursewareMeta` 为准。
- 失败：`422`（zip 超限/缺 index.html/路径穿越/文件数超 20），`403`（角色不够/scope 不足），`401`（key 吊销）。
- API Key 通道注意：key 的 scope 只约束 key 通道；发布端点强制 FACILITATOR 角色，key 不直通角色——发布是人的动作。

## 2. 状态机

```
上传 ──▶ draft（草稿文档，可反复重传覆盖）
          │
          └─ publish（FACILITATOR）──▶ published（发布快照，内容不可变）
                                          │
                     再上传 draft ──▶ 再 publish ──▶ 新发布版本（swap 指针）
```

- 发布版本走文档版本通道（`documents.current_version_id` + 版本历史），课程详情页按 `courses.courseware_document_id` 渲染当前发布版。
- 重新上传草稿不影响已发布版本；再次发布产生新版本并切换指针。

## 3. 打包与渲染（服务端行为，作者须适配）

- 上传时服务端校验 zip：必须含 `index.html`（根或单一顶层目录）、≤20 文件、解压后总量 ≤8MB、拒绝绝对路径与 `..` 穿越、忽略 `__MACOSX/` 与 `.DS_Store`。
- 服务端把 `index.html` 内相对引用的 `<link>` / `<script>` 内联成**单文件 HTML**，并注入兼容垫片（例如控制台修复）。因此作者只需交付三件套；不要手工内联、不要用 ES module、不要 `import()`。
- 渲染：课程详情页 `<iframe srcdoc="…" sandbox="allow-scripts …">`，**无 allow-same-origin** → opaque origin。localStorage/cookie/父框访问全部禁止；hash 写入合法。

## 4. 沙箱兼容清单（上传前逐项自查）

| 特性 | 沙箱内行为 | 处理 |
|---|---|---|
| `localStorage` 等 | 抛 SecurityError | 禁用；状态放内存 |
| `history.pushState/replaceState` | 抛 SecurityError | try/catch 包裹，先更新 UI |
| `location.hash = …` | 合法，触发 hashchange | 深链唯一通道 |
| `hashchange` 监听 | 正常 | 配合 hash 写入 |
| 外链资源 | 不加载（且违反零依赖） | 全内联 |
| `iframe` 嵌套 / `window.top` | 受限 | 不用 |
| 定时器/动画/Canvas/WebAudio | 正常 | 放心用；音频须用户手势触发 |

## 5. 章节正文深链卡（`[!courseware]` 指令）

课件在平台有**双呈现面**：课程详情页整页渲染（`courses.courseware_document_id`）+
章节 Markdown 正文里的**深链卡**（前端 `web/src/composables/useMarkdownRenderer.ts`
卡片指令渲染，非后端端点）：

```markdown
> [!courseware]
> 标题: 第 2 课演示课件
> 跳转: s20
```

- `标题:` 可选（缺省用课件名）；`跳转:` 可选 slide id（`#s20` 形式深链进课件指定页）。
- 课件未配置（`hasCourseware=false`）时卡片渲染为**禁用态**，不报错。
- 深链卡的目标页必须真实存在——生成章节正文时 slide id 要与三件套里的 `.slide` id 对齐。

## 6. Agent 交付清单

1. 三件套通过 `file://` 离线自检（每页、每个交互、键盘+触摸）。
2. `audit_courseware.py` 零 ERROR。
3. zip 上传草稿 → 人工在 GUI 预览草稿 → 请求导师（FACILITATOR）点击发布。
4. 平台内验证：深链 `#sNN`、逐页动画重播、无控制台 SecurityError。
