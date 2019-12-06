import sys
import datetime

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
    st = runner.startTime
    frequency = runner.frequency

    # 倒計時
    print("countdown: ", end="")
    while True:
        ct = datetime.datetime.now()
        print("\b\b\b\b\b\b\b\b\b\b\b\b\b\b{}".format(st - ct), end="", flush=True)
        if ct > st:
            break

    # 總測試次數
    for index in range(0, frequency):
        print()
        runner.__start__()
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
