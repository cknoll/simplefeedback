from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.forms import ModelForm
from .models import Document

# Create your views here.

class Staticpage(View):
    def get(self, request, slug=None, doc_key=None, owner_key=None, mode=None, doc_pk=None):
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
            template = "base/doc_new.html"
            self._new_doc(context)
        elif mode == "new_preview":
            template = "base/doc_new.html"
            self._new_doc(context, doc_pk=doc_pk, owner_key=owner_key)

        return render(request, template, context)

    def post(self, request, **kwargs):
        print(request.POST)
        form = DocumentForm(request.POST)
        doc: Document = form.save()
        # from ipydex import IPS; IPS()
        if request.POST.get("action") == "save":
            assert doc.doc_key
            assert doc.owner_key
            url = reverse("documentpage", kwargs={"slug": doc.slug, "doc_key": doc.doc_key, "owner_key": doc.owner_key})
            return HttpResponseRedirect(url)

        return self.get(request, mode="new_preview", doc_pk=doc.pk, owner_key=doc.owner_key)

    def _new_doc(self, context, owner_key=None, doc_pk=None):
        if doc_pk is None:
            context["data"]["formset"] = DocumentForm()
            return

        doc = get_object_or_404(Document, pk=doc_pk)
        if doc.owner_key != owner_key:
            # TODO: use different exception here
            raise KeyError("owner key does not match")
        context["data"]["preview_doc"] = doc
        context["data"]["formset"] = DocumentForm(instance=doc)


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ["slug", "content"]
