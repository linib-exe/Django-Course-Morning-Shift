from django.urls import path 
from todoapp import views

urlpatterns = [
    path('get-todo',views.get_TODO,name='get-todo'),
    path('post-todo',views.save_TODO,name='post-todo')
]