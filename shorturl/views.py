from django.shortcuts import render, redirect
from .models import Url
import random
import string

# Create your views here.
def redirect_url(request, id):
    urls = Url.objects.filter(short=id).first()
    link = urls.url
    # for i in urls:
    #     link = i.url
    return redirect(link)

def index(request):
    if request.method == "POST":
        link = request.POST.get("link")
        short = ""
        if Url.objects.filter(url=link).exists():
            urls = Url.objects.all()
            for i in urls:
                if i.url == link:
                    short = i.short
                    break
        else:    
            short = get_short_code()
            if request.user.is_authenticated:
                owner = request.user
                url = Url(url=link, short=short, owner=owner)
                url.save()
            else:
                url = Url(url=link, short=short)
                url.save()
        new_url = request.get_host() + "/" + short
        return render(request, 'shorturl/index.html', {"new_url":new_url})

    return render(request, 'shorturl/index.html')

def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        if Url.objects.filter(short=short_id).exists():
            continue
        else:
            return short_id 