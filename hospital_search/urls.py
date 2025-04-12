from django.contrib import admin 
from django.urls import path
from .views import hospital_search_view

app_name = 'hospital_search'


urlpatterns = [
    path('', hospital_search_view, name='hospital_search'),
     path('admin/', admin.site.urls),
]
