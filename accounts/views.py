from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from accounts.models import AccountTypeTable
from accounts.renderers import AccountTypeJSONRenderer
from accounts.serializers import AccountTypeSerializer


class AccountTypeViewSet(ModelViewSet):
    queryset = AccountTypeTable.objects.all()
    serializer_class = AccountTypeSerializer
    renderer_classes = (AccountTypeJSONRenderer,)
    # parser_classes = (MultiPartParser,)
