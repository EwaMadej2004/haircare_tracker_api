from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from django.db import models
from rest_framework.permissions import AllowAny

from .models import HairProduct, HairProfile
from .serializers import HairProfileSerializer
from .serializers import HairProductSerializer

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def hairprofile_list(request):

    if request.method == "GET":
        if request.user.is_staff:
            profiles = HairProfile.objects.all()
        else:
            profiles = HairProfile.objects.filter(user=request.user)

        serializer = HairProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = HairProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def hairprofile_detail(request, pk):

    profile = get_object_or_404(HairProfile, pk=pk)

    
    if not request.user.is_staff and profile.user != request.user:
        return Response(
            {"detail": "Brak uprawnień"},
            status=status.HTTP_403_FORBIDDEN
        )

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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


from .models import HairRoutineEntry
from .serializers import HairRoutineEntrySerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_hair_routines(request):
    routines = HairRoutineEntry.objects.filter(user=request.user)
    serializer = HairRoutineEntrySerializer(routines, many=True)
    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recommended_products(request):
    try:
        profile = request.user.hair_profile
    except HairProfile.DoesNotExist:
        return Response(
            {"detail": "Brak profilu włosów"},
            status=status.HTTP_400_BAD_REQUEST
        )

    products = HairProduct.objects.filter(
        is_featured=True
    ).filter(
        models.Q(suitable_porosity=profile.porowatosc) |
        models.Q(suitable_porosity="")
    ).filter(
        models.Q(suitable_curl_type=profile.skret) |
        models.Q(suitable_curl_type="")
    )

    serializer = HairProductSerializer(products, many=True)
    return Response(serializer.data)

