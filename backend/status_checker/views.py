import json
import asyncio
import aiohttp
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


async def check_url(url, session):
    try:
        request_url = str(url.url)
        async with session.head(request_url, allow_redirects=True) as response:
            status = response.status
            url.status_code = status
    except Exception as e:
        url.status_code = 404
    finally:
        url.save()


async def lookup_urls(urls):
    tasks = list()

    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(check_url(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


def check_status(request):
    urls = Url.objects.filter(user=request.user, check_status=True)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(lookup_urls(urls))
    loop.close()
    return JsonResponse({"success": 1})


@csrf_exempt
def change_status(request):
    request_body = json.loads(request.body)
    url_id = request_body.get('id')
    status = request_body.get('check_status')
    url = Url.objects.filter(id=url_id)[0]
    url.check_status = status
    if status is False:
        url.status_code = None
    url.save()
    return JsonResponse({"success": 1})
