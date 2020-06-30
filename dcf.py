import requests
import argparse as ap
from bs4 import BeautifulSoup

class stock:
    def __init__(self, ticker: str, cik: int, name: str, sic_desc: str,
            sic_code: int):
        self.ticker = ticker.upper()
        self.cik = cik
        self.name = name
        self.sic_desc = sic_desc
        self.sic_code = sic_code
    
    def __str__(self):
        return "{} ({})\nCIK: {}\nSIC: {} ({})".format(self.name, self.ticker,
                self.cik, self.sic_desc, self.sic_code)

# Gets a compny's basic information from the Edgar database and returns a
# 'stock' object storing the information.
def get_company_info(ticker) -> stock:
    assert(isinstance(ticker, str))
    xml = requests.get('https://www.sec.gov/cgi-bin/browse-edgar',
            params={'CIK': ticker, 'Find': 'Search', 'owner': 'exclude',
                'action': 'getcompany', 'output': 'atom'})
    if xml.status_code != requests.codes.ok:
        return None
    page = BeautifulSoup(xml.text, 'lxml')
    try: 
        return stock(
            ticker,
            int(page.cik.text),
            page.find('conformed-name').text,
            page.find('assigned-sic-desc').text,
            page.find('assigned-sic').text
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

# using Risk Free Rate + [Beta x ( Expected Market Return - Risk Free Rate )] to
# estimate the cost of equity.
# Risk Free Rate is assumed to be the current rate of return on a 10 year
# treasury bond. Expected market return
def cost_of_equity(beta, rfr, emr):
    return 0

print(get_risk_free_rate())

