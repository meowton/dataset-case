from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from DataMatcher import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", views.user_login),
    path("logout/", views.user_logout),
    path("login/submit", views.submit_login),
    path('', views.home),
    path('upload/', views.upload),
    path('compare/', views.compare),
    path('compare/results', views.submit_comparison)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
