from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import AppUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if AppUser.objects.filter(username=username).exists():
            return Response({"error": "Username taken"}, status=409)

        if AppUser.objects.filter(email=email).exists():
            return Response({"error": "Email in use"}, status=409)

        user = AppUser(username=username, email=email)
        user.set_password(password)
        user.save()

        return Response({"message": "User registered successfully"}, status=201)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = AppUser.objects.get(username=username)
        except AppUser.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=401)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        refresh["username"] = user.username
        refresh["role"] = user.role
        refresh["email"] = user.email

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })

class MeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payload = request.auth.payload  # <- to jest token JWT

        return Response({
            "username": payload.get("username"),
            "email": payload.get("email"),
            "role": payload.get("role"),
        })
