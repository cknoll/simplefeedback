from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

# Create your views here.

class Staticpage(View):
    def get(self, request):
        context = {
        }

        return render(request, "base/example.html", context)
