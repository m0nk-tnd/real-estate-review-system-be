import jwt

from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken

from .serializers import RegisterSerializer
from .serializers import UserSerializer
from .models import TenantProfile, LandlordProfile


def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


class LoginJWT(ObtainJSONWebToken):
    user_serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = {}
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            user_id = jwt.decode(response.data['token'], settings.SECRET_KEY, algorithms=['HS256'])['user_id']
            tenant_profile = get_object_or_none(TenantProfile, user_id=user_id)
            landlord_profile = get_object_or_none(LandlordProfile, user_id=user_id)
            if tenant_profile:
                data.update({'profile_type': 'tenant'})
            if landlord_profile:
                data.update({'profile_type': 'landlord'})
            response.data.update(data)
        return response


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = serializer.save(request)
        return Response({
            "user_profile": UserSerializer(user_profile, context=self.get_serializer_context()).data, 
            "message": "User Created Successfully.",
        })
