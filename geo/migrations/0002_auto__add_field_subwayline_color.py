# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SubwayLine.color'
        db.add_column('geo_subwayline', 'color',
                      self.gf('django.db.models.fields.CharField')(default='FF0000', max_length=6),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SubwayLine.color'
        db.delete_column('geo_subwayline', 'color')


    models = {
        'geo.city': {
            'Meta': {'object_name': 'City'},
            'geojson': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'geo.place': {
            'Meta': {'object_name': 'Place'},
            'adresss': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.City']"}),
            'geojson': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'geo.subwayline': {
            'Meta': {'object_name': 'SubwayLine'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'FF0000'", 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'geo.subwaystation': {
            'Meta': {'object_name': 'SubwayStation'},
            'geojson': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lines': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'stations'", 'symmetrical': 'False', 'through': "orm['geo.SubwayStop']", 'to': "orm['geo.SubwayLine']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'geo.subwaystop': {
            'Meta': {'object_name': 'SubwayStop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.SubwayLine']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.SubwayStation']"})
        }
    }

    complete_apps = ['geo']