# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Promo'
        db.create_table(u'promos_promo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('discount', self.gf('django.db.models.fields.FloatField')()),
            ('start_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'promos', ['Promo'])


    def backwards(self, orm):
        # Deleting model 'Promo'
        db.delete_table(u'promos_promo')


    models = {
        u'promos.promo': {
            'Meta': {'object_name': 'Promo'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.FloatField', [], {}),
            'end_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_at': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['promos']