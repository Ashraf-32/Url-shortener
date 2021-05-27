from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UrlSerializer, UserSerializer
from shorturl.models import Url

import string, random

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins

# Url create view
class UrlAPIView(APIView):
    serializer_class = UrlSerializer

    def post(self, *args, **kwargs):
        link = self.request.data.get("url")
        if Url.objects.filter(url=link).exists():
            mod = Url.objects.get(url=link)
            serializer = UrlSerializer(mod)
            new_dict = serializer.data
            new_dict.pop("url_id")
            new_dict.pop("owner")
            new_dict['short'] = self.request.get_host() + '/l/' + new_dict['short']
            return Response(new_dict, status=201)
        short = get_short_code()
        serializer = UrlSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            if self.request.user.is_authenticated:
                serializer.save(owner=self.request.user)
                serializer.save(short=short)
            else:
                serializer.save(short=short)
            new_dict = serializer.data
            new_dict['short'] = self.request.get_host() + '/l/' + new_dict['short']
            new_dict.pop("owner")
            new_dict.pop("url_id")
            return Response(new_dict, status=201)
        return Response({"details": "Bad request"}, status=400)


# Register user view
class RegisterAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(self.request.data)
            token= Token.objects.create(user=user)
            return Response({"user": serializer.data, "token": token.key}, status=201)
        return Response({"details": "Bad request"}, status=400)

# Logout View
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, *args, **kwargs):
        token = Token.objects.get(user=self.request.user)
        if token:
            token.delete()
            return Response({"details": "Successfully logged out."}, status=200)
        return Response({"details": "You are not logged in."}, status=401)


# User profile
class ProfileAPIView(generics.ListAPIView, mixins.ListModelMixin):
    serializer_class = UrlSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Url.objects.filter(owner=self.request.user)
    
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        user_obj = {
            "username": request.user.username,
            "email": request.user.email
        }
        for r in res.data:
            r['short'] = self.request.get_host() + '/l/' + r['short']
            r.pop('owner')
            r.pop('url_id')
        res.data.insert(0, user_obj)
        return res


# Generates short code for url
def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        if Url.objects.filter(short=short_id).exists():
            continue
        else:
            return short_id