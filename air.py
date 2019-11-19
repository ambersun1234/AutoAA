import sys

# self defined functions
from airasia import AutoAA

if __name__ == "__main__":
    showTemp = None
    try:
        showTemp = sys.argv[1]
    except :
        pass

    # start auto ticket crawler
    runner = AutoAA.AutoAA(showTemp)
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
    print()
    runner.selectReturnPrice()
    print()
    runner.getSpecialOffer()
    print()
    runner.fillInfo()
