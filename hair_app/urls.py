from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.urls import path
from .views import (
    hairprofile_list,
    hairprofile_detail,
    hairproduct_list,
    hairproduct_detail,
)
from .views import RegisterView
from .views import my_hair_routines
from .views import recommended_products




urlpatterns = [
    
    path("profiles/", hairprofile_list, name="hairprofile-list"),
    path("profiles/<int:pk>/", hairprofile_detail, name="hairprofile-detail"),

    
    path("products/", hairproduct_list, name="hairproduct-list"),
    path("products/<int:pk>/", hairproduct_detail, name="hairproduct-detail"),
    path('register/', RegisterView.as_view(), name='register'),
    path("my-routines/", my_hair_routines, name="my-hair-routines"),
    path("recommended-products/", recommended_products, name="recommended-products"),
]

