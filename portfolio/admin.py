from django.contrib import admin
# Register your models here.
from portfolio.models import (
    Portfolio,
    PortfolioItem
)

models = [
    Portfolio,
    PortfolioItem,
]

for model in models:
    admin.site.register(model)
