#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from logzero import logger

from sizun.scrappers import OuestFranceScrapper
from sizun.db import engine, save_advertisements


def main(args):
    """ Main entry point of the app """
    logger.info(args)
    if args.source == 'ouest_france':
        logger.info('Scrapping Ouest France...')
        ads = OuestFranceScrapper().scrap()
    else:
        raise 'Source not implemented'
    save_advertisements(ads)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("source", help="Real estate advertisement source")

    # Optional argument flag which defaults to False
    # parser.add_argument("-f", "--flag", action="store_true", default=False)

    args = parser.parse_args()
    main(args)