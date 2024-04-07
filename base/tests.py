import time
import json

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from bs4 import BeautifulSoup
from django.urls import reverse
from django.conf import settings
from base import models

from splinter import Browser

from ipydex import IPS


# this number might need to change if the fixtures change
NUMBER_OF_FIXTURE_ANNOTATIONS = 7


class TestCore1(TestCase):
    fixtures = ["base/testdata/fixtures01.json"]

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

    def test_030_review_doc(self):
        # slug does not matter
        response = self.client.get(reverse("reviewpage", args=("foo", "8ada4")))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"utc_doc_review", response.content)

        all_annotations = models.RecogitoAnnotation.objects.all()
        self.assertEqual(len(all_annotations), NUMBER_OF_FIXTURE_ANNOTATIONS)

        post_data = {
            "doc_key" : "8ada4",
            "reviewer_name" : "rv1",
            "re_annotation_list" : [
                {
                    "@context" : "http://www.w3.org/ns/anno.jsonld",
                    "body" : [ {
                        "purpose" : "commenting",
                        "type" : "TextualBody",
                        "value" : "test-comment1"
                        } ],
                    "id" : "#6c132403-dff1-4705-96b9-932e4ce3150f",
                    "target" : { "selector" : [
                            {
                            "exact" : "document",
                            "type" : "TextQuoteSelector"
                            },
                            {
                            "end" : 40,
                            "start" : 32,
                            "type" : "TextPositionSelector"
                            }
                        ] },
                    "type" : "Annotation"
                },
                {
                    "@context" : "http://www.w3.org/ns/anno.jsonld",
                    "body" : [ {
                        "purpose" : "commenting",
                        "type" : "TextualBody",
                        "value" : "test-comment2"
                        } ],
                    "id" : "#fb3b5729-ce67-4432-a6c1-6dd142d78c89",
                    "target" : { "selector" : [
                            {
                            "exact" : "document",
                            "type" : "TextQuoteSelector"
                            },
                            {
                            "end" : 208,
                            "start" : 200,
                            "type" : "TextPositionSelector"
                            }
                        ] },
                    "type" : "Annotation"
                }
                ],
            "re_app" : "simplefeedback",
        }

        api_url = reverse("api_add")
        response = self.client.post(api_url, data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        all_annotations = models.RecogitoAnnotation.objects.all()
        self.assertEqual(len(all_annotations), NUMBER_OF_FIXTURE_ANNOTATIONS + 2)

        # retrieve the posted annotations from owner page
        api_url = reverse("api_get_ok", args=("18477d7d87", ))
        response = self.client.get(api_url)

        feedbacks = json.loads(response.content)
        self.assertEqual(len(feedbacks), 2)
        feedback1 = feedbacks[1]
        self.assertEqual(feedback1["reviewer"], "rv1")
        self.assertEqual(len(feedback1["annotation_list"]), 2)

        self.assertEqual(feedback1["annotation_list"][0]["comment_value"], "test-comment1")

    def test_040_owner_page(self):
        url = reverse("documentpage", kwargs={"slug": "test-doc1", "doc_key": "8ada4", "owner_key": "18477d7d87"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        bs = BeautifulSoup(response.content, 'html.parser')
        json_element = bs.find(id="review_nbr")
        review_nbr = json_element.contents[0]
        self.assertEqual(review_nbr, "1")


class TestGUI(StaticLiveServerTestCase):
    fixtures = ["base/testdata/fixtures01.json"]
    headless = False

    def setUp(self) -> None:
        self.options_for_browser = dict(driver_name='chrome', headless=self.headless)

        self.browsers = []

        return

    def tearDown(self):

        # quit all browser instances (also those which where not created by setUp)
        for browser in self.browsers:
            browser.quit()

    def get_browser_log(self, browser):
        res = browser.driver.get_log("browser")
        browser.logs.append(res)
        return res

    def new_browser(self):
        """
        create and register a new browser

        :return: browser object and its index
        """
        browser = Browser(**self.options_for_browser)
        browser.logs = []
        self.browsers.append(browser)

        return browser

    def test_make_review(self):

        b1 = self.new_browser()
        url = reverse("reviewpage", kwargs={"slug": "test-doc1", "doc_key": "8ada4"})
        b1.visit(f"{self.live_server_url}{url}")
        self.assertEqual(len(b1.find_by_tag("textarea")), 0)
        b1.find_by_id("click-target1").double_click()
        b1.find_by_tag("textarea").fill("test comment1")
        btn_OK = get_element_by_html_content(b1.find_by_tag("button"), "Ok")
        self.assertEqual(btn_OK.html, "Ok")
        btn_OK.click()
        b1.find_by_id("reviewerName").fill("test-reviewer1")
        btn_submit = b1.find_by_id("mainSubmit")

        all_annotations0 = models.RecogitoAnnotation.objects.all()
        self.assertEqual(len(all_annotations0), NUMBER_OF_FIXTURE_ANNOTATIONS)

        btn_submit.click()

        # give some time for the request to be processed
        time.sleep(0.1)

        all_annotations1 = models.RecogitoAnnotation.objects.all()
        self.assertEqual(len(all_annotations1), NUMBER_OF_FIXTURE_ANNOTATIONS + 1)

# #################################################################################################

# auxiliary functions:

# #################################################################################################


def get_element_by_html_content(element_list: list, content: str):

    for elt in element_list:
        if elt.html == content:
            res_elt = elt
            return res_elt

    raise ValueError(f"Could not find element with content \"{content}\"")


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
