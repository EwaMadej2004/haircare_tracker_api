from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.urls import path
from .views import hairprofile_list, hairprofile_detail

urlpatterns = [
    path("profiles/", hairprofile_list, name="hairprofile-list"),
    path("profiles/<int:pk>/", hairprofile_detail, name="hairprofile-detail"),
]
