from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse("You are at codElevate homepage.")
    return render(request,'website/index.html')

# def myprofile(request):
#     return HttpResponse("You are at your codElevate profile page.")

# def courses(request):
#     return HttpResponse("You are at your codElevate courses page.")

# def login(request):
#     return HttpResponse("You are at codElevate login page.")

# def dashboard(request):
#     return HttpResponse("You are at codElevate dashboard.")