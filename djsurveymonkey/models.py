from django.db import models


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
    

class Page(models.Model):
    page_id = models.CharField(max_length=255, primary_key=True)
    survey = models.ForeignKey('Survey', related_name='pages')
    heading = models.CharField(max_length=255)
    sub_heading = models.CharField(max_length=255)

    class Meta:
        db_table = 'surveymonkey_page'

        
class Item(models.Model):
    answer = models.ForeignKey('Answer', related_name='items')
    position = models.PositiveIntegerField()
    type = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
        
    class Meta:
        db_table = 'surveymonkey_item'

        
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

        
class Question(models.Model):
    question_id = models.CharField(max_length=255, primary_key=True)
    page = models.ForeignKey(Page, related_name='questions')
    heading = models.CharField(max_length=255)
    position = models.PositiveIntegerField()
    type_family = models.CharField(max_length=255)
    type_subtype = models.CharField(max_length=255)

    class Meta:
        db_table = 'surveymonkey_question'

        
class CustomVariable(models.Model):
    variable_label = models.CharField(max_length=255)
    question = models.ForeignKey(Question)
    survey = models.ForeignKey('Survey', related_name='custom_variables')

    class Meta:
        db_table = 'surveymonkey_custom_variable'

    
class Survey(models.Model):
    survey_id = models.CharField(max_length=255, primary_key=True)
    template = models.ForeignKey(Template, null=True)
    from_survey = models.ForeignKey('self', null=True)
    date_created = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(null=True)
    custom_variable_count = models.PositiveIntegerField(null=True)
    language_id = models.PositiveIntegerField(null=True)
    num_responses = models.PositiveIntegerField(null=True)
    question_count = models.PositiveIntegerField(null=True)
    nickname = models.CharField(max_length=255)
    title_enabled = models.NullBooleanField()
    title_text = models.CharField(max_length=255)
    analysis_url = models.URLField(max_length=255)

    class Meta:
        db_table = 'surveymonkey_survey'


class Collector(models.Model):
    collector_id = models.CharField(max_length=255, primary_key=True)
    date_created = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(null=True)
    name = models.CharField(max_length=255)
    open = models.NullBooleanField()
    type = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    class Meta:
        db_table = 'surveymonkey_collector'

    
class EmailMessage(models.Model):
    email_message_id = models.CharField(max_length=255, primary_key=True)
    reply_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body_text = models.TextField(null=True)

    class Meta:
        db_table = 'surveymonkey_email_message'
    

class Recipient(models.Model):
    recipient_id = models.CharField(max_length=255, primary_key=True)
    collector = models.ForeignKey(Collector, related_name='recipients')
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    custom_id = models.CharField(max_length=255)

    class Meta:
        db_table = 'surveymonkey_recipient'
    

class Respondent(models.Model):
    respondent_id = models.CharField(max_length=255, primary_key=True)
    date_started = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(null=True)
    collector = models.ForeignKey(Collector)
    collection_mode = models.CharField(max_length=255)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
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
    
