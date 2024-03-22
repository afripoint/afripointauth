import datetime
import random
from direct7 import Client

from django.conf import settings
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from otpauth.models import OTPUpdate
from utils.utils import send_html_email
from .serializers import OTPVerifySerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

# from .serializers import OTPVerificationSerializer
from rest_framework.permissions import AllowAny

client = Client(api_token=settings.D7_NETWORK_SECRET_KEY)

User = get_user_model()


# class OTPVerificationView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = OTPVerifySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "OTP verified successfully!"}, status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    UserModel View.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["PATCH"])
    def verify_otp(self, request, pk=None):
        instance = self.get_object()
        if (
            not instance.is_active
            and instance.otp == request.data.get("otp")
            and instance.otp_expiry
            and timezone.now() < instance.otp_expiry
        ):
            instance.is_active = True
            instance.otp_expiry = None
            instance.max_otp_try = settings.MAX_OTP_TRY
            instance.otp_max_out = None
            instance.save()
            return Response(
                "Successfully verified the user.", status=status.HTTP_200_OK
            )

        return Response(
            "User active or Please enter the correct OTP.",
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["PATCH"])
    def regenerate_otp(self, request, pk=None):
        """
        Regenerate OTP for the given user and send it to the user.
        """
        instance = self.get_object()
        if int(instance.max_otp_try) == 0 and timezone.now() < instance.otp_max_out:
            return Response(
                "Max OTP try reached, try after an hour",
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        max_otp_try = int(instance.max_otp_try) - 1

        instance.otp = otp
        instance.otp_expiry = otp_expiry
        instance.max_otp_try = max_otp_try
        if max_otp_try == 0:
            # Set cool down time
            otp_max_out = timezone.now() + datetime.timedelta(hours=1)
            instance.otp_max_out = otp_max_out
        elif max_otp_try == -1:
            instance.max_otp_try = settings.MAX_OTP_TRY
        else:
            instance.otp_max_out = None
            instance.max_otp_try = max_otp_try
        instance.save()
        send_html_email("Your OTP", instance.phone_number, otp)
        return Response("Successfully generate new OTP.", status=status.HTTP_200_OK)


class OTPVerificationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = OTPVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print("request.data", request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            key = serializer.validated_data["otp_code"]

            # Find the OTPUpdate instance based on the phone number
            try:
                otp_update = OTPUpdate.objects.get(phone_number=phone_number)
                otp_id = otp_update.otp_id

                # Verify the OTP
                try:
                    client.verify.verify_otp(otp_id=otp_id, otp_code=key)
                    return Response(
                        {"message": "OTP verified successfully."},
                        status=status.HTTP_200_OK,
                    )
                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )
            except OTPUpdate.DoesNotExist:
                return Response(
                    {
                        "error": "OTPUpdate instance not found for the provided phone number."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
