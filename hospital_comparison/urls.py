from django.urls import path
from . import views

app_name = "hospital_comparison"

urlpatterns = [
    path("", views.compare_hospitals_view, name="compare"),
]
