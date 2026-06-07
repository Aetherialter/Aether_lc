# Aether_lc

Aether_lc 是一个面向 LeetCode 中文站的本地刷题 CLI 工具。

当前版本是 `v0.5.0`。这个版本在 `v0.4.0` 的单文件本地测试工作流基础上，新增了 `lc submit` 远程提交与判题结果轮询。

## v0.5.0 功能

- 复用本机浏览器中的 `leetcode.cn` 登录态。
- 浏览器 Cookie 自动读取失败时，支持手动粘贴 Cookie。
- 将本地 session 保存到 `.aether_lc/session.json`。
- 检查本地 session 是否仍然有效。
- 展示账号基础信息和已通过题目统计。
- 支持按题号在线获取 LeetCode 中文站题目详情。
- 支持分页展示题目索引列表。
- 支持 `lc solve <题号>` 在线拉取题目、展示题面、覆盖写入根目录 `solution.py` 并打开。
- 生成 `solution.py` 时会自动加入题目元信息、常用 Python 刷题标准库导入、提交区域标记和 `run_cases()` 本地测试入口。
- 支持 `lc test` 运行根目录 `solution.py`，根据退出码展示本地测试通过或失败。
- 支持 `lc submit` 从根目录 `solution.py` 提取提交区域代码，提交到 LeetCode 中文站并轮询判题结果。
- 使用独立的 `service.py` 管理应用层取题流程，复用 `get` 与 `solve` 的核心逻辑。
- 使用独立的 `workspace.py` 管理 `solution.py` 生成与打开逻辑。
- 使用独立的 `ui.py` 管理终端输出，避免 CLI 逻辑和展示逻辑混在一起。

## 环境要求

- Windows
- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- 已经在浏览器中登录 LeetCode 中文站账号

## 安装

克隆仓库后，使用 `uv` 安装依赖：

```powershell
git clone <your-repository-url>
cd Aether_lc
uv sync
```

查看 CLI 帮助：

```powershell
uv run lc --help
```

也可以通过 Python 模块方式运行：

```powershell
uv run python -m aether_lc --help
```

## 命令说明

### 登录

```powershell
uv run lc login
```

`lc login` 会先尝试从本机浏览器读取 `leetcode.cn` Cookie。如果自动读取失败，会提示你手动粘贴 Cookie。

登录态验证成功后，会保存到：

```text
.aether_lc/session.json
```

### 检查登录状态

```powershell
uv run lc status
```

检查本地 session 是否有效，并显示当前登录账号。

### 查看账号详情

```powershell
uv run lc profile
```

展示账号基础信息和刷题统计：

```text
Username
Real Name
Premium
Solved: All / Easy / Medium / Hard
Total: All / Easy / Medium / Hard
```

### 获取题目详情

```powershell
uv run lc get 1
```

根据题号查找 LeetCode 中文站题目，并在线展示题目详情、难度、标签和题面内容。

### 生成解题模板

```powershell
uv run lc solve 1
```

根据题号在线获取题目详情，展示题面，并覆盖写入根目录：

```text
solution.py
```

`solution.py` 是当前题目的通用解题模板文件。`lc solve` 会强制覆盖该文件，请在切换题目前自行保存当前解法。

生成后的 `solution.py` 会包含题目元信息和提交区域标记：

```python
# @lc problem_id: 1
# @lc title: Two Sum
# @lc title_slug: two-sum

# @lc submit_begin
class Solution:
    ...
# @lc submit_end
```

`lc submit` 只会提交 `# @lc submit_begin` 和 `# @lc submit_end` 之间的代码。你可以在该区域内保留 LeetCode 允许的 `import`、全局常量、helper 函数和 `class Solution`。

### 运行本地测试

```powershell
uv run lc test
```

`lc test` 会运行根目录 `solution.py` 中的 `run_cases()`。你可以在 `run_cases()` 中手动添加本地断言：

```python
assert solution.twoSum([2, 7, 11, 15], 9) == [0, 1]
```

默认只显示本地测试通过或失败，不展示 Python traceback。

`lc test` 只验证本地 `run_cases()`，本地测试通过不代表远程 LeetCode 一定通过。

### 远程提交

```powershell
uv run lc submit
```

`lc submit` 会从当前根目录 `solution.py` 读取题目元信息和提交区域代码，提交到 LeetCode 中文站，并轮询展示判题结果。

当前提交目标来自 `solution.py` 顶部元信息，因此执行远程提交前请先使用：

```powershell
uv run lc solve <题号>
```

### 展示题目列表

```powershell
uv run lc show
uv run lc show --limit 20 --skip 0
```

