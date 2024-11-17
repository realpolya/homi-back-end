from rest_framework import generics, status
from rest_framework.response import Response
from .models import Amenity
from .serializers import AmenitySerializer

# retrieve all amenities, query by a set of ids, create an amenity
# to query by ids, do this: http://127.0.0.1:8000/amenities/?ids=1,2,3
# to query all, do this: http://127.0.0.1:8000/amenities/
class AmenitiesList(generics.ListCreateAPIView):
    serializer_class = AmenitySerializer

    def get_queryset(self):
        ids = self.request.query_params.get('ids')
        if ids:
            id_list = ids.split(",")
            return Amenity.objects.filter(id__in=id_list)
        return Amenity.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"error": "no amenities matched your search"},
                status=status.HTTP_404_NOT_FOUND
                )
        return super().get(request, *args, **kwargs)



__all__ = ["AmenitiesList"]
