# AutoAA
Automatic ticket crawler for air asia

## Disclaimer
+ This article is for **educational usage**, user's implementation belongs to one's personal behavior
+ The author doesn't bear any legal reponsibility
+ This original python code is completely following [General Data Protection Regulation - GDPR](https://gdpr-info.eu/) rules, if any user change any part of the code, then there's no guarantee that the modified code will still follow [General Data Protection Regulation - GDPR](https://gdpr-info.eu/) rules

## Privacy Policy
+ We have a simple [Privacy Policy](./policy.md) where we state how we handle your information

## Todo list
+ Credit card fill in
+ Actual purchase airline ticket

## Clone Repo
```=1
git clone https://github.com/ambersun1234/AutoAA.git
```

## Dependencies
+ selenium - `sudo pip3 install selenium`
+ chrome driver - visit [ChromDriver - WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads) download correspond driver
    + and place `chromedriver` in `/usr/local/bin`

## Usage
+ copy [./config/config.ini.example](./config/config.ini.example) and rename to `config.ini` and place it under `./config`
+ modify the user information inside `config.ini`
+ run program
    + simply `python3 air.py` or `python3 air.py show`
+ note: this ticket-snatching program is `actually not fully automatic`, thus user should stay in front of the computer and wait for AutoAA's instructions

## Config note
+ login section: contain your login information, user must register an account before using AutoAA
+ flight section: departure and arrival should fill in `full station name` or `abbreviation`
+ flight section: departure date and returnDate should follow standard date formate(e.g. 2020/01/23)
+ service section: vip indicate the service level, in this case we have:
    + `0` stands for `no vip`
    + `1` stands for `Value Pack`: baggage allowance, standard seat selection and 1 meal
    + `2` stands for `Premium Flex`: baggage allowance, hot and standard seat selection, 1 meal, change of date time and lounge access
    + `3` stands for `Premium Flatbed`: baggage allowance, flatbed selection, 1 meal, change of date time, lounge access, entertainment access and baggage delivery
+ passenger info config file
    + the default type is as follows
    + `a2            = YOURFIRSTNAME,YOURLASTNAME,2020/01/01,F,N`
    + you'll need to fill your personal information in predestinate order
        + `first name, last name, birthday(date format as YYYY/MM/DD), physical gender(F, M), need wheelchair or not`
        + and each of the column is separate by comma respectively, any incorrect input will terminate AutoAA immediately

## License
+ This project is licensed under MIT License - see the [LICENSE](https://github.com/ambersun1234/AutoAA/blob/master/LICENSE) file for detail
