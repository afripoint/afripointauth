from django.shortcuts import render
from ipware import get_client_ip

# Create your views here.

def home(request):
    client_ip, is_routable = get_client_ip(request)
    print(client_ip, is_routable)
    return render(request, 'pages/home.html')
