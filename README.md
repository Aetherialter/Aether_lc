# Aether_lc

Aether_lc 是一个面向 LeetCode 中文站的本地刷题 CLI 工具。

当前版本是 `v0.1.0`。这个版本只聚焦一个完整的小闭环：复用登录态、检查 session 状态、展示账号详情和刷题统计。

## v0.1.0 功能

- 复用本机浏览器中的 `leetcode.cn` 登录态。
- 浏览器 Cookie 自动读取失败时，支持手动粘贴 Cookie。
- 将本地 session 保存到 `.aether_lc/session.json`。
- 检查本地 session 是否仍然有效。
- 展示账号基础信息和已通过题目统计。
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

## 当前限制

- `v0.1.0` 暂不支持拉取题目详情。
- `v0.1.0` 暂不生成本地 `solution.py`。
- `v0.1.0` 暂不运行本地测试用例。
- `v0.1.0` 暂不支持远程提交。
- `lc profile` 的刷题统计来自 LeetCode 中文站题库状态接口，因此可能需要等待几秒。

## 开发与验证

运行代码检查：

```powershell
uv run ruff check .
```

验证当前 CLI 功能：

```powershell
uv run lc status
uv run lc profile
```

项目已经安装 `pytest`，但 `v0.1.0` 暂时还没有有意义的自动化测试。

## 版本路线

- `v0.1`: 登录、session 状态检查、账号详情展示。
- `v0.2`: 题目列表与题目详情拉取。
- `v0.3`: 本地题目工作区生成。
- `v0.4`: 本地样例运行器。
- `v0.5`: 远程提交与判题结果轮询。
- `v0.6`: 稳定性、诊断命令、文档和 GitHub Actions。
- `v1.0`: 完整的 LeetCode 中文站本地刷题 CLI 工作流。

## 项目结构

```text
src/aether_lc/
  auth.py      浏览器/手动 Cookie 读取与本地 session 存储
  client.py    LeetCode 中文站 HTTP 客户端与账号统计
  cli.py       Typer 命令入口
  ui.py        基于 Rich 的终端输出
```

## 项目定位

这个项目目前是个人学习与简历项目。当前阶段重点不是堆功能，而是通过小版本逐步练习 Python 工程结构、CLI 设计、HTTP 客户端封装、GitHub 提交与 Release 流程。
