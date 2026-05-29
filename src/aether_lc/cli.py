from typer import Typer, Exit
from aether_lc.auth import (
    get_cookies_from_browser,
    get_cookies_from_input,
    load_session,
    save_session,
)
from aether_lc.client import LeetCodeClient
from aether_lc.ui import (
    loading,
    success,
    warning,
    error,
    render_profile,
    render_problem_detail,
    render_problem_list,
)
from aether_lc.problem import (
    parse_question_id,
    normalize_problem_summaries,
    find_problem_by_id,
    normalize_problem_detail,
)

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
    session = load_session()
    if not session:
        warning("未登录, 请先执行 lc login")
        raise Exit(1)
    cookies = session.get("cookies")
    if not isinstance(cookies, dict):
        error("session 格式错误, 请重新执行 lc login")
        raise Exit(1)
    with LeetCodeClient(cookies) as client:
        status_info = client.user_status()
        if status_info and status_info.get("isSignedIn"):
            username = status_info.get("username", "未知用户")
            success(f"在线状态: 当前账号 {username}")
        else:
            error("session 有问题或已过期")
            raise Exit(1)


@app.command()
def profile() -> None:
    session = load_session()
    if not session:
        warning("未登录, 请先执行 lc login")
        raise Exit(1)
    cookies = session.get("cookies")
    if not isinstance(cookies, dict):
        error("session 格式错误, 请重新执行 lc login")
        raise Exit(1)
    with LeetCodeClient(cookies) as client:
        with loading("正在获取账户信息..."):
            profile_info = client.account_profile()
        if not profile_info:
            error("获取账户信息失败")
            raise Exit(1)

        render_profile(profile_info)

@app.command()
def get(question_id: str) -> None:
    parse_result = parse_question_id(question_id)
    if not parse_result.ok():
        error(parse_result.error_message() or "题号解析失败")
        raise Exit(1)
    assert parse_result.question_id is not None
    normalized_question_id = parse_result.question_id
    session = load_session()
    if not session:
        warning("未登录, 请先执行 lc login")
        raise Exit(1)
    cookies = session.get("cookies")
    if not isinstance(cookies, dict):
        error("session 格式错误, 请重新执行 lc login")
        raise Exit(1)
    with LeetCodeClient(cookies) as client:
        with loading("正在获取题目索引..."):
            problem_data = client.problem_list(limit=5000)
        if not problem_data:
            error("获取题目索引失败")
            raise Exit(1)
        questions = problem_data.get("questions", [])
        problem_summaries = normalize_problem_summaries(questions)
        problem_summary = find_problem_by_id(problem_summaries, normalized_question_id)
        if not problem_summary:
            error(f"未找到题号 {normalized_question_id}")
            raise Exit(1)
        with loading("正在获取题目详情..."):
            target_problem_detail = client.problem_detail(problem_summary.title_slug)
        if not target_problem_detail:
            error(f"获取题目详情失败: {problem_summary.title_slug}")
            raise Exit(1)
        problem_detail = normalize_problem_detail(target_problem_detail)
    render_problem_detail(problem_detail)


@app.command()
def show(limit: int = 50, skip: int = 0) -> None:
    session = load_session()
    if not session:
        warning("未登录, 请先执行 lc login")
        raise Exit(1)
    cookies = session.get("cookies")
    if not isinstance(cookies, dict):
        error("session 格式错误, 请重新执行 lc login")
        raise Exit(1)
    with LeetCodeClient(cookies) as client:
        with loading("正在获取题目索引..."):
            problem_data = client.problem_list(limit=limit, skip=skip)
        if not problem_data:
            error("获取题目索引失败")
            raise Exit(1)
        questions = problem_data.get("questions", [])
        problem_summaries = normalize_problem_summaries(questions)
    render_problem_list(problem_summaries)
if __name__ == "__main__":
    app()
