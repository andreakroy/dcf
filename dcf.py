import requests
import argparse as ap
from bs4 import BeautifulSoup, SoupStrainer
import yfinance as yf
import json
import re
class stock:
    def __init__(self, ticker: str, cik: int, name: str, sector: str, 
            last_10k_date: str, accession_num: str,  beta: float,
            net_income: int, tax_expense: int, interest_expense: int):
        self.ticker = ticker
        self.cik = cik
        self.name = name
        self.sector = sector
        self.last_10k_date = last_10k_date
        self.accession_num = accession_num
        self.beta = beta
        self.net_income = net_income
        self.tax_expense = tax_expense
        self.interest_expense = interest_expense
    
    # using CAPM formuala:
    # Risk Free Rate + [Beta x ( Expected Market Return - Risk Free Rate )]
    # Risk Free Rate is assumed to be the current rate of return on a 10 year
    # treasury bond. Expected market return is conservatively assumed to be
    # roughly 8%
    def cost_of_equity(self, rfr):
        return rfr + self.beta * (.08 - rfr)
   
    # using the formula EBIT / Interest Expenses
    def interest_coverage_ratio(self):
        return self.ebit() / self.interest_expense
    
    # using tables from A. Damodaran to relate interest coverage ratio to
    # default spread.
    def default_spread(self):
        ic = self.interest_coverage_ratio


    
    # calculation of Earnings Before Interest and Taxes
    # using EBIT = Net Income + Interest Expense + Tax Expense
    def ebit(self)
        return self.net_income + self.tax_expense + self.interest_expense

    def __str__(self):
        return '{} ({} - CIK: {})\nSector: {}\nLast 10-K ({}): {}'.format(
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
    
    # pull data from Yahoo Finance API
    t = yf.Ticker(ticker)
    info = t.info
    
    # find the accession number latest annual report (SEC 10-K)
    # assumes that the latest annual report is the first in the list
    # returned
    report_entry = page.find('entry')
    # Why the heck is "accession-nunmber" the tag in the xml schema???
    acc_num = ''.join(filter(lambda x: x != '-', 
        report_entry.find('accession-nunber').text))
    # Gets the company CIK
    cik = int(page.cik.text)
    
    '''
    # Parses the xml to find the id of the doc with income or operations
    # statements
    xml = requests.get('https://sec.gov/cgi-bin/viewer',
            params={'action': 'view', 'cik': cik,
                'accession_number': acc_num})
    report = BeautifulSoup(xml.text, 'lxml')
    doc_id = report.find(lambda tag: re.compile(
        '(?i)consolidated statements of income').match(tag.text))['id']
    
    xml = requests.get('https://sec.gov/Archives/edgar/data/{}/{}'.format(
        cik, acc_num))
    docs = BeautifulSoup(xml.text, 'lxml')
    link = docs.find(lambda tag: re.compile(
        '(?i){}\.'.format(doc_id)).match(tag.text)).find('a')['href']
    print(link)
    xml = requests.get('https://sec.gov{}'.format(link))
    income_sheet = BeautifulSoup(xml.text, 'lxml')
    net_income = income_sheet.find(lambda tag: re.compile(
        '(?i)net').search(tag.text))
    print(net_income)
    '''
    return stock(
        ticker.upper(),
        cik,
        info['longName'], 
        page.find('assigned-sic-desc').text,
        report_entry.find('filing-date').text,
        acc_num,
        float(info['beta']),
        0,
        0,
        0
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

msft = get_company_data("goog")
print(msft)
