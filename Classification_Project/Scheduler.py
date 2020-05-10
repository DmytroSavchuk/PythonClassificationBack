import os
import shutil
import threading
import time

import schedule

from Classification_Project.ApplicationConstants import ApplicationConstants
from Classification_Project.ConsoleLogger import console_logger

tmp_clear_hour_interval = 6
session_storage_clear_hour_interval = 6


class Scheduler:
    def schedule_clearing_tmp_folder(self):
        threading.Thread(target=execute).start()


def execute():
    schedule.every(tmp_clear_hour_interval).hours.do(__clear_tmp_folder_job)

    while 1:
        schedule.run_pending()
        time.sleep(1)


def __clear_tmp_folder_job():
    console_logger.info("Clearing tmp folder...")

    shutil.rmtree(ApplicationConstants.get_constant("UPLOADS_FOLDER_PATH"))

    os.mkdir(ApplicationConstants.get_constant("UPLOADS_FOLDER_PATH"))