分页展示 LeetCode 中文站题目索引。默认展示前 50 道题。

## 安全说明

本项目会在本地保存 LeetCode 登录态，用于复用浏览器 session。该文件可能包含敏感 Cookie 信息。

不要提交这些文件或目录：

```text
.aether_lc/
.venv/
```

当前 `.gitignore` 已经忽略这些路径。

根目录 `solution.py` 是公开的空占位文件，会被提交到仓库；它不应包含个人解法后再提交。

## 当前限制

- `v0.5.0` 暂不保存题目详情到本地数据库。
- `v0.5.0` 只维护根目录单个 `solution.py`，不会生成本地题目目录。
- `v0.5.0` 暂不自动解析题面样例，`run_cases()` 中的断言需要手动添加。
- `v0.5.0` 远程提交仅支持 Python3。
- `lc solve` 会覆盖根目录 `solution.py`。
- `lc test` 默认隐藏 Python traceback，只展示本地测试结果；若 `run_cases()` 中没有断言，命令仍会显示本地测试通过，这是当前版本允许的轻量化设计。
- `lc submit` 依赖 `solution.py` 顶部题目元信息和提交区域标记；如果手动删除这些内容，需要重新执行 `lc solve <题号>`。
- `solution.py` 中的自动导入可能在编辑器中产生未使用导入提示，这是为了保证本地解题时常用库可直接使用。
- 当前版本仅自动读取 Chrome 的 LeetCode 中文站 Cookie，其他浏览器支持会在后续版本完善。
- 当前版本限定 Windows 环境，跨平台打开 `solution.py` 会在后续版本完善。
- 当前版本为了保持轻量，每次按题号获取详情时会在线拉取题目索引；后续缓存版本会优化重复请求。
- 当前版本对网络请求失败只展示简化错误信息；后续诊断版本会补充更细的错误原因。
- `lc profile` 的刷题统计来自 LeetCode 中文站题库状态接口，因此可能需要等待几秒。
- `lc get`、`lc show` 和 `lc solve` 依赖 LeetCode 中文站接口和网络状态。

## 开发与验证

运行代码检查：

```powershell
uv run ruff format src tests
uv run ruff check src pyproject.toml
uv run pytest
```

验证当前 CLI 功能：

```powershell
uv run lc status
uv run lc profile
uv run lc get 1
uv run lc show
uv run lc solve 1
uv run lc test
uv run lc submit
```

当前版本提供了最小自动化测试，重点覆盖 `solution.py` 生成、题目元信息解析和提交区域 marker 校验。

发布前需要确认根目录 `solution.py` 为空，避免把个人题解提交到公开仓库。

## 版本路线

- `v0.1`: 登录、session 状态检查、账号详情展示。
- `v0.2`: 在线题目索引查询与题目详情展示。
- `v0.3`: 纯在线解题模板工作流，覆盖写入单个 `solution.py`。
- `v0.4`: 单文件本地测试工作流，执行 `solution.py` 中的 `run_cases()`。
- `v0.5`: 远程提交与判题结果轮询。
- `v0.6`: 稳定性、诊断命令、文档和 GitHub Actions。
- `v1.0`: 完整的 LeetCode 中文站本地刷题 CLI 工作流。

## 项目结构

```text
src/aether_lc/
  auth.py      浏览器/手动 Cookie 读取与本地 session 存储
  client.py    LeetCode 中文站 HTTP 客户端、账号统计与题目请求
  cli.py       Typer 命令入口
  problem.py   题号解析与题目数据标准化
  service.py   应用层流程，复用登录态、题目索引和题目详情获取逻辑
  ui.py        基于 Rich 的终端输出
  workspace.py solution.py 生成、打开与本地运行逻辑
tests/
  test_workspace.py  solution.py 生成与解析的最小自动化测试
```

## 项目定位

这个项目目前是轻量 GitHub CLI 工具。当前阶段重点不是堆功能，而是通过小版本逐步练习 Python 工程结构、CLI 设计、HTTP 客户端封装、GitHub 提交与 Release 流程。更完整的简历项目版能力，例如后端、数据库、前端和 AI/Agent 工作流，应作为独立产品线规划。

## License

本项目使用 [MIT License](LICENSE) 开源，允许个人或商业场景使用、修改、分发和闭源二次开发，但需要保留原始版权和许可证声明。

第三方依赖遵循各自许可证。当前主要依赖中没有发现 GPL 或 AGPL 依赖；需要额外关注的是 `browser-cookie3` 标注为 LGPL，`certifi` 标注为 MPL-2.0，其余核心依赖主要为 MIT、BSD、Apache-2.0、ISC 或 PSF 等宽松许可证。
