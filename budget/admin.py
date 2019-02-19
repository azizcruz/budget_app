from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Project, Category, Expense
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    """ Here we costumize the project admin page """
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)
admin.site.register(Expense)
