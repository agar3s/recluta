# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Company.website'
        db.alter_column(u'empleo_desarrolladores_company', 'website', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Company.image'
        db.alter_column(u'empleo_desarrolladores_company', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))
        # Deleting field 'Offer.offer_company_that_publishes'
        db.delete_column(u'empleo_desarrolladores_offer', 'offer_company_that_publishes')


    def backwards(self, orm):

        # Changing field 'Company.website'
        db.alter_column(u'empleo_desarrolladores_company', 'website', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'Company.image'
        db.alter_column(u'empleo_desarrolladores_company', 'image', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100))
        # Adding field 'Offer.offer_company_that_publishes'
        db.add_column(u'empleo_desarrolladores_offer', 'offer_company_that_publishes',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'empleo_desarrolladores.applicant': {
            'Meta': {'object_name': 'Applicant'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mail': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'})
        },
        u'empleo_desarrolladores.company': {
            'Meta': {'object_name': 'Company'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nit': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'offers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['empleo_desarrolladores.Offer']", 'symmetrical': 'False'}),
            'phone': ('django.db.models.fields.IntegerField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'empleo_desarrolladores.offer': {
            'Meta': {'object_name': 'Offer'},
            'applicants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['empleo_desarrolladores.Applicant']", 'through': u"orm['empleo_desarrolladores.OfferApplicant']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_description': ('django.db.models.fields.TextField', [], {}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'Bogota'", 'max_length': '100', 'null': 'True'}),
            'mandatory_skills': ('django.db.models.fields.TextField', [], {}),
            'offer_valid_time': ('django.db.models.fields.DateTimeField', [], {}),
            'optional_skills': ('django.db.models.fields.TextField', [], {}),
            'salary': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'type_contract': ('django.db.models.fields.CharField', [], {'default': "'TF'", 'max_length': '2'})
        },
        u'empleo_desarrolladores.offerapplicant': {
            'Meta': {'object_name': 'OfferApplicant'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['empleo_desarrolladores.Applicant']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observation': ('django.db.models.fields.TextField', [], {}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['empleo_desarrolladores.Offer']"})
        },
        u'empleo_desarrolladores.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'biography': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['empleo_desarrolladores.Company']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['empleo_desarrolladores']