import sys

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup as bs

from config.aaConfig import aaConfig
from parser.aaConfigParser import aaConfigParser

class AutoAA:
    def __init__(self):
        self.browser = None
        self.pr = aaConfigParser()
        self.url = "https://www.airasia.com/en/gb"

        self.pr.__run__() # read user's config

        try:
            # prevent to open another new chrome window
            # options = webdriver.ChromeOptions()
            # options.add_argument("--headless")

            self.browser = webdriver.Chrome(
                # chrome_options=options,
                executable_path='/usr/local/bin/chromedriver'
            )
        except selenium.common.exceptions.WebDriverException as e:
            print("chromedriver need to be in /usr/local/bin. exit AutoAA")
            sys.exit(1)
        except selenium.common.exceptions.SessionNotCreatedException as e:
            print("chromedriver version not matching. exit AutoAA")
            sys.exit(1)

        # start
        self.browser.get(self.url)

    def __login__(self):
        # bring up login page
        WebDriverWait(self.browser, 3).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH, '//button[contains(@class, "{} {}")]'.format(
                    aaConfig.loginModalFieldClass1,
                    aaConfig.loginModalFieldClass2
                    )
                )
            )
        ).click()

        # fill user's information to login
        WebDriverWait(self.browser, 3).until(
            EC.element_to_be_clickable((By.ID, aaConfig.loginEmailFieldId))
        ).send_keys(self.pr.loginEmail)

        WebDriverWait(self.browser, 3).until(
            EC.element_to_be_clickable((By.ID, aaConfig.loginPasswordFieldId))
        ).send_keys(self.pr.loginPassword)

        WebDriverWait(self.browser, 3).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH, '//button[@class="{}" and @type="{}"]'.format(
                    aaConfig.loginButtonFieldClass,
                    aaConfig.loginButtonFieldType
                    )
                )
            )
        ).click()

        # verify
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "BIG Member ID")]'))
        )

if __name__ == "__main__":
    # start auto ticket crawler
    runner = AutoAA()
    runner.__login__()
