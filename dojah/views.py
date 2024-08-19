from django.shortcuts import render
from dojah.serializsers import (
    BVNSerializer,
    NINSerializer,
    PhoneNumberSerializer,
    VitualNINSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.utils import Dojah
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from creditswitch.bills.renderers import BillJSONRenderer


class KYCPhoneNumberView(APIView):
    @swagger_auto_schema(
        operation_summary="Use this endpoint to validate phone number",
        operation_description="""
        """,
        tags=["KYC"],
    )
    def get(self, request):
        serializer = PhoneNumberSerializer(data=request.query_params)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get("phone_number")
            dojah = Dojah()
            response_data = dojah.phone_verification(
                "/api/v1/kyc/phone_number/basic", phone_number
            )
            return Response(
                response_data, status=status.HTTP_200_OK
            )  # Directly return the dict
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NINLookupView(APIView):
    @swagger_auto_schema(
        operation_summary="Use this endpoint to lookup NIN",
        operation_description="""
        """,
        tags=["KYC"],
    )
    def get(self, request):
        serializer = NINSerializer(data=request.query_params)
        if serializer.is_valid():
            nin = serializer.validated_data.get("nin")
            dojah = Dojah()
            response_data = dojah.lookup_nin("/api/v1/kyc/nin", nin)
            return Response(
                response_data, status=status.HTTP_200_OK
            )  # Directly return the dict
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VirtualNINLookupView(APIView):
    @swagger_auto_schema(
        operation_summary="Use this endpoint to lookup virtual NIN",
        operation_description="""
        """,
        tags=["KYC"],
    )
    def get(self, request):
        serializer = VitualNINSerializer(data=request.query_params)
        if serializer.is_valid():
            vnin = serializer.validated_data.get("vnin")
            dojah = Dojah()
            response_data = dojah.lookup_vnin("/api/v1/kyc/vnin", vnin)
            return Response(
                response_data, status=status.HTTP_200_OK
            )  # Directly return the dict
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BVNLookupView(APIView):
    @swagger_auto_schema(
        operation_summary="Use this endpoint to lookup virtual BVN",
        operation_description="""
        """,
        tags=["KYC"],
    )
    def get(self, request):
        serializer = BVNSerializer(data=request.query_params)
        if serializer.is_valid():
            bvn = serializer.validated_data.get("bvn")
            dojah = Dojah()
            response_data = dojah.lookup_bvn("/api/v1/kyc/bvn/full", bvn)
            return Response(
                response_data, status=status.HTTP_200_OK
            )  # Directly return the dict
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import json

# class PhoneNumberVerificationView(APIView):
#     def post(self, request):
#         try:
#             phone_number = request.query_params.get("phone_number")

#             if not phone_number:
#                 return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

#             dojah = Dojah()
#             response = dojah.phone_verification(phone_number, method='post')

#             return Response(response, status=status.HTTP_200_OK)
#         except json.JSONDecodeError:
#             return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Create your views here.
