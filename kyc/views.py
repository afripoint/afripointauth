from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from kyc.models import KYCModel
from kyc.serializers import KYCSerializer


# Create your views here.
class KYCAPIView(APIView):
    def get_object(self, user_id):
        try:
            return KYCModel.objects.get(user__id=user_id)
        except KYCModel.DoesNotExist:
            return None

    def get(self, request, user_id):
        item = self.get_object(user_id)
        if not item:
            return Response(
                {"errors": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = KYCSerializer(item)
        print("DATA", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=KYCSerializer)
    def put(self, request, user_id):
        item = self.get_object(user_id)
        if not item:
            return Response(
                {"errors": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = KYCSerializer(
            item, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
