from django.shortcuts import render
from dojah.serializsers import (
    BVNSerializer,
    DriverLicenseSerializer,
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
        operation_summary="Use this endpoint to lookup  BVN",
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


class DriverLicenseView(APIView):
    @swagger_auto_schema(
        operation_summary="Use this endpoint to lookup drivers license",
        operation_description="""
        """,
        tags=["KYC"],
    )
    def get(self, request):
        serializer = DriverLicenseSerializer(data=request.query_params)
        if serializer.is_valid():
            driver_license = serializer.validated_data.get("driver_license")
            dojah = Dojah()
            response_data = dojah.driver_license_lookup(
                "/api/v1/kyc/dl", driver_license
            )
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
