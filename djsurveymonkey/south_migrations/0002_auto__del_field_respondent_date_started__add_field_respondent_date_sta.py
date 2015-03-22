# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Respondent.date_started'
        db.delete_column('surveymonkey_respondent', 'date_started')

        # Adding field 'Respondent.date_start'
        db.add_column('surveymonkey_respondent', 'date_start',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)


        # Changing field 'Respondent.collector'
        db.alter_column('surveymonkey_respondent', 'collector_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djsurveymonkey.Collector'], null=True))

    def backwards(self, orm):
        # Adding field 'Respondent.date_started'
        db.add_column('surveymonkey_respondent', 'date_started',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Deleting field 'Respondent.date_start'
        db.delete_column('surveymonkey_respondent', 'date_start')


        # User chose to not deal with backwards NULL issues for 'Respondent.collector'
        raise RuntimeError("Cannot reverse this migration. 'Respondent.collector' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Respondent.collector'
        db.alter_column('surveymonkey_respondent', 'collector_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djsurveymonkey.Collector']))

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
            'sub_heading': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': u"orm['djsurveymonkey.Survey']"})
        },
        u'djsurveymonkey.question': {
            'Meta': {'object_name': 'Question', 'db_table': "'surveymonkey_question'"},
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['djsurveymonkey.Page']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'type_family': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type_subtype': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        u'djsurveymonkey.survey': {
            'Meta': {'object_name': 'Survey', 'db_table': "'surveymonkey_survey'"},
            'analysis_url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'custom_variable_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'from_survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djsurveymonkey.Survey']", 'null': 'True'}),
            'language_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_responses': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'question_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'survey_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djsurveymonkey.Template']", 'null': 'True'}),
            'title_enabled': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'title_text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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