from rest_framework import serializers

from apps.parts.models import AutoPartsCategory, Brand, AutoParts


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class AutoPartsCategorySerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = AutoPartsCategory
        fields = "id", "name", "children"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class AutoPartSerializer(serializers.ModelSerializer):
    seller = serializers.CharField(source="seller.company_name", read_only=True)

    class Meta:
        model = AutoParts
        read_only_fields = ["seller", "rating", "is_active"]
        fields = "id", "seller", "is_new", "price", "date_of_pubication", "rating"
        extra_kwargs = {"is_new": {"required": True}}
        # extra_kwargs = {"brand": {"required": True}, "category": {"required": True}}
