from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
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
