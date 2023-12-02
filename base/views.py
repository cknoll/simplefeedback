from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.forms import ModelForm
from .models import Document

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

        template = "base/main_old.html"
        if mode == "new":
            template = "base/new_doc.html"
            self._new_doc(context)

        return render(request, template, context)

    def _new_doc(self, context):
        context["data"]["formset"] = DocumentForm()


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ["slug", "content"]
