import argparse
from datetime import datetime
from logzero import logger

from sizun.db import count_new_advertisements


def main(args):
    """ Verify if new ads have been saved and triggers stuff accordingly. """
    try:
        start_date = datetime.strptime(
            args.date,
            '%Y-%m-%dT%H:%M:%S%z'
        )
        count = count_new_advertisements(start_date)
        if count:
            logger.info(f'{count} new houses saved.')
    except ValueError as error:
        logger.error('Date cannot be converted to format YYYY-mm-ddTHH:MM:SS')
        raise error


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("date", help="Date")

    # Optional argument flag which defaults to False
    # parser.add_argument("-f", "--flag", action="store_true", default=False)

    args = parser.parse_args()
    main(args)