import requests
import time
from config import USER_AGENT, REQUEST_TIMEOUT

HEADERS = {"User-Agent": USER_AGENT}

def fetch_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)

    except requests.exceptions.RequestException as e:
        raise Exception("Connection error while fetching {url}: {e}")

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch{url}: status code {response.status_code}")