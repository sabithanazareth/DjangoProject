
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/',  views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('get-all-users/', views.get_all_users),
    path('user/<str:email>/', views.get_user_by_email),
    path('user/update/<str:email>/', views.update_user),
    path('user/delete/<str:email>/', views.delete_user),
]