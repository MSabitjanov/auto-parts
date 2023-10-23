from rest_framework import serializers

from apps.images.models import AutoPartsImages, MasterImages


class MasterImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterImages
        fields = "__all__"


class AutoPartsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoPartsImages
        fields = "__all__"