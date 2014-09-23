# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DesignClothing'
        db.create_table(u'designs_designclothing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clothing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clothings.Clothing'])),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'designs', ['DesignClothing'])

        # Adding M2M table for field clothings on 'Design'
        m2m_table_name = db.shorten_name(u'designs_design_clothings')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('design', models.ForeignKey(orm[u'designs.design'], null=False)),
            ('designclothing', models.ForeignKey(orm[u'designs.designclothing'], null=False))
        ))
        db.create_unique(m2m_table_name, ['design_id', 'designclothing_id'])


    def backwards(self, orm):
        # Deleting model 'DesignClothing'
        db.delete_table(u'designs_designclothing')

        # Removing M2M table for field clothings on 'Design'
        db.delete_table(db.shorten_name(u'designs_design_clothings'))


    models = {
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
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'designs.design': {
            'Meta': {'object_name': 'Design'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'designs_for_me'", 'to': u"orm['auth.User']"}),
            'clothings': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['designs.DesignClothing']", 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'designer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'my_designs'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_selected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Order']"}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['designs.DesignPhoto']", 'symmetrical': 'False'})
        },
        u'designs.designclothing': {
            'Meta': {'object_name': 'DesignClothing'},
            'clothing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clothings.Clothing']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'designs.designphoto': {
            'Meta': {'object_name': 'DesignPhoto'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'designer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'file': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'orders.order': {
            'Meta': {'object_name': 'Order'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'age_group': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'chest': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'my_orders'", 'to': u"orm['auth.User']"}),
            'express_info': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'foot': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'hipline': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'preferred_designer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'designed_orders'", 'to': u"orm['auth.User']"}),
            'prepayment': ('django.db.models.fields.FloatField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'created'", 'max_length': '16'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'total_price': ('django.db.models.fields.FloatField', [], {}),
            'waistline': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'weight': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'})
        }
    }

    complete_apps = ['designs']