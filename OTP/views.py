from direct7 import Client

from django.conf import settings
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from OTP.models import MFATable, OTPSettings
from OTP.serializers import (
    EmailValidationSerializer,
    EmailVerificationSerializer,
    PhoneNumberValidationSerializer,
    PhoneNumberVerificationSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny


client = Client(api_token=settings.D7_NETWORK_SECRET_KEY)
from utils.utils import infobip_send_sms, send_html_email
from utils.utils import UniqueOtpGenerator

otp_generator = UniqueOtpGenerator()
User = get_user_model()


# Phone number validation OTP
class PhoneNumberValidationView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def send_otp(self, request):
        serializer = PhoneNumberValidationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            otp = otp_generator.generate_otp()

            otp_settings = OTPSettings.objects.first()
            otp_live_time = otp_settings.otp_live_time if otp_settings else 120

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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def send_email_otp(self, request):
        serializer = EmailValidationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp = otp_generator.generate_otp()

            otp_settings = OTPSettings.objects.first()
            otp_live_time = otp_settings.otp_live_time if otp_settings else 120

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
                "Your OTP", f"Your OTP is {otp}", settings.DEFAULT_FROM_EMAIL, [email]
            )
            return Response("OTP sent successfully.", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(viewsets.ViewSet):
    permission_classes = [AllowAny]

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
