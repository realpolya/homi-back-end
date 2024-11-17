from users.serializers import UserSerializer
from rest_framework import serializers
from .models import Booking
from amenities.models import Amenity



class BookingSerializer(serializers.ModelSerializer):
    guest = UserSerializer(read_only=True)  

    class Meta:
        model = Booking
        fields = [
            'id', 
            'prop', 
            'guest', 
            'check_in_date', 
            'check_out_date', 
            'total_price', 
            'message', 
            'number_of_guests', 
            'credit_card'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        credit_card = str(representation.get('credit_card'))
        if len(credit_card) >= 4:
            representation['credit_card'] = f'**** **** **** {credit_card[-4:]}'
        return representation
