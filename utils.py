import requests
from bs4 import BeautifulSoup

def fetch_text_from_url(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        return ""
