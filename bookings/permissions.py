from rest_framework.permissions import BasePermission
from properties.models import Property

# is the user authorized to modify the booking?
class IsAuthorizedGuestHost(BasePermission):

    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:
            return False
        
        return obj.guest == request.user or obj.prop.user == request.user

class IsAuthorizedGuest(BasePermission):

    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:
            return False
        
        return obj.guest == request.user

class IsAuthorizedHost(BasePermission):

    def has_permission(self, request, view):

        print('inside isAuthorizedHost')
        prop_id = view.kwargs.get('prop_id')
        if not prop_id:
            return False

        try:
            prop_obj = Property.objects.get(id=prop_id)
        except Property.DoesNotExist:
            return False
        
        return prop_obj.user == request.user