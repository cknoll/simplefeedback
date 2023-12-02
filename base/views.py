from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

# Create your views here.

class Staticpage(View):
    def get(self, request, slug=None, doc_key=None, owner_key=None, mode=None):
        context = {
            # having a nested dict for easier debugging in the template
            "data": {
                "slug": slug,
                "doc_key": doc_key,
                "owner_key": owner_key,
                "mode": mode,
            }
        }

        return render(request, "base/example.html", context)
