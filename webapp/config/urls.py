from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

routers = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="IBelieveSurvey",
        default_version='v1',
        description="IBelieveSurvey API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls'), name='users'),
    path('templates/', include('template.urls'), name='templates'),
    path('surveys/', include('survey.urls'), name='surveys'),
]

urlpatterns += [
    re_path(r'^(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
