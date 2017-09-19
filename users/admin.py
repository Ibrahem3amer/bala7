from django.contrib import admin
from users.models import University, Faculty, Department, UserProfile, SVProfile

# Register your models here.
class UniversityAdmin(admin.ModelAdmin):
    pass

class FacultyAdmin(admin.ModelAdmin):
    pass

class DepartmentAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass

class SVProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(University, UniversityAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(SVProfile, SVProfileAdmin)