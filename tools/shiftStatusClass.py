import logging
from datetime import datetime
from bbuddyClass import BuddyClassBlob as bbc

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class ShiftStatus:
    def __init__(self):
        self.logger = logging.getLogger('ShiftStatus_bb')
        self.currentDateAndTime = datetime.now()
        self.today = self.currentDateAndTime.strftime('%A')

    def is_theatre_active(self, region):
        """
        Returns True or False when it checks time object -> hour
        :param region: label[EMEA, APAC, US]
        :return: bool
        """
        if bbc().is_weekend():
            self.logger.info("Weekend is here and all theatre are inactive.")
        else:
            if region == "APAC":
                # shift ends at 09:00 UTC +1 time so backlog buddy should be quiet at this time
                if self.currentDateAndTime.hour >= 1:
                    if self.currentDateAndTime.hour < 9:
                        return True
                    else:
                        return False
                else:
                    return False
            if region == 'EMEA':
                # shift ends at 16:00 UTC +1 time so backlog buddy should be quiet at this time
                if self.currentDateAndTime.hour >= 8:
                    if self.currentDateAndTime.hour < 16:
                        return True
                    else:
                        return False
                else:
                    return False
            if region == 'US':
                # shift ends at 02:00 UTC +1 time so backlog buddy should be quiet at this time
                # Correcting this on the main codes.
                # if currentDateAndTime.hour == 2 and currentDateAndTime.min == 0:
                if (16 <= self.currentDateAndTime.hour <= 23) or (0 <= self.currentDateAndTime.hour < 2):
                    return True
                else:
                    return False

    def is_shift_over(self, tam_region, tam_email) -> bool:
        """
        Returns True or False depending on the regional shift status.
        :param tam_region: for example BE, PL, GB etc.
        :param tam_email: user@example.com
        :return: True or False
        """
        if tam_region in bbc().EMEA_region:
            if self.is_theatre_active('EMEA'):
                shift_is_over = False
                self.logger.info(f"Shift is active for EMEA theatre -> {tam_email} is in {tam_region} region.")
                return shift_is_over
            else:
                self.logger.info(f"Shift is over for EMEA theatre -> {tam_email} is in {tam_region} region.")
                shift_is_over = True
                return shift_is_over
        if tam_region in bbc().APAC_region:
            if self.is_theatre_active('APAC'):
                shift_is_over = False
                self.logger.info(f"Shift is active for APAC theatre -> {tam_email} is in {tam_region} region.")
                return shift_is_over
            else:
                self.logger.info(f"Shift is over for APAC theatre -> {tam_email} is in {tam_region} region.")
                shift_is_over = True
                return shift_is_over
        if tam_region in bbc().US_region:
            if self.is_theatre_active('US'):
                shift_is_over = False
                self.logger.info(f"Shift is active for US theatre -> {tam_email} is in {tam_region} region.")
                return shift_is_over
            else:
                self.logger.info(f"Shift is over for US theatre -> {tam_email} is in {tam_region} region.")
                shift_is_over = True
                return shift_is_over

