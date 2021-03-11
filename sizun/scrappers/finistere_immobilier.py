import json
import re
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

from ..models.advertisement import Advertisement
from ..sources import FINISTERE_IMMOBILIER_SOURCES
from .base import Scrapper
from .utils import extract_area, formatted_price_to_int


class FinistereImmobilierScrapper(Scrapper):

    def __init__(self):
        self.urls = FINISTERE_IMMOBILIER_SOURCES

    def extract_ads(self, soup: BeautifulSoup) -> List[Advertisement]:
        ad_tags = soup.find_all('li', class_='listing')
        advertisements = list(map(lambda ad: Advertisement(
            id=None,
            source='finistere_immobilier',
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
    ad_type = ad.find(
        class_='property-type').find(class_='right').string.split(' ')[0]
    return f'{ad_type} à {_extract_city(ad).capitalize()}'


def _extract_description(ad: Tag):
    if ad.find(class_='propinfo').find('p'):
        return ad.find(class_='propinfo').find('p').string


def _extract_price(ad: Tag):
    if ad.find(class_='listing-price'):
        return formatted_price_to_int(ad.find(class_='listing-price').text)


def _extract_url(ad: Tag):
    return ad.find_all('a')[0]['href']


def _extract_garden_area(ad: Tag):
    area_info_tag = ad.find(class_='row lotsize')
    if area_info_tag:
        return extract_area(area_info_tag.find(class_='right').text, square_unit='m2')


def _extract_house_area(ad: Tag):
    area_info_tag = ad.find(class_='row sqft')
    if area_info_tag:
        return int(area_info_tag.find(class_='right').string.replace(u'\xa0', ''))


def _extract_picture_url(ad: Tag):
    return ad.find_all('img')[0]['src']


def _extract_type(ad: Tag):
    title = ad.find('header').text
    if 'Terrain' in title:
        return 'field'
    elif any(title in t for t in ['Maison', 'Propriété']):
        return 'house'
    elif 'Appartement' in title:
        return 'flat'
    else:
        return 'unknown'


def _extract_date(ad: Tag):
    return None


def _extract_ref(ad: Tag):
    return ad.find('header').text.split(' ')[0].strip()


def _extract_city(ad: Tag):
    return ad.find(class_='location').string.split(',')[0].lower()
