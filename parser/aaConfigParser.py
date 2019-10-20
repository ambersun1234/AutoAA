import configparser
import sys
import os

class aaConfigParser:
    def __init__(self):
        self.config = configparser.ConfigParser()

        self.loginEmail = None
        self.loginPassword = None

    def __run__(self):
        currentDir = os.getcwd()
        targetFile = "{}/config/config.ini".format(currentDir)

        if os.path.isfile(targetFile):
            self.config.read(targetFile)

            # read ini data to variable
            self.loginEmail = self.config["AA"]["email"]
            self.loginPassword = self.config["AA"]["password"]
        else:
            print("{} not found. exit".format(targetFile))
            sys.exit(1)
