import configparser
import sys
import os

class aaConfigParser:
    def __init__(self):
        # new config parser to read ROOT/config/config.ini
        self.config = configparser.ConfigParser()

        self.loginEmail      = None
        self.loginPassword   = None

        self.flightDeparture = None
        self.flightArrival   = None
        self.flightAdult     = None
        self.flightChildren  = None
        self.flightBaby      = None
        self.flightOne       = None
        self.flightReturn    = None

        self.vip             = None

    def __run__(self):
        currentDir = os.getcwd()
        targetFile = "{}/airasia/config/config.ini".format(currentDir)

        # if file exists
        if os.path.isfile(targetFile):
            self.config.read(targetFile)

            # read ini data to variable
            self.loginEmail      = self.config["login"]["email"]
            self.loginPassword   = self.config["login"]["password"]

            self.flightDeparture = self.config["flight"]["departure"]
            self.flightArrival   = self.config["flight"]["arrival"]
            self.flightAdult     = self.config["flight"]["adult"]
            self.flightChildren  = self.config["flight"]["children"]
            self.flightBaby      = self.config["flight"]["baby"]
            self.flightOne       = self.config["flight"]["oneway"]
            self.flightReturn    = self.config["flight"]["return"]
            self.flightDDate     = self.config["flight"]["departureDate"]
            self.flightRDate     = self.config["flight"]["returnDate"]

            self.vip             = self.config["service"]["vip"]

            if None in (
                self.loginEmail, self.loginPassword,
                self.flightDeparture, self.flightArrival, self.flightAdult, self.flightChildren,
                self.flightBaby, self.flightOne, self.flightReturn, self.flightDDate,
                self.flightRDate, self.vip
            ):
                print("AutoAA: None type variable found in ./config/config.ini. exit")
                sys.exit(1)
            else:
                print("AutoAA: ./config/config.ini read done")
        else:
            print("AutoAA: {} not found. exit".format(targetFile))
            sys.exit(1)