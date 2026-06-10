# 力扣中文站本地化刷题 CLI 工具后续版本规划

本文档是力扣中文站本地化刷题 CLI 工具的 GitHub CLI 版本路线草案，当前仓库名为 `leetcode-cn-local-cli`，用于在正式实现前确认大方向。当前产品定位是轻量、在线优先、单文件工作区的 LeetCode 中文站 CLI 工具。

## 产品边界

力扣中文站本地化刷题 CLI 工具应保持轻量 CLI 工具定位，不应默认演变成本地题库生成器。

- 保持 `solution.py` 作为唯一主要工作文件。
- 默认不生成每道题独立目录。
- 在缓存方案明确前，不保存完整题面到本地。
- 优先做小版本、可发布、能改善真实工作流的功能。
- 简历项目版的后端、数据库、前端、AI 工作流应作为另一条产品线，不混入当前 GitHub CLI 版本。

## 当前状态

- `v0.1`: 登录、session 校验、账号详情展示。
- `v0.2`: 在线题目索引和题目详情查询。
- `v0.3`: 在线解题模板工作流，生成根目录 `solution.py`。
- `v0.4`: 单文件本地测试工作流，通过 `run_cases()` 和 `lc test` 运行本地断言。
- `v0.5`: 远程提交与判题轮询，通过 `lc submit` 提交 `solution.py` 中 marker 包裹的代码。
- `v0.5.1`: 修复按题号查询高题号时只能搜索前 100 题的问题。
- `v0.5.2`: 修复远程提交使用展示题号导致提交目标不一致的问题。
- `v0.5.3`: 改善 `solution.py` 编辑体验，减少静态分析告警并补充空模板占位。
- `v0.5.4`: 修复 GraphQL `data: null` 导致 traceback，并精简 README。

## 已实现版本

### v0.5: 远程提交与判题轮询

目标：允许用户把当前 `solution.py` 中的解法提交到 LeetCode 中文站，并在 CLI 中查看判题结果。

计划范围：

- 新增 `lc submit`，不强制传题号。
- 从根目录 `solution.py` 读取题目元信息并提取待提交代码。
- 初版提交代码提取策略：只提交 `# @lc submit_begin` 与 `# @lc submit_end` 之间的代码。
- 将 Python3 解法提交到 LeetCode 中文站。
- 轮询判题结果，直到通过、失败或超时。
- 展示判题状态、运行时间、内存占用和失败用例信息。

不做内容：

- 暂不支持多语言提交。
- 暂不生成本地题目目录。
- 暂不做自动重试策略。
- 暂不从其他本地文件中猜测提交内容。
- 暂不支持从提交区域外提取用户自定义 import、全局常量或 helper 函数。

工程建议：

- HTTP 提交接口放在 `client.py`。
- 提交流程编排放在 `service.py`。
- 判题结果展示放在 `ui.py`。
- `solution.py` 仍然是唯一提交来源。
- `lc submit` 需要从 `solution.py` 中读取题目元信息，用于确认当前提交目标。
- `solution.py` 应在 `lc solve` 阶段写入题号、标题和 `title_slug` 等元信息。
- `solution.py` 应在 `lc solve` 阶段写入 `# @lc submit_begin` 和 `# @lc submit_end`，用于界定提交代码区域。

已知限制：

- 初版 `lc submit` 只提交 `# @lc submit_begin` 与 `# @lc submit_end` 之间的代码。
- 如果用户在提交区域外定义全局常量、helper 函数或自定义 import，提交时会被丢弃。
- 该限制是为了保持 v0.5 实现简单，后续版本可继续完善代码提取策略。

### v0.5.1: 高题号查询修复

目标：修复 `lc get` 和 `lc solve` 按题号查询时只能在前 100 道题中查找的问题。

更新内容：

