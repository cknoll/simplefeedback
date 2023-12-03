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
        elif mode == "review":
            self._set_doc(context, doc_key=doc_key)
            template = "base/doc_review.html"
        elif mode == "owner":
            self._set_doc(context, doc_key=doc_key, owner_key=owner_key)
            template = "base/doc_owner.html"

        return render(request, template, context)

    def post(self, request, **kwargs):
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

        doc = self._set_doc(context, doc_pk=doc_pk, owner_key=owner_key)
        context["data"]["formset"] = DocumentForm(instance=doc)

    def _set_doc(self, context, doc_pk=None, doc_key=None, owner_key=None):

        assert (doc_pk, doc_key).count(None) == 1

        if doc_pk is not None:
            doc = get_object_or_404(Document, pk=doc_pk)
        elif doc_key is not None:
            doc = get_object_or_404(Document, doc_key=doc_key)
        else:
            assert False  # cannot happen due to test above

        if owner_key is not None:
            if (doc.owner_key != owner_key):
                # TODO: use different exception here
                raise KeyError("owner key does not match")
            doc.owner_mode = True
        context["data"]["doc"] = doc
        return doc


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ["slug", "content"]
