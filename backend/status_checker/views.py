import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Url


@login_required
def home(request):
    return render(request, 'home.html')


def load_urls(request):
    urls = Url.objects.filter(user=request.user).values()
    urls = [json.dumps(i) for i in urls]
    return JsonResponse({"urls": urls})


def check_status(request):
    urls = Url.objects.filter(user=request.user, check_status=True)
    for url in urls:
        try:
            request_url = str(url.url)
            res = requests.head(request_url)
            url.status_code = res.status_code
        except Exception as e:
            url.status_code = 404
        url.save()
    return JsonResponse({"success": 1})


@csrf_exempt
def change_status(request):
    url_id = json.loads(request.body)['id']
    status = json.loads(request.body)['check_status']
    url = Url.objects.filter(id=url_id)[0]
    url.check_status = status
    if status is False:
        url.status_code = None
    url.save()
    return JsonResponse({"success": 1})
