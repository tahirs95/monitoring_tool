import logging
import time
import requests
from datetime import datetime

# log file name
LOG_FILE_NAME = "monitor.log"
logging.basicConfig(
    filename=LOG_FILE_NAME,
    filemode="w",
    format="%(levelname)s - %(message)s",
    level=logging.INFO,
)

# class to handle request response cycle
class Magnificent:
    def __init__(self):
        self.URL = "https://api.us-west-1.saucelabs.com/v1/magnificent/"
        self.sleep = 5
        self.status_code = None
        self.status = None
        self.success_count = 0
        self.failure_count = 0

    def get(self):
        """
        hit the url and update the values accordingly
        """
        try:
            resp = requests.get(self.URL)
            self.status_code = resp.status_code
            if self.status_code == 200:
                self.status = "SUCCESS"
                self.success_count += 1
            elif self.status_code == 500:
                self.status = "FAILURE"
                self.failure_count += 1
            self.log_response()

        except Exception as e:
            """
            service not working
            """
            self.status_code = 408
            self.status = "NOT RESPONDING"
            self.failure_count += 1
            self.log_response()

    def log_response(self):
        """
        log response
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        health = self.success_count / (self.success_count + self.failure_count) * 100
        log = f"{now} | {self.status_code} | {self.status} | health = {health}%"
        if self.status_code == 408:
            logging.error(log)
        else:
            logging.info(log)


def run():
    # initialize the class object
    magnificent = Magnificent()
    while True:
        magnificent.get()  # hit the service
        time.sleep(magnificent.sleep)  # sleep for specific time


if __name__ == "__main__":
    run()
