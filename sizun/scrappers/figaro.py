import re
import json
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup, Tag, NavigableString

from .base import Scrapper
from ..models.advertisement import Advertisement
from ..sources import FIGARO_SOURCES


class FigaroScrapper(Scrapper):

    def __init__(self):
        self.urls = FIGARO_SOURCES

    def extract_ads(self, soup: BeautifulSoup) -> List[Advertisement]:
        ad_tags = soup.find_all(id=re.compile('list-item-\d.+'))
        advertisements = list(map(lambda ad: Advertisement(
            id=None,
            source='figaro',
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
    name = ''
    type_name = _extract_type(ad)
    if type_name == 'house':
        name += 'Maison'
    elif type_name == 'field':
        name += 'Terrain'
    else :
        name += 'Bien'
    name += f' à {_extract_city(ad).capitalize()}'
    return name

def _extract_description(ad: Tag):
    return ad.find(class_='list-item-details__description').string

def _extract_price(ad: Tag):
    price_tag = ad.find(class_='price').find('span')
    return int(price_tag.string.strip().replace(' ', '').replace('€', '').replace(u'\xa0', u''))

def _extract_url(ad: Tag):
    return ad.find(class_='list-item-details__link')['href']

def _extract_garden_area(ad: Tag):
    if _extract_type(ad) == 'field':
        properties_tags = ad.find(class_='list-item-details__properties')
        for tag in properties_tags.children:
            if 'M2' in tag.string:
                return tag.string.strip().replace('M2', '')
    return None

def _extract_house_area(ad: Tag):
    if _extract_type(ad) == 'house':
        properties_tags = ad.find(class_='list-item-details__properties')
        for tag in properties_tags.children:
            if 'M2' in tag.string:
                return tag.string.strip().replace('M2', '')
    return None

def _extract_picture_url(ad: Tag):
    image_wrapper = ad.find(class_='item-img__alone')
    if image_wrapper and image_wrapper.find('img').get('src', None):
        return image_wrapper.find('img').get('src', None)
    elif ad.find('script'):
        lazy_url = json.loads(ad.find('script').string).get('image', None)
        if lazy_url:
            if len(lazy_url.split('icc()/')) > 1:
                return lazy_url.split('icc()/')[1].split('.jpg')[0] + '.jpg'
            else :
                return lazy_url
    return None

def _extract_type(ad: Tag):
    ad_type = ad.find(class_='list-item-details__estate-type').string
    if ad_type == 'terrain':
        return 'field'
    elif ad_type == 'maison':
        return 'house'
    else:
        return 'unknown'


def _extract_date(ad: Tag):
    return None


def _extract_ref(ad: Tag):
    return None


def _extract_city(ad: Tag):
    city_tag = ad.find(class_='list-item-details__localisation')
    if city_tag:
        return city_tag.string.split(' ')[0].lower()
    return None
