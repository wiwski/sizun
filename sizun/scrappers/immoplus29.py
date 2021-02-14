import json
import re
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

from ..models.advertisement import Advertisement
from ..sources import IMMOPLUS29_SOURCES
from .base import Scrapper
from .utils import extract_area, formatted_price_to_int


class Immoplus29Scrapper(Scrapper):

    def __init__(self):
        self.urls = IMMOPLUS29_SOURCES

    def extract_ads(self, soup: BeautifulSoup) -> List[Advertisement]:
        ad_tags = soup.find_all(class_='bloc_liste_bien')
        advertisements = list(map(lambda ad: Advertisement(
            id=None,
            source='immoplus29',
            ref=_extract_ref(ad),
            name=_extract_name(ad),
            description=_extract_description(ad),
            price=_extract_price(ad),
            url=_extract_url(ad),
            house_area=_extract_house_area(ad),
            garden_area=_extract_garden_area(ad),
            picture_url=_extract_picture_url(ad),
            localization=_extract_city(ad),
            date=_extract_date(ad),
            type=_extract_type(ad)
        ), ad_tags))
        return advertisements


def _extract_name(ad: Tag):
    ad_title = ad.find(
        class_='article-header').text.strip().capitalize()
    return f'{ad_title} à {_extract_city(ad).capitalize()}'


def _extract_description(ad: Tag):
    return None


def _extract_price(ad: Tag):
    return formatted_price_to_int(ad.find(class_='prix').text)


def _extract_url(ad: Tag):
    return ad.find_all('a')[0]['href']


def _extract_garden_area(ad: Tag):
    if _extract_type(ad) == 'field' and ad.find(class_='surface'):
        return extract_area(ad.find(class_='surface').text, regex_pattern=r'(\d+ )|(\d+.\d+)', comma_char='.')


def _extract_house_area(ad: Tag):
    if _extract_type(ad) != 'field' and ad.find(class_='surface'):
        return extract_area(ad.find(class_='surface').text, regex_pattern=r'(\d+ )|(\d+.\d+)', comma_char='.')


def _extract_picture_url(ad: Tag):
    return ad.find_all('img')[0]['src']


def _extract_type(ad: Tag):
    title = ad.find(
        class_='article-header').text.lower()
    if 'terrain' in title:
        return 'field'
    elif 'maison' in title:
        return 'house'
    elif 'appartement' in title:
        return 'flat'
    else:
        return 'unknown'


def _extract_date(ad: Tag):
    return None


def _extract_ref(ad: Tag):
    return None


def _extract_city(ad: Tag):
    return ad.find(class_='ville-block').text.strip().lower()
