from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('hair_app.urls')),
    path("api-auth/", include("rest_framework.urls")),
    path('api/token/', obtain_auth_token),   
]

