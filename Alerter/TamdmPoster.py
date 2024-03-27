import requests
import logging
from bbuddyClass import BuddyClassBlob as bbc

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Tam Alerter")

logger.info(f"Alerting TAM of ticket status change...")


def sendDMToTam(msg_to_send, user_id):
    """
    Sends the message alert to the TAM using their user_id.
    :param msg_to_send: string
    :param user_id: string
    :return: None
    """
    headers = {
        'Authorization': f'Bearer {bbc().tamBBbot_data["access_token"]}'
    }
    data = {
        'toPersonId': user_id,
        'markdown': msg_to_send
    }
    url = f'{bbc().webex_base_url}messages'
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            logger.info("Message successfully to TAM.")
        else:
            logger.info(f"Failed to send message. Status code: {response.status_code}")
    except ConnectionError as e:
        logger.info(f"Connection fails towards {url} with error {e.args}.")
    except TimeoutError as f:
        logger.info(f"Connection timed out towards {url} with error {f.args}.")
