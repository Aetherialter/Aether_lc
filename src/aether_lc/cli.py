from typer import Typer, Exit
from aether_lc.auth import (
    get_cookies_from_browser,
    get_cookies_from_input,
    save_session,
)
from aether_lc.client import LeetCodeClient
from aether_lc.ui import (
    loading,
    render_submission_result,
    success,
    warning,
    error,
    render_profile,
    render_problem_detail,
    render_problem_list,
)
from aether_lc.service import (
    get_account_profile,
    get_problem_detail_by_question_id,
    get_problem_summaries,
    get_user_status,
    submit_current_solution,
)
from aether_lc.workspace import ProblemMetadata, run_solution_file, write_solution_file

app = Typer(help="aether_lc 适用于中文站leetcode的刷题本地化cli程序")


@app.command()
def login() -> None:
    with loading("正在读取浏览器 Cookie..."):
        browser_result = get_cookies_from_browser()
    if not browser_result:
        warning("未从浏览器读取到 Cookie, 请手动粘贴")
        source, cookies = "manual", get_cookies_from_input()
    else:
        source, cookies = browser_result
    if not cookies:
        warning("未获取 cookies")
        raise Exit(1)
    with LeetCodeClient(cookies) as client:
        status = client.user_status()
        if status and status.get("isSignedIn"):
            success("成功登录")
            save_session(
                {
                    "site": "leetcode.cn",
                    "source": source,
                    "username": status["username"],
                    "cookies": cookies,
                }
            )
        else:
            warning("cookies 无效或过期")
            raise Exit(1)


@app.command()
def status() -> None:
    user_status = get_user_status()
    username = user_status.get("username", "未知用户")
    success(f"在线状态: 当前账号 {username}")


@app.command()
def profile() -> None:
    account_profile = get_account_profile()
    render_profile(account_profile)


@app.command()
def get(question_id: str) -> None:
    problem_detail = get_problem_detail_by_question_id(question_id)
    render_problem_detail(problem_detail)


@app.command()
def show(limit: int = 50, skip: int = 0) -> None:
    problem_summaries = get_problem_summaries(limit=limit, skip=skip)
    render_problem_list(problem_summaries)


@app.command()
def solve(question_id: str) -> None:
    problem_detail = get_problem_detail_by_question_id(question_id)
    render_problem_detail(problem_detail)
    if not problem_detail.python_code:
        error("未找到 Python3 代码模板")
        raise Exit(1)
    if (
        not problem_detail.question_id
        or not problem_detail.title
        or not problem_detail.title_slug
    ):
        error("题目元信息不完整，无法生成可提交的 solution.py")
        raise Exit(1)
    write_solution_file(
        problem_detail.python_code,
        ProblemMetadata(
            problem_id=problem_detail.question_id,
            title=problem_detail.title,
            title_slug=problem_detail.title_slug,
        ),
    )


@app.command()
def test() -> None:
    result = run_solution_file()
    if result.returncode:
        error("本地测试失败")
        raise Exit(result.returncode)
    success("本地测试通过")


@app.command()
def submit() -> None:
    result = submit_current_solution()
    render_submission_result(result)


if __name__ == "__main__":
    app()
