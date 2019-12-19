from django.shortcuts import render


def admin_view(request):
    return render(request, "admin_iframe.html")


def home_view(request):
    return render(request, "home.html")
