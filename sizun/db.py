from datetime import datetime

from logzero import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.advertisement import Advertisement

engine = create_engine('sqlite:///sizun.db')

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