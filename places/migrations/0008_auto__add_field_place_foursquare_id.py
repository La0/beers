# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Place.foursquare_id'
        db.add_column('places_place', 'foursquare_id',
                      self.gf('django.db.models.fields.CharField')(max_length=24, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Place.foursquare_id'
        db.delete_column('places_place', 'foursquare_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'badges.badge': {
            'Meta': {'object_name': 'Badge'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'badges.placebadge': {
            'Meta': {'unique_together': "(('place', 'badge'),)", 'object_name': 'PlaceBadge'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': "orm['badges.Badge']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Place']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'geo.city': {
            'Meta': {'object_name': 'City'},
            'geojson': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
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
        },
        'places.place': {
            'Meta': {'object_name': 'Place'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'badges': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['badges.Badge']", 'symmetrical': 'False', 'through': "orm['badges.PlaceBadge']", 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': "orm['geo.City']"}),
            'completion': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'foursquare_id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'geojson': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subways': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['geo.SubwayStation']", 'symmetrical': 'False', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'bar'", 'max_length': '10'})
        },
        'places.placehour': {
            'Meta': {'unique_together': "(('place', 'day', 'happy_hour'),)", 'object_name': 'PlaceHour'},
            'day': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'happy_hour': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hours'", 'to': "orm['places.Place']"}),
            'start': ('django.db.models.fields.TimeField', [], {})
        },
        'places.placelink': {
            'Meta': {'unique_together': "(('place', 'url'),)", 'object_name': 'PlaceLink'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['places.Place']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'article'", 'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['places']