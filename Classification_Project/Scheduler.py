import os
import shutil
import threading
import time

import schedule

tmp_clear_hour_interval = 6


class Scheduler:
    def schedule_clearing_tmp_folder(self):
        threading.Thread(target=clearing_tmp_folder_action).start()


def clearing_tmp_folder_action():
    schedule.every(tmp_clear_hour_interval).hours.do(clear_tmp_folder_job)

    while 1:
        schedule.run_pending()
        time.sleep(1)


def clear_tmp_folder_job():
    print("Clearing...")

    shutil.rmtree('resources/uploads')

    os.mkdir('resources/uploads')
