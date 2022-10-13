from django.contrib.auth import views as auth_views
from django.urls import path, include
from parlour import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('login/profile/', views.profile, name='profile'),
    path('login/edit_profile/', views.edit_profile, name="edit_profile"),
    path('services/', views.services, name='services'),
    path('thankyou/<int:id>/', views.thankyou, name='thankyou'),
]