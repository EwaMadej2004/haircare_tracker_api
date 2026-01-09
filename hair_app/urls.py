from django.urls import path
from .views import hairprofile_list

urlpatterns = [
    path("profiles/", hairprofile_list, name="hairprofile-list"),
]
