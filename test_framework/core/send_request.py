import requests

from requests.sessions import Session
from urllib3.exceptions import InsecureRequestWarning
from common.settings import API_TIMEOUT


def send_request(url, header, method, **kwargs):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    try:
        session = Session()
        response = session.request(
            method=method,
            url=url,
            headers=header,
            timeout=API_TIMEOUT,
            verify=False,
            **kwargs
        )
        return response
    except requests.exceptions.ConnectionError as e:
        # TODO: log error
        raise e
    except requests.exceptions.HTTPError as e:
        # TODO: log error
        raise e
    except requests.exceptions.RequestException as e:
        # TODO: log error
        raise e