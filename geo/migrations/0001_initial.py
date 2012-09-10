# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'City'
        db.create_table('geo_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geojson', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('geo', ['City'])

        # Adding model 'Place'
        db.create_table('geo_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geojson', self.gf('django.db.models.fields.TextField')()),
            ('adresss', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.City'])),
        ))
        db.send_create_signal('geo', ['Place'])

        # Adding model 'SubwayStation'
        db.create_table('geo_subwaystation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geojson', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('geo', ['SubwayStation'])

        # Adding model 'SubwayLine'
        db.create_table('geo_subwayline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('geo', ['SubwayLine'])

        # Adding model 'SubwayStop'
        db.create_table('geo_subwaystop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.SubwayStation'])),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.SubwayLine'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('geo', ['SubwayStop'])


    def backwards(self, orm):
        # Deleting model 'City'
        db.delete_table('geo_city')

        # Deleting model 'Place'
        db.delete_table('geo_place')

        # Deleting model 'SubwayStation'
        db.delete_table('geo_subwaystation')

        # Deleting model 'SubwayLine'
        db.delete_table('geo_subwayline')

        # Deleting model 'SubwayStop'
        db.delete_table('geo_subwaystop')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'geo.subwaystation': {
            'Meta': {'object_name': 'SubwayStation'},
            'geojson': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['geo.SubwayLine']", 'through': "orm['geo.SubwayStop']", 'symmetrical': 'False'}),
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