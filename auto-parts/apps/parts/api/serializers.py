from rest_framework import serializers

from apps.parts.models import AutoPartsCategory, Brand, AutoParts
from apps.images.api.serializers import AutoPartsImagesSerializer
from apps.parts.utils import normalize_brand_name
from apps.users.api.serializers import SellerSerializer
from apps.review.api.serializers import AutoPartsReviewSerializer

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
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all()) 
    category = serializers.PrimaryKeyRelatedField(
        queryset=AutoPartsCategory.objects.all(), required=False
    )
    company_name = serializers.CharField(source="seller.company_name", read_only=True)
    image_url = serializers.SerializerMethodField()
    seller = SellerSerializer(read_only=True)
    # reviews = AutoPartsReviewSerializer(many=True, read_only=True, source="auto_parts_reviews")
    review_count = serializers.SerializerMethodField()
        
    class Meta:
        model = AutoParts
        read_only_fields = ["seller", "rating", "is_active"]
        fields = (
            "id",
            "category",
            "brand",
            "seller",
            # "reviews",
            "review_count",
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["category"] = AutoPartsCategorySerializer(instance.category).data
        representation["brand"] = BrandSerializer(instance.brand).data
        return representation

    def get_image_url(self, obj):
        if obj.images.exists():
            image_urls = []
            for image in obj.images.all():
                image_data = {"id": image.id, "image_url": image.image.url}
                image_urls.append(image_data)
            return image_urls
        return None

    def get_review_count(self, obj):
        return obj.auto_parts_reviews.count()
    
    
class AutoPartDetailSerializer(AutoPartSerializer):
    reviews = AutoPartsReviewSerializer(many=True, read_only=True, source="auto_parts_reviews")
    
    class Meta:
        model = AutoParts
        fields = AutoPartSerializer.Meta.fields + ("reviews",)