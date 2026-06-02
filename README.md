# Aether_lc

Aether_lc 是一个面向 LeetCode 中文站的本地刷题 CLI 工具。

当前版本是 `v0.3.0`。这个版本在 `v0.2.0` 的在线题目查询基础上，新增了纯在线解题模板工作流：拉取题目后覆盖写入根目录 `solution.py`，并自动打开该文件。

## v0.3.0 功能

- 复用本机浏览器中的 `leetcode.cn` 登录态。
- 浏览器 Cookie 自动读取失败时，支持手动粘贴 Cookie。
- 将本地 session 保存到 `.aether_lc/session.json`。
- 检查本地 session 是否仍然有效。
- 展示账号基础信息和已通过题目统计。
- 支持按题号在线获取 LeetCode 中文站题目详情。
- 支持分页展示题目索引列表。
- 支持 `lc solve <题号>` 在线拉取题目、展示题面、覆盖写入根目录 `solution.py` 并打开。
- 生成 `solution.py` 时会自动加入常用 Python 刷题标准库导入。
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
data/
problems/
```

当前 `.gitignore` 已经忽略这些路径。

根目录 `solution.py` 是公开的空占位文件，会被提交到仓库；它不应包含个人解法后再提交。

## 当前限制

- `v0.3.0` 暂不保存题目详情到本地数据库。
- `v0.3.0` 只维护根目录单个 `solution.py`，不会生成本地题目目录。
- `v0.3.0` 暂不运行本地测试用例。
- `v0.3.0` 暂不支持远程提交。
- `lc solve` 会覆盖根目录 `solution.py`。
- `lc profile` 的刷题统计来自 LeetCode 中文站题库状态接口，因此可能需要等待几秒。
- `lc get`、`lc show` 和 `lc solve` 依赖 LeetCode 中文站接口和网络状态。

## 开发与验证

运行代码检查：

```powershell
uv run ruff check .
```

验证当前 CLI 功能：

```powershell
uv run lc status
uv run lc profile
uv run lc get 1
uv run lc show
uv run lc solve 1
```

项目已经安装 `pytest`，但 `v0.3.0` 暂时还没有有意义的自动化测试。

## 版本路线

- `v0.1`: 登录、session 状态检查、账号详情展示。
- `v0.2`: 在线题目索引查询与题目详情展示。
- `v0.3`: 纯在线解题模板工作流，覆盖写入单个 `solution.py`。
- `v0.4`: 本地样例运行器。
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
  workspace.py solution.py 生成与打开逻辑
```

## 项目定位

这个项目目前是个人学习与简历项目。当前阶段重点不是堆功能，而是通过小版本逐步练习 Python 工程结构、CLI 设计、HTTP 客户端封装、GitHub 提交与 Release 流程。
