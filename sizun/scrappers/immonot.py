import re
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup, Tag, NavigableString

from .base import Scrapper
from ..models.advertisement import Advertisement
from ..sources import IMMNONOT_SOURCES


class ImmonotScrapper(Scrapper):

    def __init__(self):
        self.urls = IMMNONOT_SOURCES

    def extract_ads(self, soup: BeautifulSoup) -> List[Advertisement]:
        ad_tags = soup.find_all(class_='il-card--VENT')
        advertisements = list(map(lambda ad: Advertisement(
            id=None,
            source='immonot',
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

    def fetch_html(self, url: str) -> requests.Response:
        r = requests.get('https://www.immonot.com/')
        soup = BeautifulSoup(r.text, 'html.parser')
        input_csrf_token = soup.find('input', {'name': 'WAEFIK_CSRF_TOKEN'})
        assert input_csrf_token and input_csrf_token.get('value')
        r = requests.post(url, data={
            'WAEFIK_CSRF_TOKEN': input_csrf_token.get('value'),
            'action': 'recherche',
            'indexDebut': 0,
            'tri': 'date',
            'sensTri': 'desc',
            'modePresentationListe': 'sm',
            'typesBiens': 'MAIS,APPT,TEBA,PROP',
            'transactions': 'VENT',
            'surfaceInt': '0-0',
            'surfaceExt': '0-0',
            'prix': '0-150000',
            'localite': '29790 Pont-Croix,29770 Primelin,29770 Audierne,29770 Plogoff,29770 Cléden-Cap-Sizun,29770 Goulien,29790 Beuzec-Cap-Sizun,29780 Plouhinec,29790 Confort-Meilars,29100 Poullan-sur-Mer',
            'rayon': '0',
            'reference': None,
            'nbPieces': None,
            'nbChambres': None
        })
        return r


def _extract_name(ad: Tag):
    name = ''
    type_name = _extract_type(ad)
    if type_name == 'house':
        name += 'Maison'
    elif type_name == 'field':
        name += 'Terrain'
    elif type_name == 'flat':
        name += 'Appartement'
    else :
        name += 'Bien'
    name += f' à {_extract_city(ad).capitalize()}'
    return name

def _extract_description(ad: Tag):
    return ad.find(id=re.compile('desc-fr-\d+')).string

def _extract_price(ad: Tag):
    price_tag = next(ad.find(class_='il-card-price').find('strong').children)
    return int(price_tag.string.strip().replace(' ', '').replace('€', '').replace(u'\xa0', u''))

def _extract_url(ad: Tag):
    url = ad.find(class_='il-card-head').find_all('a')[0]['href']
    return 'https://www.immonot.com' + url

def _extract_garden_area(ad: Tag):
    quickview_tags = ad.find_all(class_='il-card-quickview-item')
    for quickview_tag in quickview_tags:
        if 'Extérieur' in quickview_tag.text:
            garden_area_str = quickview_tag.find('strong').text
            return int(garden_area_str.replace(' ', '').replace('m2', ''))
    return None

def _extract_house_area(ad: Tag):
    quickview_tags = ad.find_all(class_='il-card-quickview-item')
    for quickview_tag in quickview_tags:
        if 'Intérieur' in quickview_tag.text:
            house_area_str = quickview_tag.find('strong').text
            return int(house_area_str.replace(' ', '').replace('m2', ''))
    return None

def _extract_picture_url(ad: Tag):
    image_tag = ad.find(class_='il-card-img')
    return 'https:' + image_tag.get('data-src')

def _extract_type(ad: Tag):
    ad_type = ad.find(class_='il-card-type').string
    if ad_type == 'Terrain à bâtir':
        return 'field'
    elif ad_type == 'Maison':
        return 'house'
    elif ad_type == 'Appartement':
        return 'flat'
    else:
        return 'unknown'


def _extract_date(ad: Tag):
    return None


def _extract_ref(ad: Tag):
    ref_tag = ad.find(class_='il-card-excerpt').find('small')
    return ref_tag.string.replace('Réf: ', '')


def _extract_city(ad: Tag):
    city_tag = ad.find(class_='il-card-locale')
    if city_tag:
        return city_tag.string.split(' - ')[0].lower()
    return None
