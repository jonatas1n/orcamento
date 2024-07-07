from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("", include("budget.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
