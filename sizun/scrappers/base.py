from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup, Tag
from logzero import logger

from ..models.advertisement import Advertisement


@dataclass
class Scrapper:
    # List of urls to scrap
    urls: List[str]

    def scrap(self):
        ads: List[Advertisement] = []
        for url in self.urls:
            logger.debug(f'Parsing URL : {url}')
            r = self.fetch_html(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            self.clean_soup(soup)
            try:
                ads.extend(self.extract_ads(soup))
            except AttributeError as e:
                logger.error(e)
        return ads

    def extract_ads(self, soup: BeautifulSoup) -> List[Advertisement]:
        pass

    def fetch_html(self, url: str) -> requests.Response:
        return requests.get(url)

    def clean_soup(self, soup: BeautifulSoup):
        pass
