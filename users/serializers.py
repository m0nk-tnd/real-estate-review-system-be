from rest_framework import serializers

from .models import TenantProfile, LandlordProfile
from django.contrib.auth.models import User


class TenantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantProfile
        fields = ['user', 'firstname', 'lastname', 'middlename', 'birth_date']


class LandlordProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordProfile
        fields = ['user', 'firstname', 'lastname', 'middlename', 'birth_date']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    firstname = serializers.CharField(max_length=30)
    lastname = serializers.CharField(max_length=30)
    middlename = serializers.CharField(max_length=30, allow_blank=True, allow_null=True)
    birth_date = serializers.DateField()

    password = serializers.CharField(max_length=30)
    password2 = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=40)

    is_tenant = serializers.BooleanField(default=False)
    is_landlord = serializers.BooleanField(default=False)

    def save(self, validated_data):
        user = User.objects.create_user(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        
        is_tenant = self.validated_data['is_tenant']
        is_landlord = self.validated_data['is_landlord']

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match'})
    
        user.set_password(password)
        user.save()
        if is_tenant:
            user_profile = TenantProfile(
                user=user,
                firstname=self.validated_data['firstname'],
                lastname=self.validated_data['lastname'],
                middlename=self.validated_data['middlename'],
                birth_date=self.validated_data['birth_date'],
            )
        elif is_landlord:
            user_profile = LandlordProfile(
                user=user,
                firstname=self.validated_data['firstname'],
                lastname=self.validated_data['lastname'],
                middlename=self.validated_data['middlename'],
                birth_date=self.validated_data['birth_date'],
            )
        return user_profile


class UserSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=30)
    firstname = serializers.CharField(max_length=30)
    lastname = serializers.CharField(max_length=30)
    middlename = serializers.CharField(max_length=30, allow_blank=True, allow_null=True)
    birth_date = serializers.DateField()
