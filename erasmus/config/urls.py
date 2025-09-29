
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from communities.views import CityViewSet, UniversityViewSet, CommunityViewSet

router = DefaultRouter()
router.register(r'cities', CityViewSet)
router.register(r'universities', UniversityViewSet)
router.register(r'communities', CommunityViewSet)

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html")),   # <— nueva línea
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
