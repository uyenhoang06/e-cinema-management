from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from django.core import serializers

from ..serializers.UpdateProfileSerializer import UpdateProfileSerializer
from account.models import User


class UpdateProfileView(APIView):
    def put(self, request, id):
        user = User.objects.get(id = id)
        serializer = UpdateProfileSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Update profile': serializer.data})
        return Response(serializer.errors)