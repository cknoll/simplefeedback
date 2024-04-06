from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import RecogitoAnnotation, Feedback, Document
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from . import serializers


from ipydex import IPS

@api_view(["GET"])
def get_data(request, owner_key=None):

    annotations = []
    if owner_key is not None:
        doc = get_object_or_404(Document, owner_key=owner_key)
        feedbacks = doc.feedbacks.all()
        for fb in feedbacks:
            # annotations = [ann.re_payload for ann in fb.annotations.all()]
            annotations = [ann.get_expected_structure() for ann in fb.annotations.all()]
            break
    return JsonResponse(annotations, safe=False)
    # serializer = serializers.FeedbackSerializer(feedbacks, many=True)

    # res = serializer.data
    # response = Response(res)
    # w = {"re_app":"simplefeedback","re_id":"95937184-078a-49c0-8037-d8495b593674","re_payload":{"@context":"http://www.w3.org/ns/anno.jsonld","type":"Annotation","body":[{"type":"TextualBody","value":"comment1 like model","purpose":"commenting"}],"target":{"selector":[{"type":"TextQuoteSelector","exact":"document"},{"type":"TextPositionSelector","start":32,"end":40}]},"id":"#95937184-078a-49c0-8037-d8495b593674"}}
    # response.data = w
    # # from ipydex import IPS; IPS()
    # return response


@api_view(["POST"])
def add_data(request):
    # print("api call add")

    # during development: delete all existing objects
    # for w in RecogitoAnnotation.objects.all(): w.delete()
    # for w in Feedback.objects.all(): w.delete()


    # todo: validate incomming data (non-trivial because we have no model for it)

    # make a copy and convert to dict
    assert type(request.data) == dict
    shared_data: dict = request.data.copy()

    reviewer_name = shared_data.pop("reviewer_name")
    re_annotation_list = shared_data.pop("re_annotation_list")
    assert isinstance(re_annotation_list, list)

    # adapt for some schema change
    shared_data.pop("re_id", None)
    doc = get_object_or_404(Document, doc_key=shared_data.get("doc_key"))
    feedback = Feedback(reviewer=reviewer_name, document=doc)

    # save to create primary key
    feedback.save()

    for re_annotation in re_annotation_list:

        new_data = shared_data.copy()
        new_data.update(re_annotation)
        new_data["re_id"] = re_annotation["id"].lstrip("#")
        new_data["re_feedback"] = feedback.id
        new_data["re_payload"] = re_annotation
        serializer = serializers.RecogitoAnnotationSerializer(data=new_data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as ex:
            print(ex)
            # from ipydex import IPS; IPS()
            raise
        serializer.save()


    return Response("OK")

    # TODO handle the error case
    return Response(serializer.data)
