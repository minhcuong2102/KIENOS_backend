from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class AuthToken(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
