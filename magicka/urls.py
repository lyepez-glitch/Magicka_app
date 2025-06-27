from django.urls import path
from . import views
from .views import RegisterUserView, LoginUserView, UpdateProfileView, LaunchAttackView, GetPowers,GetProfile,GetAttacks,AttackUser,GetAllUsersView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('users/<int:id>/', UpdateProfileView.as_view(), name='update-profile'),
    path('launchattack/', LaunchAttackView.as_view(), name='launch-attack'),
    path('powers/', GetPowers.as_view(), name='get-powers'),
    path('attacks/', GetAttacks.as_view(), name='get-attacks'),
    path('attackUser/', AttackUser.as_view(), name='attack_user'),
    # path('users/<int:id>/', GetProfile.as_view(), name='get_profile'),
    path('users/', GetAllUsersView.as_view(), name='get_users'),
]
