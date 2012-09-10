# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Place'
        db.delete_table('geo_place')

        # Adding field 'City.slug'
        db.add_column('geo_city', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', unique=True, max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Place'
        db.create_table('geo_place', (
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.City'])),
            ('adresss', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geojson', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('geo', ['Place'])

        # Deleting field 'City.slug'
        db.delete_column('geo_city', 'slug')


    models = {
        'geo.city': {
            'Meta': {'object_name': 'City'},
            'geojson': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
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