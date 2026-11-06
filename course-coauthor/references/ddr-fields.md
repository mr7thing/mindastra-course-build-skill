# 四类字段原语（DDR）：把四问落到结构化提交上

> 过程数据只能来自**结构化提交**，不能从对话里抽。
> 学员不该直接看到"四问填空"（会变成八股），所以四问藏在字段设计里。

## 1. 一张表

| 原语 | 对应四问 | 字段（key 全小写） | 采集时点 |
|---|---|---|---|
| **A 靶向冲突** | 这是真问题吗 | `discarded_direction` + `specific_conflict` | 提交时 |
| **B 判据归因** | 凭什么这么判断 | `basis_type` + `basis_anchor` | 提交时 |
| **C 验证差值** | 我怎么知道我是对的 | `prediction` + `confidence` → `result` + `delta` | **分两次** |
| **D 镣铐校验** | 真实约束下能否成立 | `hard_constraint`（约束/数字+单位/来源） | 提交时 |
| **E AI 协作裁决** | 我怎么和 AI 一起做出这个判断 | `ai_collab`（intent/options/choice/prediction/verify） | 提交时（**与 C 的 prediction 分开**：E 记「预判 AI 会在哪错」，C 记「预判现实结果」；**不允许合并**） |

> E 是**每关必选**，而且是权重最高的一类。细则见 `ai-collaboration.md`。
> C 跨关：`decision_key` 写在里程碑 spec 顶层（不是字段），命名 `<开链关 key>-<主题>`，相邻两关同值；规则见 SKILL §5.2。

## 2. 为什么是这四类

- **A** 逼出"被放弃的平庸方向"——每个人的放弃项不同，**天然异质化**，最难表演。
- **B** 把"我以为"换成"我依据什么"，且只认**一个锚点**（原话、差评率、实测值）。
- **C** 是"比之前前进一步"的唯一证据；**必须在做事之前锁定预测**。
- **D** 是设计与艺术的分界线：有没有一条能被现实否掉的数。

## 3. 每关怎么配：1 项目 + E + 1 交付

| 关（示意） | 项目原语 | AI 协作 | 交付字段 |
|---|---|---|---|
| M1 立项 | A | **E** | 1 |
| M2 调研 | B | **E** | 1 |
| M3 方案 | C（prediction 锁定） | **E** | 1 |
| M4 落地 | D | **E** | 1 |
| M5 交付 | C（result 追加）或 D | **E** | 1 |

**3 类起、5 类封顶；字段 3–6 个**：普通关 4 个起（1 项目 + E 的 group_list + 1 交付），C 跨关 +1；**D 关允许只有 3 个**（D 只有 1 个字段）。顶格时先砍可选的 `mentor_question`。

## 4. 字段片段（可直接改）

```jsonc
// A 靶向冲突
{ "key": "discarded_direction", "title": "我放弃的那个方向", "type": "textarea",
  "required": true, "guidance": "你最初想做、或市面上最常见但你否掉的方向；写清否掉的理由。" }
{ "key": "specific_conflict", "title": "具体场景里的阻碍", "type": "textarea",
  "required": true, "max_length": 120, "guidance": "谁 + 在什么场景 + 被什么具体挡住。不写形容词。" }

// B 判据归因
{ "key": "basis_type", "title": "这次判断主要依据", "type": "single_select",
  "required": true, "options": [{ "value": "field", "label": "田野访谈" }, { "value": "data", "label": "数据/差评" },
                                 { "value": "theory", "label": "理论工具" }, { "value": "material", "label": "材料/实测" }] }
{ "key": "basis_anchor", "title": "唯一锚点", "type": "textarea", "required": true,
  "guidance": "一条具体锚点：原话 + 谁说的，或数值 + 来源。" }

// C 验证差值（两阶段）
{ "key": "prediction", "title": "我的预测（提交后不可改）", "type": "textarea", "required": true,
  "guidance": "你认为下一步会发生什么？必须可被验证。" }
{ "key": "confidence", "title": "置信度", "type": "text", "required": true,
  "guidance": "只填 高 / 中 / 低。" }
// 结果出来后追加
{ "key": "result", "title": "实际结果", "type": "textarea", "required": true }
{ "key": "delta", "title": "预期与结果的差异", "type": "textarea", "required": true,
  "guidance": "差在哪；如果重来，你改哪里。" }

// D 镣铐校验
{ "key": "hard_constraint", "title": "硬约束体检", "type": "group_list", "required": true,
  "min_items": 1, "max_items": 3,
  "fields": [
    { "key": "constraint", "title": "约束是什么（钱/工艺/工期/合规）", "type": "text", "required": true },
    { "key": "value", "title": "数字 + 单位", "type": "text", "required": true },
    { "key": "source", "title": "这个数从哪来（问谁/查哪）", "type": "textarea", "required": true }
  ] }
```

## 5. 平台约束（会 422 的）

- 字段类型只有 9 种：`text / textarea / markdown / list / group_list / asset / link / single_select / confirm`——**没有 `number`**，数字用 `text`。
- `group_list` 子字段只能是 `text` / `textarea`。
- 字段 key 必须 `^[a-z][a-z0-9_]*$`（大写下划线导不进去）。
- 一关字段总数控制在 4–6 个。

## 6. 反例

| 反例 | 问题 |
|---|---|
| "请描述你的设计思路" | 作文，事后合理化 |
| 六关都问"AI 使用记录" | 同一份作业做六遍 |
| `prediction` 和 `result` 同一关填 | 拿到的是"事后解释"，不是预测 |
| `basis_type` 只给"AI 分析"选项 | 诱导把判断外包给 AI |
| 每关都上四类原语 | 表单地狱，学员放弃 |

## 7. 价值回路（数据必须还回去，否则没人认真填）

| 对象 | 拿回什么 | 什么时候 |
|---|---|---|
| 学员 | 判断轨迹：改了几次主意、被什么说服、预测命中率 | 每关小结 + 结课报告 |
| 导师 | 判断画像：置信度校准（高置信的准不准）、被什么说服 | 放行时由 `summary-review` 子技能给出 |
| 课程 | 同类命题的决策分布与结果分布（导师示范的依据） | 导师示范时 |

**数据只记录、不评价**：决策点不自动算分；唯一的质量信号是导师旁注。

## 8. 防表演

| 风险 | 处方 |
|---|---|
| 事后合理化 | `prediction` 事前锁定、不可改；`result` 只能追加 |
| 写漂亮话 | 字段短、有字数上限；不给长作文题 |
| 挑好听的记 | 只记变更点；AI 比对前后版本，漏记标出（提示，不拦截） |
| 抄别人的判断 | `basis_anchor` 要求带来源（谁、何时、在哪），对不上会露馅 |
| 把判断外包给 AI | `basis_type` 不设"AI 分析"选项 |
