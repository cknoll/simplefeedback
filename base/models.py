from django.db import models
import secrets

# for the sake of reduced complexity we implement our own serialize methods here
# this should be professionallized in the future

class Document(models.Model):
    slug = models.SlugField(max_length=500, blank=False, null=False)
    owner_key = models.SlugField(max_length=20, blank=False, null=False)
    doc_key = models.SlugField(max_length=20, blank=False, null=False)
    content = models.TextField()
    comment_for_reviewers = models.TextField(blank=True)
    render_markdown = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # secrets.token_hex(3) -> 3 Bytes give 6 Chars
        self.doc_key = secrets.token_hex(3)[:5]
        self.owner_key = secrets.token_hex(5)
        super().save(*args, **kwargs)

    def serialize(self):
        res = {
            "pk": self.pk,
            "_type": str(type(self)),
            "slug": self.slug,
            "owner_key": self.owner_key,
            "doc_key": self.doc_key,
            "content": self.content,
            "comment_for_reviewers": self.comment_for_reviewers,
            "render_markdown": self.render_markdown,
        }
        return res


class Feedback(models.Model):
    reviewer = models.CharField(max_length=250, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=False, related_name="feedbacks")

    def serialize(self, ann_list=True):
        """
        return the object as as serializable dict
        """
        res = {
            "pk": self.pk,
            "_type": str(type(self)),
            "reviewer": self.reviewer,
            "date": self.date,
            "document": self.document.serialize(),
        }
        if ann_list:
            # access related manager (reverse of foreign key relation below)
            res["annotation_list"] = [ann.serialize() for ann in self.annotations.all()]

        return res


# taken from https://github.com/acdh-oeaw/django-recogito
class RecogitoAnnotation(models.Model):
    re_id = models.CharField(max_length=100, primary_key=True)
    re_text = models.TextField(blank=True, null=True)
    re_start = models.IntegerField(blank=True, null=True)
    re_end = models.IntegerField(blank=True, null=True)
    re_payload = models.JSONField(blank=True, null=True)
    re_app = models.CharField(max_length=100, blank=True, null=True)
    re_model = models.CharField(max_length=100, blank=True, null=True)
    re_object_id = models.CharField(max_length=100, blank=True, null=True)
    re_field_name = models.CharField(max_length=100, blank=True, null=True)

    # this allows to access all related RecogitoAnnotaion objects via `feedback.annoations` (related Manager)
    re_feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, null=False, related_name="annotations")

    def __str__(self):
        return f"{self.re_text} ({self.re_id})"

    def serialize(self):
        """
        The JS API expects a specific data structure (schema) which is different from what it provides
        when the data is sent. This method transforms the data into that expected structure.
        """
        res = {
            "pk": self.pk,
            "_type": str(type(self)),
            "start": self.re_start,
            "end": self.re_end,
            "text": self.re_text, # target text
            "comment_value": self.re_payload["body"][0]["value"],
            # save a reference to the feedback but without annotation list (prevent inifinite reference circle)
            "feedback": self.re_feedback.serialize(ann_list=False)
        }
        return res

    def save(self, *args, **kwargs):
        if self.re_payload:
            data = self.re_payload
            target = data['target']['selector']
            for y in target:
                if 'start' in y.keys():
                    self.re_start = y['start']
                    self.re_end = y['end']
                else:
                    self.re_text = y['exact']
        super().save(*args, **kwargs)
