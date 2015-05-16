import time
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.forms import model_to_dict

from surveymonkey import api, calls, objects
from surveymonkey.utils import cached_property

from djsurveymonkey.models import Survey

try:
    API_KEY = getattr(settings, 'SURVEYMONKEY_API_KEY')
except AttributeError:
    raise ImproperlyConfigured("'SURVEYMONKEY_API_KEY' is a required setting.")
ACCESS_TOKEN = getattr(settings, 'SURVEYMONKEY_ACCESS_TOKEN', None)


class CallMixin(object):

    def update_from_response(self, obj, response,
                             fields=None, exclude_fields=None, commit=True):
        keys = set(response.keys())
        obj_field_set = {field.name for field in obj._meta.fields}
        related_field_set = set(obj._meta.get_all_field_names()) - obj_field_set
        if fields is None:
            exclude_field_set = (set(exclude_fields or []))
            field_set = obj_field_set - exclude_field_set
            related_field_set = related_field_set - exclude_field_set
        else:
            field_set = set(fields)
            related_field_set = related_field_set.intersection(field_set)
            field_set = field_set - related_field_set
        field_set = field_set.intersection(keys)
        related_field_set = related_field_set.intersection(keys)
        for field_name in field_set:
            setattr(obj, field_name, response[field_name])
        if commit:
            obj.save()
        if related_field_set:
            related_models = {}
            for rel_obj, _ in obj._meta.get_all_related_objects_with_model():
                related_models[rel_obj.field.related_query_name()] = rel_obj.model
            for related_field_name in related_field_set:
                response_list = response[related_field_name]
                if isinstance(response_list, list):
                    model = related_models[related_field_name]
                    self.create_or_update_from_response_list(
                        model, response_list, obj._meta.pk.name, obj.pk)
        return obj

    def create_or_update_from_response_list(
            self, model, response_list, parent_pk_name, parent_pk):
        pk_name = model._meta.pk.name
        obj_ids = [o[pk_name] for o in response_list]
        known_objs = {}
        for obj in model.objects.filter(pk__in=obj_ids):
            known_objs[obj.pk] = obj
        objs = []
        for obj_response in response_list:
            obj = known_objs.get(obj_response[pk_name], model())
            setattr(obj, parent_pk_name, parent_pk)
            obj = self.update_from_response(obj, obj_response)
            objs.append(obj)
        return objs

    
class Batch(CallMixin, calls.Batch):

    def _recipient_to_object(self, recipient):
        return objects.Recipient(**model_to_dict(recipient, fields=[
            'email', 'first_name', 'last_name', 'custom_id'
        ]))

    def _update_recipients(self, recipients, recipients_report, collector_id, commit=True):
        recipient_ids = dict([(r['email'], r['reipient_id'])
                              for r in recipients_report['recipients']
                              if 'email' in r and 'reipient_id' in r])
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
        recipients_report = response.data.get('recipients_report')
        if recipients_report:
            self._update_recipients(recipients, recipients_report, collector.pk)
        response.survey = survey
        response.collector = collector
        response.email_message = email_message
        return response                    

    def create_flow(self, survey, collector, recipients, email_message):
        # the param in create_flow is "survey_title" instead of "title",
        # or title['text'] like in other calls.
        params = {
            'survey': objects.Survey(
                survey.survey_title, 
                **model_to_dict(survey, fields=['template_id', 'from_survey_id'])),
            'collector': objects.Collector(
                recipients=map(self._recipient_to_object, recipients),
                **model_to_dict(collector, fields=['type', 'name', 'send'])),
            'email_message': objects.EmailMessage(
                **model_to_dict(email_message, fields=[
                    'reply_email', 'subject', 'body_text']))
        }
        response = super(Batch, self).create_flow(**params)
        return self._update_from_response(
            survey, collector, recipients, email_message, response)

    def send_flow(self, survey, collector, recipients, email_message):
        params = {
            'collector': objects.Collector(
                recipients=map(self._recipient_to_object, recipients),
                **model_to_dict(collector, fields=['type', 'name', 'send'])),
            'email_message': objects.EmailMessage(
                **model_to_dict(email_message, fields=[
                    'reply_email', 'subject', 'body_text']))
        }
        response = super(Batch, self).send_flow(survey.pk, **params)
        return self._update_from_response(
            survey, collector, recipients, email_message, response)


class Surveys(CallMixin, calls.Surveys):

    def get_survey_list(self, *args, **kwargs):
        response = super(Surveys, self).get_survey_list(*args, **kwargs)
        response.surveys = self.create_or_update_from_response_list(
            Survey, response.data['surveys'])
        return response

    def get_survey_details(self, survey):
        response = super(Surveys, self).get_survey_details(survey.pk)
        response.survey = self.update_from_response(survey, response.data)
        return response


class Collectors(CallMixin, calls.Collectors):

    def create_collector(self, survey, collector):
        response = super(Collectors, self).create_collector(
            survey.pk, objects.Collector(
                **model_to_dict(collector, fields=['type', 'name'])))
        response.collector = self.update_from_response(collector, response.data)
        response.collector.survey = survey
        return response

        
class SurveyMonkey(api.SurveyMonkey):

    def __init__(self, access_token=ACCESS_TOKEN, silent=not settings.DEBUG, **kwargs):
        # here for development convenience.
        self.native = api.SurveyMonkey(
            API_KEY, access_token=access_token, silent=silent, **kwargs)
        super(SurveyMonkey, self).__init__(
            API_KEY, access_token=access_token, silent=silent, **kwargs)

    def call(self, *args, **kwargs):
        # a temporary way of reducing chance of throttling
        time.sleep(1)
        return super(SurveyMonkey, self).call(*args, **kwargs)

    @cached_property
    def batch(self):
        return Batch(self)

    @cached_property
    def surveys(self):
        return Surveys(self)

    @cached_property
    def collectors(self):
        return Collectors(self)
