from collections import OrderedDict
from django.test import TestCase, tag

from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_registration.models import RegisteredSubject
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED

from ..metadata import CrfMetadataGetter
from ..models import CrfMetadata, RequisitionMetadata
from ..rules import site_metadata_rules
from .metadata_rules import register_to_site_reference_configs
from .models import Enrollment, SubjectVisit
from .visit_schedule import visit_schedule


class TestMetadataGetter(TestCase):

    def setUp(self):
        register_to_site_reference_configs()
        site_metadata_rules.registry = OrderedDict()

        site_visit_schedules._registry = {}
        site_visit_schedules.loaded = False
        site_visit_schedules.register(visit_schedule)
        self.schedule = site_visit_schedules.get_schedule(
            visit_schedule_name='visit_schedule',
            schedule_name='schedule')
        self.subject_identifier = '1111111'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier)
        self.assertEqual(CrfMetadata.objects.all().count(), 0)
        self.assertEqual(RequisitionMetadata.objects.all().count(), 0)
        Enrollment.objects.create(subject_identifier=self.subject_identifier)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            visit_code=self.schedule.visits.first.code)
        self.subject_visit = SubjectVisit.objects.create(
            appointment=self.appointment,
            subject_identifier=self.subject_identifier,
            reason=SCHEDULED)

    def test_objects_none_no_appointment(self):
        subject_identifier = None
        visit_code = None
        getter = CrfMetadataGetter(
            subject_identifier=subject_identifier,
            visit_code=visit_code)
        self.assertEqual(getter.metadata_objects.count(), 0)

    def test_objects_none_no_visit_with_appointment(self):
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='BLAH')
        getter = CrfMetadataGetter(
            appointment=appointment)
        self.assertEqual(getter.metadata_objects.count(), 0)

    def test_objects_not_none_without_appointment(self):
        getter = CrfMetadataGetter(
            subject_identifier=self.subject_identifier,
            visit_code=self.appointment.visit_code)
        self.assertGreater(getter.metadata_objects.count(), 0)

    def test_objects_not_none_from_appointment(self):
        getter = CrfMetadataGetter(appointment=self.appointment)
        self.assertGreater(getter.metadata_objects.count(), 0)