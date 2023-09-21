import requests
import time
import parsel
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    """
    Realiza uma requisição HTTP GET para a URL especificada, com um intervalo
    mínimo de 1 segundo entre as requisições, utilizando um cabeçalho
    "user-agent" falso para simular um agente de usuário.

    Args:
        url (str): A URL de destino para a requisição.

    Returns:
        str or None: O conteúdo da resposta da requisição como texto, caso a
        requisição seja bem-sucedida, ou None em caso de falha na requisição.

    Raises:
        requests.RequestException: Exceção lançada se ocorrer um erro na
        realização da requisição.
    """

    headers = {"user-agent": "Fake user-agent"}

    try:
        time.sleep(1)
        response = requests.get(url=url, headers=headers, timeout=3)
        response.raise_for_status()

        return response.text
    except requests.RequestException:
        return None


# Requisito 2
def scrape_updates(html_content):
    """
    Realiza web scraping no conteúdo HTML fornecido e extrai os URLs das
    notícias ou atualizações encontrados na página.

    Args:
        html_content (str): O conteúdo HTML da página da web a ser analisada.

    Returns:
        list[str]: Uma lista de URLs das notícias ou atualizações encontrados
        na página. Retorna uma lista vazia se nenhum URL for encontrado.

    """
    html_selector = parsel.Selector(text=html_content)
    urls_news = html_selector.css(
        "article h2.entry-title a::attr(href)"
    ).getall()

    return [] if urls_news is None else urls_news


# Requisito 3
def scrape_next_page_link(html_content):
    """
    Realiza web scraping no conteúdo HTML fornecido e extrai o URL do link
    para a próxima página, quando disponível.

    Args:
        html_content (str): O conteúdo HTML da página da web a ser analisada.

    Returns:
        str or None: O URL do link para a próxima página, se encontrado, ou
        None se não houver um link para a próxima página.

    """
    html_selector = parsel.Selector(text=html_content)
    url_next = html_selector.css("a.next::attr(href)").get()

    return url_next


# Requisito 4
def scrape_news(html_content):
    """
    Realiza a extração de informações de uma página de notícias a partir do
    conteúdo HTML.

    Args:
        html_content (str): O conteúdo HTML da página da notícia.

    Returns:
        dict: Um dicionário contendo as informações extraídas, incluindo a URL,
        o título, a data de publicação, o autor, o tempo estimado de
        leitura, o resumo e a categoria da notícia.
    """

    html_selector = parsel.Selector(text=html_content)

    # scrape_news_get_url
    url = html_selector.xpath('//html/head/link[@rel="canonical"]/@href').get()

    # scrape_news_get_title
    title = html_selector.css("h1.entry-title::text").get()

    # scrap_news_timestamp
    timestamp = html_selector.css("li.meta-date::text").get()
    # scrap_news_writer
    writer = html_selector.css("li.meta-author a::text").get()

    # scrap_news_reading_time
    reading_time = html_selector.css("li.meta-reading-time::text").re_first(
        r"\d*"
    )

    # scrap_news_summary
    summary = html_selector.xpath(
        'string(//div[@class="entry-content"]/p)'
    ).get()

    # scrap_news_category
    category = html_selector.css("div.meta-category span.label::text").get()

    return {
        "url": url,
        "title": title.strip(),
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": int(reading_time),
        "summary": summary.strip(),
        "category": category,
    }


# Requisito 5
def get_tech_news(amount):
    url = "https://blog.betrybe.com/"
    urls = []

    while amount > 0:
        html_text = fetch(url)
        scraped_urls = scrape_updates(html_text)
        amount -= len(scraped_urls)

        if amount > 0:
            url = scrape_next_page_link(html_text)
            urls.extend(scraped_urls)
        else:
            end = len(scraped_urls) + amount
            urls.extend(scraped_urls[:end])

    scraped_news = [scrape_news(fetch(url)) for url in urls]
    create_news(scraped_news)
    return scraped_news


get_tech_news(46)
