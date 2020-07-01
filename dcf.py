import requests
import argparse as ap
from bs4 import BeautifulSoup
import yfinance as yf
import json
import pandas as pd

class stock:
    def __init__(self, ticker: str, cik: int, name: str, sector: str, 
            last_10k_date: str, accession_num: str, beta: float):
        self.ticker = ticker
        self.cik = cik
        self.name = name
        self.sector = sector
        self.last_10k_date = last_10k_date
        self.accession_num = accession_num
        self.beta = beta
    
    # using CAPM formuala:
    # Risk Free Rate + [Beta x ( Expected Market Return - Risk Free Rate )]
    # Risk Free Rate is assumed to be the current rate of return on a 10 year
    # treasury bond. Expected market return is conservatively assumed to be
    # roughly 8%
    def cost_of_equity(self, rfr):
        return rfr + self.beta * (.08 - rfr)
   
    # using the formula EBIT / Interest Expenses
    def interest_coverage_ratio(self):
        return 0
    
    # calculation of Earnings Before Interest and Taxes
    # using EBIT = Revenue - Cost of Goods and Services - OPEX
    #            = Gross Profit - OPEX
    # Pulling Gross Profit and OPEX data from latest annual report in Edgar
    def ebit(self):
        return 0
    def __str__(self):
        return "{} ({} - CIK: {})\nSector: {}\nLast Annual Report ({}): {}".format(
                self.name, self.ticker, self.cik, self.sector,
                self.accession_num, self.last_10k_date)

# Gets a company's basic information from the Yahoo Finance API and Edgar
# Database
def get_company_data(ticker) -> stock:
    assert(isinstance(ticker, str))
    # scrape Edgar DB for the latest 10-K SEC filing
    xml = requests.get('https://www.sec.gov/cgi-bin/browse-edgar',
        params={'CIK': ticker, 'Find': 'Search', 'owner': 'exclude','action': 'getcompany',
            'output': 'atom', 'start': 0, 'count': 10, 'type': '10-K'})
    if xml.status_code != requests.codes.ok:
        return None
    page = BeautifulSoup(xml.text, 'lxml')
    try:
        # pull data from Yahoo Finance API
        t = yf.Ticker(ticker)
        info = t.info
        
        # find latest annual report (SEC 10-K)
        # assumes that the latest annual report is the first in the list
        # returned
        report_entry = page.find('entry')
        #report = requests.get(report_entry.find('filing-href').text).text
        #rep = BeautifulSoup(report, 'lxml')
        print(report_entry.find('accession-nunber').text)
        #print(report.text)
        return stock(
            ticker.upper(),
            int(page.cik.text),
            info['longName'], 
            page.find('assigned-sic-desc').text,
            report_entry.find('filing-date').text,
            # "accession-nunmber" [sic] is the tag in the xml schema
            report_entry.find('accession-nunber').text,
            float(info['beta'])
        )
    except:
        return None

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

msft = get_company_data("aal")
print(msft)
