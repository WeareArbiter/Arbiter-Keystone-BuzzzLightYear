from django.contrib import admin

# Register your models here.
from defacto.models import (
    DefactoReg,
    AgentData,
    AgentCalcData,
    ScoreData,
    RankData,
    RelativeCalc,
    )

models = [
    DefactoReg,
    AgentData,
    AgentCalcData,
    ScoreData,
    RankData,
    RelativeCalc
    ]

for model in models:
    admin.site.register(model)
