from rest_framework.permissions import BasePermission

# is the user authorized to modify the property listing?
class IsAuthorized(BasePermission):

    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:
            return False
        
        return obj.user == request.user