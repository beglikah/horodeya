from django.shortcuts import render
from django.http import HttpResponse
import socket


# Create your views here.
def test_cookie(request):
    if not request.COOKIES.get('color'):
        response = HttpResponse('color')
        response.set_cookie('color', 'blue')
        return response
    else:
        return HttpResponse(
            "Your favorite color is {0}".format(request.COOKIES.get('color'))
        )


def track_user(request):
    response = render(request, 'home/track_user.html')
    if not request.COOKIES.get('visits'):
        response = HttpResponse(
            "This is your first visit to the site. "
            "From now on I will track your vistis to this site."
        )
        response.set_cookie('visits', '1', 3600 * 24 * 365 * 2)
    else:
        visits = int(request.COOKIES.get('visits', '1')) + 1
        response.set_cookie('visits', str(visits), 3600 * 24 * 365 * 2)
    return response


def get_user_ip(request):
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    device = "Your Computer Name is:" + hostname
    ip_address = "Your Computer IP Address is:" + IPAddr
    print(device, ip_address)
    return HttpResponse(device, ip_address)
