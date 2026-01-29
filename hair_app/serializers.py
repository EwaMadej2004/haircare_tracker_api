from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    HairProfile,
    HairProduct,
    HairRoutineEntry,
    HairTip,
)


class HairProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairProfile
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class HairProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairProduct
        fields = "__all__"


class HairRoutineEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = HairRoutineEntry
        fields = "__all__"


class HairTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairTip
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    
    hair_type = serializers.CharField()
    porosity = serializers.CharField()
    hair_length = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'hair_type',
            'porosity',
            'hair_length',
        ]

    def create(self, validated_data):
        hair_type = validated_data.pop('hair_type')
        porosity = validated_data.pop('porosity')
        hair_length = validated_data.pop('hair_length')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

        HairProfile.objects.create(
            user=user,
            hair_type=hair_type,
            porosity=porosity,
            hair_length=hair_length
        )

        return user
