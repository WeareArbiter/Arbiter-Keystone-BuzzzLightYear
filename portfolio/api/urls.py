from django.conf.urls import url

from portfolio.api.views import (
    PortfolioAPIView,
    PortfolioDetailAPIView,
    PortfolioItemAPIView,
    PortfolioItemDetailAPIView,
    PortfolioSpecsAPIView,
)

urlpatterns = [
    url(r'^portfolio/$', PortfolioAPIView.as_view(), name="portfolio"),
    url(r'^portfolio/(?P<pk>\d+)/$', PortfolioDetailAPIView.as_view(), name="portfolio-detail"),
    url(r'^item/$', PortfolioItemAPIView.as_view(), name="portfolio-item"),
    url(r'^item/(?P<pk>\d+)/$',PortfolioItemDetailAPIView.as_view(), name="portfolio-item-detail"),
    url(r'^specs/$', PortfolioSpecsAPIView.as_view(), name="portfolio-specs"),
    # url(r'^portfolio/(?P<pk>\d+)/optimization/$', PortfolioOptimizationAPIView.as_view(), name="portfolio-optimization"),
    # url(r'^portfolio-ratio/$', PortfolioRatioAPIView.as_view(), name="portfolio-ratio"),
    # url(r'^today-portfolio/$',TodayPortfolioAPIView.as_view(), name="today-portfolio"),
    # url(r'^today-portfolio/(?P<pk>\d+)$',TodayPortfolioDetailAPIView.as_view(), name="today-portfolio-detail"),
]
