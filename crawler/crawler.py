import pandas as pd
import time
import requests
from bs4 import BeautifulSoup

def main():
    l = []
    for i in range(1, 54):
        print(f"----------------------Parsing {i} request -------------------------------------")
        base_request = f"http://www.cophieu68.vn/historyprice.php?currentPage={i}&id=^vnindex"
        r = requests.get(base_request)
        soup = BeautifulSoup(r.text)
        table = soup.findAll('table')[1]
        rows = table.findAll('tr')
        
        for row in rows[1:]:
            td = row.findAll('td')
            date_time = td[1].get_text()
            reference_price = float(td[2].get_text().replace(',', ''))
            close_price = float(td[5].get_text().replace(',', ''))
            volume = int(td[6].get_text().replace(',', ''))
            open_price = float(td[7].get_text().replace(',', ''))
            high_price = float(td[8].get_text().replace(',', ''))
            low_price = float(td[9].get_text().replace(',', ''))
            foreign_buy = int(td[11].get_text().replace(',', ''))
            foreign_sell = int(td[12].get_text().replace(',', ''))
            item = {
                "Date": date_time,
                "Reference": reference_price,
                "Close": close_price,
                "Volume": volume,
                "Open": open_price,
                "High": high_price,
                "Low": low_price,
                "Foreign_Buy": foreign_buy,
                "Foreign_Sell": foreign_sell
            }
            l.append(item)
        time.sleep(2)

    df = pd.DataFrame(l[::-1])
    df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y")
    df.set_index('Date')
    return df
if __name__ == '__main__':
    df = main()
    some_path = ""
    df.to_csv(some_path, index=False)
