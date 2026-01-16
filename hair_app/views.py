from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import HairProfile
from .serializers import HairProfileSerializer

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def hairprofile_list(request):
    if request.method == "GET":
        profiles = HairProfile.objects.all()
        serializer = HairProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = HairProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def hairprofile_detail(request, pk):
    try:
        profile = HairProfile.objects.get(pk=pk)
    except HairProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = HairProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = HairProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def hairproduct_list(request):
    if request.method == "GET":
        products = HairProduct.objects.all()
        serializer = HairProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = HairProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def hairproduct_detail(request, pk):
    try:
        product = HairProduct.objects.get(pk=pk)
    except HairProduct.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = HairProductSerializer(product)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = HairProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
