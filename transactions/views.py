# views.py
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import (
    TransactionLog,
    TransactionDetails,
    Transaction,
)
from .serializers import (
    TransactionSerializer,
    TransactionLogSerializer,
    TransactionDetailsSerializer,
)


class TransactionList(APIView):
    @swagger_auto_schema(
        operation_summary="Use this endpoint to get trasaction list",
        operation_description="""
        """,
        tags=["Transactions"],
    )
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TransactionSerializer, tags=["Transactions"])
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetail(APIView):
    @swagger_auto_schema(
        operation_summary="Use this endpoint to get trasaction detail",
        operation_description="""
        """,
    )
    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    @swagger_auto_schema(tags=["Transactions"])
    def get(self, request, pk):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TransactionSerializer, tags=["Transactions"])
    def put(self, request, pk):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TransactionSerializer, tags=["Transactions"])
    def delete(self, request, pk):
        transaction = self.get_object(pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionLogList(APIView):
    @swagger_auto_schema(
        operation_summary="Use this endpoint to get trasaction log list",
        operation_description="""
        """,
    )
    def get(self, request):
        logs = TransactionLog.objects.all()
        serializer = TransactionLogSerializer(logs, many=True)
        return Response(serializer.data)


class TransactionLogDetail(APIView):
    @swagger_auto_schema(
        operation_summary="Use this endpoint to get trasaction log detail",
        operation_description="""
        """,
    )
    def get_object(self, pk):
        try:
            return TransactionLog.objects.get(pk=pk)
        except TransactionLog.DoesNotExist:
            raise Http404

    @swagger_auto_schema(tags=["Transactions"])
    def get(self, request, pk):
        log = self.get_object(pk)
        serializer = TransactionLogSerializer(log)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TransactionLogSerializer, tags=["Transactions"])
    def delete(self, request, pk):
        log = self.get_object(pk)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionDetailsList(APIView):
    @swagger_auto_schema(tags=["Transactions"])
    def get(self, request):
        details = TransactionDetails.objects.all()
        serializer = TransactionDetailsSerializer(details, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=TransactionDetailsSerializer, tags=["Transactions"]
    )
    def post(self, request):
        serializer = TransactionDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
