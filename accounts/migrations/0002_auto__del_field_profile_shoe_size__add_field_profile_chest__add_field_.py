# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Profile.shoe_size'
        db.delete_column(u'accounts_profile', 'shoe_size')

        # Adding field 'Profile.chest'
        db.add_column(u'accounts_profile', 'chest',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)

        # Adding field 'Profile.hipline'
        db.add_column(u'accounts_profile', 'hipline',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)

        # Adding field 'Profile.foot'
        db.add_column(u'accounts_profile', 'foot',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)


        # Changing field 'Profile.weight'
        db.alter_column(u'accounts_profile', 'weight', self.gf('django.db.models.fields.CharField')(default='', max_length=16))

        # Changing field 'Profile.height'
        db.alter_column(u'accounts_profile', 'height', self.gf('django.db.models.fields.CharField')(default='', max_length=16))

        # Changing field 'Profile.waistline'
        db.alter_column(u'accounts_profile', 'waistline', self.gf('django.db.models.fields.CharField')(default='', max_length=16))

    def backwards(self, orm):
        # Adding field 'Profile.shoe_size'
        db.add_column(u'accounts_profile', 'shoe_size',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Profile.chest'
        db.delete_column(u'accounts_profile', 'chest')

        # Deleting field 'Profile.hipline'
        db.delete_column(u'accounts_profile', 'hipline')

        # Deleting field 'Profile.foot'
        db.delete_column(u'accounts_profile', 'foot')


        # Changing field 'Profile.weight'
        db.alter_column(u'accounts_profile', 'weight', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Profile.height'
        db.alter_column(u'accounts_profile', 'height', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Profile.waistline'
        db.alter_column(u'accounts_profile', 'waistline', self.gf('django.db.models.fields.FloatField')(null=True))

    models = {
        u'accounts.profile': {
            'Meta': {'object_name': 'Profile'},
            'age_group': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'chest': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'foot': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'hipline': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preferred_style': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'waistline': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'weight': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']