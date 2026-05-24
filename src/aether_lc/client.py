import httpx
BASE_URL = "https://leetcode.cn"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Safari/537.36"
)

USER_STATUS_QUERY = {
    "query": """
        query userStatus {
            userStatus {
                isSignedIn
                username
                realName
                avatar
                isPremium
            }
        }
    """
}

DIFFICULTY_MAP = {
    1: "Easy",
    2: "Medium",
    3: "Hard",
}


class LeetCodeClient:
    def __init__(self, cookies: dict[str, str] | None = None):
        self.client = httpx.Client(
            base_url=BASE_URL,
            follow_redirects=True,
            timeout=20.0,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json, text/plain, */*",
                "Origin": BASE_URL,
                "Referer": f"{BASE_URL}/",
            },
        )
        if cookies:
            self.client.cookies.update(cookies)
    
    def user_status(self) -> dict | None:
        try:
            response = self.client.post("/graphql/", json=USER_STATUS_QUERY, timeout=10)
            response.raise_for_status()
            result = response.json()
        except (httpx.HTTPError, ValueError):
            return None
        return result.get("data", {}).get("userStatus")

    def problem_stats(self) -> dict | None:
        try:
            response = self.client.get("/api/problems/all/", timeout=20)
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError):
            return None

        stats = {
            "solved": {
                "All": 0,
                "Easy": 0,
                "Medium": 0,
                "Hard": 0,
            },
            "total": {
                "All": 0,
                "Easy": 0,
                "Medium": 0,
                "Hard": 0,
            },
        }

        for item in payload.get("stat_status_pairs", []):
            difficulty_level = item.get("difficulty", {}).get("level")
            difficulty = DIFFICULTY_MAP.get(difficulty_level)

            if not difficulty:
                continue

            stats["total"]["All"] += 1
            stats["total"][difficulty] += 1

            if item.get("status") == "ac":
                stats["solved"]["All"] += 1
                stats["solved"][difficulty] += 1
        
        return stats
    
    def account_profile(self) -> dict | None:
        status = self.user_status()
        if not status or not status.get("isSignedIn"):
            return None
        problem_profile = self.problem_stats()
        if not problem_profile:
            return None
        return {
            "username": status.get("username"),
            "real_name": status.get("realName"),
            "avatar": status.get("avatar"),
            "is_premium": status.get("isPremium"),
            "solved": problem_profile.get("solved"),
            "total": problem_profile.get("total"),
        }

    def close(self) -> None:
        self.client.close()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
if __name__ == '__main__':
    pass