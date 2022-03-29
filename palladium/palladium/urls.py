'''This includes all urls of all the application'''
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('',TemplateView.as_view(template_name="home/index.html"),name='home'),
    path('accounts/logout/',TemplateView.as_view(template_name='logout.html'),name='logout'),
    path('rent/', include('rentezzy.urls')),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
