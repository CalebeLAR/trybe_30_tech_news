from tech_news.database import search_news
import re


# Requisito 7
def search_by_title(title):
    """Seu código deve vir aqui"""
    result = list()
    regex = re.compile(title.lower(), re.IGNORECASE)
    searched_news = search_news({"title": {"$regex": regex}})

    if not searched_news:
        return []

    for new in searched_news:
        result.append((new["title"], new["url"]))

    return result


# Requisito 8
def search_by_date(date):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    raise NotImplementedError
