from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields = ('googleId', 'profile_pic', 'bio','is_host','profits')
        read_only_fields = ('profits',)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer(required=False) #leaving this as false since the profile info isn't necessary to sign up


    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name','last_name', 'profile')


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # automatically create a profile for each user that signs up
        Profile.objects.create(user=user)
        return user
    

    def update(self, instance, validated_data):
        #this is all the properties that just belong to the profile model
        profile_data = validated_data.pop('profile', None)


        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name) 
              
        instance.save()


        #this is if we are requesting the profile data immediately at sign in. will retreive data, otherwise it'll create the profile model 
        if profile_data:
            profile, created = Profile.objects.get_or_create(user=instance)
            for key, value in profile_data.items():
                setattr(profile, key,value)
            profile.save()

        return instance

