from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import RecogitoAnnotation, Feedback
from . import serializers


from ipydex import IPS

@api_view(["GET"])
def get_data(request):

    objs = RecogitoAnnotation.objects.all()
    seralizer = serializers.RecogitoAnnotationSerializer(objs, many=True)

    return Response(seralizer.data)


@api_view(["POST"])
def add_data(request):

    # during development: delete all existing objects
    for w in RecogitoAnnotation.objects.all(): w.delete()
    for w in Feedback.objects.all(): w.delete()

    # todo: validate incomming data (non-trivial because we have no model for it)

    shared_data: dict = request.data.copy()
    reviewer_name = shared_data.pop("reviewer_name")
    re_annotation_list = shared_data.pop("re_annotation_list")

    # adapt for some schema change
    shared_data.pop("re_id", None)


    # Problem: feedback hat bisher keinen pk
    feedback = Feedback(author=reviewer_name)

    # save to create primary key
    feedback.save()

    for re_annotation in re_annotation_list:
        new_data = shared_data.copy()
        new_data.update(re_annotation)
        new_data["re_id"] = re_annotation["id"].lstrip("#")
        new_data["re_feedback"] = feedback.id
        seralizer = serializers.RecogitoAnnotationSerializer(data=new_data)
        try:
            seralizer.is_valid(raise_exception=True)
        except Exception as ex:
            print(ex)
            raise
        seralizer.save()


    return Response("OK")

    # TODO handle the error case
    return Response(seralizer.data)
