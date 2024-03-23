import requests
import logging
from bbuddyClass import BuddyClassBlob as bbc

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Tam Alerter")


def send_message_to_email(email, ticket):
    """
    Sends Alert message directly to TAM using their email address.
    :param email: TAM's email address
    :param ticket: Ticket data in dict format.
    :return:
    """
    logger.info(f"Alerting TAM of ticket status change...")
    # Header using the TAM Backlog Bot access token.
    headers = {
        'Authorization': f'Bearer {bbc().tamBBbot_data["access_token"]}'
    }
    # Add the TAM email as a parameter.
    params = {
        'email': email
    }
    msg_to_send = f"### Ticket status change !!! ({ticket['ticket_id']}) \n " \
                  f"Ticket number: #[{ticket['ticket_id']}]({bbc().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                  f"Subject: {ticket['subject']} \n " \
                  f"***Status***: {ticket['status']} \n " \
                  f"***Updated at***: {ticket['updates'][-1]['timestamp']} \n "  \
                  f"***Latest external update***: \n {ticket['updates'][-1]['body']}" \

    # Fetches and parses out the user_id using the user email as parameter.
    url = f'{bbc().webex_base_url}people'
    response = requests.get(url, headers=headers, params=params)
    user_data = response.json()
    if 'items' in user_data and len(user_data['items']) > 0:
        try:
            user_id = user_data['items'][0]['id']

            # Send a message to the user using their Webex ID
            data = {
                'toPersonId': user_id,
                'markdown': msg_to_send
            }
            response = requests.post(f'{bbc().webex_base_url}messages', headers=headers, json=data)
            if response.status_code == 200:
                logger.info("Message successfully to TAM.")
            else:
                logger.info(f"Failed to send message. Status code: {response.status_code}")
        except KeyError as e:
            logger.info("User ID not found.")
    else:
        logger.info("User not found.")


if __name__ == '__main__':
    # Example usage
    pass
    # email = 'jalero@cisco.com'
    # message = 'Hello, this is a test message from the Webex API.'
    #
    # send_message_to_email(email, message, access_token)
