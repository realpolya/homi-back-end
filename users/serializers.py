from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields = ('googleId', 'profile_pic', 'bio','is_host','profits')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer(required=False) #leaving this as false since the profile info isn't necessary to sign up

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        #if we end up asking for additional info when creating user, this helps separate them in the model
        profile_data = validated_data.pop('profile',None)

        if profile_data: # If we make it a requirement for users to provide the additional info to begin with, it will create the data already within the sign up
            Profile.objects.create(user=user, **profile_data)

        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()

        if profile_data:
            profile, created = Profile.objects.get_or_create(user=instance)
            for key, value in profile_data.items():
                setattr(profile, key,value)
            profile.save()

        return instance

