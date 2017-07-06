from django.contrib import admin
from cms.models import Topic, Material

# Register your models here.
class TopicAdmin(admin.ModelAdmin):
    pass

class MaterialAdmin(admin.ModelAdmin):
    pass

admin.site.register(Topic, TopicAdmin)
admin.site.register(Material, TopicAdmin)
