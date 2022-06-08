import requests
import fake_useragent
from typing import NamedTuple
from bs4 import BeautifulSoup as BS
from get_currency_info import _get_response_from_site
from exceptions import ConnectionErrorException


def get_best_bank_to_buy_curr() -> str:
    """
    This function provides user with name of bank, where he/she can buy currency with the cheapest cost.
    :return: Bank name (str)
    """

    myfin_response = _get_response_from_site('https://myfin.by/currency/minsk')
    if not myfin_response.ok:
        raise ConnectionErrorException("Bot can't get response from website. Sorry...")
    else:
        pass

def _parse_response_with_bank_info(response: str) -> str:
    soup = BS(response, 'lxml')
    banks_info_list = soup.find('tbody', id='currency_tbody').find_all('tr', class_='tr-tb')
    # here I will continue to parse banks info..................................................................


if __name__ == '__main__':
    _parse_response_with_bank_info(response=_get_response_from_site('https://myfin.by/currency/minsk').text)

