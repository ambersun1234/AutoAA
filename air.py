import sys

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup as bs

# self defined functions
from config.aaConfig import aaConfig
from parser.aaConfigParser import aaConfigParser

class AutoAA:
    def __init__(self, show):
        self.browser = None
        self.pr = aaConfigParser()
        self.url = "https://www.airasia.com/zh/tw"

        self.departureFullNameList = dict()
        self.departureAbbrevNameList = dict()
        self.arrivalFullNameList = dict()
        self.arrivalAbbrevNameList = dict()

        self.pr.__run__() # read user's config

        try:
            # prevent to open another new chrome window
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")

            # command line argument
            if show == "show":
                self.browser = webdriver.Chrome(
                    executable_path='/usr/local/bin/chromedriver'
                )
            else:
                self.browser = webdriver.Chrome(
                    chrome_options=options,
                    executable_path='/usr/local/bin/chromedriver'
                )
        except selenium.common.exceptions.WebDriverException as e:
            print("AutoAA: Chromedriver need to be in /usr/local/bin. exit")
            sys.exit(1)
        except selenium.common.exceptions.SessionNotCreatedException as e:
            print("AutoAA: Chromedriver version not matching. exit")
            sys.exit(1)

        try:
            # start
            print("AutoAA: Start selenium on {}... ".format(self.url), end="")
            self.browser.get(self.url)
            print("done\n")
        except:
            print("error. exit")
            sys.exit(1)

    def selectTicketNum(self):
        print("AutoAA: Selecting ticket number... ")
        userTicket = {
            0: int(self.pr.flightAdult),
            1: int(self.pr.flightChildren),
            2: int(self.pr.flightBaby)
        }
        print("AutoAA: {} adults, {} children, {} infants".format(
            userTicket[0],
            userTicket[1],
            userTicket[2]
        ))

        if userTicket[2] > userTicket[0]:
            print("AutoAA: error! 1 infant need at least 1 adult")
            sys.exit(1)

        # click ticket number button to bring up manual
        WebDriverWait(self.browser, 3).until(
            EC.element_to_be_clickable(
                (By.ID, aaConfig.flightIdField)
            )
        ).click()

        # wait pop up menu show
        WebDriverWait(self.browser, 3).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH, '//div[@id="{}"]//div[contains(@class, "{} {}")]'.format(
                        aaConfig.flightIdField,
                        aaConfig.flightField1,
                        aaConfig.flightField2
                    )
                )
            )
        )
        # get current ticket status number
        dropdown = self.browser.find_elements_by_xpath(
            '//div[contains(@class, "{} {}")] \
            //ul[@class="{}"] \
            //li[contains(@class, "{} {}")] \
            //div[contains(@class, "{} {}")] \
            //div[@class="{}"] \
            //span[@class="{}"]'.format(
                aaConfig.flightField1,
                aaConfig.flightField2,
                aaConfig.flightField3,
                aaConfig.flightField4,
                aaConfig.flightField2,
                aaConfig.flightField5,
                aaConfig.flightField6,
                aaConfig.flightField7,
                aaConfig.flightField8
            )
        )

        # press button
        tempTicketClass = {
            0: "adult",
            1: "child",
            2: "infant"
        }
        # iterate 3 kinds of ticket number(website)
        counter = 0
        for element in dropdown:
            # get offset of config.ini with website's
            offset = userTicket.get(counter, 0) - int(element.text)
            for i in range(offset):
                # click add ticket button
                self.browser.find_element_by_id(
                    "{}{}{}".format(
                        aaConfig.flightButtonFieldHead,
                        tempTicketClass.get(counter, 0),
                        aaConfig.flightButtonFieldTail
                    )
                ).click()
            counter += 1

        # get current ticket status number
        dropdown = self.browser.find_elements_by_xpath(
            '//div[contains(@class, "{} {}")] \
            //ul[@class="{}"] \
            //li[contains(@class, "{} {}")] \
            //div[contains(@class, "{} {}")] \
            //div[@class="{}"] \
            //span[@class="{}"]'.format(
                aaConfig.flightField1,
                aaConfig.flightField2,
                aaConfig.flightField3,
                aaConfig.flightField4,
                aaConfig.flightField2,
                aaConfig.flightField5,
                aaConfig.flightField6,
                aaConfig.flightField7,
                aaConfig.flightField8
            )
        )

        # verify operation, recheck
        counter = 0
        for element in dropdown:
            offset = userTicket.get(counter, 0) - int(element.text)
            counter += 1
            if offset != 0:
                print("AutoAA: Selecting ticket number error. exit")
                sys.exit(1)
        print("AutoAA: Selecting ticket number done")

    def selectFlight(self):
        print("AutoAA: Checking flight departure and arrival... ")
        # get flight departure and arrival from config file
        fd = self.pr.flightDeparture
        fa = self.pr.flightArrival

        # check departure flight location
        departureClcikerId = self.getDepartureList(fd)
        if departureClcikerId == -1:
            print("failed")
            print("AutoAA:     {} not found. exit".format(fd))
            sys.exit(1)
        else:
            print("AutoAA:     {} ({}) found".format(
                self.departureFullNameList.get(departureClcikerId, 0),
                self.departureAbbrevNameList.get(departureClcikerId, 0)
            ))
            # click departure location on list
            self.browser.find_element_by_id(
                "{}{}".format(aaConfig.departureListField, departureClcikerId)
            ).click()

        # check arrival flight location
        arrivalClickerId = self.getArrivalList(fa)
        if arrivalClickerId == -1:
            print("failed")
            print("AutoAA:     {} not found. exit".format(fd))
            sys.exit(1)
        else:
            print("AutoAA:     {} ({}) found".format(
                self.arrivalFullNameList.get(arrivalClickerId, 0),
                self.arrivalAbbrevNameList.get(arrivalClickerId, 0)
            ))
            # click arrival location on list
            self.browser.find_element_by_id(
                "{}{}".format(aaConfig.arrivalListField, arrivalClickerId)
            ).click()

    def getArrivalList(self, configArrival):
        print("AutoAA: Get departure list... ", end="")
        # bring up arrival list
        WebDriverWait(self.browser, 3).until(
            EC.element_to_be_clickable(
                (By.ID, aaConfig.arrivalBoxField)
            )
        )
        # get all arrival name
        items = self.browser.find_element_by_id(
            aaConfig.arrivalBoxField
        ).find_elements_by_tag_name("li")

        # write to internal array list
        counter = 0
        for element in items:
            tempF, tempA = element.text.split("\n")
            self.arrivalFullNameList[counter]   = tempF
            self.arrivalAbbrevNameList[counter] = tempA
            # found config arrival location
            # abort constructing arrival list
            if configArrival == tempF or configArrival == tempA:
                print("done")
                return counter
            counter += 1

        return -1

    def getDepartureList(self, configDeparture):
        print("AutoAA: Get departure list... ", end="")
        # bring up departure list
        WebDriverWait(self.browser, 3).until(
            EC.element_to_be_clickable(
                (By.ID, aaConfig.departureButtonField)
            )
        ).click()

        # get all departure name
        items = self.browser.find_element_by_id(
            aaConfig.departureBoxField
        ).find_elements_by_tag_name("li")

        # write to internal array list
        counter = 0
        for element in items:
            tempF, tempA = element.text.split("\n")
            self.departureFullNameList[counter]   = tempF
            self.departureAbbrevNameList[counter] = tempA
            # found config departure location
            # abort constructing departure list
            if configDeparture == tempF or configDeparture == tempA:
                print("done")
                return counter
            counter += 1

        return -1

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

        try:
            # fill user's email to login
            WebDriverWait(self.browser, 3).until(
                EC.element_to_be_clickable((By.ID, aaConfig.loginEmailFieldId))
            ).send_keys(self.pr.loginEmail)

            # fill user's password to login
            WebDriverWait(self.browser, 3).until(
                EC.element_to_be_clickable((By.ID, aaConfig.loginPasswordFieldId))
            ).send_keys(self.pr.loginPassword)

            print("AutoAA: Logging to air asia... ", end="")
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
        except selenium.common.exceptions.TimeoutException as e:
            print("failed. exit")
            sys.exit(1)

        # verify
        try:
            # get air asia user id on website
            WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH, '//*[contains(text(), "BIG會員帳號")]'
                    )
                )
            )
            print("done")
            # get air asia true user name
            tuserName = self.browser.find_element_by_xpath(
                '//div[@class="{}"]//span[@class="{}"]'.format(
                    aaConfig.loginPrompt1, aaConfig.loginPrompt2
                )
            ).text
            print("AutoAA: Welcome, {}!".format(tuserName))
            # close login panel
            self.browser.find_element_by_xpath(
                '(//button[@aria-label="{}"])[2]'.format(
                    "Close navigation"
                )
            ).click()
        except selenium.common.exceptions.TimeoutException as e:
            print("failed. exit")
            sys.exit(1)

if __name__ == "__main__":
    showTemp = None
    try:
        showTemp = sys.argv[1]
    except :
        pass

    # start auto ticket crawler
    runner = AutoAA(showTemp)
    runner.__login__()
    print()
    runner.selectTicketNum()
    print()
    runner.selectFlight()
