from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render, kwargs={'template_name': 'index.html'}, name='start_page'),
    path('manager/', include('restaurateur.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('foodcartapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
