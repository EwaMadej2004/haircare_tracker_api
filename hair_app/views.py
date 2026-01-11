from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import HairProfile
from .serializers import HairProfileSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def hairprofile_list(request):
    if request.method == "GET":
        profiles = HairProfile.objects.filter(user=request.user)
        serializer = HairProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = HairProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def hairprofile_detail(request, pk):
    profile = get_object_or_404(
        HairProfile,
        pk=pk,
        user=request.user
    )

    if request.method == "GET":
        serializer = HairProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = HairProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)