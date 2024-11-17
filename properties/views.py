from rest_framework import generics, status
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer

class PropertiesList(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
