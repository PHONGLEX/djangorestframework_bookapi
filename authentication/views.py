import jsonpickle
import jwt

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import auth
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import *
from .utils import EmailHelper


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        site = get_current_site(request).domain
        token = RefreshToken.for_user(user)
        url = reverse('email-verify')
        link = "http://" + site + url + "?token=" + str(token)
        body = "Hi " + user.name + "\n Please use the link below to verify your account " + link
        data = {
            "subject": "Verify your account",
            "body": body,
            "to": user.email
        }
        EmailHelper.send_mail(data)
        return Response({"message": "We've sent you an email to verify your account"}, status=status.HTTP_201_CREATED)


class EmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    token_param = openapi.Parameter('token', openapi.IN_QUERY, description="token param", type=openapi.TYPE_STRING)


    @swagger_auto_schema(manual_parameters=[token_param])
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'message': "Successfully activate"})
        except jwt.exceptions.ExpiredSignatureError as e:
            return Response({"error": "Token is expired, please request a new one"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({"error": "Token is invalid, please request a new one"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email)

        if user.exists():
            user = user[0]
            uidb64 = urlsafe_base64_encode(force_bytes(jsonpickle.encode(user)))
            token = PasswordResetTokenGenerator().make_token(user)
            site = get_current_site(request).domain
            url = reverse("reset-password-confirm", kwargs={
                "uidb64": uidb64,
                "token": token
            })
            link = "http://" + site + url
            body = "Hi " + user.name + "\n Please use the link below to reset your password " + link
            data = {
                "subject": "Reset your password",
                "body": body,
                "to": user.email
            }
            EmailHelper.send_mail(data)

            return Response({"message": "We've sent you an email to reset your password"}, status=status.HTTP_200_OK)


class CheckPasswordResetTokenView(APIView):
    def post(self, request, uidb64, token):
        try:
            obj = smart_str(urlsafe_base64_decode(uidb64))
            user = jsonpickle.decode(obj)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Token is invalid, please request a new one"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"success": True, "uidb64": uidb64, "token": token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Token is invalid, please request a new one"}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = CheckPasswordResetTokenSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"message": "Changed password successfully"}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)