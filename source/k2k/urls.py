"""k2k URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import include, url
from k2k.views import  site,administration, subcategory_view, order_view
from django.conf.urls.static import static
from k2k import settings

urlpatterns = [
    url(r'^administration/', include(administration.urls)),
    url(r'^administration/subcategory', include(subcategory_view.urls)),
    url(r'^administration/order', include(order_view.urls)),
    url(r'^', include(site.urls)), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)