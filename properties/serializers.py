from rest_framework import serializers
from .models import Property, Photo, Address
from amenities.serializers import AmenitySerializer

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Property
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Photo
        fields = '__all__'