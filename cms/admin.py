from django.contrib import admin
from django.contrib.auth.models import User
from cms.models import Topic, Material, Task, Professor, TopicTable


class TopicAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        """
        Returns topics that lays in SV scope in case of staff, returns all topics otherwise. 
        """
        qs = super(TopicAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id__in = request.user.profile.topics.all())


class MaterialAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Assigns default value for User field. limits Topics field to user's topics. 
        """
        if db_field.name == "user":
            kwargs["queryset"]  = User.objects.filter(id = request.user.id)
            kwargs["initial"]   = request.user.id
        elif db_field.name == "topic" and not request.user.is_superuser:
            kwargs["queryset"]  = Topic.objects.filter(id__in = request.user.profile.topics.all())

        return super(MaterialAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    
    def get_queryset(self, request):
        """
        Returns materials that lays in SV scope in case of staff, returns all materials otherwise. 
        """
        qs = super(MaterialAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(content_type__lt = 3)
        return qs.filter(topic_id__in = request.user.profile.topics.all(), content_type__lt = 3)


class TaskAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        """
        Returns tasks that lays in SV scope in case of staff, returns all tasks otherwise. 
        """
        qs = super(TaskAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter()
        return qs.filter(topic_id__in = request.user.profile.topics.all())


class ProfessorAdmin(admin.ModelAdmin):
    pass


class TopicTableAdmin(admin.ModelAdmin):
    exclude = ('json',)


admin.site.register(Topic, TopicAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(TopicTable, TopicTableAdmin)