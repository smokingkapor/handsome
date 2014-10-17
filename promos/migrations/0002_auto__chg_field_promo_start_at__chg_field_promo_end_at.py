# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Promo.start_at'
        db.alter_column(u'promos_promo', 'start_at', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Promo.end_at'
        db.alter_column(u'promos_promo', 'end_at', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):

        # Changing field 'Promo.start_at'
        db.alter_column(u'promos_promo', 'start_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Promo.end_at'
        db.alter_column(u'promos_promo', 'end_at', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'promos.promo': {
            'Meta': {'object_name': 'Promo'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.FloatField', [], {}),
            'end_at': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_at': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['promos']