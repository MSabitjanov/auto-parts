from rest_framework import serializers

from apps.parts.models import AutoPartsCategory, Brand, AutoParts
from apps.images.api.serializers import AutoPartsImagesSerializer


class RecursivePartCategorySerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

    class Meta:
        ref_name = "RecursivePartSerializer"


class FilterCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class AutoPartsCategorySerializer(serializers.ModelSerializer):
    children = RecursivePartCategorySerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = AutoPartsCategory
        fields = "id", "name", "children"


class AutoPartListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoPartsCategory
        fields = "id", "name", "parent"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class AutoPartSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = AutoPartsCategorySerializer(read_only=True)
    company_name = serializers.CharField(source="seller.company_name", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AutoParts
        read_only_fields = ["seller", "rating", "is_active"]
        fields = (
            "id",
            "category",
            "brand",
            "seller",
            "company_name",
            "name",
            "description",
            "characteristics",
            "is_new",
            "price",
            "date_of_pubication",
            "last_updated",
            "rating",
            "image_url",
        )
        extra_kwargs = {"is_new": {"required": True}}
        # extra_kwargs = {"brand": {"required": True}, "category": {"required": True}}

    def get_image_url(self, obj):
        if obj.images.exists():
            return obj.images.first().image.url
        return None
