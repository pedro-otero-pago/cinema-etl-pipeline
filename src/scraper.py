import requests
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

    except requests.exceptions.RequestException as e:
        raise Exception("Connection error while fetching {url}: {e}")

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch{url}: status code {response.status_code}")