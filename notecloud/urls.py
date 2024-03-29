from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from utils.bots import BotView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/notes/', include('notes.urls', namespace='notes')),
    path('api/forums/', include('forums.urls', namespace='forums')),
    path('api/bots/daily/', BotView.as_view(), name='daily_bot'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.LOCAL_SERVER:
    urlpatterns += [
        path(
            'restapi/',
            include('rest_framework.urls', namespace='rest_framework')
        )
    ]

    if 'drf_yasg' in settings.INSTALLED_APPS:
        from rest_framework import permissions
        from drf_yasg.views import get_schema_view
        from drf_yasg import openapi

        schema_view = get_schema_view(
            openapi.Info(
                title="notecloud APIs",
                default_version='beta',
            ),
            public=True,
            permission_classes=[permissions.AllowAny],
        )
        urlpatterns += [
            re_path(
                r'^swagger(?P<format>\.json|\.yaml)$',
                schema_view.without_ui(cache_timeout=0),
                name='schema-json'
            ),
            re_path(
                r'^swagger/$',
                schema_view.with_ui('swagger', cache_timeout=0),
                name='schema-swagger-ui'
            ),
            re_path(
                r'^redoc/$',
                schema_view.with_ui('redoc', cache_timeout=0),
                name='schema-redoc'
            ),
        ]
