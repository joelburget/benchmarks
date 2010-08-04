# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'UserProfile.ownpostsSubscribe'
        db.delete_column('users_userprofile', 'ownpostsSubscribe')

        # Deleting field 'UserProfile.groupPostsSubscribe'
        db.delete_column('users_userprofile', 'groupPostsSubscribe')

        # Deleting field 'UserProfile.allProblemsSubscribe'
        db.delete_column('users_userprofile', 'allProblemsSubscribe')

        # Deleting field 'UserProfile.commentsSubscribe'
        db.delete_column('users_userprofile', 'commentsSubscribe')

        # Adding field 'UserProfile.commentResponseSubscribe'
        db.add_column('users_userprofile', 'commentResponseSubscribe', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.ownPostCommentSubscribe'
        db.add_column('users_userprofile', 'ownPostCommentSubscribe', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.groupPostSubscribe'
        db.add_column('users_userprofile', 'groupPostSubscribe', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.allProblemSubscribe'
        db.add_column('users_userprofile', 'allProblemSubscribe', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'UserProfile.ownpostsSubscribe'
        db.add_column('users_userprofile', 'ownpostsSubscribe', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.groupPostsSubscribe'
        db.add_column('users_userprofile', 'groupPostsSubscribe', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.allProblemsSubscribe'
        db.add_column('users_userprofile', 'allProblemsSubscribe', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.commentsSubscribe'
        db.add_column('users_userprofile', 'commentsSubscribe', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Deleting field 'UserProfile.commentResponseSubscribe'
        db.delete_column('users_userprofile', 'commentResponseSubscribe')

        # Deleting field 'UserProfile.ownPostCommentSubscribe'
        db.delete_column('users_userprofile', 'ownPostCommentSubscribe')

        # Deleting field 'UserProfile.groupPostSubscribe'
        db.delete_column('users_userprofile', 'groupPostSubscribe')

        # Deleting field 'UserProfile.allProblemSubscribe'
        db.delete_column('users_userprofile', 'allProblemSubscribe')


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
            'allProblemSubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'commentResponseSubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'groupPostSubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ownPostCommentSubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'showemail': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['users']
