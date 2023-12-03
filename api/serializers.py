from rest_framework import serializers
from base.models import RecogitoAnnotation, Feedback


class RecogitoAnnotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecogitoAnnotation
        fields = "__all__"

    def is_valid(self, *, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)


class FeedbackSerializer(serializers.ModelSerializer):
    # see https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    annotations = RecogitoAnnotationSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = "__all__"

    def is_valid(self, *, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)
