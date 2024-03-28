import requests
import logging
import json

from requests.exceptions import ProxyError

from bbuddyClass import BuddyClassBlob as bbc

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('retPeopleData')


def retPeopleData(tam_email) -> json:
    """
    Produces a json file of the requests sent to get people status.
    :param tam_email: email address of TAM.
    :return: json file containing teh TAM data.
    """
    url = f'{bbc().webex_base_url}people'
    params = {
        "email": tam_email
    }
    try:
        logger.info(f"Fetching WebEx data for TAM {tam_email} -> STARTED")
        webex_resp = requests.get(url, params=params, headers=bbc().webex_headers)
        logger.info(f"Fetching WebEx data for TAM {tam_email} -> COMPLETED")
        return json.loads(webex_resp.content)
    except ConnectionError as e:
        logger.info(f"Connection fails towards {url} with error {e.args}.")
        return None
    except TimeoutError as f:
        logger.info(f"Connection timed out towards {url} with error {f.args}.")
        return None
    except ProxyError as f:
        logger.info(f"Connection timed out towards {url} with due to ProxyError {f.args}.")
        return None
