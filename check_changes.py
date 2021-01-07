import argparse
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from logzero import logger

from sizun.db import count_new_advertisements

load_dotenv()


def main(args):
    """ Verify if new ads have been saved and triggers stuff accordingly. """
    try:
        start_date = datetime.strptime(
            args.date,
            '%Y-%m-%dT%H:%M:%S%z'
        )
        count = count_new_advertisements(start_date)
        if count:
            logger.info(f'{count} new houses saved. Triggering new build.')
            netlify_hook = os.getenv('NETLIFY_BUILD_HOOK')
            if not netlify_hook:
                raise ValueError('NETLIFY_BUILD_HOOK variable should be set.')
            r = requests.post(netlify_hook)
            r.raise_for_status()
            logger.info('Build triggered.')
        else:
            logger.info('No new saved ads. Exiting.')
    except ValueError as error:
        logger.error('Date cannot be converted to format YYYY-mm-ddTHH:MM:SS+00:00')
        raise error


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("date", help="Date")

    # Optional argument flag which defaults to False
    # parser.add_argument("-f", "--flag", action="store_true", default=False)

    args = parser.parse_args()
    main(args)