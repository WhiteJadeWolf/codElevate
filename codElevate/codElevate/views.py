from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse("You are at codElevate homepage.")
    return render(request,'website/index.html')