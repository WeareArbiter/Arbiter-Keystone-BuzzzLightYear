from django.contrib import admin

from defacto.models import (
    KospiAgentData,
    KospiTruePriceData,
    KosdaqAgentData,
    KosdaqTruePriceData,
    KospiAbsoluteScore,
    KosdaqAbsoluteScore,
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
    KospiAbsoluteScore,
    KosdaqAbsoluteScore,
    KospiScoreData,
    KosdaqScoreData,
    RankData,
    KospiRelativeCalc,
    KosdaqRelativeCalc,
]

for model in models:
    admin.site.register(model)
