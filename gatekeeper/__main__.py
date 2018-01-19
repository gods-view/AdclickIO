import time
import schedule
import traceback
import logging

from .worker import popads
from .worker import zeropark
from .worker import exoclick
from .worker import propellerads
from .worker import trafficjunky


def job():
    start = time.time()
    print("start: job time: " + str(start))
    # listTS = [trafficjunky]
    listTS = [popads, zeropark, exoclick, propellerads, trafficjunky]

    for ts in listTS:
        try:
            print('start -->' + str(ts))
            ts(retrive_new=False)
        except Exception as e:
            print(str(ts) + ' is error ,and error : ' + str(e) + " continue next TS !")
            logging.error(traceback.format_exc())
            continue

    end = time.time()

    print("use time :" + str(end - start))


def checkoutUser():
    start = time.time()
    print("start checkout time: " + str(start))
    # listTS = [trafficjunky]
    listTS = [popads, zeropark, exoclick, propellerads, trafficjunky]

    for ts in listTS:
        try:
            print('start checkout  -->' + str(ts))
            ts(retrive_new=True)
        except Exception as e:
            print(str(ts) + ' is error ,and error : ' + str(e) + " continue next TS !")
            logging.error(traceback.format_exc())
            continue

    end = time.time()

    print("use time :" + str(end - start))
    print("checkout end !")


def main():
    print("gatekeepr, heartbreaker")

    schedule.every(10).minutes.do(checkoutUser).run()  # checkout user is not first

    schedule.every(12).hours.do(job).run()  # run: Run the job and immediately reschedule it.

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(e)
            logging.error(traceback.format_exc())


if __name__ == "__main__":
    main()
