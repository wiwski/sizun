from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.advertisement import Advertisement

engine = create_engine('sqlite:///sizun.db')

Advertisement.metadata.create_all(engine)


def save_advertisements(advertisements: Advertisement):
    session = (sessionmaker(bind=engine))()
    for ad in advertisements:
        match = session.query(Advertisement).filter_by(
            url=ad.url
        ).count()
        if not match:
            session.add(ad)
    session.commit()