from __future__ import absolute_import, unicode_literals
from celery.decorators import task

from .Crawler import Scrape_WebData
from stockapi.models import (
    Ticker,
    KospiOHLCV,
    KosdaqOHLCV,
    KospiNet,
    KosdaqNet,
    Info,)
