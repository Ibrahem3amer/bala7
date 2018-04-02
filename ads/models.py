from datetime import timedelta

from django.db import models
from django.utils.timezone import now


class BasicAd(models.Model):
    """
    A model that represents a base ad that can be displayed anywhere.
    """

    # Attributes
    name = models.CharField(max_length=220)
    image = models.ImageField(upload_to='ads/basic_ads')
    linked_url = models.URLField(null=True, blank=True)
    department = models.ForeignKey(
        to='users.Department',
        related_name='basic_ads',
        on_delete=models.CASCADE
    )
    section = models.PositiveSmallIntegerField(null=True, blank=True)
    life_time = models.PositiveSmallIntegerField(
        verbose_name='Ad Lifetime',
        help_text='Indicates the time (in days) ad should live before being disabled.'
    )
    start_date = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)
    termination_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    advertiser = models.ForeignKey(
        to='ads.Advertiser',
        related_name='basic_ads',
        on_delete=models.CASCADE
    )

    # Methods
    def activate_ad(self):
        """
        Activates the add and set the deadline to the termination date.
        :return: Void
        """
        self.start_date = now()
        self.termination_date = self.start_date + timedelta(self.life_time)
        self.is_active = True
        self.save()

    def deactivate_ad(self):
        """
        Deactivates a current ad and sets the termination date.
        :return: Void
        """
        self.termination_date = now()
        self.is_active = False
        self.save()

    def set_ad_lifetime(self, new_lifetime):
        """
        Sets new deadline to a current ad.
        :param new_lifetime: A positive integer that represents the new lifetime of the add.
        :return: Void
        """
        self.life_time = new_lifetime
        self.termination_date = self.start_date + timedelta(new_lifetime)
        self.save()

class Advertiser(models.Model):
    """
    A model that represents the advertiser info.
    """

    # Attributes
    name = models.CharField(max_length=220)
    website = models.URLField(null=True, blank=True)



