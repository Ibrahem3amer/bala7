from django.db import models


class BasicAd(models.Model):
    """
    A model that represents a base ad that can be displayed anywhere.
    """

    # Attributes
    name = models.CharField(max_length=220)
    image = models.ImageField(upload_to='ads/basic_ads')
    department = models.ForeignKey(
        to='users.Department',
        related_name='basic_ads',
        on_delete=models.CASCADE
    )
    section = models.PositiveSmallIntegerField(null=True, blank=True)
    life_time = models.PositiveSmallIntegerField(
        verbose_name='Ad Lifetime',
        help_text='Indicates the time ad should live before being disabled.'
    )
    start_date = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    # advertiser = models.ForeignKey(
    #     to='ads.Advertiser',
    #     related_name='basic_ads',
    #     on_delete=models.CASCADE
    # )
