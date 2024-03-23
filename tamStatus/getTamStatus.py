import requests
import logging
import json
from bbuddyClass import BuddyClassBlob as bbc

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('TAM PTO Bot')


def ret_tam_on_pto_list() -> list:
    logger.info("Returning List of Team members that are Out Of Office. - STARTED")
    """
    Returns a list of TAMS members with status set to OutOfOffice
    """
    ooo_tams = []
    country_list = []
    for tam_email in bbc().tams_email_list:
        # Passing the email as a parameter -> this is needed for the @ symbol on the email be encoded with the "urllib.parse" lib.
        params = {
            "email": tam_email
        }
        url = f'{bbc().webex_base_url}people'
        webex_resp = requests.get(url, params=params, headers=bbc().webex_headers)
        for country in json.loads(webex_resp.content)['items'][0]['addresses']:
            country_list.append(country['country'])
        status = json.loads(webex_resp.content)['items'][0]['status']
        displayName = json.loads(webex_resp.content)['items'][0]['displayName']
        email = json.loads(webex_resp.content)['items'][0]['emails']
        region = json.loads(webex_resp.content)['items'][0]['addresses'][0]['country']
        if status == 'OutOfOffice':
            msg_data = {
                'name': displayName,
                'status': status,
                'email': email,
                'region': region
            }
            ooo_tams.append(msg_data)
    logger.info("Returning List of Team members that are Out Of Office. - COMPLETED")
    logger.info(f"Returning list -> {ooo_tams}")
    return ooo_tams


def is_tam_on_pto(tam_email) -> bool:
    logger.info("Cross-checking TAM email with ooo TAMs list -> STARTED")
    is_on_pto = False
    ooo_tams = ret_tam_on_pto_list()
    for tam_status in ooo_tams:
        if tam_email == tam_status['email'][0]:
            is_on_pto = True
    logger.info("Cross-checking TAM email with ooo TAMs list -> COMPLETED")
    return is_on_pto


if __name__ == '__main__':
    print(ret_tam_on_pto_list())
