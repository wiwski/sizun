import argparse

import sentry_sdk
from logzero import logger

from sentry import load_sentry
from sizun.db import save_advertisements
from sizun.scrappers import (AudierneImmobilierScrapper,
                             BourseImmobilierScrapper, FigaroScrapper,
                             FinistereImmobilierScrapper, ImmonotScrapper,
                             OuestFranceScrapper, PlaneteImmobilierScrapper,
                             SuperimmoScrapper)


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
    elif args.source == 'planete_immobilier':
        ads = PlaneteImmobilierScrapper().scrap()
    elif args.source == 'audierne_immobilier':
        ads = AudierneImmobilierScrapper().scrap()
    elif args.source == 'bourse_immobilier':
        ads = BourseImmobilierScrapper().scrap()
    elif args.source == 'finistere_immobilier':
        ads = FinistereImmobilierScrapper().scrap()
    else:
        raise ValueError('Source not implemented')
    logger.info(f'Scrapped {args.source}...')
    if not ads:
        logger.error(
            f'Scrapper {args.source} didn\'t find any ad... Is it broken ?')
    save_advertisements(ads)


if __name__ == "__main__":
    load_sentry()
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("source", help="Real estate advertisement source")

    # Optional argument flag which defaults to False
    # parser.add_argument("-f", "--flag", action="store_true", default=False)

    args = parser.parse_args()
    main(args)
