import argparse

from logzero import logger

from sizun.db import save_advertisements
from sizun.scrappers import (FigaroScrapper, ImmonotScrapper,
                             OuestFranceScrapper, SuperimmoScrapper)


def main(args):
    """ Main entry point of the app """
    if args.source == 'ouest_france':
        ads = OuestFranceScrapper().scrap()
    elif args.source == 'immonot':
        ads = ImmonotScrapper().scrap()
    elif args.source == 'figaro':
        ads = FigaroScrapper().scrap()
    elif args.source == 'superimmo':
        ads = SuperimmoScrapper().scrap()
    else:
        raise 'Source not implemented'
    logger.info(f'Scrapped {args.source}...')
    save_advertisements(ads)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("source", help="Real estate advertisement source")

    # Optional argument flag which defaults to False
    # parser.add_argument("-f", "--flag", action="store_true", default=False)

    args = parser.parse_args()
    main(args)
