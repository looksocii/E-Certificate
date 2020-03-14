from django.urls import path
from . import views
from E_Certificate.settings import MEDIA_URL
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('uploadfile/extract/', views.upload, name="upload"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)