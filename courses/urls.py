from django.urls import path

from .views import course_list, course_action

# API URLS
urlpatterns = [
    path("<str:id>/", view=course_action, name="language_action"),
    path("", view=course_list, name="course_list")

]
