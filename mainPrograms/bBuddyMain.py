from tamStatus.getTamStatus import ret_tam_on_pto_list, is_tam_on_pto
from zendeskProcess.zenDesk import get_ticket_per_users
from Alerter.alertTAM import send_message_to_email
from tools.shiftStatus import theatre_shift_time, is_shift_over
from datetime import datetime
from bbuddyClass import BuddyClassBlob as bbc
import logging
import time
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Zendesk Data')

currentDateAndTime = datetime.now()
today = currentDateAndTime.strftime('%A')

handled_tickets = []


def backlogBuddyMain():
    """
    Runs the main backlog buddy program.
    :return:
    """
    while True:

        if (today == "Saturday" and (currentDateAndTime.hour > 2 and currentDateAndTime.minute > 0)) or (
                today == "Sunday"):
            logger.info("Weekend is here, waiting for new week to begin.")
        else:
            logger.info("Running BackLog Buddy Main program")
            for tam_email in bbc().tams_email_list:
                # Checks if TAM is on PTO (returns boolean -> True if on PTO)
                is_on_pto, tam_region = is_tam_on_pto(tam_email)
                if is_on_pto:
                    # If TAM is on PTO no need to run the backlog buddy service for them, so they're skipped.
                    logger.info(f"Skipping TAM -> {tam_email} due to PTO status.")
                else:
                    if is_shift_over(tam_region, tam_email) is None or False:
                        logger.info(f'Shift still active for TAM {tam_email} in {tam_region} region.')
                        logger.info(f"TAM -> {tam_email}is not on PTO.")
                        logger.info(f"Checking for TAM -> {tam_email} tickets_data with 'open' status - STARTED.")
                        tickets_data = get_ticket_per_users(tam_email)
                        logger.info(f"Checking for TAM -> {tam_email} tickets_data with 'open' status - COMPLETED.")
                        for ticket_data in tickets_data[tam_email]:
                            # Filter on ticket_data for tickets with OPEN status.
                            if ticket_data['status'] == "open":
                                if ticket_data['ticket_id'] not in handled_tickets:
                                    logger.info(f"Posting open ticket_data alert to TAM {tam_email} -> STARTED.")
                                    # Sends the message to the TAM's email - Direct message - on WEbEx teams
                                    # if tam_email == 'jalero@cisco.com':
                                    #     send_message_to_email(tam_email, ticket_data)
                                    send_message_to_email(tam_email, ticket_data)
                                    # Logs the ticket_data as already handled to avoid any duplicates
                                    handled_tickets.append(ticket_data['ticket_id'])
                                    logger.info(f"Posting open ticket_data alert to TAM {tam_email} -> COMPLETED.")
                    else:
                        logger.info(f"Shift is over for TAM {tam_email} in {tam_region} region.")
            logger.info(f"Handled tickets_data so far -> {handled_tickets}")
        logger.info(f"Pausing for 10 seconds..")
        time.sleep(10)


if __name__ == '__main__':
    # List_of_tams = ['jalero@cisco.com', 'kvindas@cisco.com', 'dforcade@cisco.com', 'nnwobodo@cisco.com']
    List_of_tams = ['jalero@cisco.com']
    # backlogBuddyMain(bbc().tams_email_list)
    backlogBuddyMain()
