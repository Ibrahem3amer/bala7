from django.contrib import admin

from .models import BasicAd, Advertiser


@admin.register(BasicAd)
class BasicAdAdmin(admin.ModelAdmin):
    pass


@admin.register(Advertiser)
class AdvertiserAdmin(admin.ModelAdmin):
    pass
