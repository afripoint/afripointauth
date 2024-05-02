from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser

from .models import Profile
from .serializers import ProfileSerializer
from .renderers import ProfileJSONRenderer
from .pagination import ProfilePagination
from .serializers import ProfileSerializer, UpdateProfileSerializer

User = get_user_model()


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)
    pagination_class = ProfilePagination

    def get_queryset(self):
        queryset = Profile.objects.selected_related("user")
        return queryset

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile


class UpdateProfileView(generics.RetrieveAPIView):
    serializer_class = UpdateProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        profile = self.request.user.profile
        return profile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
