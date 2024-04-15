from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


from accounts.models import AccountTypeTable
from accounts.renderers import AccountTypeJSONRenderer
from accounts.serializers import AccountTypeSerializer


# class AccountTypeViewSet(ModelViewSet):
#     queryset = AccountTypeTable.objects.all()
#     serializer_class = AccountTypeSerializer
#     renderer_classes = (AccountTypeJSONRenderer,)
#     # parser_classes = (MultiPartParser,)


class AccountTypeViewSet(APIView):
    def get(self, request):
        items = AccountTypeTable.objects.filter(active=True)
        serializer = AccountTypeSerializer(items, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AccountTypeSerializer)
    def post(self, request):
        serializer = AccountTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountTypeDetail(APIView):
    def get_object(self, pk):
        try:
            AccountTypeTable.objects.get(pk=pk)
        except AccountTypeTable.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"error": "Account type does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = AccountTypeSerializer(item)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AccountTypeSerializer)
    def put(self, request, pk):
        item = self.get_object(pk)

        if not item:
            return Response(
                {"error": "Account type not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AccountTypeSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"errors": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
