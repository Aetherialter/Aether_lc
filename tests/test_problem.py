from aether_lc.problem import normalize_problem_detail


def test_normalize_problem_detail_keeps_frontend_and_submit_question_ids() -> None:
    detail = normalize_problem_detail(
        {
            "questionId": "2265",
            "questionFrontendId": "2161",
            "translatedTitle": "根据给定数字划分数组",
            "title": "Partition Array According to Given Pivot",
            "titleSlug": "partition-array-according-to-given-pivot",
            "difficulty": "Medium",
            "translatedContent": "<p>content</p>",
            "content": "",
            "topicTags": [{"name": "Array"}],
            "codeSnippets": [
                {"langSlug": "python3", "code": "class Solution:\n    pass"}
            ],
        }
    )

    assert detail.question_id == "2161"
    assert detail.submit_question_id == "2265"
    assert detail.title_slug == "partition-array-according-to-given-pivot"
