# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Supplier'
        db.create_table(u'clothings_supplier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('security_code', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'clothings', ['Supplier'])

        # Adding field 'Clothing.supplier'
        db.add_column(u'clothings_clothing', 'supplier',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clothings.Supplier'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Supplier'
        db.delete_table(u'clothings_supplier')

        # Deleting field 'Clothing.supplier'
        db.delete_column(u'clothings_clothing', 'supplier_id')


    models = {
        u'clothings.clothing': {
            'Meta': {'object_name': 'Clothing'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'colors': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'sizes': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clothings.Supplier']", 'null': 'True', 'blank': 'True'})
        },
        u'clothings.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'security_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'})
        }
    }

    complete_apps = ['clothings']