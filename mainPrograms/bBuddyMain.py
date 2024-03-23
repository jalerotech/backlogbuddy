from bbuddyClass import BuddyClassBlob as bbc
from tamStatus.getTamStatus import ret_tam_on_pto_list, is_tam_on_pto
from zendeskProcess.zenDesk import get_ticket_per_users
from Alerter.alertTAM import send_message_to_email
import logging
import time
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Zendesk Data')

handled_tickets = []


def backlogBuddyMain():
    while True:
        logger.info("Running BackLog Buddy Main program")
        for tam_email in bbc().tams_email_list:
            if is_tam_on_pto(tam_email):
                logger.info(f"Skipping TAM -> {tam_email} due to PTO status.")
            else:
                logger.info(f"TAM -> {tam_email}is not on PTO.")
                logger.info(f"Checking for tickets with 'open' status - STARTED.")
                tickets = get_ticket_per_users(tam_email)
                logger.info(f"Checking for tickets with 'open' status - COMPLETED.")
                for ticket in tickets[tam_email]:
                    if ticket['status'] == "open":
                        if ticket['ticket_id'] not in handled_tickets:
                            logger.info(f"Posting open ticket alert to TAM {tam_email} -> STARTED.")
                            print(ticket)
                            # send_message_to_email(tam, ticket)
                            handled_tickets.append(ticket['ticket_id'])
                            logger.info(f"Posting open ticket alert to TAM {tam_email} -> COMPLETED.")

        logger.info(f"Handled tickets so far -> {handled_tickets}")
        logger.info(f"Pausing for 10 seconds..")
        time.sleep(10)


if __name__ == '__main__':
    # List_of_tams = ['jalero@cisco.com', 'kvindas@cisco.com', 'dforcade@cisco.com', 'nnwobodo@cisco.com']
    List_of_tams = ['jalero@cisco.com']
    # backlogBuddyMain(bbc().tams_email_list)
    backlogBuddyMain()
