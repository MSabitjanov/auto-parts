from django.urls import path, include

from .routers import router
from .views import SellerImagesCreateRetrieveUpdateDestroyAPIView


urlpatterns = [
    path("", include(router.urls)),
    path("seller-images/", SellerImagesCreateRetrieveUpdateDestroyAPIView.as_view(), name="seller-images"),
]