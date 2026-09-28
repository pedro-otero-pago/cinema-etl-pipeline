import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import USER_AGENT, REQUEST_TIMEOUT

HEADERS = {"User-Agent": USER_AGENT}

_retry = Retry(
    total=4,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)

_session = requests.Session()
_session.headers.update(HEADERS)
_session.mount("https://", HTTPAdapter(max_retries=_retry))
_session.mount("http://", HTTPAdapter(max_retries=_retry))


def fetch_html(url):
    try:
        response = _session.get(url, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Connection error while fetching {url}: {e}") from e

    if response.status_code == 200:
        return response.text
    raise Exception(f"Failed to fetch {url}: status code {response.status_code}")