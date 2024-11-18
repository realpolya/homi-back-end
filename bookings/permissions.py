from rest_framework.permissions import BasePermission

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