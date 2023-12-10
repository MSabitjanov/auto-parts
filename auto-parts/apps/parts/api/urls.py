from django.urls import path, include

from .views import AutoPartsCategoryListAPIView, BrandListAPIView, AutoPartViewSet, AutoPartByCategory, SellerAutoParts
from .routers import router

urlpatterns = [
    path("part-categories/", AutoPartsCategoryListAPIView.as_view()),
    path("part-brands/", BrandListAPIView.as_view()),
    path("", include(router.urls)),
    path("auto-part/category/<int:category_id>/", AutoPartByCategory.as_view()),
    path("sellers/<int:seller_id>/auto-parts/", SellerAutoParts.as_view(), name="seller-auto-parts"),
]
