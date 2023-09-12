import requests
import time


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
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
