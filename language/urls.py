from django.urls import path

from .views import language_list, language_action

# API URLS
urlpatterns = [
    path("<str:id>/", view=language_action, name="language_action"),
    path("", view=language_list, name="language_list")

]
