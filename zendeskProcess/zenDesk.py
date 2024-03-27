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
    try:
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
                    updates = get_ticket_updates(ticket)
                    ticket_data = {
                        'ticket_id': ticket['id'],
                        'subject': ticket['subject'],
                        'status': ticket['status'],
                        'updates': updates
                    }
                    logger.info(f"Ticket ID: {ticket['id']}, Subject: {ticket['subject']}")
                    user_tickets[user_email].append(ticket_data)

        else:
            logger.info(f"Failed to retrieve tickets: {response.status_code}")
        logger.info(f"Fetching tickets for the user {user_email} - COMPLETED")
        return user_tickets
    except ConnectionError as e:
        logger.info(f"Connection fails towards Zendesk with error {e.args}.")
    except TimeoutError as f:
        logger.info(f"Connection timed out towards Zendesk with error {f.args}.")


def get_ticket_updates(ticket):
    # ticket_audit_url = f'{bbc().zendesk_base_url}tickets/{ticket["id"]}/audits.json'
    try:
        ticket_audit_url = f'{bbc().zendesk_base_url}tickets/{ticket["id"]}/comments.json'
        req_audit = requests.get(ticket_audit_url, headers=bbc().zendesk_headers)
        ticket_comments = req_audit.json()['comments']
        comment_data_dict = []
        for comment in ticket_comments:
            if comment['type'] == "Comment":
                if comment['public']:
                    comment_data = {
                        "body": comment['body'],
                        "timestamp": comment['created_at'],
                        "is_public": comment['public']
                    }
                    comment_data_dict.append(comment_data)
        return comment_data_dict
    except ConnectionError as e:
        logger.info(f"Connection fails towards Zendesk (comments URL) with error {e.args}.")
    except TimeoutError as f:
        logger.info(f"Connection timed out towards Zendesk (comments URL) with error {f.args}.")


if __name__ == '__main__':
    agent_email = 'jalero@cisco.com'
    get_ticket_per_users(agent_email)
