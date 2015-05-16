from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from json_field import JSONField

__all__ = [
    'Template', 'Page', 'Item', 'Answer', 'Question', 'CustomVariable',
    'Survey', 'Collector', 'EmailMessage', 'Recipient', 'Respondent', 'Response'
]

@python_2_unicode_compatible
class Template(models.Model):
    template_id = models.CharField(max_length=255, primary_key=True)
    language_id = models.PositiveIntegerField(null=True)
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    long_description = models.CharField(max_length=255)    
    is_available_to_current_user = models.NullBooleanField()
    is_featured = models.NullBooleanField()
    is_certified = models.NullBooleanField()
    page_count = models.PositiveIntegerField(null=True)
    question_count = models.PositiveIntegerField(null=True)
    preview_url = models.URLField(max_length=255)
    category_id = models.CharField(max_length=255)
    category_name = models.CharField(max_length=255)
    category_desciption = models.CharField(max_length=255)
    date_created = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(null=True)

    class Meta:
        db_table = 'surveymonkey_template'
    
    def __str__(self):
        return self.title

        
@python_2_unicode_compatible
class Page(models.Model):
    page_id = models.CharField(max_length=255, primary_key=True)
    survey = models.ForeignKey('Survey', related_name='pages')
    heading = models.CharField(max_length=255)
    sub_heading = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'surveymonkey_page'
    
    def __str__(self):
        name = "%s - %s" % (self.survey, self.pk)
        if self.heading:
            name = "%s - %s" % (name, self.heading)
        return name

        
@python_2_unicode_compatible
class Item(models.Model):
    answer = models.ForeignKey('Answer', related_name='items')
    position = models.PositiveIntegerField()
    type = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
        
    class Meta:
        db_table = 'surveymonkey_item'
    
    def __str__(self):
        return "%s - %s" % (self.type, self.text)

        
@python_2_unicode_compatible
class Answer(models.Model):
    answer_id = models.CharField(max_length=255, primary_key=True)
    position = models.PositiveIntegerField()
    text = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    visible = models.BooleanField()
    weight = models.PositiveIntegerField()
    apply_all_rows = models.BooleanField()
    is_answer = models.BooleanField()

    class Meta:
        db_table = 'surveymonkey_answer'
    
    def __str__(self):
        return "%s: %s - %s" % (self.position, self.type, self.text)

        
@python_2_unicode_compatible
class Question(models.Model):
    question_id = models.CharField(max_length=255, primary_key=True)
    page = models.ForeignKey(Page, related_name='questions')
    heading = models.CharField(max_length=255)
    position = models.PositiveIntegerField()
    type = JSONField(null=True)

    class Meta:
        db_table = 'surveymonkey_question'
    
    def __str__(self):
        return "%s: %s" % (self.position, self.heading)

        
@python_2_unicode_compatible
class CustomVariable(models.Model):
    variable_label = models.CharField(max_length=255)
    question = models.ForeignKey(Question)
    survey = models.ForeignKey('Survey', related_name='custom_variables')

    class Meta:
        db_table = 'surveymonkey_custom_variable'
    
    def __str__(self):
        return "Survey: %s, Question: %s - %s" % (
            self.survey, self.question_id, self.variable_name)

    
@python_2_unicode_compatible
class Survey(models.Model):
    survey_id = models.CharField(max_length=255, primary_key=True)
    template = models.ForeignKey(Template, null=True, related_name='derived_surveys')
    from_survey = models.ForeignKey('self', null=True, related_name='derived_surveys')
    date_created = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(null=True)
    custom_variable_count = models.PositiveIntegerField(null=True)
    language_id = models.PositiveIntegerField(null=True)
    num_responses = models.PositiveIntegerField(null=True)
    question_count = models.PositiveIntegerField(null=True)
    nickname = models.CharField(max_length=255)
    title = JSONField(null=True)
    analysis_url = models.URLField(max_length=255)

    class Meta:
        db_table = 'surveymonkey_survey'

    @property
    def survey_title(self, value):
        if isinstance(self.title, dict):
            return self.title.get('text', self.nickname)
        return self.nickname

    @survey_title.setter
    def survey_title(self, value):
        if not self.title:
            self.title = {}
        self.title['text'] = value
        
    def __str__(self):
        return self.survey_title


@python_2_unicode_compatible
class Collector(models.Model):
    collector_id = models.CharField(max_length=255, primary_key=True)
    date_created = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(null=True)
    name = models.CharField(max_length=255)
    open = models.NullBooleanField()
    type = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    send = models.NullBooleanField()

    class Meta:
        db_table = 'surveymonkey_collector'
    
    def __str__(self):
        return self.name

    
@python_2_unicode_compatible
class EmailMessage(models.Model):
    email_message_id = models.CharField(max_length=255, primary_key=True)
    reply_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body_text = models.TextField(null=True)

    class Meta:
        db_table = 'surveymonkey_email_message'
    
    def __str__(self):
        return "%%s - %s" % (self.reply_email, self.subject)
    

@python_2_unicode_compatible
class Recipient(models.Model):
    recipient_id = models.CharField(max_length=255, primary_key=True)
    collector = models.ForeignKey(Collector, related_name='recipients')
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    custom_id = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'surveymonkey_recipient'
    
    def __str__(self):
        return ("%s %s <%s>" % (self.first_name, self.last_name, self.email)).strip()


@python_2_unicode_compatible
class Respondent(models.Model):
    respondent_id = models.CharField(max_length=255, primary_key=True)
    date_start = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(null=True)
    collector = models.ForeignKey(Collector, null=True)
    collection_mode = models.CharField(max_length=255)
    custom_id = models.CharField(max_length=255)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    ip_address = models.IPAddressField()
    status = models.CharField(max_length=255)
    analysis_url = models.URLField(max_length=255)
    recipient = models.ForeignKey(Recipient, null=True)

    class Meta:
        db_table = 'surveymonkey_respondent'
    
    def __str__(self):
        return ("%s %s <%s>" % (self.first_name, self.last_name, self.email)).strip()


@python_2_unicode_compatible
class Response(models.Model):
    respondent = models.ForeignKey(Respondent)
    question = models.ForeignKey(Question)
    answers = JSONField(null=True)        
    date_retrieved = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'surveymonkey_response'
    
    def __str__(self):
        return "%s: %s" % (self.question, self.respondent)

        
## Below is a response related model that need some real data to be modeled properly
        
class ResponseAnswer(models.Model):
    row = models.ForeignKey(Answer)
    col = models.ForeignKey(Answer)
    col_choice = models.ForeignKey(Answer)
    text = models.CharField(max_length=32768)    

    class Meta:
        abstract = True
        
        
        
