import re
from typing import List

from bs4 import BeautifulSoup, Tag

from ..models.advertisement import Advertisement
from ..sources import SUPERIMMO_SOURCES
from .base import Scrapper
from .utils import formatted_price_to_int


class SuperimmoScrapper(Scrapper):

    def __init__(self):
        self.urls = SUPERIMMO_SOURCES

    def extract_ads(self, soup: BeautifulSoup) -> List[Advertisement]:
        ad_tags = soup.find_all('article', class_=re.compile('listing-id-\S.'))
        advertisements = list(map(lambda ad: Advertisement(
            id=None,
            source='superimmo',
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
    title = ad.find('b', class_='titre').string
    return f'{title} à {_extract_city(ad).capitalize()}'


def _extract_description(ad: Tag):
    if ad.find('p', class_='js-desc-truncate'):
        return ad.find('p', class_='js-desc-truncate').string
    elif ad.find(class_='links-bloc').previous_sibling and ad.find(class_='links-bloc').previous_sibling.previous_sibling:
        return ad.find(class_='links-bloc').previous_sibling.previous_sibling.string


def _extract_price(ad: Tag):
    price_tag = ad.find(class_='prix')
    if price_tag and price_tag.string:
        return formatted_price_to_int(price_tag.string)
    # In case of "Prix en baisse"
    elif price_tag.children:
        for child_tag in price_tag.children:
            if child_tag.string and '€' in child_tag.string:
                return int(child_tag.string.strip().replace(' ', '').replace('€', '').replace(u'\xa0', u''))


def _extract_url(ad: Tag):
    return 'https://www.superimmo.com' + ad.find(class_='listing-link')['href']


def _extract_garden_area(ad: Tag):
    if _extract_type(ad) in ['house', 'flat']:
        media_heading_tag = ad.find(class_='media-heading')
        if media_heading_tag and list(media_heading_tag.children):
            link_tag = next(media_heading_tag.children)
            if link_tag:
                info_text = link_tag.string
                for text in info_text.split(' - '):
                    if 'ter.' in text:
                        return int(text.replace('ter.', '').replace('m²', '').replace(' ', ''))
    elif _extract_type(ad) == 'field':
        title = ad.find(class_='titre').string
        try:
            return int(re.sub('[^0-9]', '', title))
        except ValueError:
            return None
    return None


def _extract_house_area(ad: Tag):
    if _extract_type(ad) in ['house', 'flat']:
        title = ad.find(class_='titre').string
        house_area = re.sub('[^0-9]', '', title)
        if house_area:
            return int(house_area)
    return None


def _extract_picture_url(ad: Tag):
    return ad.find_all('img')[1]['src']


def _extract_type(ad: Tag):
    ad_type = ad.find(class_='titre').string.split(' ')[0]
    if ad_type == 'Terrain':
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
    return None


def _extract_city(ad: Tag):
    for b_tag in ad.find_all('b'):
        if b_tag.string and '(29' in b_tag.string:
            return b_tag.string.split(' (')[0]
    return None
