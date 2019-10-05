import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def highlight():
    return "background-color: yellow"


def save_page(r):
    with open("test.html", "w") as file:
        file.write(r.text)


class WebScraper:
    def __init__(self):
        self.table = pd.DataFrame(columns=self.house_names)
        for date_url in self.date_urls:
            date = self.dates[date_url]
            self.table.loc[date] = [0] * len(self.house_names)

    housing_page = "https://accommodation.fmel.ch/StarRezPortal/6892834A/1/1/EN-Welcome_to_FMEL_hous"
    date_url_16_10 = "https://accommodation.fmel.ch/StarRezPortal/B2364089/30/302/Book_now-House_selection?TermID=877&ClassificationID=1&DateStart=16%20October%202019&DateEnd=16%20October%202024"
    date_url_01_11 = "https://accommodation.fmel.ch/StarRezPortal/45B94C3A/30/302/Book_now-House_selection?TermID=874&ClassificationID=1&DateStart=01%20November%202019&DateEnd=01%20November%202024"
    date_url_16_11 = "https://accommodation.fmel.ch/StarRezPortal/710AA5AE/30/302/Book_now-House_selection?TermID=878&ClassificationID=1&DateStart=16%20November%202019&DateEnd=16%20November%202024"
    date_url_01_12 = "https://accommodation.fmel.ch/StarRezPortal/77D1585C/30/302/Book_now-House_selection?TermID=875&ClassificationID=1&DateStart=01%20December%202019&DateEnd=01%20December%202024"

    dates = {
        date_url_16_10: "16/10",
        date_url_01_11: "01/11",
        date_url_16_11: "16/11",
        date_url_01_12: "01/12",
    }

    date_urls = [
        # date_url_01_05,
        # date_url_16_05,
        # date_url_01_06,
        # date_url_16_06,
        # date_url_01_07,
        # date_url_16_07,
        date_url_16_10,
        date_url_01_11,
        date_url_16_11,
        date_url_01_12


    ]

    best_choise = [
        'Atrium',
        'Bourdonnette',
        'Triaudes',
        'Ochettes',
        'Square',
    ]

    house_names = [
        'Atrium',
        'Azur',
        'Bourdonnette',
        'Ochettes',
        'Triaudes',
        'Cèdres',
        'Colline',
        'Falaises',
        'Jordils',
        'Marcolet',
        'Rainbow',
        'Rhodanie',
        'Square',
        'Staehli',
        'Yverdon',
        'Zenith',
    ]

    login_page = "https://accommodation.fmel.ch/StarRezPortal/AE18865B/7/8/Login-Login?IsContact=False"
    login_url = "https://accommodation.fmel.ch/StarRezPortal/General/Register/register/Login"

    login_data = {"invalidCredentialsMessage": "The credentials provided are invalid.",
                  "pageID": 8,
                  "password": "", ############# TODO # FMEL account
                  "rememberLogin": False,
                  "username": ""  ############# TODO
                  }

    def is_logged(self, s):
        r = s.get(self.housing_page)
        login = r.text.count('Login')
        logout = r.text.count('Log Out')
        if login > 0 and logout == 0:
            return False
        if login == 0 and logout > 0:
            return True
        print("Something wrong^")
        print("Login", login)
        print("Log Out", logout)
        return False

    def update_housing(self):
        s = requests.Session()
        # Collect headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
        r = s.get(self.login_page)
        soup = BeautifulSoup(r.text, 'html.parser')
        headers['__RequestVerificationToken'] = soup.find("input", attrs={'name': '__RequestVerificationToken'})[
            'value']

        # Login
        r = s.post(self.login_url, data=self.login_data, headers=headers)
        logged_in = self.is_logged(s)
        print("Logged in?", logged_in)

        if not logged_in:
            save_page(r)

        table = pd.DataFrame(columns=self.house_names)
        for date_url in self.date_urls:
            date = self.dates[date_url]
            r = s.get(date_url)
            # print("\n  ", date)
            table.loc[date] = [1 if r.text.count(house_name) > 0 else 0
                               for house_name in self.house_names]
        table.style.applymap(highlight, subset=self.best_choise)
        # table.iloc[2].Atrium = 1  # todo delete
        # table.iloc[1].Staehli = -1  # todo delete
        self.table = table

    def get_updates(self):
        old_table = self.table
        self.update_housing()
        new_table = self.table
        updates_text = ""
        diff_matrix = old_table - new_table
        for row_ind in range(len(diff_matrix)):
            row = diff_matrix.iloc[row_ind].to_list()
            indexes_open = [i for i, x in enumerate(row) if x == -1]
            indexes_close = [i for i, x in enumerate(row) if x == 1]
            for index in indexes_open:
                updates_text += "Opened booking for {} from {}\n".format(self.house_names[index],
                                                                         self.dates[self.date_urls[row_ind]]) \
                                + "Link: " + self.date_urls[row_ind] + "\n"
            for index in indexes_close:
                updates_text += "Closed booking for {} from {}\n".format(self.house_names[index],
                                                                         self.dates[self.date_urls[row_ind]]) \
                                + "Link: " + self.date_urls[row_ind] + "\n"
        return updates_text
