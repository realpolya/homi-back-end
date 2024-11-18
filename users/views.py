# from django.shortcuts import render 

# Create your views here.
from .models import Profile
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import ProfileSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username = response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data
        })

class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
  
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user: str = request.user

    #Need a try to populate the profile if available
    try: 
       profile = user.profile
    except Profile.DoesNotExist:
       profile = None

    refresh = RefreshToken.for_user(request.user)  
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data,
      'profile': ProfileSerializer(profile).data if profile else None
    })
  
class UserProfileView(generics.RetrieveUpdateAPIView):
   permission_classes = [permissions.IsAuthenticated]
   queryset = User.objects.all()
   serializer_class = UserSerializer

   def get(self,request,*args,**kwargs):
      user = request.user
 

      user_serializer = UserSerializer(user)

      try: 
         profile = user.profile
         profile_serializer = ProfileSerializer(profile)
      except Profile.DoesNotExist:
         profile_serializer = None

      return Response({
          'user': user_serializer.data,
          'profile': profile_serializer.data if profile else None  
        })
   
   def patch(self, request, *args, **kwargs):
      user = request.user
      data = request.data

      user_serializer = UserSerializer(user, data=data, partial=True)
      if user_serializer.is_valid():
          user_serializer.save()

          try:
              profile = user.profile
          except Profile.DoesNotExist:
              profile = None

          if profile: #This is again to confirm if profile exists already within the User. 
              profile_serializer = ProfileSerializer(profile, data=data, partial=True)
              if profile_serializer.is_valid():
                  profile_serializer.save()
              else:
                  return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          else:
              # If no profile exists, create a new one with the given data
              profile_serializer = ProfileSerializer(data=data, partial=True)
              if profile_serializer.is_valid():
                  profile_serializer.save(user=user)
              else:
                  return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

          return Response({
              'user': user_serializer.data,
              'profile': profile_serializer.data if profile else profile_serializer.data
          })
      else:
          return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)