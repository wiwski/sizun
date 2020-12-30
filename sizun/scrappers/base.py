from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup, Tag
from logzero import logger
import requests

from ..models.advertisement import Advertisement

@dataclass
class Scrapper:
    # List of urls to scrap
    urls: List[str]


    def scrap(self):
        ads: List[Advertisement] = []
        for url in self.urls:
            logger.debug(f'Parsing URL : {url}')
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            self.clean_soup(soup)
            ads.extend(self.extract_ads(soup))
        return ads
        
    
    def extract_ads(self, soup: BeautifulSoup) -> List[Advertisement]:
        pass

    def clean_soup(self, soup: BeautifulSoup):
        pass