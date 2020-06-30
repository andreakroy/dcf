import requests
import argparse as ap
from bs4 import BeautifulSoup
import yfinance as yf
import json

class stock:
    def __init__(self, ticker: str, name: str, sector: str, beta: float):
        self.ticker = ticker
        self.name = name
        self.sector = sector
        self.beta = beta
    
    # using Risk Free Rate + [Beta x ( Expected Market Return - Risk Free Rate )] to
    # estimate the cost of equity.
    # Risk Free Rate is assumed to be the current rate of return on a 10 year
    # treasury bond. Expected market return is conservatively assumed to be
    # roughly 8%
    def cost_of_equity(self):
        rfr = get_risk_free_rate()
        return rfr + self.beta * (.08 - rfr)

    def __str__(self):
        return "{} ({})\nSector: {}".format(self.name, self.ticker, self.sector)

# Gets a company's basic information from the Yahoo Finance API
def get_company_data(ticker) -> stock:
    assert(isinstance(ticker, str))
    t = yf.Ticker(ticker)
    info = t.info
    return stock(
            ticker.upper(),
            info['longName'],
            info['sector'],
            float(info['beta']),
        )

# Gets the current Risk Free Rate (the 10 Year US Treasury
# Bond yield) by querying the US Treasury website.
def get_risk_free_rate() -> float:
    xml = requests.get('https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%206%20and%20year(NEW_DATE)%20eq%202020')
    if xml.status_code != requests.codes.ok:
        return None
    page = BeautifulSoup(xml.text, "lxml")
    return float(page.find_all('d:bc_10year')[-1].text)

def wacc(re, rd, e, d, t, v):
    return 0

msft = get_company_data("MSFT")
print(msft.cost_of_equity())
