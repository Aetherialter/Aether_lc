from typer import Exit

from aether_lc.auth import load_session
from aether_lc.client import LeetCodeClient
from aether_lc.problem import (
    ProblemDetail,
    ProblemSummary,
    find_problem_by_id,
    normalize_problem_detail,
    normalize_problem_summaries,
    parse_question_id,
)
from aether_lc.ui import error, loading, warning


def _load_cookies_from_session() -> dict[str, str]:
    session = load_session()
    if not session:
        warning("未登录, 请先执行 lc login")
        raise Exit(1)
    cookies = session.get("cookies")
    if not isinstance(cookies, dict):
        error("session 格式错误, 请重新执行 lc login")
        raise Exit(1)
    return cookies


def _parse_question_id_or_exit(question_id: str) -> str:
    parse_result = parse_question_id(question_id)
    if not parse_result.ok():
        error(parse_result.error_message() or "题号解析失败")
        raise Exit(1)
    assert parse_result.question_id is not None
    return parse_result.question_id


def _find_problem_summary_by_question_id(
    problems: list[ProblemSummary],
    question_id: str,
) -> ProblemSummary:
    problem_summary = find_problem_by_id(problems, question_id)
    if not problem_summary:
        error(f"未找到题号 {question_id}")
        raise Exit(1)
    return problem_summary


def get_user_status() -> dict:
    cookies = _load_cookies_from_session()
    with LeetCodeClient(cookies) as client:
        user_status = client.user_status()
    if not user_status or not user_status.get("isSignedIn"):
        error("session 有问题或已过期")
        raise Exit(1)
    return user_status


def get_account_profile() -> dict:
    cookies = _load_cookies_from_session()
    with LeetCodeClient(cookies) as client:
        with loading("正在获取账户信息..."):
            account_profile = client.account_profile()
    if not account_profile:
        error("获取账户信息失败")
        raise Exit(1)
    return account_profile


def get_problem_summaries(limit: int = 50, skip: int = 0) -> list[ProblemSummary]:
    cookies = _load_cookies_from_session()
    with LeetCodeClient(cookies) as client:
        with loading("正在获取题目索引..."):
            problem_list_data = client.problem_list(limit=limit, skip=skip)
    if not problem_list_data:
        error("获取题目索引失败")
        raise Exit(1)
    questions = problem_list_data.get("questions", [])
    return normalize_problem_summaries(questions)


def get_problem_detail_by_question_id(question_id: str) -> ProblemDetail:
    normalized_question_id = _parse_question_id_or_exit(question_id)
    cookies = _load_cookies_from_session()
    with LeetCodeClient(cookies) as client:
        with loading("正在获取题目索引..."):
            problem_list_data = client.problem_list(limit=5000)
        if not problem_list_data:
            error("获取题目索引失败")
            raise Exit(1)
        questions = problem_list_data.get("questions", [])
        problem_summaries = normalize_problem_summaries(questions)
        problem_summary = _find_problem_summary_by_question_id(
            problem_summaries,
            normalized_question_id,
        )
        with loading("正在获取题目详情..."):
            problem_detail_data = client.problem_detail(problem_summary.title_slug)
        if not problem_detail_data:
            error(f"获取题目详情失败: {problem_summary.title_slug}")
            raise Exit(1)
        problem_detail = normalize_problem_detail(problem_detail_data)
    return problem_detail
