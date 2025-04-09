from django.urls import path
from .views import compare_hospitals_view

app_name = "hospital_comparison"

urlpatterns = [
    path('', compare_hospitals_view, name='compare'),
]


