from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.forms import model_to_dict

from surveymonkey import api, calls, objects
from surveymonkey.utils import cached_property

try:
    API_KEY = getattr(settings, 'SURVEYMONKEY_API_KEY')
except AttributeError:
    raise ImproperlyConfigured("'SURVEYMONKEY_API_KEY' is a required setting.")
ACCESS_TOKEN = getattr(settings, 'SURVEYMONKEY_ACCESS_TOKEN', None)


class CallMixin(object):

    def update_from_response(self, instance, response,
                             fields=None, exclude_fields=None, commit=True):
        if fields is None:
            field_set = {field.name for field in instance._meta.fields}
            if exclude_fields is not None:
                field_set = field_set - set(exclude_fields)
        else:
            field_set = set(fields)
        keys = set(response.keys())
        fields = keys.union(field_set)            
        for field_name in fields:
            setattr(instance, response[field_name])
        if commit:
            instance.save()

    
class Batch(CallMixin, calls.Batch):

    def _recipient_to_object(self, recipient):
        return objects.Recipient(**model_to_dict(recipient, fields=[
            'email', 'first_name', 'last_name', 'custom_id'
        ]))

    def _update_recipients(self, recipients, recipients_report, collector_id, commit=True):
        recipient_ids = dict([(r.email, r.reipient_id)
                              for r in recipients_report['recipients']])
        added_recipients = []
        for recipient in recipients:
            recipient.recipient_id = recipient_ids.get(recipient.email, '')
            if recipient.recipient_id:
                added_recipients.append(recipient)
                if commit:
                    recipient.save()

    def _update_from_response(self, survey, collector, recipients, email_message, response):
        self.update_from_response(survey, response.data['survey'])
        self.update_from_response(collector, response.data['collector'])
        email_message_response = response.data.get('email_message')
        if email_message_response:
            self.update_from_response(email_message, email_message_response)
        recipients_report = response.get('recipients_report')
        if recipients_report:
            self._update_recipients(recipients, recipients_report, collector.pk)
        return response                    

    def create_flow(self, survey, collector, recipients, email_message):
        # for some reason the param in create_flow is "survey_title" instead of "title",
        # like in other calls.
        params = {
            'survey': objects.Survey(
                survey.title, 
                **model_to_dict(survey, fields=['template_id', 'from_survey_id'])),
            'collector': objects.Collector(
                recipients=map(self._recipient_to_object, recipients),
                **model_to_dict(collector, fields=['type', 'name', 'send'])),
            'email_message': objects.EmailMessage(
                **model_to_dict(email_message, fields=[
                    'reply_email', 'first_name', 'last_name', 'custom_id']))
        }
        return self._update_from_response(super(Batch, self).create_flow(**params))

    def send_flow(self, survey, collector, recipients, email_message):
        params = {
            'collector': objects.Collector(
                recipients=map(self._recipient_to_object, recipients),
                **model_to_dict(collector, fields=['type', 'name', 'send'])),
            'email_message': objects.EmailMessage(
                **model_to_dict(email_message, fields=[
                    'reply_email', 'first_name', 'last_name', 'custom_id']))
        }
        return self._update_from_response(super(Batch, self).send_flow(survey.pk, **params))

        
class SurveyMonkey(api.SurveyMonkey):

    def __init__(self, access_token=ACCESS_TOKEN, silent=not settings.DEBUG, **kwargs):
        super(SurveyMonkey, self).__init__(
            API_KEY, access_token=access_token, silent=silent, **kwargs) 

    @cached_property
    def batch(self):
        return Batch(self)
