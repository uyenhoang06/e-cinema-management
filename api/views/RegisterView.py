from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.RegisterSerializer import RegisterSerializer
from account.models import User


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        User.objects.create_user(
            serializer.validated_data['email'],
            serializer.validated_data['username'],
            serializer.validated_data['password'],
        )
        return Response({"Register successfully" : serializer.data})
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
