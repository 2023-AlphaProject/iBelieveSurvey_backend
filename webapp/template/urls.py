from django.urls import path, include
from rest_framework import routers

from .views import TemplateViewSet

router = routers.DefaultRouter()
router.register(r'', TemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
