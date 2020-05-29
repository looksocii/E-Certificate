from django.urls import path
from . import views
from ProjectBase.settings import MEDIA_URL
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
     path('singup/', views.my_register, name='singup'),
    path('upload/', views.upload, name="upload"),
    path('issue/', views.issue, name="issue"),
    path('issuing/', views.issuing, name="issuing"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)