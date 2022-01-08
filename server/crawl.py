import requests
from bs4 import BeautifulSoup
import requests.packages.urllib3
import datetime
from urllib.parse import urljoin


def get_live_exchangerate():
    currencies = []
    currencies_abbr = []
    spot_sell_rates = []
    cash_sell_rates = []
    exchange_rates = []
    live_exchangerates = {}
    ''' Request '''
    requests.packages.urllib3.disable_warnings()
    url = 'https://rate.bot.com.tw/xrt?Lang=en-US'
    re = requests.get(url, verify=False)
    soup = BeautifulSoup(re.text, 'html.parser')
    ''' 
	Find abbr. of currencies and Spot/Cash selling rate
	(priority of exchange rate: Spot/Cash selling rate)
	Save them to dictionary live_exchangerates: <abbr. of currencies>(str): <exchange rate>(float)
	'''
    # find currencies
    table = soup.find('tbody')
    trs = table.find_all('tr')
    for tr in trs:
        currency = tr.find('div', {
            'class': 'visible-phone print_hide'
        }).text.strip()
        currencies.append(currency)
        cash_sell_rate = tr.find('td', {
            'data-table': 'Cash Selling'
        }).text.strip().replace('\r', '').replace('\n', '')
        cash_sell_rates.append(cash_sell_rate)
        spot_sell_rate = tr.find('td', {
            'data-table': 'Spot Selling'
        }).text.strip().replace('\r', '').replace('\n', '')
        spot_sell_rates.append(spot_sell_rate)

    # get abbr. of currencies
    for i in range(len(currencies)):
        tmp = currencies[i].split('(')[1]
        tmp = tmp[:-1]
        currencies_abbr.append(tmp)

    # get exchange rate
    for i in range(len(spot_sell_rates)):
        if spot_sell_rates[i] == '-':
            exchange_rates.append(float(cash_sell_rates[i]))
        else:
            exchange_rates.append(float(spot_sell_rates[i]))

    # build dictionary
    for i in range(len(currencies_abbr)):
        live_exchangerates[currencies_abbr[i]] = exchange_rates[i]

    return live_exchangerates


def abbr_currency_to_country(live_exchange_rates):
    countries = {}  # abbr_currency: country
    target_countries = {}
    ''' Request '''
    requests.packages.urllib3.disable_warnings()
    url = 'https://www.easymarkets.com/int/learn-centre/discover-trading/currency-acronyms-and-abbreviations/'
    re = requests.get(url, verify=False)
    soup = BeautifulSoup(re.text, 'html.parser')
    ''' Get Countries by abbr. of currencies '''
    # Get all countries and their abbr. of currencies
    table = soup.find('table', {'class': 'table table-striped table-hover'})
    table = soup.find('tbody')
    trs = table.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        country_currency = tds[0].text.strip()
        value = ' '.join(country_currency.split()[:-1])
        key = tds[1].text.strip()
        countries[key] = value

    # Get target countries
    for key in live_exchange_rates:
        target_countries[key] = countries[key]

    # Correct certain countries
    target_countries['GBP'] = 'United Kingdom'
    target_countries['KRW'] = 'Korea'
    target_countries['EUR'] = 'Euro Zone'

    return target_countries


def get_avg_exchangerate(countries):
    avg_exchangerates = {}
    avg_NTD_to_USD = 0
    ''' Request '''
    requests.packages.urllib3.disable_warnings()
    ''' Get date '''
    date = datetime.datetime.now()
    year = str(date.year - 20)
    '''Change USA to Taiwan'''
    countries['USD'] = 'Taiwan'
    ''' For every country, calculate average exchange rate '''
    for abbr_currency, country in countries.items():
        rate_sum = 0
        rate_num = 0
        avg_rate = 0
        url = f'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange?fields=exchange_rate&filter=country:in:({country},{country.upper()}),record_date:gte:{year}-01-01'
        rates = requests.get(url, verify=False).json()
        rate_num = rates['meta']['count']
        rates_lst = rates['data']
        for rates_d in rates_lst:
            rate = float(rates_d['exchange_rate'])
            rate_sum += rate
        avg_rate = rate_sum / rate_num
        avg_exchangerates[abbr_currency] = avg_rate
    ''' Caculate average exchange rate: NTD/XX'''
    avg_NTD_to_USD = avg_exchangerates['USD']
    for abbr_currency, avg_rate in avg_exchangerates.items():
        if abbr_currency == 'USD':
            avg_exchangerates[abbr_currency] = round(
                avg_exchangerates[abbr_currency], 4)
            continue
        avg_XX_to_USD = avg_exchangerates[abbr_currency]
        avg_exchangerates[abbr_currency] = avg_NTD_to_USD / avg_XX_to_USD
        avg_exchangerates[abbr_currency] = round(
            avg_exchangerates[abbr_currency], 4)
    ''' Write USA back '''
    countries['USD'] = 'USA'

    return avg_exchangerates


