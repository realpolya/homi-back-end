from rest_framework import serializers
from .models import Property, Photo, Address
from amenities.serializers import AmenitySerializer

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('latitude', 'longitude')

class PhotoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Photo
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    first_photo = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('user',)
    
    def get_first_photo(self, obj):
        first_photo = obj.photos.first()
        if first_photo:
            return PhotoSerializer(first_photo).data
        return None