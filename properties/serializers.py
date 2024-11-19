from rest_framework import serializers
from .models import Property, Photo, Address
from amenities.models import Amenity

class AmenitySerializer(serializers.ModelSerializer):
    '''read-only version of amenity serializer'''
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'image']
        read_only_fields = ['id', 'name', 'image']


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

    amenities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Amenity.objects.all(),
    )
    amenities_nested = AmenitySerializer(source='amenities', many=True, read_only=True)
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