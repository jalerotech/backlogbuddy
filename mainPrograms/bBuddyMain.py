from bbuddyClass import BuddyClassBlob as bbc
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


def backlogBuddyMain(tams):
    while True:
        for tam in tams:
            logger.info("Running BackLog Buddy Main program")
            tickets = get_ticket_per_users(tam)
            for ticket in tickets[tam]:
                if ticket['ticket_id'] not in handled_tickets:
                    if ticket['status'] == "open":
                        send_message_to_email(tam, ticket)
                        handled_tickets.append(ticket['ticket_id'])
                else:
                    logger.info(f"Ticket {ticket['ticket_id']} has already been processed")
            logger.info(f"Handled tickets so far -> {handled_tickets}")
            logger.info(f"Pausing for 10 seconds..")
            time.sleep(10)


if __name__ == '__main__':
    List_of_tams = ['jalero@cisco.com', 'kvindas@cisco.com', 'dforcade@cisco.com', 'nnwobodo@cisco.com']
    backlogBuddyMain(List_of_tams)
