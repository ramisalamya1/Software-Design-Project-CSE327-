from django.urls import path 
from . import views 

app_name = 'booking'
  
urlpatterns = [ 
         path('<int:hospital_id>/', views.book_appointment, name='book_appointment'),
] 