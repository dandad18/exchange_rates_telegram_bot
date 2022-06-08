import requests
import fake_useragent
from bs4 import BeautifulSoup as BS
from typing import NamedTuple
from enum import Enum
from exceptions import ConnectionErrorException


header = {
    'user-agent': fake_useragent.UserAgent().random
}


class Currency(Enum):
    USD = (0, 'US Dollar', 'USD')
    EUR = (1, 'Euro', 'EUR')
    RUB = (2, 'Russian rubles (100)', 'RUB')


class CurrencyInfo(NamedTuple):
    name: Currency
    sale: float
    buy: float
    national_bank: float


def get_exchange_rates_info(currency: str) -> CurrencyInfo:
    # Some actions with Currency
    curr_as_enum = None
    for enum_curr in Currency:
        if currency == enum_curr.value[2]:
            curr_as_enum = enum_curr

    # Getting
    myfin_response = _get_response_from_site(url='https://myfin.by/currency/minsk')
    if not myfin_response.ok:
        raise ConnectionErrorException("Bot can't get response from website. Sorry...")
    else:
        return _parse_response(response=myfin_response.text, currency=curr_as_enum)


def _get_response_from_site(url: str) -> requests.models.Response:
    return requests.get(url, headers=header)


def _parse_response(response: str, currency: Currency) -> CurrencyInfo:
    soup = BS(response, 'lxml')
    finance_table = soup.find('div', class_='table-responsive')
    info_about_curr = finance_table.find('table').find('tbody').find_all('tr')[currency.value[0]].find_all('td')
    return CurrencyInfo(
        name=currency.value[1],
        sale=float(info_about_curr[1].text),
        buy=float(info_about_curr[2].text),
        national_bank=float(info_about_curr[3].text)
    )
