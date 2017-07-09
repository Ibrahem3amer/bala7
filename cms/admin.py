from django.contrib import admin
from cms.models import Topic, Material, Task

# Register your models here.
class TopicAdmin(admin.ModelAdmin):
    pass

class MaterialAdmin(admin.ModelAdmin):
    pass

class TaskAdmin(admin.ModelAdmin):
    pass

admin.site.register(Topic, TopicAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Task, TaskAdmin)
