from typer import Typer, Exit
from aether_lc.auth import (
    get_cookies_from_browser,
    get_cookies_from_input,
    load_session,
    save_session,
)
from aether_lc.client import LeetCodeClient
from aether_lc.ui import loading, success, warning, error, render_profile


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


if __name__ == "__main__":
    app()
