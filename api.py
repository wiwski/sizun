from flask_api import FlaskAPI

from sentry import load_sentry
from sizun.db import fetch_latest_advertisments

load_sentry()

app = FlaskAPI(__name__)


@app.route('/')
def home():
    ads = fetch_latest_advertisments(price_max=200000)
    return {'advertisments': list(map(lambda ad: {
        'id': ad.id,
        'ref': ad.ref,
        'name': ad.name,
        'description': ad.description,
        'price': ad.price,
        'source': ad.source,
        'url': ad.url,
        'house_area': ad.house_area,
        'garden_area': ad.garden_area,
        'picture_url': ad.picture_url,
        'localization': ad.localization,
        'date': ad.date,
        'type': ad.type,
        'created': ad.created
    }, ads))}


if __name__ == "__main__":
    app.run(debug=True)
