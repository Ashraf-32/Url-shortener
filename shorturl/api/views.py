from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UrlSerializer
from shorturl.models import Url
import string, random

class UrlAPIView(APIView):
    serializer_class = UrlSerializer

    def post(self, *args, **kwargs):
        link = self.request.data.get("url")
        if Url.objects.filter(url=link).exists():
            mod = Url.objects.get(url=link)
            serializer = UrlSerializer(mod)
            new_dict = serializer.data
            new_dict['short'] = self.request.get_host() + '/l/' + new_dict['short']
            return Response(new_dict, status=201)
        short = get_short_code()
        # new = Url.objects.create(url=link, short=short)
        serializer = UrlSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(short=short)
            new_dict = serializer.data
            new_dict['short'] = self.request.get_host() + '/l/' + new_dict['short']
            return Response(new_dict, status=201)
        return Response({"details": "Bad request"}, status=400)

    
def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        if Url.objects.filter(short=short_id).exists():
            continue
        else:
            return short_id