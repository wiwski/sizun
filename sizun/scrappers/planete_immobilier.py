import json
import re
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

from ..models.advertisement import Advertisement
from ..sources import PLANETE_IMMOBILIER_SOURCES
from .base import Scrapper


class PlaneteImmobilierScrapper(Scrapper):

    def __init__(self):
        self.urls = PLANETE_IMMOBILIER_SOURCES

    def extract_ads(self, soup: BeautifulSoup) -> List[Advertisement]:
        ad_tags = soup.find_all('div', class_='res_div1')
        advertisements = list(map(lambda ad: Advertisement(
            id=None,
            source='planete_immobilier',
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
    ad_type = _extract_type(ad)
    type_mapping = {
        'flat': 'appartement',
        'house': 'maison',
        'field': 'terrain',
        'unknown': 'bien'
    }
    return f'{type_mapping[ad_type].capitalize()} à {_extract_city(ad).capitalize()}'


def _extract_description(ad: Tag):
    description_tag = ad.find('p', {'itemprop': 'description'})
    for tag in description_tag.children:
        if tag.string and tag.string[:3] == ' : ':
            return tag.string[3:]


def _extract_price(ad: Tag):
    return int(ad.find('div', {'itemprop': 'price'})['content'])


def _extract_url(ad: Tag):
    return 'http://www.planete-immobilier.fr' + ad.find('a', class_='prod_details')['href']


def _extract_garden_area(ad: Tag):
    if _extract_type(ad) == 'field':
        description = _extract_description(ad)
        index = description.find('m²')
        if index != -1:
            area_list = []
            while index > 0:
                index = index - 1
                if description[index] == ' ':
                    continue
                if not description[index].isdigit():
                    break
                area_list.append(description[index])
            if area_list:
                return int(''.join(reversed(area_list)))
    return None


def _extract_house_area(ad: Tag):
    return None


def _extract_picture_url(ad: Tag):
    picture_link_style = ad.find('a', {'itemprop': 'url'})['style']
    for style in picture_link_style.split(';'):
        if 'background-image' in style:
            return style.split('url(')[1][:-1]


def _extract_type(ad: Tag):
    title = ad.find(class_='loc_details').text
    if 'Terrain' in title:
        return 'field'
    elif 'Maison' in title:
        return 'house'
    else:
        return 'unknown'


def _extract_date(ad: Tag):
    return None


def _extract_ref(ad: Tag):
    return ad.find('p', {'itemprop': 'description'}).find('strong').string.replace('Ref. ', '')


def _extract_city(ad: Tag):
    details = ad.find('div', class_='loc_details').text.replace('Terrain Constructible ', '').replace(
        'Maison ', '')
    city = []
    for word in details.split(' '):
        if 'CAP' not in word and not word.isdigit():
            city.append(word)
            continue
        break
    if city:
        return ' '.join(city).lower()
    return None