def get_per_exchangerate(live_exchangerates, avg_exchangerates):
    per_exchangerates = {}
    ''' Calculate percentage of rise of fall in exchange rate: (live_exchangerate - avg_exchangerate) / avg_exchangerate x 100 % '''
    for abbr_currency, live_exchangerate in live_exchangerates.items():
        avg_exchangerate = avg_exchangerates[abbr_currency]
        per_exchangerate = round(
            ((live_exchangerate - avg_exchangerate) / avg_exchangerate * 100),
            2)
        per_exchangerates[abbr_currency] = per_exchangerate

    return per_exchangerates


def sort_per_exchangerate(per_exchangerates):
    return sorted(per_exchangerates.items(), key=lambda d: d[1])


def get_crime_safety_index(countries):
    crime_safety_indexes = {}
    index_links = {}
    ''' Request '''
    requests.packages.urllib3.disable_warnings()
    url = 'https://www.numbeo.com/crime/'
    re = requests.get(url, verify=False)
    soup = BeautifulSoup(re.text, 'html.parser')
    ''' Get links for all countries '''
    table = soup.find('table', {'class': 'related_links'})
    As = table.find_all('a')
    for a in As:
        country = a.text
        nextpage = a['href']
        index_links[country] = urljoin(url, nextpage)
    ''' Modify certain countries '''
    countries['USD'] = 'United States'
    countries['KRW'] = 'South Korea'
    ''' For target countries, go to the link and get crime index and safety index '''
    for abbr_currency, country in countries.items():
        if abbr_currency == 'EUR':
            crime_safety_indexes[abbr_currency] = [None, None]
            continue

        # request
        index_link = index_links[country]
        re_index = requests.get(index_link, verify=False)
        soup_index = BeautifulSoup(re_index.text, 'html.parser')

        # get crime index and safety index
        index_table = soup_index.find('table', {'class': 'table_indices'})
        trs = index_table.find_all('tr')[1:]
        crime_index = float(trs[0].find_all('td')[1].text.strip())
        safety_index = float(trs[1].find_all('td')[1].text.strip())

        # save to crime_safety_indexes
        crime_safety_indexes[abbr_currency] = [crime_index, safety_index]
    ''' Write back certain countries '''
    countries['USD'] = 'USA'
    countries['KRW'] = 'Korea'

    return crime_safety_indexes


''' Main '''
country_data = {}


def process_data():
    live_exchangerates = get_live_exchangerate()
    countries = abbr_currency_to_country(live_exchangerates)
    avg_exchangerates = get_avg_exchangerate(countries)
    per_exchangerates = get_per_exchangerate(live_exchangerates,
                                             avg_exchangerates)
    sort_per_exchangerates = sort_per_exchangerate(per_exchangerates)
    crime_safety_indexes = get_crime_safety_index(countries)

    for abbr_currency, per_exchangerate in sort_per_exchangerates:
        country_data[countries[abbr_currency]] = {
            'liveExchangerates': live_exchangerates[abbr_currency],
            'avgExchangerates': avg_exchangerates[abbr_currency],
            'perExchangerate': per_exchangerate,
            'crimeIndex': crime_safety_indexes[abbr_currency][0],
            'safetyIndex': crime_safety_indexes[abbr_currency][1],
        }

    return country_data


if __name__ == '__main__':
    process_data()
    print([*country_data.keys()])
