from rest_framework import serializers
from .models import HairProfile
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
