import pytest

from aether_lc import workspace
from aether_lc.workspace import ProblemMetadata, WorkspaceError


def test_build_solution_content_writes_metadata_and_submit_markers() -> None:
    metadata = ProblemMetadata(
        problem_id="1",
        title="Two Sum",
        title_slug="two-sum",
    )

    content = workspace.build_solution_content(
        "class Solution:\n    pass",
        metadata,
    )

    assert "# @lc problem_id: 1" in content
    assert "# @lc title: Two Sum" in content
    assert "# @lc title_slug: two-sum" in content
    assert "# @lc submit_begin" in content
    assert "# @lc submit_end" in content
    assert "def run_cases() -> None:" in content


def test_parse_solution_submission_reads_metadata_and_submit_code(
    tmp_path,
    monkeypatch,
) -> None:
    solution_file = tmp_path / "solution.py"
    solution_file.write_text(
        "\n".join(
            [
                "# @lc problem_id: 1",
                "# @lc title: Two Sum",
                "# @lc title_slug: two-sum",
                "",
                "# @lc submit_begin",
                "class Solution:",
                "    pass",
                "# @lc submit_end",
                "",
                "def run_cases() -> None:",
                "    pass",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(workspace, "SOLUTION_FILE", solution_file)

    metadata, code = workspace.parse_solution_submission()

    assert metadata == ProblemMetadata(
        problem_id="1",
        title="Two Sum",
        title_slug="two-sum",
    )
    assert code == "class Solution:\n    pass"


def test_parse_solution_submission_rejects_missing_marker(
    tmp_path,
    monkeypatch,
) -> None:
    solution_file = tmp_path / "solution.py"
    solution_file.write_text(
        "\n".join(
            [
                "# @lc problem_id: 1",
                "# @lc title: Two Sum",
                "# @lc title_slug: two-sum",
                "class Solution:",
                "    pass",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(workspace, "SOLUTION_FILE", solution_file)

    with pytest.raises(WorkspaceError, match="提交区域标记不完整"):
        workspace.parse_solution_submission()
