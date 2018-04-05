from django.contrib import admin

# Register your models here.
from defacto.models import (
    KospiAgentData,
    KospiTruePriceData,
    KosdaqAgentData,
    KosdaqTruePriceData,
    KospiAbsoulteScore,
    KosdaqAbsoulteScore,
    KospiScoreData,
    KosdaqScoreData,
    RankData,
    KospiRelativeCalc,
    KosdaqRelativeCalc,
    )

models = [
    KospiAgentData,
    KospiTruePriceData,
    KosdaqAgentData,
    KosdaqTruePriceData,
    KospiAbsoulteScore,
    KosdaqAbsoulteScore,
    KospiScoreData,
    KosdaqScoreData,
    RankData,
    KospiRelativeCalc,
    KosdaqRelativeCalc,
    ]

for model in models:
    admin.site.register(model)
