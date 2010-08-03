# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'UserProfile.commentsSubscribe'
        db.add_column('users_userprofile', 'commentsSubscribe', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.ownpostsSubscribe'
        db.add_column('users_userprofile', 'ownpostsSubscribe', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.groupPostsSubscribe'
        db.add_column('users_userprofile', 'groupPostsSubscribe', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.allProblemsSubscribe'
        db.add_column('users_userprofile', 'allProblemsSubscribe', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Changing field 'UserProfile.bio'
        db.alter_column('users_userprofile', 'bio', self.gf('django.db.models.fields.CharField')(max_length=500))


    def backwards(self, orm):
        
        # Deleting field 'UserProfile.commentsSubscribe'
        db.delete_column('users_userprofile', 'commentsSubscribe')

        # Deleting field 'UserProfile.ownpostsSubscribe'
        db.delete_column('users_userprofile', 'ownpostsSubscribe')

        # Deleting field 'UserProfile.groupPostsSubscribe'
        db.delete_column('users_userprofile', 'groupPostsSubscribe')

        # Deleting field 'UserProfile.allProblemsSubscribe'
        db.delete_column('users_userprofile', 'allProblemsSubscribe')

        # Changing field 'UserProfile.bio'
        db.alter_column('users_userprofile', 'bio', self.gf('django.db.models.fields.CharField')(max_length=200))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'allProblemsSubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'commentsSubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'groupPostsSubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ownpostsSubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'showemail': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['users']