- 按题号获取题目详情时改为分页查询 LeetCode 中文站题目索引。
- 修复高题号如 `2196` 无法通过 `lc get` 或 `lc solve` 找到的问题。
- 非法题号输入时保持简化错误提示，避免继续触发 Python traceback。

不做内容：

- 暂不引入本地题目索引缓存。
- 暂不改变 `lc show` 的分页展示语义。
- 暂不扩大远程提交或本地测试能力。

### v0.5.2: 远程提交目标修复

目标：修复远程提交时将展示题号当作 LeetCode 内部提交 ID 使用的问题，避免提交目标和网页端记录不一致。

更新内容：

- 题目详情查询新增 LeetCode 内部 `questionId`。
- `solution.py` 元信息新增 `submit_question_id`，用于远程提交。
- `problem_id` 保持为展示题号，继续用于用户识别当前题目。
- `lc submit` 改为使用 `submit_question_id` 作为提交 payload 中的 `question_id`。
- 补充题目详情标准化和提交元信息解析测试。

不做内容：

- 暂不改变 `lc submit` 的命令参数设计。
- 暂不支持多语言提交。
- 暂不做提交前目标确认交互。

### v0.5.3: solution.py 编辑体验修复

目标：降低刚生成 `solution.py` 后 VSCode/Pylance 和 Ruff 的编辑器提示干扰，让单文件刷题工作区更适合直接编辑。

更新内容：

- 生成 `solution.py` 时加入 Pyright 文件级配置，关闭未使用导入和未使用变量提示。
- 生成 `solution.py` 时加入 Ruff 文件级配置，关闭刷题工作区中的未使用导入和未使用变量提示。
- 将 `from typing import *` 改为显式 `typing` 导入，避免 star import 相关静态分析告警。
- 为 LeetCode 返回的空 Python 方法模板追加轻量 `pass` 占位，避免刚执行 `lc solve` 后立即 `lc test` 因空方法体失败。

不做内容：

- 暂不实现复杂模板规范化器。
- 暂不改变 `run_cases()` 的本地测试入口设计。
- 暂不处理链表、二叉树等注释类型定义的自动展开；用户需要本地测试复杂结构题时，可自行取消注释 `TreeNode` / `ListNode` 等模板定义。

### v0.5.4: GraphQL data:null 防御与文档精简

目标：修复 LeetCode GraphQL 返回 `data: null` 时 CLI 直接 traceback 的问题，并让 GitHub README 更适合首页阅读。

更新内容：

- `user_status()`、`problem_list()`、`problem_detail()` 对 GraphQL `data` 字段增加类型检查。
- 当 `data` 不是字典时返回简化失败结果，由 service 层展示现有错误提示。
- 精简 README，保留项目定位、快速开始、核心命令、`solution.py` 规则、限制和开发验证。
- 在 README 中明确树、链表题本地测试需要用户按需取消注释 `TreeNode` / `ListNode`。

不做内容：

- 暂不引入完整错误结果类型。
- 暂不区分网络异常、参数错误和接口异常的具体原因。
- 暂不自动展开复杂题型的注释类型定义。

### v0.6: 诊断命令与稳定性

目标：提升 CLI 在 Cookie 失效、网络异常、接口变化和本地文件异常时的可诊断性。

计划范围：

- 新增 `lc doctor`。
- 检查 session 文件是否存在、格式是否正确。
- 检查 cookies 是否有效。
- 检查 LeetCode 中文站基础连通性。
- 检查 `solution.py` 是否存在、是否可运行。
- 改进网络失败、session 过期、缺少 Python3 模板、题号非法等错误提示。
- 在 `lc submit` 提交前展示当前提交目标，便于用户确认题号、标题和 `title_slug`。
- 为纯逻辑模块补充基础自动化测试。

不做内容：

- 暂不引入数据库。
- 暂不做自动浏览器登录。
- 默认不做依赖真实 LeetCode 账号的端到端测试。

工程建议：

