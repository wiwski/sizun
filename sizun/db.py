import os
import pathlib
from datetime import datetime

from dotenv import load_dotenv
from logzero import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.advertisement import Advertisement

load_dotenv(pathlib.Path(__file__).parent.absolute() / '../.env')
sql_lite_db_path = os.getenv('SQLITE_DB_FILE_PATH')
assert sql_lite_db_path
engine = create_engine(f'sqlite:///{sql_lite_db_path}')

Advertisement.metadata.create_all(engine)


def save_advertisements(advertisements: Advertisement):
    session = (sessionmaker(bind=engine))()
    inserted_advertisements_count = 0
    for ad in advertisements:
        match = session.query(Advertisement).filter_by(
            url=ad.url
        ).count()
        if not match:
            session.add(ad)
            inserted_advertisements_count += 1
    session.commit()
    logger.info(f'Saved {inserted_advertisements_count} new advertisements.')


def count_new_advertisements(start_date: datetime):
    session = (sessionmaker(bind=engine))()
    return session.query(Advertisement).filter(
        Advertisement.created.between(start_date, datetime.now())
    ).count()


def fetch_latest_advertisments():
    session = (sessionmaker(bind=engine))()
    return session.query(Advertisement).order_by(Advertisement.created.desc()).limit(50).all()


def delete_advertisements_with_params(**kwargs):
    session = (sessionmaker(bind=engine))()
    rows_deleted = session.query(Advertisement).filter_by(**kwargs).delete()
    session.commit()
    return rows_deleted
