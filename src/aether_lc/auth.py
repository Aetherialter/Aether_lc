import browser_cookie3
from pathlib import Path
import json

LC_DOMAIN = "leetcode.cn"
# BROWSER_LOADERS = [("Edge", browser_cookie3.edge), ("Chrome", browser_cookie3.chrome)]
BROWSER_LOADERS = [("Chrome", browser_cookie3.chrome)]

REQUIRED_COOKIE_NAMES = ("LEETCODE_SESSION", "csrftoken")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SESSION_DIR = PROJECT_ROOT / ".aether_lc"
SESSION_FILE = SESSION_DIR / "session.json"


def get_cookies_from_browser() -> tuple[str, dict[str, str]] | None:
    for browser_name, loader in BROWSER_LOADERS:
        try:
            cookie_jar = loader(domain_name=LC_DOMAIN)

        except Exception:
            continue

        cookies_dict = {
            cookie.name: cookie.value
            for cookie in cookie_jar
            if cookie.domain and cookie.domain.lstrip(".").endswith(LC_DOMAIN)
        }
        if all(name in cookies_dict for name in REQUIRED_COOKIE_NAMES):
            return browser_name, {
                "LEETCODE_SESSION": cookies_dict["LEETCODE_SESSION"],
                "csrftoken": cookies_dict["csrftoken"],
            }

    return None


def get_cookies_from_input() -> dict[str, str] | None:
    cookies = input("请输入你的cookies\n")
    cookies_dict = {}
    for item in cookies.split(";"):
        if "=" in item:
            key, val = item.strip().split("=", 1)
            cookies_dict[key] = val

    if all(name in cookies_dict for name in REQUIRED_COOKIE_NAMES):
        return {
            "LEETCODE_SESSION": cookies_dict["LEETCODE_SESSION"],
            "csrftoken": cookies_dict["csrftoken"],
        }

    return None


def save_session(session_data: dict) -> None:
    file_path = SESSION_FILE
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, indent=4, ensure_ascii=False)


def load_session() -> dict | None:
    file_path = SESSION_FILE
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


if __name__ == "__main__":
    pass
