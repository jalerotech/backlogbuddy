import logging
from datetime import datetime
from bbuddyClass import BuddyClassBlob as bbc

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('ShifttimeData')
currentDateAndTime = datetime.now()
today = currentDateAndTime.strftime('%A')


def theatre_shift_time(region) -> bool:
    """
    Returns True or False when it checks time object -> hour
    :param region: label[EMEA, APAC, US]
    :return: bool
    """
    if today == "Saturday" or today == "Sunday":
        logger.info("Weekend is here and all theatre are inactive.")
    else:
        if region == "APAC":
            # shift ends at 09:00 UTC +1 time so backlog buddy should be quiet at this time
            if currentDateAndTime.hour >= 9:
                return True
            else:
                return False
        if region == 'EMEA':
            # shift ends at 16:00 UTC +1 time so backlog buddy should be quiet at this time
            if currentDateAndTime.hour >= 16:
                return True
            else:
                return False
        if region == 'US':
            # shift ends at 02:00 UTC +1 time so backlog buddy should be quiet at this time
            if currentDateAndTime.hour >= 2:
                return True
            else:
                return False


def is_shift_over(tam_region, tam_email) -> bool:
    """
    Returns True or False depending on the regional shift status.
    :param tam_region: for example BE, PL, GB etc.
    :param tam_email: user@example.com
    :return: True or False
    """
    if tam_region in bbc().EMEA_region:
        if not theatre_shift_time('EMEA'):
            logger.info(f"Shift is over for EMEA theatre -> {tam_email} is in {tam_region} region.")
            shift_is_over = True
            return shift_is_over
    if tam_region in bbc().APAC_region:
        if not theatre_shift_time('APAC'):
            logger.info(f"Shift is over for APAC theatre -> {tam_email} is in {tam_region} region.")
            shift_is_over = True
            return shift_is_over
    if tam_region in bbc().US_region:
        if not theatre_shift_time('US'):
            logger.info(f"Shift is over for US theatre -> {tam_email} is in {tam_region} region.")
            shift_is_over = True
            return shift_is_over
