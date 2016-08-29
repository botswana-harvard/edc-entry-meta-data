import sys

from django.apps.config import AppConfig as DjangoAppConfig
from django.apps import apps as django_apps

from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, MISSED_VISIT


class AppConfig(DjangoAppConfig):
    name = 'edc_metadata'
    verbose_name = 'Edc Metadata'
    app_label = 'edc_example'
    crf_model_name = 'crfmetadata'
    requisition_model_name = 'requisitionmetadata'
    create_on_reasons = [SCHEDULED, UNSCHEDULED]
    delete_on_reasons = [MISSED_VISIT]
    reason_field = 'reason'

    def ready(self):
        from .signals import metadata_update_on_post_save, metadata_create_on_post_save
        sys.stdout.write('Loading {} ...\n'.format(self.verbose_name))
        if self.app_label == self.name:
            sys.stdout.write('  * using default metadata models from \'{}\'\n'.format(self.app_label))
        else:
            sys.stdout.write('  * using custom metadata models from \'{}\'\n'.format(self.app_label))
        sys.stdout.write(' Done loading {}.\n'.format(self.verbose_name))

    @property
    def crf_model(self):
        """Returns the meta data model used by Crfs."""
        return django_apps.get_model(self.app_label, self.crf_model_name)

    @property
    def requisition_model(self):
        """Returns the meta data model used by Requisitions."""
        return django_apps.get_model(self.app_label, self.requisition_model_name)

    def get_metadata_model(self, category):
        if category == 'crf':
            return self.crf_model
        elif category == 'requisition':
            return self.requisition_model
        return None

    def get_metadata(self, subject_identifier, **options):
        return {
            'crf': self.crf_model.objects.filter(
                subject_identifier=subject_identifier, **options),
            'requisition': self.requisition_model.objects.filter(
                subject_identifier=subject_identifier, **options)}