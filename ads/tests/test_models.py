from datetime import datetime, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now

from test_plus import TestCase

from users.models import University, Faculty, Department
from ..models import BasicAd, Advertiser


class BasicAdTest(TestCase):

    def setUp(self):
        self.image = SimpleUploadedFile(name='image', content='ssssssssssssss'.encode('utf-8'))
        self.uni = University.objects.create(name='Test university')
        self.fac = Faculty.objects.create(name='Test faculty', university=self.uni)
        self.dep = Department.objects.create(name='Test dep', faculty=self.fac)

    def test_create_minimal_basic_ad(self):
        """Asserts that a new basic add will be created successfully."""

        # Test setup
        advertiser = Advertiser.objects.create(
            name='test_advertiser',
            website='www.test.com'
        )
        # Test body
        ad = BasicAd.objects.create(
            name='test_ad',
            image=self.image,
            department=self.dep,
            life_time=3,
            start_date=datetime.now(),
            advertiser=advertiser
        )
        # Test assertion
        self.assertEqual(BasicAd.objects.all().count(), 1)

    def test_activate_ad(self):
        """Assert that Ad activation method will handle the process of activation."""

        # Test setup
        advertiser = Advertiser.objects.create(
            name='test_advertiser',
            website='www.test.com'
        )
        ad = BasicAd.objects.create(
            name='test_ad',
            image=self.image,
            department=self.dep,
            life_time=3,
            start_date=datetime.now(),
            advertiser=advertiser
        )
        expected_termination_date = now() + timedelta(ad.life_time)

        # Test body
        ad.activate_ad()

        # Test assertion
        last_created_ad = BasicAd.objects.last()
        self.assertTrue(last_created_ad.is_active)
        self.assertIsNotNone(last_created_ad.termination_date)
        self.assertEqual(last_created_ad.termination_date.date(), expected_termination_date.date())
        self.assertGreaterEqual(last_created_ad.termination_date, last_created_ad.start_date)

    def test_deactivate_ad(self):
        """Assert that Ad deactivation method will disable the ad."""

        # Test setup
        advertiser = Advertiser.objects.create(
            name='test_advertiser',
            website='www.test.com'
        )
        ad = BasicAd.objects.create(
            name='test_ad',
            image=self.image,
            department=self.dep,
            life_time=3,
            start_date=now()-timedelta(3),
            advertiser=advertiser,
            is_active=True,
            termination_date=now()
        )

        # Test body
        ad.deactivate_ad()

        # Test assertion
        last_created_ad = BasicAd.objects.last()
        self.assertFalse(last_created_ad.is_active)
        self.assertEqual(last_created_ad.termination_date.date(), now().date())

    def test_change_ad_lifetime_active_ad(self):
        """Assert that changing ad lifetime will affect its termination date."""

        # Test setup
        advertiser = Advertiser.objects.create(
            name='test_advertiser',
            website='www.test.com'
        )
        ad = BasicAd.objects.create(
            name='test_ad',
            image=self.image,
            department=self.dep,
            life_time=3,
            start_date=datetime.now(),
            advertiser=advertiser,
            is_active=True
        )
        new_lifetime = 7
        expected_termination_date = now() + timedelta(new_lifetime)

        # Test body
        ad.set_ad_lifetime(new_lifetime)

        # Test assertion
        last_created_ad = BasicAd.objects.last()
        self.assertTrue(last_created_ad.is_active)
        self.assertIsNotNone(last_created_ad.termination_date)
        self.assertEqual(last_created_ad.termination_date.date(), expected_termination_date.date())
        self.assertGreaterEqual(last_created_ad.termination_date, last_created_ad.start_date)