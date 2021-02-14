import os
import pathlib
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
from logzero import logger
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

from .models.advertisement import Advertisement

load_dotenv(pathlib.Path(__file__).parent.absolute() / '../.env')
sql_lite_db_path = os.getenv('SQLITE_DB_FILE_PATH')
assert sql_lite_db_path
engine = create_engine(f'sqlite:///{sql_lite_db_path}')

Advertisement.metadata.create_all(engine)


def save_advertisements(advertisements: Advertisement, change_if_first_time=True):
    session = (sessionmaker(bind=engine))()

    # Checks if it is first time we insert the source in the DB.
    # If it is, we modify the created field so that it doesn't appears in front of the latests results
    all_sources_in_db = _get_all_source_in_db()

    inserted_advertisements_count = 0
    for ad in advertisements:
        # Checks another ad with same URL doesn't already exist
        match = session.query(Advertisement).filter_by(
            url=ad.url
        ).count()
        if not match:
            is_first_source_insert = ad.source not in all_sources_in_db
            if is_first_source_insert:
                oldest_advertisement_created_date = _get_oldest_advertisement_creation_date()
                ad.created = oldest_advertisement_created_date
            session.add(ad)
            inserted_advertisements_count += 1
    session.commit()
    logger.info(f'Saved {inserted_advertisements_count} new advertisements.')


def count_new_advertisements(start_date: datetime):
    session = (sessionmaker(bind=engine))()
    return session.query(Advertisement).filter(
        Advertisement.created.between(start_date, datetime.now())
    ).count()


def fetch_latest_advertisments(price_max: int = None):
    session = (sessionmaker(bind=engine))()
    query = session.query(Advertisement)
    if price_max is not None:
        query = query.filter(
            or_(
                Advertisement.price <= price_max,
                Advertisement.price == None
            )
        )
    return query.order_by(Advertisement.created.desc()).limit(50).all()


def delete_advertisements_with_params(**kwargs):
    session = (sessionmaker(bind=engine))()
    rows_deleted = session.query(Advertisement).filter_by(**kwargs).delete()
    session.commit()
    return rows_deleted


def _get_all_source_in_db() -> List[str]:
    import itertools
    session = (sessionmaker(bind=engine))()
    query = session.query(Advertisement.source).group_by(
        Advertisement.source).all()
    session.close()
    return list(itertools.chain(*query))


def _get_oldest_advertisement_creation_date() -> Optional[datetime]:
    session = (sessionmaker(bind=engine))()
    oldest_advertisement_created_date = session.query(
        Advertisement.created).order_by(Advertisement.created.asc()).first()
    if oldest_advertisement_created_date:
        return oldest_advertisement_created_date[0]
