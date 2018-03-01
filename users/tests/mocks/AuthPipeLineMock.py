from django.contrib.auth import get_user_model
from test_plus.test import TestCase
from users.models import University, Faculty, Department


class Pipline_mock(TestCase):

    def __init__(self):
        self.strategy = Stategy()
        self.backend = Backend()
        self.user = self.make_user('pipeline_user')
        super(Pipline_mock, self).__init__()


class Stategy():
    """Mocks the strategy instance of django social auth."""

    def __init__(self):
        self.university = University.objects.create(
            name='pipline_test_university',
        )
        self.faculty = Faculty.objects.create(
            name='pipline_test_faculty',
            university=self.university
        )
        self.department = Department.objects.create(
            name='pipeline_test_department',
            faculty=self.faculty
        )
        self.first_form_data = {
            'university': self.university.pk,
            'faculty': self.faculty.pk,
            'department': self.department.pk
        }
        self.session_get_dict = {
            'first_form_data': self.first_form_data
        }

    def session_get(self, session_variable_name):
        """Simulates the call for the session variable."""
        try:
            return self.session_get_dict[session_variable_name]
        except KeyError:
            return {}


class Backend():
    """Mocks the backend instance in django auth pipeline."""
    pass