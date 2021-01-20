import os

import sentry_sdk
from dotenv import load_dotenv

load_dotenv()


def load_sentry():
    if os.getenv('SENTRY_URL'):
        sentry_sdk.init(
            os.getenv('SENTRY_URL'),
            traces_sample_rate=1.0
        )
