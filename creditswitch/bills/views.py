from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from creditswitch.bills.models import (
    CreditSwitchAirTimeService,
    CreditSwitchDataService,
    CreditSwitchEletricityService,
    CreditSwitchShowmaxService,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from creditswitch.bills.renderers import BillJSONRenderer
from utils.utils import CreditSwitch, airtime_checksum
from rest_framework.decorators import renderer_classes
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    CreditSwitchAirTimeServiceSerializer,
    CreditSwitchDataServiceSerializer,
    CreditSwitchEletricitySerializer,
    CreditSwitchShowmaxSerializer,
    ElectricityPurchaseSerializer,
    ElectricityValidateRequestSerializer,
    MultichoicePurchaseSerializer,
    MultichoiceValidateCustomerSerializer,
    PurchaseAirtimeSerializer,
    PurchaseDataSerializer,
    ServiceIdSerializer,
    ShowMaxPaySerializer,
)


class PurchaseAirtimeView(APIView):
    @swagger_auto_schema(
        request_body=PurchaseDataSerializer,
        responses={201: openapi.Response("Created", PurchaseDataSerializer)},
        operation_summary="Use this endpoint to handle airtime purchases",
        operation_description="""
        """,
    )
    def post(self, request):
        try:
            serializer = PurchaseAirtimeSerializer(data=request.data)
            if serializer.is_valid():
                service_id = serializer.validated_data["service_id"]
                amount = serializer.validated_data["amount"]
                recipient = serializer.validated_data["recipient"]

                credit_switch = CreditSwitch()
                response = credit_switch.purchase_airtime(service_id, amount, recipient)
                print("response", response)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@renderer_classes([BillJSONRenderer])
class DataPlansView(APIView):
    @swagger_auto_schema(
        request_body=ServiceIdSerializer,
        responses={201: openapi.Response("Created", ServiceIdSerializer)},
        operation_summary="Use this endpoint to get data plans",
        operation_description="""
        """,
    )
    def post(self, request):
        try:
            serializer = ServiceIdSerializer(data=request.data)
            if serializer.is_valid():
                service_id = serializer.validated_data["service_id"]
                credit_switch = CreditSwitch()
                response = credit_switch.data_plans(service_id)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class PurchaseDataView(APIView):
    @swagger_auto_schema(
        request_body=PurchaseDataSerializer,
        responses={201: openapi.Response("Created", PurchaseDataSerializer)},
        operation_summary="Use this endpoint to handle data bundle purchases",
        operation_description="""
        """,
    )
    def post(self, request):
        try:
            serializer = PurchaseDataSerializer(data=request.data)
            if serializer.is_valid():
                service_id = serializer.validated_data["service_id"]
                product_id = serializer.validated_data["product_id"]
                amount = serializer.validated_data["amount"]
                recipient = serializer.validated_data["recipient"]

                credit_switch = CreditSwitch()
                response = credit_switch.purchase_data(
                    service_id, amount, recipient, product_id
                )
                print("response", response)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@renderer_classes([BillJSONRenderer])
