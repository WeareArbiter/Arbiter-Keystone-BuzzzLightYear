from django.contrib import admin
# Register your models here.
from portfolio.models import (
    Portfolio,
    PortfolioItem,
    PortfolioSpecs,
)

models = [
    Portfolio,
    PortfolioItem,
    PortfolioSpecs,
]

for model in models:
    admin.site.register(model)
