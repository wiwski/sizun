import re
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, NavigableString, Tag

from ..models.advertisement import Advertisement
from ..sources import OUEST_FRANCE_SOURCES
from .base import Scrapper


class OuestFranceScrapper(Scrapper):

    def __init__(self):
        self.urls = OUEST_FRANCE_SOURCES

    def extract_ads(self, soup: BeautifulSoup) -> List[Advertisement]:
        ads = soup.find_all(class_='annLink')
        advertisements = list(map(lambda ad: Advertisement(
            id=None,
            source='ouest_france',
            ref=_extract_ref(ad),
            name=ad.find(class_='annTitre').string.strip(),
            description=ad.find(class_='annTexte').string.strip(),
            price=_extract_price(ad),
            url='https://www.ouestfrance-immo.com/' + ad['href'],
            house_area=_extract_house_area(ad),
            garden_area=0,
            picture_url=ad.find(class_='photoClassique').find('img')[
                'data-original'],
            localization=_extract_city(ad),
            date=_extract_date(ad),
            type=_extract_type(ad)
        ), ads))
        return advertisements


def _extract_house_area(ad: Tag):
    information_tag = ad.find(class_='annCriteres')
    if information_tag:
        for information in information_tag.children:
            if not type(information) == NavigableString and 'm²' in information.text:
                return information.text.replace(' ', '').replace('m²', '')
    return None


def _extract_type(ad: Tag):
    name = ad.find(class_='annTitre').string
    if 'Maison' in name:
        return 'house'
    elif 'Terrain' in name:
        return 'field'
    else:
        return 'unknown'


def _extract_date(ad: Tag):
    date_str = ad.find(class_='annDebAff').string.strip()
    try:
        return datetime.strptime(date_str, '%d/%m/%y')
    except ValueError:
        return None


def _extract_ref(ad: Tag):
    description = ad.find(class_='annTexte').string
    search = re.findall(r'Réf. ([\d]+)', description) or [None]
    return search[0]


def _extract_city(ad: Tag):
    city_tag = ad.find(class_='annVille')
    if city_tag:
        return city_tag.string.lower()
    return None


def _extract_price(ad: Tag):
    price_tag = ad.find(class_='annPrix')
    price = None
    if price_tag.string:
        price = int(price_tag.string.replace(
            '\xa0€', '').strip().replace(' ', ''))
    # In case of "Prix en baisse"
    elif list(price_tag.children):
        for t in price_tag.children:
            if t.string and '€' in t.string:
                price = int(t.string.replace(
                    '\xa0€', '').strip().replace(' ', ''))
                break
    return price
