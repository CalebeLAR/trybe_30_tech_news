from tech_news.analyzer.reading_plan import (
    ReadingPlanService,
)  # noqa: F401, E261, E501
import pytest

mongodb = [
    {
        "title": "title 4  min new",
        "reading_time": 4,
    },
    {
        "title": "title 3 min new",
        "reading_time": 3,
    },
    {
        "title": "title 10 min new",
        "reading_time": 10,
    },
    {
        "title": "title 12 min new",
        "reading_time": 12,
    },
    {
        "title": "title 15 min new",
        "reading_time": 15,
    },
]

return_reading_plan = {
    "readable": [
        {
            "unfilled_time": 3,
            "chosen_news": [
                (
                    "title 4  min new",
                    4,
                ),
                (
                    "title 3 min new",
                    3,
                ),
            ],
        },
        {
            "unfilled_time": 0,
            "chosen_news": [
                (
                    "title 10 min new",
                    10,
                )
            ],
        },
    ],
    "unreadable": [
        ("title 12 min new", 12),
        ("title 15 min new", 15),
    ],
}


def test_reading_plan_group_news(monkeypatch):
    def mock_find_news():
        return mongodb

    monkeypatch.setattr(
        "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy",
        mock_find_news,
    )

    # caso receba um parametro inválido
    with pytest.raises(
        ValueError, match="Valor 'available_time' deve ser maior que zero"
    ):
        ReadingPlanService().group_news_for_available_time(-1)

    returned = ReadingPlanService().group_news_for_available_time(10)
    print(ReadingPlanService().group_news_for_available_time(10))

    assert returned == return_reading_plan
