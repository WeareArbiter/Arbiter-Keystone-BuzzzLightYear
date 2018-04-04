from django.contrib import admin

# Register your models here.
from defacto.models import (
    DefactoReg,
    KospiAgentData,
    KospiAgentCalcData,
    KosdaqAgentData,
    KosdaqAgentCalcData,
    KospiScoreData,
    KosdaqScoreData,
    RankData,
    KospiRelativeCalc,
    KosdaqRelativeCalc,
    )

models = [
    DefactoReg,
    KospiAgentData,
    KospiAgentCalcData,
    KosdaqAgentData,
    KosdaqAgentCalcData,
    KospiScoreData,
    KosdaqScoreData,
    RankData,
    KospiRelativeCalc,
    KosdaqRelativeCalc,
    ]

for model in models:
    admin.site.register(model)
