from django.db import models
import secrets



class Document(models.Model):
    slug = models.SlugField(max_length=500, blank=False, null=False)
    owner_key = models.SlugField(max_length=20, blank=False, null=False)
    doc_key = models.SlugField(max_length=20, blank=False, null=False)
    content = models.TextField()

    def save(self, *args, **kwargs):
        self.reviewer_key = secrets.token_hex(5)
        self.owner_key = secrets.token_hex(10)
        super().save(*args, **kwargs)


class Feedback(models.Model):
    author = models.CharField(max_length=250, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=False,)


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

    # new
    re_feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, null=False,)

    def __str__(self):
        return f"{self.re_text} ({self.re_id})"

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
