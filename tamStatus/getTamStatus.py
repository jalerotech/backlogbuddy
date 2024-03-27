import logging
from typing import Tuple, Any
from mainPrograms.fetchPeopleDataWebEx import retPeopleData

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('TAM PTO Bot')


def ret_tam_pto_status(tam_email) -> dict:
    logger.info("Checking TAM's availability. - STARTED")
    """
    Returns data of TAM's email address if their status is set to OutOfOffice on WebEx.
    """
    ooo_tams = []
    country_list = []
    # WebEx data fetching on a separate script.
    peopleData = retPeopleData(tam_email)
    if peopleData:
        for country in peopleData['items'][0]['addresses']:
            country_list.append(country['country'])
        status = peopleData['items'][0]['status']
        displayName = peopleData['items'][0]['displayName']
        mail = peopleData['items'][0]['emails']
        region = peopleData['items'][0]['addresses'][0]['country']
        if status == 'OutOfOffice':
            msg_data = {
                'name': displayName,
                'status': status,
                'email': mail,
                'region': region
            }
            ooo_tams.append(msg_data)
            return msg_data
    logger.info("Checking TAM's availability. - COMPLETED")


def is_tam_on_pto(tam_email) -> tuple[bool, Any]:
    """
    Checks if the TAM's email matches the results produced by the "ret_tam_pto_status" function.
    Extra checks done here to make sure that the email returned by the "ret_tam_pto_status" is the same as the TAM email input.
    :param tam_email: TAM's email address - e.g. jalero@cisco.com
    :return:
    """
    logger.info(f"Cross-checking TAM email {tam_email} with WebEx status -> STARTED")
    is_on_pto = False
    tam_pto_status = ret_tam_pto_status(tam_email)
    if tam_pto_status:
        if is_on_pto == tam_pto_status['email'][0]:
            is_on_pto = True
    logger.info(f"Cross-checking TAM email {tam_email} with WebEx status -> COMPLETED")
    return is_on_pto, ret_tam_region(tam_email)


def ret_tam_region(tam_email) -> dict:
    """
    Checks and returns the TAM's region information using the input email address.
    :param tam_email: TAM's email address e.g. jalero@cisco.com
    :return: region and user_id dict -> e.g. {"region": "BE", "user_id":"<id_string>"
    """
    logger.info("Returning TAM region label. - STARTED")
    """
    Returns TAM region information using the provided TAM's email address.
    """
    peopleData = retPeopleData(tam_email)
    region = peopleData['items'][0]['addresses'][0]['country']
    user_id = peopleData['items'][0]['id']
    region_and_user_id = {
        'region': region,
        'user_id': user_id
    }
    if region:
        logger.info(f"Returning TAM {tam_email}'s region label. - COMPLETED")
        return region_and_user_id


if __name__ == '__main__':
    email = ""
    print(ret_tam_pto_status(email))
