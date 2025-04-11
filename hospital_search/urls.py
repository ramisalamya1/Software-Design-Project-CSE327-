from django.contrib import admin 
from django.urls import path
from .views import hospital_search_view


urlpatterns = [
    path('', hospital_search_view, name='hospital_search'),
     path('admin/', admin.site.urls),
]