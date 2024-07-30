from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

from .serializers import UserSerializer


class CustomUserAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: openapi.Response("Created", UserSerializer)},
        operation_summary="User serializer",
        operation_description="""
            
        """,
        tags=["Users"],
    )
    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.none()
