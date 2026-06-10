from dataclasses import dataclass
from enum import Enum
from typing import Any


class QuestionIdError(str, Enum):
    EMPTY = "empty"
    NOT_DECIMAL = "not_decimal"
    NOT_POSITIVE = "not_positive"
    LEADING_ZERO = "leading_zero"


QUESTION_ID_ERROR_MESSAGES = {
    QuestionIdError.EMPTY: "题号不能为空",
    QuestionIdError.NOT_DECIMAL: "题号必须是正整数",
    QuestionIdError.NOT_POSITIVE: "题号必须大于 0",
    QuestionIdError.LEADING_ZERO: "题号不能以 0 开头",
}


@dataclass(frozen=True)
class ParseQuestionIdResult:
    question_id: str | None = None
    error: QuestionIdError | None = None

    @property
    def ok(self) -> bool:
        return self.error is None

    @property
    def error_message(self) -> str | None:
        if self.error is None:
            return None
        return QUESTION_ID_ERROR_MESSAGES[self.error]


@dataclass(frozen=True)
class ProblemSummary:
    question_id: str
    title: str
    title_slug: str
    difficulty: str
    paid_only: bool
    tags: list[str]


@dataclass(frozen=True)
class ProblemDetail:
    question_id: str
    submit_question_id: str
    title: str
    title_slug: str
    difficulty: str
    tags: list[str]
    content_html: str
    python_code: str | None


def parse_question_id(raw: str) -> ParseQuestionIdResult:
    text = raw.strip()

    if not text:
        return ParseQuestionIdResult(error=QuestionIdError.EMPTY)

    if not text.isdecimal():
        return ParseQuestionIdResult(error=QuestionIdError.NOT_DECIMAL)

    if text == "0":
        return ParseQuestionIdResult(error=QuestionIdError.NOT_POSITIVE)

    if text.startswith("0"):
        return ParseQuestionIdResult(error=QuestionIdError.LEADING_ZERO)

    return ParseQuestionIdResult(question_id=text)


def normalize_problem_summary(raw: dict[str, Any]) -> ProblemSummary:
    question_id = raw.get("frontendQuestionId", "")
    question_id = str(question_id) if isinstance(question_id, (str, int)) else ""
    title = raw.get("title", "")
    title_slug = raw.get("titleSlug", "")
    difficulty = raw.get("difficulty", "")
    paid_only = bool(raw.get("paidOnly", False))
    tags = [tag.get("name", "") for tag in raw.get("topicTags", [])]

    return ProblemSummary(
        question_id=question_id,
        title=title,
        title_slug=title_slug,
        difficulty=difficulty,
        paid_only=paid_only,
        tags=tags,
    )


def normalize_problem_summaries(
    raw_items: list[dict[str, Any]],
) -> list[ProblemSummary]:
    summaries = [normalize_problem_summary(raw) for raw in raw_items]
    return summaries


def find_problem_by_id(
    problems: list[ProblemSummary], question_id: str
) -> ProblemSummary | None:
    for problem in problems:
        if question_id == problem.question_id:
            return problem
    return None


def extract_python_code(code_snippets: list[dict[str, Any]]) -> str | None:
    for snippet in code_snippets:
        if snippet.get("langSlug") == "python3":
            return snippet.get("code", "")

    return None


def normalize_problem_detail(raw: dict[str, Any]) -> ProblemDetail:
    tags = [tag.get("name", "") for tag in raw.get("topicTags", [])]

    return ProblemDetail(
        question_id=raw.get("questionFrontendId", ""),
        submit_question_id=raw.get("questionId", ""),
        title=raw.get("translatedTitle") or raw.get("title", ""),
        title_slug=raw.get("titleSlug", ""),
        difficulty=raw.get("difficulty", ""),
        tags=tags,
        content_html=raw.get("translatedContent") or raw.get("content", ""),
        python_code=extract_python_code(raw.get("codeSnippets", [])),
    )
