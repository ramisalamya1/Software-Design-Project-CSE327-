from django.urls import path 
from . import views 
  
urlpatterns = [ 
         path('<int:hospital_id>/', views.book_appointment, name='book_appointment'),
] 