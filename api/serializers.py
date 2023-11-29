from rest_framework import serializers
from base.models import RecogitoAnnotation


# class RecogitoAnnotationSerializer(serializers.HyperlinkedModelSerializer):
class RecogitoAnnotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecogitoAnnotation
        fields = "__all__"
        # fields = ['url', ] + [x.name for x in model._meta.get_fields()]

    def is_valid(self, *, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)
