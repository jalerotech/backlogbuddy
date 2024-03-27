from bbuddyClass import BuddyClassBlob as bbc


def generateAlertMsg(ticket) -> str:
    """
    Generates the status message using the ticket information received.
    :param ticket: ticket dict.
    :return: message string
    """
    # Latest message picket from the list of updates using the -1 index.
    if ticket:
        msg_to_send = f"### Ticket status change !!! ({ticket['ticket_id']}) \n " \
                      f"Ticket number: #[{ticket['ticket_id']}]({bbc().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                      f"Subject: {ticket['subject']} \n " \
                      f"***Status***: {ticket['status']} \n " \
                      f"***Updated at***: {ticket['updates'][-1]['timestamp']} \n "  \
                      f"***Latest external update***: \n {ticket['updates'][-1]['body']} \n "
        return msg_to_send
