from rest_framework import serializers
from .models import Property, Photo, Address
from amenities.serializers import AmenitySerializer

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('prop', 'latitude', 'longitude', 'address_string')
        # fields = ('street', 'city', 'state', 'zip_code', 'country', 'latitude', 'longitude', 'address_string')

class PhotoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ('prop',)
        # fields = ('link',)

class PropertySerializer(serializers.ModelSerializer):

    amenities = AmenitySerializer(many=True)
    address = AddressSerializer()
    photos = PhotoSerializer(many=True)
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