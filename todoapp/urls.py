from django.urls import path 
from . import views
urlpatterns = [
    path('create/',views.create),
    path('retreive/',views.retreive,name='retreive'),
    path('update/<int:id>/',views.update),
    path('delete/<int:id>/',views.delete),
    path('register/',views.register,name='register'),
    path('login/',views.loginn,name='login'),
    path('logout/',views.logoutt,name='logout'),
    path('search/',views.search,name='search'),
    path('api/login/', views.login_user, name='login_user'),

]
