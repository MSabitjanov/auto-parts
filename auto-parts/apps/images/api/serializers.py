from rest_framework import serializers

from apps.images.models import AutoPartsImages, MasterImages, SellerImage


class MasterImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterImages
        fields = "__all__"
        read_only_fields = ["master"]


class AutoPartsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoPartsImages
        fields = "__all__"


class SellerImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerImage
        fields = "__all__"