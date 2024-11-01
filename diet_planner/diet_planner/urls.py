from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path("", include("users_account.urls")),
    path("", include("home.urls")),
    path("dietitian/", include("dietitian.urls")),
    path("user/", include("public_user.urls")),
    path("administration/", include("admin_side.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
