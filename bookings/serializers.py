from rest_framework import serializers
from .models import Booking
from properties.models import Property
from users.serializers import UserSerializer
from properties.serializers import PropertySerializer


class BookingSerializer(serializers.ModelSerializer):
    guest = UserSerializer(read_only=True)  
    prop = PropertySerializer(read_only=True)

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

    #Checker in backend side to be able to store CC with only showing last 4 
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        credit_card = str(representation.get('credit_card'))
        if len(credit_card) >= 4:
            representation['credit_card'] = f'**** **** **** {credit_card[-4:]}'
        return representation




