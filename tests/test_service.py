import pytest
from typer import Exit

from aether_lc import service
from aether_lc.client import ClientErrorKind, ClientResult
from aether_lc.workspace import ProblemMetadata


class FakeClient:
    def __init__(self, cookies: dict[str, str]) -> None:
        self.cookies = cookies

    def __enter__(self) -> "FakeClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        return None


def test_get_user_status_exits_on_client_error(monkeypatch) -> None:
    class ErrorClient(FakeClient):
        def user_status(self) -> ClientResult:
            return ClientResult(error=ClientErrorKind.NETWORK)

    monkeypatch.setattr(service, "load_session", lambda: {"cookies": {"k": "v"}})
    monkeypatch.setattr(service, "LeetCodeClient", ErrorClient)

    with pytest.raises(Exit):
        service.get_user_status()


def test_get_problem_summaries_exits_on_invalid_response(monkeypatch) -> None:
    class InvalidProblemListClient(FakeClient):
        def problem_list(self, limit: int = 50, skip: int = 0) -> ClientResult:
            return ClientResult(data=None)

    monkeypatch.setattr(service, "load_session", lambda: {"cookies": {"k": "v"}})
    monkeypatch.setattr(service, "LeetCodeClient", InvalidProblemListClient)

    with pytest.raises(Exit):
        service.get_problem_summaries()


def test_submit_current_solution_returns_submission_result_data(monkeypatch) -> None:
    class SubmitClient(FakeClient):
        def submit_solution(
            self,
            title_slug: str,
            question_id: str,
            code: str,
        ) -> ClientResult:
            assert title_slug == "two-sum"
            assert question_id == "1"
            assert code == "class Solution:\n    pass"
            return ClientResult(data=123)

        def get_submission_result(self, submission_id: int) -> ClientResult:
            assert submission_id == 123
            return ClientResult(
                data={
                    "state": "SUCCESS",
                    "status_msg": "Accepted",
                }
            )

    monkeypatch.setattr(service, "load_session", lambda: {"cookies": {"k": "v"}})
    monkeypatch.setattr(service, "LeetCodeClient", SubmitClient)
    monkeypatch.setattr(
        service,
        "parse_solution_submission",
        lambda: (
            ProblemMetadata(
                problem_id="1",
                submit_question_id="1",
                title="Two Sum",
                title_slug="two-sum",
            ),
            "class Solution:\n    pass",
        ),
    )

    result = service.submit_current_solution()

    assert result == {
        "state": "SUCCESS",
        "status_msg": "Accepted",
    }
