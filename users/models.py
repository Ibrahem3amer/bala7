#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from cms.validators import GeneralCMSValidator

import re


class SVProfile(models.Model):
    # Attributes
    name = models.CharField(max_length=200, validators=[GeneralCMSValidator.name_validator])
    desc = models.TextField()
    logo = models.ImageField(default='doctor.jpg')

    def __str__(self):
        return self.name


class Entity(models.Model):
    # Helpers
    type_choices = [(1, 'عام'), (2, 'خاص'), (3, 'أهلي')]
    study_choices = [(1, 'فصول دراسية'), (2, 'ساعات معتمدة'), (3, 'غير ذلك')]

    # Attributes
    name = models.CharField(max_length=100, default='no name')
    bio = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    rank = models.PositiveIntegerField(default=0)
    entity_type = models.PositiveIntegerField(choices=type_choices, default=1)
    study_type = models.PositiveIntegerField(choices=study_choices, default=1)
    slug = models.CharField(max_length=10, default='')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class University(Entity):
    headmaster = models.ForeignKey(
        'cms.Professor',
        related_name='managed_universities',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


class Faculty(Entity):
    # Attributes
    university = models.ForeignKey(
        University,
        related_name='faculties',
        on_delete=models.CASCADE,
        null=True
    )
    headmaster = models.ForeignKey(
        'cms.Professor',
        related_name='managed_faculties',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.university.name + ' - ' + self.name


class Department(Entity):
    # Attributes
    faculty = models.ForeignKey(
        Faculty,
        related_name='departments',
        on_delete=models.CASCADE,
        null=True,
    )
    team = models.ForeignKey(
        SVProfile,
        related_name='departments',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.faculty.university.name + ' - ' + self.faculty.name + ' - ' + self.name


class UserProfile(models.Model):
    # Helpers
    gender_choices = [(1, 'ذكر'), (2, 'أنثى'), (3, 'غير ذلك')]
    status_choices = [(1, 'ناجح'), (2, 'راسب'), (3, 'ناجح بمواد'), (4, 'تحشسن مجموع')]

    # Attributes
    level = models.IntegerField(default=1)
    gender = models.PositiveIntegerField(choices=gender_choices, default=3)
    count_of_posts = models.IntegerField(default=0)
    count_of_replies = models.IntegerField(default=0)
    academic_stats = models.PositiveIntegerField(choices=status_choices, default=1)
    last_active_device = models.CharField(max_length=200)
    section = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
        null=True
    )
    department = models.ForeignKey(
        Department,
        related_name='depart_users',
        on_delete=models.SET_NULL,
        null=True
    )
    faculty = models.ForeignKey(
        Faculty,
        related_name='fac_users',
        on_delete=models.SET_NULL,
        null=True
    )
    university = models.ForeignKey(
        University,
        related_name='uni_users',
        on_delete=models.SET_NULL,
        null=True
    )
    topics = models.ManyToManyField(
        'cms.Topic'
    )

    @classmethod
    def make_form_new_profile(cls, user_obj, department=None, faculty=None, university=None):
        """
        Accepts user object and creates his corresponding profile due to his form data. Returns error if existing.

        >>>make_form_new_profile(user, department)
        <UserProfile object>

        >>>make_form_new_profile()
        Error: expected two paramater

        >>>make_form_new_profile(user)
        <UserProfile object> with department = null

        >>>make_form_new_profile(existing_user)
        Error: Existing profile
        """
        user_profile = UserProfile.objects.create(department=department, faculty=faculty, university=university)
        if not UserProfile.link_profile_to_user(user_obj, user_profile):
            # Existing profile.
            user_profile = user_obj.profile
        user_profile.save()
        # Update user's default topics.
        cls.set_default_topics(user_profile)
        return user_profile

    @classmethod
    def set_default_topics(cls, user_profile):
        """
        Assigns all of profile's department topics to user.
        :param user_profile: A UserProfile instance.
        :return: Void.
        """
        try:
            topics = user_profile.department.topics.all()
            for topic in topics:
                user_profile.topics.add(topic)
        except Department.DoesNotExist:
            # No UserProfile was added.
            pass
        except AttributeError:
            pass



    @classmethod
    def link_profile_to_user(cls, user_obj, profile_obj):
        """(user, profile) -> Boolean

        Accepts User object and profile object and link them together. Returns false if no profile object or error.

        >>>link_profile_to_user(user, profile)
        True
        >>>link_profile_to_user(user)
        Error, expected 2 paramaters.
        >>>link_profile_to_user(user, profile=none)
        False
        >>>link_profile_to_user(existing_linked_user, profile)
        False
        """

        # Missed parameter
        if profile_obj is None:
            return False

        user_obj.profile = profile_obj
        user_obj.save()
        return True

    @classmethod
    def validate_name(cls, new_username):
        """
        Takes new user name and validates it against emptiness or exsiting.

        >>>validate_name(blank_username)
        False
        >>>validate_name(vaild_username)
        True
        >>>validate_name(existing_username)
        False
        """
        if not new_username or new_username in ['', ' ']:
            return False
        if User.objects.filter(username=new_username).exists():
            return False
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9]*[._-]?[a-zA-Z0-9]+$', new_username):
            return False

        return True

    @classmethod
    def change_username(cls, new_username, user_obj):
        """
        Takes a validated new username and assigns it to the user.
        """
        user_obj.username = new_username
        user_obj.save()
        return True

    @classmethod
    def validate_mail(cls, new_email, new_email_confirmation, api=False):
        """
        Takes new usermail and its confirmation and validates them.

        >>>validate_mail(email, unmatched_confirm)
        False
        >>>validate_mail(email, confirm)
        True
        >>>validate_mail(existing_email, confirm)
        False
        >>>validate_mail(unvalid_email, confirm)
        False
        """
        if not api and new_email != new_email_confirmation:
            return False
        if User.objects.filter(email=new_email).exists():
            return False
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", new_email):
            return False

        # Valid email
        return True

    @classmethod
    def change_mail(cls, new_email, user_obj):
        """
        Takes a validated email and user and changes the latter's
        """
        user_obj.email = new_email
        user_obj.save()

        return

    @classmethod
    def validate_new_password(cls, old_password, new_password, new_password_confirmation, user_obj):
        """
        Takes old, new userpassword and its confirmation, hashes and validates them.

        >>>validate_mail(right_old, new, confirm)
        True
        >>>validate_mail(wrong_old, new, confirm)
        False
        >>>validate_mail(right_old, new, unmatched)
        False
        >>>validate_mail(right_old, invalid_new, confirm)
        False
        """

        if not check_password(old_password, user_obj.password):
            return False
        else:
            if new_password != new_password_confirmation:
                return False
            try:
                validate_password(new_password)
            except ValidationError:
                return False

        # Valid password
        return True

    @classmethod
    def change_password(cls, new_password, user_obj):
        """
        Takes a validated email and user and changes the latter's
        """
        user_obj.set_password(new_password)
        user_obj.save()

        return

    @classmethod
    def update_education_info(cls, info, user_obj):
        """
        Takes a dict that contains new university, faculty and department ids. validates them and change them in user.

        >>>update_education_info(info, user)
        True
        >>>update_education_info(non-existing_info, user)
        False
        """
        try:
            new_univeristy = University.objects.get(id=info['new_university_id'])
            new_faculty = Faculty.objects.get(id=info['new_faculty_id'])
            new_dep = Department.objects.get(id=info['new_department_id'])
        except ObjectDoesNotExist:
            return False

        UserProfile.objects.filter(user=user_obj).update(
            university=new_univeristy,
            faculty=new_faculty,
            department=new_dep,
            section=int(info['new_section_number'])
        )
        user_obj.profile.topics.clear()
        for topic in new_dep.topics.all():
            user_obj.profile.topics.add(topic)

        return True

    def __str__(self):
        return self.user.username


class ContactUs(models.Model):
    # Attributes
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

# Pipeline customization method to complete user profile. 
# I mdae it oustide of class so that it can be valid package path --> users.models."Function_name"
# not "class_name"
def make_social_new_profile(strategy, backend, user, response, *args, **kwargs):
    """ Customize the python_social_auth pipeline flow by saving user profile."""

    # Already existing user.
    if UserProfile.objects.filter(user=user).exists():
        return

    first_form_data = strategy.session_get('first_form_data')
    try:
        department = Department.objects.get(pk=int(first_form_data['department']))
        faculty = Faculty.objects.get(pk=int(first_form_data['faculty']))
        university = University.objects.get(pk=int(first_form_data['university']))
    except (ObjectDoesNotExist, KeyError):
        UserProfile.objects.create(user=user)
        return

    # create complete profile, default behaviour that adds all department's topics.
    user_profile = UserProfile.objects.create(
        user=user,
        department=department,
        faculty=faculty,
        university=university,
    )
    try:
        from cms.models import Topic
        user_profile.topics = Topic.objects.filter(department=department).all()
        user_profile.save()
    except ImportError:
        pass


# Creating authtication tokens for users.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
