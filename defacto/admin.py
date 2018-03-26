from django.contrib import admin

# Register your models here.
from defacto.models import (
    DefactoTicker,
    DefactoReg,
    AgentData,
    AgentCalcData,
    ScoreData,
    RankData,
    )

models = [
    DefactoTicker,
    DefactoReg,
    AgentData,
    AgentCalcData,
    ScoreData,
    RankData
    ]

for model in models:
    admin.site.register(model)
