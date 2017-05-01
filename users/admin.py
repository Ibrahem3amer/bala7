from django.contrib import admin
from users.models import University, Faculty, Department

# Register your models here.
class UniversityAdmin(admin.ModelAdmin):
    pass

class FacultyAdmin(admin.ModelAdmin):
    pass

class DepartmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(University, UniversityAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department, DepartmentAdmin)