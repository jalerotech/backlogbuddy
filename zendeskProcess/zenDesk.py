import json
import requests
import logging
from bbuddyClass import BuddyClassBlob as bbc

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Zendesk Data Script')


def get_ticket_per_users(user_email) -> dict[list]:
    """
    Fetches the tickets assigned to the user using the agent's email address which is known to Zendesk.
    for example jalero@cisco.com.
    :param user_email: jalero@cisco.com
    :return: List of tickets
    """
    user_tickets = {}
    logger.info(f"Fetching tickets for the user {user_email} - STARTED")
    zendesk_response = requests.get(f"{bbc().zendesk_user_url}search.json?query={user_email}",
                                    headers=bbc().zendesk_headers)
    zendesk_json_resp = json.loads(zendesk_response.content)
    agent_id = zendesk_json_resp['users'][0]['id']

    zendesk_url = f'{bbc().zendesk_user_url}{agent_id}/tickets/assigned.json'
    response = requests.get(zendesk_url, headers=bbc().zendesk_headers)

    # Handle the response
    if response.status_code == 200:
        tickets = response.json()['tickets']
        user_tickets.update({user_email: []})
        for ticket in tickets:
            if ticket['status'] != 'closed':
                ticket_data = {
                    'ticket_id': ticket['id'],
                    'subject': ticket['subject'],
                    'status': ticket['status']
                }
                logger.info(f"Ticket ID: {ticket['id']}, Subject: {ticket['subject']}")
                user_tickets[user_email].append(ticket_data)

    else:
        logger.info(f"Failed to retrieve tickets: {response.status_code}")
    logger.info(f"Fetching tickets for the user {user_email} - COMPLETED")
    return user_tickets


if __name__ == '__main__':
    agent_email = 'jalero@cisco.com'
    get_ticket_per_users(agent_email)
