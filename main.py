from WebScraper import WebScraper
from Notifier import Notifier
from time import sleep
from datetime import datetime, timedelta
import os

CHECKING_INTERVAL = 60 * 1
sender_login =  ############# TODO # mail account
sender_password =  ############# TODO
notifier = Notifier(sender_login, sender_password)

notifier.add_receiver() #to do



web_scraper = WebScraper()
work_start_hour = 9
work_end_hour = 18

while True:
    datetime_cur = datetime.today()
    print("\nNow", datetime_cur.strftime("%Y/%m/%d - %H.%M.%S"))

    if not (work_start_hour < datetime_cur.hour < work_end_hour):
        if datetime_cur.hour > work_end_hour:
            work_start_datetime = datetime_cur.replace(hour=work_start_hour, minute=0, second=0)\
                                  + timedelta(days=1)
        else:
            work_start_datetime = datetime_cur.replace(hour=work_start_hour, minute=0, second=0)

        work_brake = (work_start_datetime - datetime_cur).seconds
        print("Sleep for {} seconds".format(work_brake))
        print("Wake up at {}".format(datetime_cur + timedelta(seconds=work_brake)))
        sleep(work_brake)

    updates = web_scraper.get_updates()
    if updates != "":
        print(updates)
        notifier.send_mail(updates)
    else:
        print("No updates")

    # table_str = web_scraper.table.to_string().encode('ascii', 'ignore').decode('ascii')
    # print(web_scraper.table)

    sleep(CHECKING_INTERVAL)
