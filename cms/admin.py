import json
from django.contrib import admin
from django.contrib.auth.models import User
from users.models import Department, Faculty, University
from cms.models import Topic, Material, Task, Professor, TopicTable, Exam, UserPost, UserComment, Event
from cms.custom_admin_forms import SupervisiorMaterialForm, SupervisiorTaskForm


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

    form = SupervisiorMaterialForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Assigns default value for User field. limits Topics field to user's topics."""
        if db_field.name == "user":
            kwargs["queryset"]  = User.objects.filter(id = request.user.id)
            kwargs["initial"]   = request.user.id
        elif db_field.name == "topic" and not request.user.is_superuser:
            kwargs["queryset"]  = Topic.objects.filter(id__in = request.user.profile.topics.all())

        return super(MaterialAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Limits the choices of professors for the limit of user."""

        if db_field.name == "professor" and not request.user.is_superuser:
            kwargs["queryset"]  = Professor.objects.filter(faculty_id=request.user.profile.faculty.id)
        
        return super(MaterialAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)      
    
    def get_queryset(self, request):
        """
        Returns materials that lays in SV scope in case of staff, returns all materials otherwise. 
        """
        qs = super(MaterialAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(content_type__lt = 3)
        return qs.filter(topic_id__in = request.user.profile.topics.all(), content_type__lt = 3)

class ExamAdmin(admin.ModelAdmin):

    exclude = ('content_type', 'term', 'week_number')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Assigns default value for User field. limits Topics field to user's topics. 
        """
        if db_field.name == "user":
            kwargs["queryset"]  = User.objects.filter(id = request.user.id)
            kwargs["initial"]   = request.user.id
        elif db_field.name == "topic" and not request.user.is_superuser:
            kwargs["queryset"]  = Topic.objects.filter(id__in = request.user.profile.topics.all())

        return super(ExamAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Limits the choices of professors for the limit of user."""
        if db_field.name == "professor" and not request.user.is_superuser:
            kwargs["queryset"]  = Professor.objects.filter(faculty_id=request.user.profile.faculty.id)
        
        return super(ExamAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)        

    def get_queryset(self, request):
        """
        Returns materials that lays in SV scope in case of staff, returns all materials otherwise. 
        """
        qs = super(ExamAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(content_type__lt = 3)
        return qs.filter(topic_id__in = request.user.profile.topics.all(), content_type__lt = 3)


class TaskAdmin(admin.ModelAdmin):

    form = SupervisiorTaskForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Assigns default value for User field. limits Topics field to user's topics."""
        if db_field.name == "user":
            kwargs["queryset"]  = User.objects.filter(id = request.user.id)
            kwargs["initial"]   = request.user.id
        elif db_field.name == "topic" and not request.user.is_superuser:
            kwargs["queryset"]  = Topic.objects.filter(id__in = request.user.profile.topics.all())

        return super(TaskAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Limits the choices of professors for the limit of user."""
        if db_field.name == "professor" and not request.user.is_superuser:
            kwargs["queryset"]  = Professor.objects.filter(faculty_id=request.user.profile.faculty.id)
        
        return super(TaskAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)       

    def get_queryset(self, request):
        """
        Returns tasks that lays in SV scope in case of staff, returns all tasks otherwise. 
        """
        qs = super(TaskAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter()
        return qs.filter(topic_id__in = request.user.profile.topics.all())


class EventAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ limits department to user's departments."""
        if db_field.name == 'dep':
            if not request.user.is_superuser:
                kwargs["queryset"] = Department.objects.filter(id=request.user.profile.department.id)
            else:
                kwargs["queryset"] = Department.objects.all()
        elif db_field.name == 'faculty' and request.user.is_superuser:
            kwargs["queryset"] = Faculty.objects.all()
        elif db_field.name == 'university' and request.user.is_superuser:
            kwargs["queryset"] = University.objects.all()
        
        return super(EventAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        """ Returns events that lays in SV scope in case of staff, returns all events otherwise."""
        qs = super(EventAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(dep=request.user.profile.department)

    def get_form(self, request, obj=None, **kwargs):
        """ Hides all_app label from staff."""
        if not request.user.is_superuser:
            self.exclude = ('all_app', 'faculty', 'university')
        return super(EventAdmin, self).get_form(request, obj, **kwargs)


class ProfessorAdmin(admin.ModelAdmin):
    pass


class TopicTableAdmin(admin.ModelAdmin):
    
    fields = ['topic']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """limits Topics field to user's topics."""
        if db_field.name == "topic" and not request.user.is_superuser:
            kwargs["queryset"]  = Topic.objects.filter(id__in = request.user.profile.topics.all())

        return super(TopicTableAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Overrides the change view that displays change_form.html"""
        
        # Grapping table that matches topic_id.
        topic = TopicTable.objects.get(id=object_id)

        # Generating off-days list on-fly for template.
        off_days = [ day for day in topic.off_days ]

        # Attaching table topics and places as extra context. 
        extra_context = extra_context or {}
        extra_context['topics_table'] = topic.to_list(topic.topics)
        extra_context['places_table'] = topic.to_list(topic.places)
        extra_context['off_days'] = topic.to_list(topic.off_days)

        return super(TopicTableAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def save_model(self, request, obj, form, change):
        """Adds sv inputs to table instance."""

        # Populating data from request input.
        request_topics =  [[0]*6 for i in range(7)]
        request_places =  [[0]*6 for i in range(7)]
        for day in range(7):
            day_index = '_'+str(day)
            for peroid in range(6):
                period_index = '_'+str(peroid)
                request_topics[day][peroid] = request.POST['topic'+day_index+period_index]
                request_places[day][peroid] = request.POST['place'+day_index+period_index]
        off_days = request.POST.getlist('off_days[]', None)
        
        # Save data to table instance.
        obj.topics = request_topics
        obj.places = request_places
        obj.off_days = off_days

        super(TopicTableAdmin, self).save_model(request, obj, form, change)


class UserPostAdmin(admin.ModelAdmin):
    pass


class UserCommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicTable, TopicTableAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(UserPost, UserPostAdmin)
admin.site.register(UserComment, UserCommentAdmin)
admin.site.register(Event, EventAdmin)