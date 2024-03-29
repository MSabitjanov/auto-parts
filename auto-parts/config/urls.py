"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import swagger_urls

urlpatterns = [
    path("api/auth/", include("apps.authentication.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("apps.users.api.urls")),
    path("api/", include("apps.review.api.urls")),
    path("api/", include("apps.parts.api.urls")),
    path("api/", include("apps.images.api.urls")),
    path("api/", include("apps.communication.api.urls")),
]

urlpatterns += swagger_urls.urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
