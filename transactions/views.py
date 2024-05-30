# views.py
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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


# class TransactionStatusList(APIView):
#     def get(self, request):
#         statuses = TransactionStatus.objects.all()
#         serializer = TransactionStatusSerializer(statuses, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = TransactionStatusSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TransactionStatusDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return TransactionStatus.objects.get(pk=pk)
#         except TransactionStatus.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         status = self.get_object(pk)
#         serializer = TransactionStatusSerializer(status)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         status = self.get_object(pk)
#         serializer = TransactionStatusSerializer(status, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         status = self.get_object(pk)
#         status.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionList(APIView):
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetail(APIView):
    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, pk):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transaction = self.get_object(pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionLogList(APIView):
    def get(self, request):
        logs = TransactionLog.objects.all()
        serializer = TransactionLogSerializer(logs, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = TransactionLogSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionLogDetail(APIView):
    def get_object(self, pk):
        try:
            return TransactionLog.objects.get(pk=pk)
        except TransactionLog.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        log = self.get_object(pk)
        serializer = TransactionLogSerializer(log)
        return Response(serializer.data)

    # def put(self, request, pk):
    #     log = self.get_object(pk)
    #     serializer = TransactionLogSerializer(log, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        log = self.get_object(pk)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionDetailsList(APIView):
    def get(self, request):
        details = TransactionDetails.objects.all()
        serializer = TransactionDetailsSerializer(details, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TransactionDetailsDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return TransactionDetails.objects.get(pk=pk)
#         except TransactionDetails.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         details = self.get_object(pk)
#         serializer = TransactionDetailsSerializer(details)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         details = self.get_object(pk)
#         serializer = TransactionDetailsSerializer(details, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         details = self.get_object(pk)
#         details.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