class MerchantDetailsView(APIView):
    @swagger_auto_schema(
        operation_summary="Use this endpoint to get Merchant details including merchant account balance on Creditswitch",
        operation_description="""
        """,
    )
    def post(self, request):
        try:
            credit_switch = CreditSwitch()
            response = credit_switch.merchant_details()
            if response["statusCode"] == "00":
                return Response(
                    {"message": "Success", "data": response}, status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Failed to retrieve merchant details"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@renderer_classes([BillJSONRenderer])
class TransactionStatusView(APIView):
    def get(self, request):
        try:
            serializer = ServiceIdSerializer(data=request.query_params)
            if serializer.is_valid():
                service_id = serializer.validated_data["service_id"]
                credit_switch = CreditSwitch()
                response = credit_switch.transaction_status(service_id)
                print("response", response)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@renderer_classes([BillJSONRenderer])
class ShowmaxView(APIView):
    def get(self, request):
        try:
            credit_switch = CreditSwitch()
            response = credit_switch.showmax()
            return Response(response, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@renderer_classes([BillJSONRenderer])
class StartimeView(APIView):
    @swagger_auto_schema(
        operation_summary="Use this endpoint to handle startime TV subscription",
        operation_description="""
        """,
    )
    def post(self, request):
        try:
            credit_switch = CreditSwitch()
            response = credit_switch.startimes()
            return Response(response, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@renderer_classes([BillJSONRenderer])
class ShowMaxPayView(APIView):
    @swagger_auto_schema(
        request_body=MultichoiceValidateCustomerSerializer,
        responses={
            201: openapi.Response("Created", MultichoiceValidateCustomerSerializer)
        },
        operation_summary="This is responsible for handling purchase of showmax packages",
        operation_description="""
            
        """,
    )
    def post(self, request):
        try:
            serializer = ShowMaxPaySerializer(data=request.data)
            if serializer.is_valid():
                service_id = serializer.validated_data["service_id"]
                amount = serializer.validated_data["amount"]
                subscriptionType = serializer.validated_data["subscriptionType"]
                customerNo = serializer.validated_data["customerNo"]
                invoicePeriod = serializer.validated_data["invoicePeriod"]
                packageName = serializer.validated_data["packageName"]

                credit_switch = CreditSwitch()
                response = credit_switch.showmax_recharge(
                    service_id,
                    amount,
                    subscriptionType,
                    customerNo,
                    invoicePeriod,
                    packageName,
                )
                print("response", response)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class CreditSwitchAirTimeServiceView(ListAPIView):
    queryset = CreditSwitchAirTimeService.objects.all()
    serializer_class = CreditSwitchAirTimeServiceSerializer


class CreditSwitchEletricityServiceView(ListAPIView):
    queryset = CreditSwitchEletricityService.objects.all()
    serializer_class = CreditSwitchEletricitySerializer


class CreditSwitchDataServiceView(ListAPIView):
    queryset = CreditSwitchDataService.objects.all()
    serializer_class = CreditSwitchDataServiceSerializer


class CreditSwitchShowmaxServiceView(ListAPIView):
    queryset = CreditSwitchShowmaxService.objects.all()
    serializer_class = CreditSwitchShowmaxSerializer


@renderer_classes([BillJSONRenderer])
class MultichoiceValidateCustomerView(APIView):
    @swagger_auto_schema(
        request_body=MultichoiceValidateCustomerSerializer,
        responses={
            201: openapi.Response("Created", MultichoiceValidateCustomerSerializer)
        },
        operation_summary="Use this endpoint to handle Multichoice customer validation",
        operation_description="""
        """,
    )
    def post(self, request):
        try:
            serializer = MultichoiceValidateCustomerSerializer(data=request.data)
            if serializer.is_valid():
                service_id = serializer.validated_data["service_id"]
                customer_no = serializer.validated_data["customer_no"]
                credit_switch = CreditSwitch()
                response = credit_switch.multichoice_validate_customer_number(
                    customer_no, service_id
                )
                print("response", response)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@renderer_classes([BillJSONRenderer])
class MultichoiceProductCodeView(APIView):
    @swagger_auto_schema(
        request_body=ServiceIdSerializer,
        responses={201: openapi.Response("Created", ServiceIdSerializer)},
        operation_summary="Use this endpoint to handle Multichoice product codes view",
        operation_description="""
        """,
    )
    def post(self, request):
        try:
            serializer = ServiceIdSerializer(data=request.data)
            if serializer.is_valid():
                service_id = serializer.validated_data["service_id"]
                credit_switch = CreditSwitch()
                response = credit_switch.multichoice_product_codes(service_id)
                print("response", response)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@renderer_classes([BillJSONRenderer])
class MultichoiceProductAddonsView(APIView):
    @swagger_auto_schema(
        request_body=ServiceIdSerializer,
        responses={201: openapi.Response("Created", ServiceIdSerializer)},
        operation_summary="Use this endpoint to handle Multichoice product addons",
        operation_description="""
        """,
    )
    def post(self, request):
        try:
            serializer = ServiceIdSerializer(data=request.data)
            if serializer.is_valid():
                service_id = serializer.validated_data["service_id"]
                credit_switch = CreditSwitch()
                response = credit_switch.multichoice_product_codes(service_id)
                print("response", response)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class MultichoicePurchaseView(APIView):
    @swagger_auto_schema(
        request_body=MultichoicePurchaseSerializer,
        responses={201: openapi.Response("Created", MultichoicePurchaseSerializer)},
        operation_summary="Use this endpoint to handle multichoice product purchases",
        operation_description="""
        """,
    )
    def post(self, request):
        try:
            serializer = MultichoicePurchaseSerializer(data=request.data)
            if serializer.is_valid():
                service_id = serializer.validated_data["service_id"]
                amount = serializer.validated_data["amount"]
                customer_name = serializer.validated_data["customer_name"]
                customer_no = serializer.validated_data["customer_no"]
                products_codes = serializer.validated_data["products_codes"]
                invoice_period = serializer.validated_data["invoice_period"]

                credit_switch = CreditSwitch()
                response = credit_switch.purchase_multichoice_product(
                    service_id,
                    amount,
                    customer_no,
                    customer_name,
                    products_codes,
                    invoice_period,
                )
                print("response", response)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@renderer_classes([BillJSONRenderer])
class ElectricityValidateRequestView(APIView):
    @swagger_auto_schema(
        request_body=ElectricityValidateRequestSerializer,
        responses={
            201: openapi.Response("Created", ElectricityValidateRequestSerializer)
        },
        operation_summary="Use this endpoint to handle validate electricity request ",
        operation_description="""
        """,
    )
    def post(self, request):
        try:
            serializer = ElectricityValidateRequestSerializer(data=request.data)
            if serializer.is_valid():
                service_id = serializer.validated_data["service_id"]
                customer_account_id = serializer.validated_data["customer_account_id"]

                credit_switch = CreditSwitch()
                response = credit_switch.electricity_validate_request(
                    service_id, customer_account_id
                )
                print("response", response)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@renderer_classes([BillJSONRenderer])
class ElectricityPurchaseView(APIView):
    @swagger_auto_schema(
        request_body=ElectricityPurchaseSerializer,
        responses={201: openapi.Response("Created", ElectricityPurchaseSerializer)},
        operation_summary="Use this endpoint to handle electricity purchase",
        operation_description="""
        """,
    )
    def post(self, request):
        try:
            serializer = ElectricityPurchaseSerializer(data=request.data)
            if serializer.is_valid():
                service_id = serializer.validated_data["service_id"]
                customer_account_id = serializer.validated_data["customer_account_id"]
                amount = serializer.validated_data["amount"]
                customer_name = serializer.validated_data["customer_name"]
                customer_address = serializer.validated_data["customer_address"]

                credit_switch = CreditSwitch()
                response = credit_switch.electricity_purchase(
                    service_id,
                    customer_account_id,
                    amount,
                    customer_name,
                    customer_address,
                )
                print("response", response)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
