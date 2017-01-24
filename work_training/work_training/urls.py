from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^fifa/', include('fifa_league.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'__debug__/', include(debug_toolbar.urls)),
    ]
