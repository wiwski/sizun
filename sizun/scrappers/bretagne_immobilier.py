import json
import re
from typing import List

import requests
from bs4 import BeautifulSoup, Tag

from ..models.advertisement import Advertisement
from ..sources import BRETAGNE_IMMOBILIER_SOURCES
from .base import Scrapper
from .utils import formatted_price_to_int


class BretagneImmobilierScrapper(Scrapper):

    def __init__(self):
        self.urls = BRETAGNE_IMMOBILIER_SOURCES

    def extract_ads(self, soup: BeautifulSoup) -> List[Advertisement]:
        ad_tags = soup.find_all('div', class_='property')
        advertisements = list(map(lambda ad: Advertisement(
            id=None,
            source='bretagne_immobilier',
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
    ad_type = ad.find(class_='col-xs-6 col-md-7').find('a').string.strip()
    return f'{ad_type} à {_extract_city(ad).capitalize()}'


def _extract_description(ad: Tag):
    return ad.find('p', class_='col-md-12').text


def _extract_price(ad: Tag):
    return formatted_price_to_int(ad.find('h4', class_='text-right').text)


def _extract_url(ad: Tag):
    return ad.find_all('a')[0]['href']


def _extract_garden_area(ad: Tag):
    return None


def _extract_house_area(ad: Tag):
    return None


def _extract_picture_url(ad: Tag):
    return 'http://www.bretagneimmobilier.bzh' + ad.find_all('img')[0]['src']


def _extract_type(ad: Tag):
    title = ad.find(class_='col-xs-6 col-md-7').find('a').text
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
    return ad.find('span', class_='label label-default not-bold').string


def _extract_city(ad: Tag):
    return ad.find(class_='localisation').text.split(' (29')[0].strip().lower()
