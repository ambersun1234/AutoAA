import configparser
import sys
import os

class aaConfigParser:
    def __init__(self):
        # new config parser to read ROOT/config/config.ini
        self.config = configparser.ConfigParser(allow_no_value=True)
        # https://stackoverflow.com/questions/335695/lists-in-configparser

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

        self.adultInfo       = list()
        self.childrenInfo    = list()
        self.babyInfo        = list()

    def __run__(self):
        currentDir = os.getcwd()
        targetFile = "{}/airasia/config/config.ini".format(currentDir)

        # if file exists
        if os.path.isfile(targetFile):
            self.config.read(targetFile)

            try:
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
                self.contactEmail    = self.config["contact"]["email"]
                self.contactTel      = self.config["contact"]["tel"]
            except KeyError as e:
                print("AutoAA: config.ini missing arguments. stop")
                sys.exit(1)

            self.vip             = self.config["service"]["vip"]

            tmp = self.config.items("Adultinfo")
            for trash, value in tmp:
                mytmp = value.split(",")
                self.adultInfo.append(
                    {
                        "firstname":  mytmp[0],
                        "lastname":   mytmp[1],
                        "birthday":   mytmp[2],
                        "gender":     mytmp[3]
                    }
                )

            tmp = self.config.items("Childinfo")
            for trash, value in tmp:
                mytmp = value.split(",")
                self.childrenInfo.append(
                    {
                        "firstname":  mytmp[0],
                        "lastname":   mytmp[1],
                        "birthday":   mytmp[2],
                        "gender":     mytmp[3]
                    }
                )

            tmp = self.config.items("Babyinfo")
            for trash, value in tmp:
                mytmp = value.split(",")
                self.babyInfo.append(
                    {
                        "firstname":  mytmp[0],
                        "lastname":   mytmp[1],
                        "birthday":   mytmp[2],
                        "gender":     mytmp[3]
                    }
                )

            # if (int(self.flightAdult) != 0 and (len(self.adultInfo) + 1 != int(self.flightAdult))) or \
            #     (int(self.flightChildren) != 0 and (len(self.childrenInfo) + 1 != int(self.flightChildren))) or \
            #     (int(self.flightBaby) != 0 and (len(self.babyInfo) + 1 != int(self.flightBaby))):
            if len(self.adultInfo) != int(self.flightAdult) or \
                len(self.childrenInfo) != int(self.flightChildren) or \
                len(self.babyInfo) != int(self.flightBaby):
                print("AutoAA: inconsistent ticket number and info found in ./config/config.ini. exit")
                sys.exit(1)
            if None in (
                self.loginEmail, self.loginPassword,
                self.flightDeparture, self.flightArrival, self.flightAdult, self.flightChildren,
                self.flightBaby, self.flightOne, self.flightReturn, self.flightDDate,
                self.flightRDate, self.vip, self.contactEmail, self.contactTel
            ):
                print("AutoAA: None type variable found in ./config/config.ini. exit")
                sys.exit(1)
            else:
                print("AutoAA: ./config/config.ini read done")
        else:
            print("AutoAA: {} not found. exit".format(targetFile))
            sys.exit(1)
