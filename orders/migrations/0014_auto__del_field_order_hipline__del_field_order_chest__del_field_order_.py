# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Order.hipline'
        db.delete_column(u'orders_order', 'hipline')

        # Deleting field 'Order.chest'
        db.delete_column(u'orders_order', 'chest')

        # Deleting field 'Order.waistline'
        db.delete_column(u'orders_order', 'waistline')

        # Deleting field 'Order.hobby'
        db.delete_column(u'orders_order', 'hobby')

        # Deleting field 'Order.foot'
        db.delete_column(u'orders_order', 'foot')

        # Deleting field 'Order.is_slim'
        db.delete_column(u'orders_order', 'is_slim')

        # Adding field 'Order.clothing_size'
        db.add_column(u'orders_order', 'clothing_size',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)

        # Adding field 'Order.pants_size'
        db.add_column(u'orders_order', 'pants_size',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)

        # Adding field 'Order.pants_style'
        db.add_column(u'orders_order', 'pants_style',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)

        # Adding field 'Order.shoe_size'
        db.add_column(u'orders_order', 'shoe_size',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)

        # Adding field 'Order.situation'
        db.add_column(u'orders_order', 'situation',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Order.hipline'
        db.add_column(u'orders_order', 'hipline',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)

        # Adding field 'Order.chest'
        db.add_column(u'orders_order', 'chest',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)

        # Adding field 'Order.waistline'
        db.add_column(u'orders_order', 'waistline',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)

        # Adding field 'Order.hobby'
        db.add_column(u'orders_order', 'hobby',
                      self.gf('django.db.models.fields.CharField')(default='other', max_length=32),
                      keep_default=False)

        # Adding field 'Order.foot'
        db.add_column(u'orders_order', 'foot',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)

        # Adding field 'Order.is_slim'
        db.add_column(u'orders_order', 'is_slim',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Order.clothing_size'
        db.delete_column(u'orders_order', 'clothing_size')

        # Deleting field 'Order.pants_size'
        db.delete_column(u'orders_order', 'pants_size')

        # Deleting field 'Order.pants_style'
        db.delete_column(u'orders_order', 'pants_style')

        # Deleting field 'Order.shoe_size'
        db.delete_column(u'orders_order', 'shoe_size')

        # Deleting field 'Order.situation'
        db.delete_column(u'orders_order', 'situation')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'orders.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Country']", 'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_selected': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Province']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'orders.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Province']"})
        },
        u'orders.country': {
            'Meta': {'object_name': 'Country'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'orders.order': {
            'Meta': {'object_name': 'Order'},
            'address_city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.City']", 'null': 'True', 'blank': 'True'}),
            'address_country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Country']", 'null': 'True', 'blank': 'True'}),
            'address_province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Province']", 'null': 'True', 'blank': 'True'}),
            'age_group': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'clothing_size': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'my_orders'", 'to': u"orm['auth.User']"}),
            'express_info': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'pants_size': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'pants_style': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'preferred_designer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'designed_orders'", 'to': u"orm['auth.User']"}),
            'prepayment': ('django.db.models.fields.FloatField', [], {}),
            'price_group': ('django.db.models.fields.FloatField', [], {}),
            'report': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'shoe_size': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'situation': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'created'", 'max_length': '16'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'total_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'weight': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'})
        },
        u'orders.province': {
            'Meta': {'object_name': 'Province'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['orders']