# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Clothing.sku'
        db.add_column(u'clothings_clothing', 'sku',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True),
                      keep_default=False)

        # Adding field 'Clothing.sizes'
        db.add_column(u'clothings_clothing', 'sizes',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True),
                      keep_default=False)

        # Adding field 'Clothing.colors'
        db.add_column(u'clothings_clothing', 'colors',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True),
                      keep_default=False)

        # Adding field 'Clothing.note'
        db.add_column(u'clothings_clothing', 'note',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Clothing.sku'
        db.delete_column(u'clothings_clothing', 'sku')

        # Deleting field 'Clothing.sizes'
        db.delete_column(u'clothings_clothing', 'sizes')

        # Deleting field 'Clothing.colors'
        db.delete_column(u'clothings_clothing', 'colors')

        # Deleting field 'Clothing.note'
        db.delete_column(u'clothings_clothing', 'note')


    models = {
        u'clothings.clothing': {
            'Meta': {'object_name': 'Clothing'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'colors': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'sizes': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        }
    }

    complete_apps = ['clothings']