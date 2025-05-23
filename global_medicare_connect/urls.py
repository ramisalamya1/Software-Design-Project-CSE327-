"""
URL configuration for global_medicare_connect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from booking.views import *
from medical_records import views
from hospital_search.views import *
from django.urls import path, include
from django.conf.urls.static import static 



urlpatterns = [
    path('search/', include('hospital_search.urls')),
    path('booking/', include('booking.urls')),
    path('package/', include('package_customization.urls', namespace='package_customization')),  
    path('admin_management/', include('admin_management.urls')),
    path('admin/', admin.site.urls),
    path('medical/', include('medical_records.urls')),
    path('', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'), 
    path('hospital_comparison/', include('hospital_comparison.urls')), 
    path('reviews/', include('reviews_ratings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
