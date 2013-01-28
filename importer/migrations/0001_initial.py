# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PlaceCategory'
        db.create_table('importer_placecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('foursquare_id', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['importer.PlaceCategory'], null=True)),
        ))
        db.send_create_signal('importer', ['PlaceCategory'])


    def backwards(self, orm):
        # Deleting model 'PlaceCategory'
        db.delete_table('importer_placecategory')


    models = {
        'importer.placecategory': {
            'Meta': {'object_name': 'PlaceCategory'},
            'foursquare_id': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['importer.PlaceCategory']", 'null': 'True'})
        }
    }

    complete_apps = ['importer']