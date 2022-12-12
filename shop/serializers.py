from rest_framework import serializers
from .models import Product


class ImageSerializer(serializers.Serializer):
    path = serializers.SerializerMethodField()
    formats = serializers.SerializerMethodField()

    def get_path(self, obj):
        if obj:
            return obj.url.rsplit('.', 1)[0]
        return None

    def get_formats(self, obj):
        if obj:
            ext = obj.url.split('.')[-1]
            if ext in ['jpg', 'png']:
                return [ext, 'webp']
            return [ext]
        return None

    class Meta:
        model = Product


class ProductSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Product
        fields = '__all__'
