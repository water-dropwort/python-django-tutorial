from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

def login_(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("testpolls:index"))
        else:
            return render(request, "polls/login.html")
    elif request.method == "POST":
        user_name = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = user_name, password = password)
        # succeeded to authenticate
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("testpolls:index"))
        # failed to authenticate
        else:
            return render(request, "polls/login.html",
                          { "error_message" : "Incorrect username or password", })

def logout_(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse("testpolls:login"))
