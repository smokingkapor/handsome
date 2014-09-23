# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Clothing.image'
        db.add_column(u'clothings_clothing', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(default='clothings/default.png', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Clothing.image'
        db.delete_column(u'clothings_clothing', 'image')


    models = {
        u'clothings.clothing': {
            'Meta': {'object_name': 'Clothing'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'colors': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'clothings/default.png'", 'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'sizes': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        }
    }

    complete_apps = ['clothings']