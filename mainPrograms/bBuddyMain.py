from tamStatus.getTamStatus import is_tam_on_pto
from zendeskProcess.zenDesk import get_ticket_per_users
from Alerter.alertTAM import send_message_to_email
from tools.shiftStatus import is_shift_over
from datetime import datetime
from bbuddyClass import BuddyClassBlob as bbc
from tools.shiftStatusClass import ShiftStatus as sSc
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


def backlogBuddy(email):
    """
    Runs the backlog buddy program with the tam email address as input parameter.
    :return:
    """
    if bbc().is_weekend():
        logger.info("Weekend is here, waiting for new week to begin.")
    else:
        logger.info("Running BackLog Buddy Main program")
        # Checks and returns TAM PTO status and their region taking the TAM's email address as input.
        is_on_pto, tam_region = is_tam_on_pto(email)
        if is_on_pto:
            # If TAM is on PTO no need to run the backlog buddy service for them, so they're skipped.
            logger.info(f"Skipping TAM -> {email} due to PTO status.")
        else:
            if sSc().is_shift_over(tam_region['region'], email):
            # if is_shift_over(tam_region['region'], email):
                logger.info(f"Shift is over for TAM {email} in {tam_region['region']} region.")
            else:
                logger.info(f"Shift still active for TAM {email} in {tam_region['region']} region.")
                logger.info(f"TAM -> {email}is not on PTO.")
                logger.info(f"Checking for TAM -> {email} tickets_data with 'open' status - STARTED.")
                tickets_data = get_ticket_per_users(email)
                logger.info(f"Checking for TAM -> {email} tickets_data with 'open' status - COMPLETED.")
                for ticket_data in tickets_data[email]:
                    # Filter on ticket_data for tickets with OPEN status.
                    if ticket_data['status'] == "open":
                        if ticket_data['ticket_id'] not in handled_tickets:
                            logger.info(f"Posting open ticket_data alert to TAM {email} -> STARTED.")
                            # Sends the message to the TAM's email - Direct message - on WEbEx teams
                            if email == 'jalero@cisco.com':
                                send_message_to_email(email, ticket_data, tam_region['user_id'])
                            # send_message_to_email(email, ticket_data, tam_region['user_id'])
                            # Logs the ticket_data as already handled to avoid any duplicates
                            handled_tickets.append(ticket_data['ticket_id'])
                            logger.info(f"Posting open ticket_data alert to TAM {email} -> COMPLETED.")
    logger.info(f"Handled tickets_data so far -> {handled_tickets}")


def main():
    logger.info("Running Main program")
    while True:
        for tam_mail in bbc().tams_email_list:
            # Run the bb script with the tam_email address from the hard list in the "bbuddyMainClass.py" that instantiated with "bbc().tams_email_list".
            backlogBuddy(tam_mail)
        logger.info(f"Pausing for 30 seconds..")
        time.sleep(30)


if __name__ == '__main__':
    main()
