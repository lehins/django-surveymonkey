# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Response'
        db.create_table('surveymonkey_response', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('respondent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djsurveymonkey.Respondent'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djsurveymonkey.Question'])),
            ('answers', self.gf('json_field.fields.JSONField')(default=u'null', null=True)),
        ))
        db.send_create_signal(u'djsurveymonkey', ['Response'])

        # Deleting field 'Survey.title_enabled'
        db.delete_column('surveymonkey_survey', 'title_enabled')

        # Deleting field 'Survey.title_text'
        db.delete_column('surveymonkey_survey', 'title_text')

        # Adding field 'Survey.title'
        db.add_column('surveymonkey_survey', 'title',
                      self.gf('json_field.fields.JSONField')(default=u'null', null=True),
                      keep_default=False)

        # Deleting field 'Question.type_subtype'
        db.delete_column('surveymonkey_question', 'type_subtype')

        # Deleting field 'Question.type_family'
        db.delete_column('surveymonkey_question', 'type_family')

        # Adding field 'Question.type'
        db.add_column('surveymonkey_question', 'type',
                      self.gf('json_field.fields.JSONField')(default=u'null', null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Response'
        db.delete_table('surveymonkey_response')

        # Adding field 'Survey.title_enabled'
        db.add_column('surveymonkey_survey', 'title_enabled',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Survey.title_text'
        raise RuntimeError("Cannot reverse this migration. 'Survey.title_text' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Survey.title_text'
        db.add_column('surveymonkey_survey', 'title_text',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)

        # Deleting field 'Survey.title'
        db.delete_column('surveymonkey_survey', 'title')


        # User chose to not deal with backwards NULL issues for 'Question.type_subtype'
        raise RuntimeError("Cannot reverse this migration. 'Question.type_subtype' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Question.type_subtype'
        db.add_column('surveymonkey_question', 'type_subtype',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Question.type_family'
        raise RuntimeError("Cannot reverse this migration. 'Question.type_family' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Question.type_family'
        db.add_column('surveymonkey_question', 'type_family',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)

        # Deleting field 'Question.type'
        db.delete_column('surveymonkey_question', 'type')


    models = {
        u'djsurveymonkey.answer': {
            'Meta': {'object_name': 'Answer', 'db_table': "'surveymonkey_answer'"},
            'answer_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'apply_all_rows': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'djsurveymonkey.collector': {
            'Meta': {'object_name': 'Collector', 'db_table': "'surveymonkey_collector'"},
            'collector_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'open': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        u'djsurveymonkey.customvariable': {
            'Meta': {'object_name': 'CustomVariable', 'db_table': "'surveymonkey_custom_variable'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djsurveymonkey.Question']"}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custom_variables'", 'to': u"orm['djsurveymonkey.Survey']"}),
            'variable_label': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'djsurveymonkey.emailmessage': {
            'Meta': {'object_name': 'EmailMessage', 'db_table': "'surveymonkey_email_message'"},
            'body_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'email_message_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'reply_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'djsurveymonkey.item': {
            'Meta': {'object_name': 'Item', 'db_table': "'surveymonkey_item'"},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['djsurveymonkey.Answer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'djsurveymonkey.page': {
            'Meta': {'object_name': 'Page', 'db_table': "'surveymonkey_page'"},
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'page_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'sub_heading': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': u"orm['djsurveymonkey.Survey']"})
        },
        u'djsurveymonkey.question': {
            'Meta': {'object_name': 'Question', 'db_table': "'surveymonkey_question'"},
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['djsurveymonkey.Page']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'type': ('json_field.fields.JSONField', [], {'default': "u'null'", 'null': 'True'})
        },
        u'djsurveymonkey.recipient': {
            'Meta': {'object_name': 'Recipient', 'db_table': "'surveymonkey_recipient'"},
            'collector': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipients'", 'to': u"orm['djsurveymonkey.Collector']"}),
            'custom_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'recipient_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        },
        u'djsurveymonkey.respondent': {
            'Meta': {'object_name': 'Respondent', 'db_table': "'surveymonkey_respondent'"},
            'analysis_url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'collection_mode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'collector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djsurveymonkey.Collector']", 'null': 'True'}),
            'custom_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djsurveymonkey.Recipient']", 'null': 'True'}),
            'respondent_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'djsurveymonkey.response': {
            'Meta': {'object_name': 'Response', 'db_table': "'surveymonkey_response'"},
            'answers': ('json_field.fields.JSONField', [], {'default': "u'null'", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djsurveymonkey.Question']"}),
            'respondent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djsurveymonkey.Respondent']"})
        },
        u'djsurveymonkey.survey': {
            'Meta': {'object_name': 'Survey', 'db_table': "'surveymonkey_survey'"},
            'analysis_url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'custom_variable_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'from_survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'derived_surveys'", 'null': 'True', 'to': u"orm['djsurveymonkey.Survey']"}),
            'language_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_responses': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'question_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'survey_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'derived_surveys'", 'null': 'True', 'to': u"orm['djsurveymonkey.Template']"}),
            'title': ('json_field.fields.JSONField', [], {'default': "u'null'", 'null': 'True'})
        },
        u'djsurveymonkey.template': {
            'Meta': {'object_name': 'Template', 'db_table': "'surveymonkey_template'"},
            'category_desciption': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'category_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'is_available_to_current_user': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_certified': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_featured': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'language_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'long_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'page_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'preview_url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'question_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'template_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['djsurveymonkey']