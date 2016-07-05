# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 11:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import django_revision.revision_field
import edc_base.model.fields.hostname_modification_field
import edc_base.model.fields.userfield
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('edc_content_type_map', '0002_auto_20160625_0845'),
        ('edc_visit_schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrfEntry',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('entry_order', models.IntegerField()),
                ('group_title', models.CharField(blank=True, help_text='for example, may be used to add to the form title on the change form to group serveral forms', max_length=50, null=True)),
                ('entry_category', models.CharField(choices=[('CLINIC', 'Clinic'), ('LAB', 'Lab'), ('OTHER', 'Other')], db_index=True, default='CLINIC', max_length=25)),
                ('entry_window_calculation', models.CharField(choices=[('VISIT', 'Visit'), ('FORM', 'Form')], default='VISIT', help_text='Base the entry window period on the visit window period or specify a form specific window period', max_length=25)),
                ('default_entry_status', models.CharField(choices=[('NEW', 'New'), ('KEYED', 'Keyed'), ('MISSED', 'Missed'), ('NOT_REQUIRED', 'Not required')], default='NEW', max_length=25)),
                ('additional', models.BooleanField(default=False, help_text='If True lists the entry in additional entries')),
                ('app_label', models.CharField(max_length=50, null=True)),
                ('model_name', models.CharField(max_length=50, null=True)),
                ('content_type_map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='edc_content_type_map.ContentTypeMap', verbose_name='entry form / model')),
                ('visit_definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edc_visit_schedule.VisitDefinition')),
            ],
            options={
                'verbose_name_plural': 'Crf Entries',
                'verbose_name': 'Crf Entry',
                'ordering': ['visit_definition__code', 'entry_order'],
            },
        ),
        migrations.CreateModel(
            name='LabEntry',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('app_label', models.CharField(help_text='requisition_panel app_label', max_length=50, null=True)),
                ('model_name', models.CharField(help_text='requisition_panel model_name', max_length=50, null=True)),
                ('entry_order', models.IntegerField()),
                ('entry_category', models.CharField(choices=[('CLINIC', 'Clinic'), ('LAB', 'Lab'), ('OTHER', 'Other')], default='CLINIC', max_length=25)),
                ('entry_window_calculation', models.CharField(choices=[('VISIT', 'Visit'), ('FORM', 'Form')], default='VISIT', help_text='Base the entry window period on the visit window period or specify a form specific window period', max_length=25)),
                ('default_entry_status', models.CharField(choices=[('NEW', 'New'), ('KEYED', 'Keyed'), ('MISSED', 'Missed'), ('NOT_REQUIRED', 'Not required')], default='NEW', max_length=25)),
                ('additional', models.BooleanField(default=False, help_text='If True lists the lab_entry in additional requisitions')),
            ],
            options={
                'verbose_name_plural': 'Lab Entries',
                'verbose_name': 'Lab Entry',
                'ordering': ['visit_definition__code', 'entry_order'],
            },
        ),
        migrations.CreateModel(
            name='RequisitionPanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('aliquot_type_alpha_code', models.CharField(max_length=4)),
                ('rule_group_name', models.CharField(help_text='reference used on rule groups. Defaults to name.', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='labentry',
            name='requisition_panel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='edc_meta_data.RequisitionPanel'),
        ),
        migrations.AddField(
            model_name='labentry',
            name='visit_definition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edc_visit_schedule.VisitDefinition'),
        ),
        migrations.AlterUniqueTogether(
            name='labentry',
            unique_together=set([('visit_definition', 'requisition_panel')]),
        ),
        migrations.AlterUniqueTogether(
            name='crfentry',
            unique_together=set([('visit_definition', 'content_type_map')]),
        ),
    ]
