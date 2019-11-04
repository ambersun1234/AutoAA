import sys
import datetime
import time

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup as bs

# self defined functions
from config.aaConfig import aaConfig
from parser.aaConfigParser import aaConfigParser

def validate(date_text):
    if len(date_text) != 10:
        return False
    try:
        datetime.datetime.strptime(date_text, "%Y/%m/%d")
    except ValueError:
        return False
    else:
        return True

def padding(date_text):
    return "{:%m/%d}".format(datetime.datetime.strptime(date_text, "%m/%d"))

def shorten(date_text):
    return "{:%m/%d}".format(datetime.datetime.strptime(date_text, "%Y/%m/%d"))

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

    def setTicketType(self):
        oneWay = int(self.pr.flightOne)
        returnWay = int(self.pr.flightReturn)

        print("AutoAA: ", end="")
        if oneWay == 1 and returnWay == 1:
            print("set ticket type error. exit")
            sys.exit(1)
        else:
            if oneWay:
                self.browser.find_element_by_xpath(
                    '//label[@for="{}"]'.format(aaConfig.flightTripOne)
                ).click()
            else:
                self.browser.find_element_by_xpath(
                    '//label[@for="{}"]'.format(aaConfig.flightTripReturn)
                ).click()
            print("{} done".format("one way ticket" if oneWay else "returnWay"))

    def setTicketDate(self):
        oneWay     = int(self.pr.flightOne)
        returnWay  = int(self.pr.flightReturn)
        oneDate    = self.pr.flightDDate
        returnDate = self.pr.flightRDate

        print("AutoAA: Setting ticket date...\nAutoAA: ", end="")
        if not validate(oneDate) or not validate(returnDate):
            print("Date format incorrect. exit")
            sys.exit(1)

        if oneWay == 1 and returnWay == 1:
            print("set ticket type error. exit")
            sys.exit(1)
        else:
            # 無論如何都必須選擇起始時間
            self.browser.find_element_by_id(
                aaConfig.flightDDateField
            ).click()
            self.browser.find_element_by_id(
                aaConfig.flightDDateField
            ).clear()
            self.browser.find_element_by_id(
                aaConfig.flightDDateField
            ).send_keys(oneDate)
            print("departure date: {}".format(oneDate))
            if returnWay:
                tmp = self.browser.find_element_by_id(
                    aaConfig.flightRDateField
                )
                selenium.webdriver.ActionChains(self.browser).move_to_element(tmp).click(tmp).perform()
                self.browser.find_element_by_id(
                    aaConfig.flightRDateField
                ).clear()
                self.browser.find_element_by_id(
                    aaConfig.flightRDateField
                ).send_keys(returnDate)
                print("AutoAA: return date:    {}".format(returnDate))
            self.browser.find_element_by_xpath(
                '//button[@class="{}"]'.format(
                    "calendar-button"
                )
            ).click()
            self.browser.find_element_by_id(
                aaConfig.flightSearchField
            ).click()

    def queryFlight(self):
        oneDate = self.pr.flightDDate
        returnDate = self.pr.flightRDate

        # 等待頁面載入完成
        WebDriverWait(self.browser, 20).until(
            EC.visibility_of_element_located(
                (
                    By.ID, aaConfig.flightDepartureRightBtn
                )
            )
        )
        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located(
                (
                    By.XPATH, '//*[contains(@class, "{} {}")]'.format(
                        "fare-date-item-inner",
                        "active"
                    )
                )
            )
        )

        # 尋找當日班機
        checker = True
        oneDate = shorten(oneDate)
        # 實做 python do-while
        while checker:
            # 挑選選擇班次日期相關訊息
            lala = self.browser.find_elements_by_css_selector(
                'div[id*="{}"]'.format(
                    "{}{}".format(
                        aaConfig.flightDepartureDate,
                        aaConfig.flightDepartureIndex
                    )
                )
            )
            # 依次遞迴搜索 5 筆結果進行比對
            for element in lala:
                try:
                    tempDate = element.text.split(",")[0].replace("月", "/").replace("日", "")
                except selenium.common.exceptions.StaleElementReferenceException as e:
                    tempDate = element.text.split(",")[0].replace("月", "/").replace("日", "")
                if oneDate == padding(tempDate):
                    checker = False
                    # 取得當前 id
                    id = element.get_attribute("id").replace("{}{}".format(
                        aaConfig.flightDepartureDate,
                        aaConfig.flightDepartureIndex
                    ), "")
                    # 點擊方框，取得票價以及剩餘票數
                    self.browser.find_element_by_id(
                        "{}{}{}{}".format(
                            aaConfig.flightDepartureClickH,
                            aaConfig.flightDepartureIndex,
                            id,
                            aaConfig.flightDepartureClickT
                        )
                    ).click()
                    break
            if checker:
                # 按下一頁
                self.browser.find_element_by_xpath(
                    '//div[@id="{}"]//div[@class="{}"]'.format(
                        aaConfig.flightDepartureRightBtn,
                        aaConfig.flightScrollBarDefault
                    )
                ).click()
                # 等待頁面載入完成
                WebDriverWait(self.browser, 20).until(
                    EC.visibility_of_element_located(
                        (
                            By.ID, aaConfig.flightDepartureRightBtn
                        )
                    )
                )
                WebDriverWait(self.browser, 20).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH, '//*[contains(@class, "{} {}")]'.format(
                                "fare-date-item-inner",
                                "active"
                            )
                        )
                    )
                )
        print("AutoAA: departure date selected")

    def selectDepaturePrice(self):
        print("AutoAA: Querying departure flight price...")

        counter = 1

        try:
            # find all price button
            tflightBtn = self.browser.find_elements_by_xpath(
                '//*[contains(@id, "{}")]'.format(
                    aaConfig.flightChoosePriceField
                )
            )

            # find departure time of flight
            tjourney = self.browser.find_element_by_id(
                aaConfig.flightJourneyUpField
            )
        except selenium.common.exceptions.NoSuchElementException:
            print("AutoAA: No flights in the desired time. exit")
            sys.exit(1)
        else:
            print("AutoAA: {}".format(tjourney.text))

        # find normal seat price
        tamount = self.browser.find_element_by_xpath(
            '//*[contains(@id, "{}{}{}0-")]'.format(
                aaConfig.flightNormalSeatFieldH,
                aaConfig.flightAmountField,
                aaConfig.flightSeatFieldT
            )
        )
        currency = self.browser.find_element_by_xpath(
            '//*[contains(@id, "{}{}{}0-")]'.format(
                aaConfig.flightNormalSeatFieldH,
                aaConfig.flightCurrencyField,
                aaConfig.flightSeatFieldT
            )
        )
        tbage = self.browser.find_element_by_xpath(
            '//*[contains(@id, "{}{}{}0-")]'.format(
                aaConfig.flightNormalSeatFieldH,
                aaConfig.flightBageField,
                aaConfig.flightSeatFieldT
            )
        )
        print("AutoAA:     {}. normal seat price:      {} {} {}".format(
            counter, tamount.text, currency.text, tbage.text
        ))
        counter += 1

        # find luxury seat price
        try:
            tamount = self.browser.find_element_by_id(
                "{}{}{}0-0".format(
                    aaConfig.flightPrioritySeatFieldH,
                    aaConfig.flightAmountField,
                    aaConfig.flightSeatFieldT
                )
            )
            tbage = self.browser.find_element_by_id(
                "{}{}{}0-0".format(
                    aaConfig.flightPrioritySeatFieldH,
                    aaConfig.flightBageField,
                    aaConfig.flightSeatFieldT
                )
            )
        except selenium.common.exceptions.NoSuchElementException:
            print("AutoAA:     0. luxury flat seat price: not available")
        else:
            print("AutoAA:     {}. luxury flat seat price: {} {} {}".format(
                counter, tamount.text, currency.text, tbage.text
            ))
            counter += 1

        # find parity seat price
        parityJourney = self.browser.find_elements_by_xpath(
            '//*[contains(@id, "{}")]'.format(
                aaConfig.flightJourneyOtherField
            )
        )[1:]
        parityAmount = self.browser.find_elements_by_xpath(
            '//*[contains(@id, "{}{}{}0-")]'.format(
                aaConfig.flightSeatFieldH,
                aaConfig.flightAmountField,
                aaConfig.flightSeatFieldT
            )
        )
        parityBadge = self.browser.find_elements_by_xpath(
            '//*[contains(@id, "{}{}{}0-")]'.format(
                aaConfig.flightSeatFieldH,
                aaConfig.flightBageField,
                aaConfig.flightSeatFieldT
            )
        )[1:]

        parityFlat = self.browser.find_elements_by_xpath(
            '//*[contains(@id, "{}{}{}0-")]'.format(
                aaConfig.flightPrioritySeatFieldH,
                aaConfig.flightAmountField,
                aaConfig.flightSeatFieldT
            )
        )[1:]
        parityBadge2 = self.browser.find_elements_by_xpath(
            '//*[contains(@id, "{}{}{}0-")]'.format(
                aaConfig.flightPrioritySeatFieldH,
                aaConfig.flightBageField,
                aaConfig.flightSeatFieldT
            )
        )[1:]

        # inconsistent list size
        if len(parityBadge) != len(parityJourney):
            parityBadge = [None] * len(parityJourney)
        if len(parityFlat) != len(parityJourney):
            parityFlat = [None] * len(parityJourney)
            parityBadge2 = [None] * len(parityJourney)

        # show each seat's price
        for pj, pa, pf, pb, pb2 in zip(parityJourney, parityAmount, parityFlat, parityBadge, parityBadge2):
            print("AutoAA: {}".format(pj.text))
            print("AutoAA:     {}. normal seat price:      {} {} {}".format(
                counter, pa.text, currency.text, "" if pb is None else pb.text
            ))
            counter += 1
            if pf is None:
                print("AutoAA:     0. luxury flat seat:       not available")
            else:
                print("AutoAA:     {}. luxury flat seat price: {} {} {}\n".format(
                    counter, pf.text, currency.text, "" if pb2 is None else pb2.text
                ))
                counter += 1
        print("AutoAA: please enter the desired flight price: ")
        while True:
            chosen = int(input())
            if chosen >= counter or chosen <= 0:
                print("AutoAA:     Error index, try again")
            else:
                break
        tflightBtn[chosen - 1].click()

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
    print()
    runner.setTicketType()
    print()
    runner.setTicketDate()
    print()
    runner.queryFlight()
    print()
    runner.selectDepaturePrice()
