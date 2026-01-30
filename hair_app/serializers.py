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

    def validate_imie(self, value):
        if not (value.isalpha() and value[0].isupper()):
            raise serializers.ValidationError(
                "Imię musi zawierać tylko litery i zaczynać się wielką literą."
            )
        return value

    def validate_nazwisko(self, value):
        if not (value.isalpha() and value[0].isupper()):
            raise serializers.ValidationError(
                "Nazwisko musi zawierać tylko litery i zaczynać się wielką literą."
            )
        return value

class HairProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairProduct
        fields = "__all__"

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Nazwa produktu musi mieć co najmniej 2 znaki."
            )
        return value

    def validate_brand(self, value):
        if value and not value.replace(" ", "").isalpha():
            raise serializers.ValidationError(
                "Marka może zawierać tylko litery i spacje."
            )
        return value


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
