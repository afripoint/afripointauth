from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from drf_yasg import openapi


from customaccounts.models import AccountActivity, AccountTable, AccountTypeTable
from customaccounts.renderers import (
    AccountTableJSONRenderer,
    AccountTypeJSONRenderer,
)
from customaccounts.serializers import (
    AccountActivitySerializer,
    AccountTableSerialzer,
    AccountTypeSerializer,
)


class AccountTypeViewSet(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [AccountTypeJSONRenderer]

    @swagger_auto_schema(
        operation_summary="This endpoint is for account type",
        operation_description="""
            
        """,
        tags=["Accounts"],
    )
    def get(self, request):
        items = AccountTypeTable.objects.filter(active=True)
        serializer = AccountTypeSerializer(
            items, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AccountTypeSerializer, tags=["Accounts"])
    def post(self, request):
        serializer = AccountTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountTypeDetail(APIView):
    @swagger_auto_schema(
        operation_summary="This endpoint is for account detail",
        operation_description="""
            
        """,
        tags=["Accounts"],
    )
    def get_object(self, pk):
        try:
            AccountTypeTable.objects.get(pk=pk)
        except AccountTypeTable.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="This endpoint is for account detail",
        operation_description="""
            
        """,
        tags=["Accounts"],
    )
    def get(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"error": "Account type does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = AccountTypeSerializer(item, context={"request": request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AccountTypeSerializer, tags=["Accounts"])
    def put(self, request, pk):
        item = self.get_object(pk)

        if not item:
            return Response(
                {"error": "Account type not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AccountTypeSerializer(
            item, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["Accounts"])
    def delete(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"errors": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountView(APIView):
    renderer_classes = [AccountTableJSONRenderer]
    permission_class = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AccountTableSerialzer,
        responses={201: openapi.Response("Created", AccountTableSerialzer)},
        operation_summary="This endpoint is for accounts view",
        operation_description="""
            
        """,
        tags=["Accounts"],
    )
    def post(self, request):
        serializer = AccountTableSerialzer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["Accounts"])
    def get(self, request):
        items = AccountTable.objects.filter(active=True)
        serializer = AccountTableSerialzer(
            items, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountDetail(APIView):
    @swagger_auto_schema(
        request_body=AccountTableSerialzer,
        responses={201: openapi.Response("Created", AccountTableSerialzer)},
        operation_summary="This endpoint is for accounts update",
        operation_description="""
            
        """,
        tags=["Accounts"],
    )
    def update(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"errors": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = AccountTableSerialzer(
            item, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            AccountTable.objects.get(pk=pk)
        except AccountTable.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["Accounts"])
    def get(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"errors": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AccountTableSerialzer(item, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Accounts"])
    def delete(self, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"errors": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountActivityView(ListAPIView):
    queryset = AccountActivity.objects.all()
    serializer_class = AccountActivitySerializer

    @swagger_auto_schema(tags=["Accounts"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
