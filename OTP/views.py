from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from django.conf import settings
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from OTP.models import MFATable, OTPSettings
from OTP.renderers import PhoneNumberJSONRenderer
from OTP.serializers import (
    EmailValidationSerializer,
    EmailVerificationSerializer,
    PhoneNumberValidationSerializer,
    PhoneNumberVerificationSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from django.template.loader import render_to_string
from drf_yasg.utils import swagger_auto_schema


# client = Client(api_token=settings.D7_NETWORK_SECRET_KEY)
from utils.utils import infobip_send_sms, send_html_email
from utils.utils import UniqueOtpGenerator

otp_generator = UniqueOtpGenerator()
User = get_user_model()


# Phone number validation OTP
class PhoneNumberValidationView(viewsets.ViewSet):
    """
    Endpoint for sending OTP to phone number.
    """

    permission_classes = [AllowAny]
    renderer_classes = [PhoneNumberJSONRenderer]

    @swagger_auto_schema(request_body=PhoneNumberValidationSerializer)
    @action(detail=False, methods=["post"])
    def send_otp(self, request):
        serializer = PhoneNumberValidationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            user = User.objects.filter(phone_number=phone_number).first()
            if user:
                return Response(
                    {"error": "There is an existing account with this phone number. "},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            otp = otp_generator.generate_otp()

            otp_settings = OTPSettings.objects.first()
            otp_live_time = otp_settings.otp_live_time if otp_settings else 300

            mfa = MFATable.objects.create(
                userId=phone_number,
                mfa_code=otp,
                mfa_category="registration",
                mfa_duration=otp_live_time,
            )
            # Calculate the OTP expiry time based on the current time and otp_live_time
            otp_expiring_time = timezone.now() + timezone.timedelta(
                seconds=otp_live_time
            )
            mfa.otp_expiry = otp_expiring_time
            mfa.save()

            infobip_send_sms(phone_number, f"Your OTP is {otp}")
            return Response("OTP sent successfully.", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneNumberVerificationView(viewsets.ViewSet):
    """
    Endpoint to verify phone number OTP.
    """

    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    @swagger_auto_schema(request_body=PhoneNumberVerificationSerializer)
    @action(detail=False, methods=["post"])
    def verifyOtp(self, request):
        serializer = PhoneNumberVerificationSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data["otp"]
            phone_number = serializer.validated_data["phone_number"]

            mfa = (
                MFATable.objects.filter(userId=phone_number)
                .order_by("-date_generated")
                .first()
            )
            if otp != mfa.mfa_code:
                return Response("Invalid OTP", status=status.HTTP_400_BAD_REQUEST)

            if timezone.now() > mfa.otp_expiry:
                mfa.expired = True
                mfa.save()
                return Response("OTP has expired.", status=status.HTTP_400_BAD_REQUEST)

            if mfa.verified == True:
                return Response(
                    "OTP already verified.", status=status.HTTP_400_BAD_REQUEST
                )

            mfa.verified = True
            mfa.save()

            return Response("OTP successfully verified.", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Email validation OTP
class EmailValidationView(viewsets.ViewSet):
    """
    Email OTP generation endpoint.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=EmailValidationSerializer)
    @action(detail=False, methods=["post"])
    def send_email_otp(self, request):
        serializer = EmailValidationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                return Response(
                    {"error": "There is an existing account with this email "},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            otp = otp_generator.generate_otp()

            otp_settings = OTPSettings.objects.first()
            otp_live_time = otp_settings.otp_live_time if otp_settings else 300

            mfa = MFATable.objects.create(
                userId=email,
                mfa_code=otp,
                mfa_category="registration",
                mfa_duration=otp_live_time,
            )
            # Calculate the OTP expiry time based on the current time and otp_live_time
            otp_expiring_time = timezone.now() + timezone.timedelta(
                seconds=otp_live_time
            )
            mfa.otp_expiry = otp_expiring_time
            mfa.save()

            send_html_email(
                "Your OTP",
                render_to_string("emails/otp.html", {"otp": otp}),
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )

            return Response("OTP sent successfully.", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(viewsets.ViewSet):
    """
    Email OTP verification endpoint.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=EmailVerificationSerializer)
    @action(detail=False, methods=["post"])
    def verify_email_otp(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data["otp"]
            email = serializer.validated_data["email"]

            mfa = (
                MFATable.objects.filter(userId=email)
                .order_by("-date_generated")
                .first()
            )
            if otp != mfa.mfa_code:
                return Response("Invalid OTP", status=status.HTTP_400_BAD_REQUEST)

            if timezone.now() > mfa.otp_expiry:
                mfa.expired = True
                mfa.save()
                return Response("OTP has expired.", status=status.HTTP_400_BAD_REQUEST)

            if mfa.verified == True:
                return Response(
                    "OTP already verified.", status=status.HTTP_400_BAD_REQUEST
                )

            mfa.verified = True
            mfa.save()

            return Response("OTP successfully verified.", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
