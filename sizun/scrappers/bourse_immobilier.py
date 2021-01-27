import json
import re
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

from ..models.advertisement import Advertisement
from ..sources import BOURSE_IMMOBILIER_SOURCES
from .base import Scrapper
from .utils import formatted_area_to_int, formatted_price_to_int


class BourseImmobilierScrapper(Scrapper):

    def __init__(self):
        self.urls = BOURSE_IMMOBILIER_SOURCES

    def extract_ads(self, soup: BeautifulSoup) -> List[Advertisement]:
        ad_tags = soup.find_all('div', class_='bien-bi')
        advertisements = list(map(lambda ad: Advertisement(
            id=None,
            source='bourse_immobilier',
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
    ad_type = ad.find(class_='ville').string.split(' ')[0]
    return f'{ad_type} à {_extract_city(ad).capitalize()}'


def _extract_description(ad: Tag):
    return None


def _extract_price(ad: Tag):
    return formatted_price_to_int(ad.find(class_='prix').text)


def _extract_url(ad: Tag):
    return 'https://www.bourse-immobilier.fr' + ad.find_all('a')[0]['href']


def _extract_area(ad: Tag):
    match = re.search(
        r'\d+ m²', ad.find(class_='ville').text)
    if match:
        return int(match.group().replace(' m²', ''))


def _extract_garden_area(ad: Tag):
    if _extract_type(ad) == 'field':
        return _extract_area(ad)


def _extract_house_area(ad: Tag):
    if _extract_type(ad) in ['house', 'flat']:
        return _extract_area(ad)


def _extract_picture_url(ad: Tag):
    return ad.find(class_='container-photo')['data-src']


def _extract_type(ad: Tag):
    title = ad.find(class_='ville').text
    if 'Terrain' in title:
        return 'field'
    elif 'Maison' in title:
        return 'house'
    elif 'Appartement' in title:
        return 'flat'
    else:
        return 'unknown'


def _extract_date(ad: Tag):
    return None


def _extract_ref(ad: Tag):
    return None


def _extract_city(ad: Tag):
    return ad.find(class_='description-1').string.split(' (29')[0].lower()
