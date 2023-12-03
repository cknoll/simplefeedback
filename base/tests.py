from django.test import TestCase

from bs4 import BeautifulSoup
from django.urls import reverse
from django.conf import settings

from ipydex import IPS



class TestCore1(TestCase):

    def test_010_index(self):
        response = self.client.get(reverse("landingpage"))
        self.assertEqual(response.status_code, 200)

    def test_020_new_doc(self):
        response = self.client.get(reverse("newdocumentpage"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"utc_doc_new_create", response.content)

        form = get_first_form(response)
        txt = "utc-example-content" + "some example text "*10
        post_data = generate_post_data_for_form(form, spec_values={"slug": "the-slug", "content": txt})
        response = self.client.post(form.action_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"utc_doc_new_preview", response.content)

        # this should occure in the preview and in the form
        self.assertEqual(response.content.count(b"utc-example-content"), 2)
        post_data = generate_post_data_for_form(
            form, spec_values={"slug": "the-slug", "content": txt, "action": "save"}
        )
        response = self.client.post(form.action_url, post_data)

        # redirect to owner view
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.content.count(b"utc-example-content"), 1)


# auxiliary functions:

# helper functions copied from moodpoll
def get_first_form(response):
    """
    Auxiliary function that returns a bs-object of the first form which is specifies by action-url.

    :param response:
    :return:
    """
    bs = BeautifulSoup(response.content, 'html.parser')
    forms = bs.find_all("form")

    form = forms[0]
    form.action_url = form.attrs.get("action")

    return form


def get_form_fields_to_submit(form):
    """
    Return two lists: fields and hidden_fields.

    :param form:
    :return:
    """

    inputs = form.find_all("input")
    textareas = form.find_all("textarea")

    post_fields = inputs + textareas

    types_to_omit = ["submit", "cancel"]

    fields = []
    hidden_fields = []
    for field in post_fields:
        ftype = field.attrs.get("type")
        if ftype in types_to_omit:
            continue

        if ftype == "hidden":
            hidden_fields.append(field)
        else:
            fields.append(field)

    return fields, hidden_fields


def generate_post_data_for_form(form, default_value="xyz", spec_values=None):
    """
    Return a dict containing all dummy-data for the form

    :param form:
    :param default_value:   str; use this value for all not specified fields
    :param spec_values:     dict; use these values to override default value

    :return:                dict of post_data
    """

    if spec_values is None:
        spec_values = {}

    fields, hidden_fields = get_form_fields_to_submit(form)

    post_data = {}
    for f in hidden_fields:
        post_data[f.attrs['name']] = f.attrs['value']

    for f in fields:
        name = f.attrs.get('name')

        if name is None:
            # ignore fields without a name (relevant for dropdown checkbox)
            continue

        if name.startswith("captcha"):
            # special case for captcha fields (assume CAPTCHA_TEST_MODE=True)
            post_data[name] = "passed"
        else:
            post_data[name] = default_value

    post_data.update(spec_values)

    return post_data
