from django.contrib import admin
from portfolio.models import *

class ProjectImageInline(admin.StackedInline):
    model = ProjectImage
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline', 'category', 'featured')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        ProjectImageInline,
    ]
    exclude = ('rendered_description',)

    def set_featured(self, request, queryset):
        queryset.update(featured=True)
    set_featured.short_description = 'Mark selected projects as featured'

    def remove_featured(self, request, queryset):
        queryset.update(featured=False)
    remove_featured.short_description = 'Mark selected projects as not featured'

    actions = [set_featured, remove_featured]


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'project_count')

    def project_count(self, obj):
        return str(obj.project_set.count())
    project_count.short_description = 'Projects'


admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
