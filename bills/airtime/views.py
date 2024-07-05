from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from utils.utils import CreditSwitch, airtime_checksum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PurchaseAirtimeSerializer, PurchaseDataSerializer, ServiceIdSerializer



class PurchaseAirtimeView(APIView):
    def post(self, request):
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
    


class PurchaseDataView(APIView):
    def post(self, request):
        serializer = PurchaseDataSerializer(data=request.data)
        if serializer.is_valid():
            service_id = serializer.validated_data["service_id"]
            product_id = serializer.validated_data["product_id"]
            amount = serializer.validated_data["amount"]
            recipient = serializer.validated_data["recipient"]

            credit_switch = CreditSwitch()
            response = credit_switch.purchase_data(service_id, amount, recipient, product_id )
            print("response", response)
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class MerchantDetailsView(APIView):
    def post(self, request):
        credit_switch = CreditSwitch()
        response = credit_switch.merchant_details()
        if response["statusCode"] == "00":
            return Response( {"message": "Success", "data": response},  status=status.HTTP_200_OK)
        return Response({"message": "Failed to retrieve merchant details"}, status=status.HTTP_400_BAD_REQUEST)


class TransactionStatusView(APIView):
    def get(self, request):
        serializer = ServiceIdSerializer(data=request.query_params)
        if serializer.is_valid():
            service_id = serializer.validated_data["service_id"]
            credit_switch = CreditSwitch()
            response = credit_switch.transaction_status(service_id)
            print("response", response)
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DataPlansView(APIView):
    def post(self, request):
        serializer = ServiceIdSerializer(data=request.data)
        if serializer.is_valid():
            service_id = serializer.validated_data["service_id"]
            credit_switch = CreditSwitch()
            response = credit_switch.data_plans(service_id)
            print("response", response)
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ShowmaxView(APIView):
    def get(self, request):
        credit_switch = CreditSwitch()
        response = credit_switch.showmax()
        return Response(response, status=status.HTTP_200_OK)
    


class StartimeView(APIView):
    def post(self, request):
        credit_switch = CreditSwitch()
        response = credit_switch.startimes()
        return Response(response, status=status.HTTP_200_OK)
    
    






# @csrf_exempt
# def airtime_vend_request(request):
#     if request.method == "POST":
#         try:
#             data = {
#                 "login_id": 315474,
#                 "request_id": "hjhabxhjXBXHxvAVX",
#                 "service_id": "A04E",
#                 "request_amount": 100,
#                 "recipient": "08161177351",
#             }

#             # Extract the required fields from the request body
#             login_id = data.get("login_id")
#             request_id = data.get("request_id")
#             service_id = data.get("service_id")
#             request_amount = data.get("request_amount")
#             recipient = data.get("recipient")

#             if not all([request_id, service_id, request_amount, recipient]):
#                 return JsonResponse({"error": "Missing required fields"}, status=400)

#             # Generate checksum
#             checksum = airtime_checksum(
#                 login_id, request_id, service_id, request_amount, private_key, recipient
#             )

#             # Prepare the payload
#             payload = {
#                 "login_id": login_id,
#                 "request_id": request_id,
#                 "service_id": service_id,
#                 "request_amount": request_amount,
#                 "checksum": checksum,
#                 "recipient": recipient,
#             }

#             # Initialize CreditSwitch and make the POST request
#             cs = CreditSwitch()
#             response = cs.post("airtime/mvend", params=json.dumps(payload))

#             # Return the response from CreditSwitch
#             return JsonResponse(response.json(), status=response.status_code)

#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Invalid HTTP method"}, status=405)
