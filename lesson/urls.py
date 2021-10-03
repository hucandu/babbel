from django.urls import path

from .views import lesson_list, lesson_action

# API URLS
urlpatterns = [
    path("<str:id>/", view=lesson_action, name="lesson_action"),
    path("", view=lesson_list, name="lesson_list")

]
