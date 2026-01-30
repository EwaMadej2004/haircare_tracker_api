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

    skret = serializers.ChoiceField(
        choices=HairProfile.CURL_TYPE,
        write_only=True
    )
    porowatosc = serializers.ChoiceField(
        choices=HairProfile.POROSITY,
        write_only=True
    )
    dlugosc = serializers.ChoiceField(
        choices=HairProfile.HAIR_LENGTH,
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'skret',
            'porowatosc',
            'dlugosc',
        ]

    def create(self, validated_data):
        skret = validated_data.pop('skret')
        porowatosc = validated_data.pop('porowatosc')
        dlugosc = validated_data.pop('dlugosc')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

        HairProfile.objects.create(
            user=user,
            skret=skret,
            porowatosc=porowatosc,
            dlugosc=dlugosc
        )

        return user

