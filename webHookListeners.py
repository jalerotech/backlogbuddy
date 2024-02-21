import requests
import logging
from bbuddyClass import BuddyClassBlob as bbc
from webexteamssdk import WebexTeamsAPI, Webhook

logger = logging.getLogger("Change Alerter script.")

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

auth_token = bbc().tamBBbot_data['access_token']
room_id = bbc().tqw_room_id
# tamBBbot_room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vNDRlODBkOTAtYzk3MS0xMWVlLWFkZWEtYmRkZjY2MzQ3MGUz"
api = WebexTeamsAPI(access_token=auth_token)


def process_incoming_msg(msg):
    print(f"Received Message: {msg.text}")


def Listener() -> None:
    """
    :return: None
    """

    while True:
        try:
            for message in api.messages.list(webhookData=True, roomId=room_id):
                process_incoming_msg(message)
        except KeyboardInterrupt as e:
            break


if __name__ == '__main__':
    Listener()
