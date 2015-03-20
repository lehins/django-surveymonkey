from django.forms import model_to_dict

from surveymonkey import api, calls, objects
from surveymonkey.utils import cached_property


class Batch(calls.Batch):

    def create_flow(self, survey, collector, recipients, email_message):
        def to_recipient(r):
            return objects.Recipient(**model_to_dict(r, fields=[
                'email', 'first_name', 'last_name', 'custom_id'
            ]))
        # for some reason the param in create_flow is "survey_title" instead of "title",
        # like in other calls.
        params = {
            'survey': objects.Survey(
                survey.title, 
                **model_to_dict(survey, fields=['template_id', 'from_survey_id'])),
            'collector': objects.Collector(
                recipients=map(to_recipient, recipients),
                **model_to_dict(survey, fields=['type', 'name', 'send'])),
            'email_message': objects.EmailMessage(
                **model_to_dict(email_message, fields=[
                    'reply_email', 'first_name', 'last_name', 'custom_id']))
        }
        response = super(Batch, self).create_flow(**params)
        return response

class SurveyMonkey(api.SurveyMonkey):

    @cached_property
    def batch(self):
        return Batch(self)
