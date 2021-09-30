from django.urls import path

from .views import register_user, user_management, login_user

# API URLS
urlpatterns = [
    path("register/", view=register_user, name="register"),
    path("login/", view=login_user, name="login"),
    path("<str:id>/", view=user_management, name="user_data"),
]
