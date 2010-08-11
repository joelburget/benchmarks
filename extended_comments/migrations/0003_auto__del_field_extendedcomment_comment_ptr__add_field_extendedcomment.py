# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ExtendedComment.comment_ptr'
        db.delete_column('extended_comments_extendedcomment', 'comment_ptr_id')

        # Adding field 'ExtendedComment.id'
        db.add_column('extended_comments_extendedcomment', 'id', self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True), keep_default=False)

        # Adding field 'ExtendedComment.content_type'
        db.add_column('extended_comments_extendedcomment', 'content_type', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='content_type_set_for_extendedcomment', to=orm['contenttypes.ContentType']), keep_default=False)

        # Adding field 'ExtendedComment.object_pk'
        db.add_column('extended_comments_extendedcomment', 'object_pk', self.gf('django.db.models.fields.TextField')(default=0), keep_default=False)

        # Adding field 'ExtendedComment.site'
        db.add_column('extended_comments_extendedcomment', 'site', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['sites.Site']), keep_default=False)

        # Adding field 'ExtendedComment.user'
        db.add_column('extended_comments_extendedcomment', 'user', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User']), keep_default=False)

        # Adding field 'ExtendedComment.published'
        db.add_column('extended_comments_extendedcomment', 'published', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=0, blank=True), keep_default=False)

        # Adding field 'ExtendedComment.comment'
        db.add_column('extended_comments_extendedcomment', 'comment', self.gf('django.db.models.fields.TextField')(default=0, max_length=3000), keep_default=False)

        # Changing field 'ExtendedComment.file'
        db.alter_column('extended_comments_extendedcomment', 'file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True))


    def backwards(self, orm):
        
        # We cannot add back in field 'ExtendedComment.comment_ptr'
        raise RuntimeError(
            "Cannot reverse this migration. 'ExtendedComment.comment_ptr' and its values cannot be restored.")

        # Deleting field 'ExtendedComment.id'
        db.delete_column('extended_comments_extendedcomment', 'id')

        # Deleting field 'ExtendedComment.content_type'
        db.delete_column('extended_comments_extendedcomment', 'content_type_id')

        # Deleting field 'ExtendedComment.object_pk'
        db.delete_column('extended_comments_extendedcomment', 'object_pk')

        # Deleting field 'ExtendedComment.site'
        db.delete_column('extended_comments_extendedcomment', 'site_id')

        # Deleting field 'ExtendedComment.user'
        db.delete_column('extended_comments_extendedcomment', 'user_id')

        # Deleting field 'ExtendedComment.published'
        db.delete_column('extended_comments_extendedcomment', 'published')

        # Deleting field 'ExtendedComment.comment'
        db.delete_column('extended_comments_extendedcomment', 'comment')

        # Changing field 'ExtendedComment.file'
        db.alter_column('extended_comments_extendedcomment', 'file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))


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
        'extended_comments.extendedcomment': {
            'Meta': {'object_name': 'ExtendedComment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_extendedcomment'", 'to': "orm['contenttypes.ContentType']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'published': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['extended_comments']
