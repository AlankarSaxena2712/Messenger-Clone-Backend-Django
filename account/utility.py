from django.contrib import auth

from rest_framework.authtoken.models import Token


def create_token(number, password):
    user = auth.authenticate(username=number, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return token
