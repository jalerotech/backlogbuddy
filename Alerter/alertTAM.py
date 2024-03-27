import requests
import logging
from Alerter.TamdmPoster import sendDMToTam
from Alerter.alertMsgGenerator import generateAlertMsg

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Tam Alerter")


def send_message_to_email(email, ticket, user_id) -> None:
    """
    Gets the message to sent from the "generateAlertMsg" function then posts the message using the "sendDMToTam" to the TAM.
    :param email: TAM's email address
    :param ticket: Ticket data in dict format.
    :param user_id: WebEx user_id -> str
    :return: None
    """
    logger.info(f"Alerting TAM-> {email} of ticket status change...")

    msg_to_send = generateAlertMsg(ticket)
    sendDMToTam(msg_to_send, user_id)
