from django.urls import path 
from todoapp import views

urlpatterns = [
    path('get-todo',views.get_TODO,name='get-todo')
]