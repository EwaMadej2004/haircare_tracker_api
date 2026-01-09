from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import HairProfile
from .serializers import HairProfileSerializer
@api_view(["GET"])
def hairprofile_list(request):
    profiles = HairProfile.objects.all()
    serializer = HairProfileSerializer(profiles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