- 网络相关诊断应明确提示，避免静默执行过多请求。
- 优先测试 `problem.py` 和 `workspace.py` 中的纯逻辑。
- 诊断输出不得泄露 Cookie 或 session 敏感信息。

### v0.7: 轻量缓存

目标：提升重复查询题目索引和题目详情时的速度，同时避免项目变成本地题库。

计划范围：

- 在 `.aether_lc/cache/` 下建立轻量缓存。
- 缓存题目索引元信息和更新时间。
- 可选缓存 `solve` 所需的最小题目详情元信息。
- 新增 `lc cache clear`。
- 增加缓存过期策略。

不做内容：

- 暂不强制引入完整数据库。
- 暂不保存用户解法历史。
- 暂不生成每题 Markdown 或目录。

工程建议：

- 初期优先使用 JSON 文件。
- 只有当查询需求明确增加时再考虑 SQLite。
- 缓存数据必须和 `solution.py` 工作区分离。

### v0.8: 样例提取原型

目标：尝试从题面中提取简单样例，并在安全时预填到 `solution.py` 的 `run_cases()` 中。

计划范围：

- 在 `problem.py` 中新增 `SampleCase` 数据模型。
- 从题面 HTML 中提取常见的输入和输出示例。
- 在 `solution.py` 中生成可编辑的断言建议。
- 对无法稳定解析的样例明确标记，而不是强行猜测。

不做内容：

- 不保证支持链表、二叉树、图、自定义判题等复杂题型。
- 不做复杂 Markdown 或自然语言解析器。
- 不声称自动生成的样例完整覆盖题目。

工程建议：

- 该功能应定位为 best effort。
- 生成内容必须允许用户手动编辑。
- `lc test` 不应依赖网络请求。

### v0.9: 打包、测试与 CI

目标：提升仓库作为公开 GitHub 项目的可靠性和发布质量。

计划范围：

- 添加 GitHub Actions，执行 lint 和测试。
- 为题号解析、工作区生成、CLI 命令注册补充有意义的测试。
- 保持 README 中的安装命令、仓库名和 Release 说明与真实 GitHub 仓库一致。
- 增加 release checklist。
- 增加 changelog 或 release notes 模板。

不做内容：

- 暂不发布到 PyPI，除非安装方式和维护预期已经明确。
- 暂不建设大型文档站。

工程建议：

- CI 不应依赖真实 LeetCode 登录态。
- 真实接口检查应保持手动或显式启用。

### v1.0: 稳定轻量 CLI

目标：形成完整、稳定、轻量的 LeetCode 中文站本地刷题 CLI 工作流。

预期工作流：

```powershell
uv run lc login
uv run lc profile
uv run lc show
uv run lc get 1
uv run lc solve 1
uv run lc test
uv run lc submit
```

预期质量：

- 命令行为清晰。
- 单文件解题工作流稳定。
- 错误提示和诊断能力可用。
- 支持远程提交和判题轮询。
- 具备基础自动化测试和 CI。
- README 足够支撑新用户安装和使用。

## 简历项目版方向

简历项目版可以复用该 CLI 中沉淀出的接口理解、工作流设计和题目数据处理经验，但应作为独立产品线。

可能范围：

- 后端 API。
- 数据库记录题目、提交、复盘和练习历史。
- 前端 Dashboard。
- AI 读题、提示、复盘或 Review 工作流。
- Docker 部署。
- CI/CD 和完整文档。

在 CLI 版本达到稳定 `v1.0` 前，不建议将这些能力混入当前轻量 GitHub CLI。

## 待确认决策

- `solution.py` 的提交区域 marker 是否需要支持自定义名称？
- `lc test` 是否永久保持隐藏 traceback，还是未来提供调试开关？
- 缓存功能一开始使用 JSON，还是在需求明确后直接引入 SQLite？
- 样例提取应放在远程提交之前实现，还是延后到 `v1.0` 之后？
