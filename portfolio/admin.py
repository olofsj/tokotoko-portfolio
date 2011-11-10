from django.contrib import admin
from portfolio.models import *

class ProjectImageInline(admin.StackedInline):
    model = ProjectImage
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline', 'category', 'featured', 'site_link')
    search_fields = ('name', 'tagline', 'short_description', 'description',
            'category__name')
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        ProjectImageInline,
    ]
    exclude = ('rendered_description',)

    def site_link(self, obj):
        return '<a href="%s">View on site</a>' % obj.get_absolute_url()
    site_link.allow_tags = True

    def set_featured(self, request, queryset):
        queryset.update(featured=True)
    set_featured.short_description = 'Mark selected projects as featured'

    def remove_featured(self, request, queryset):
        queryset.update(featured=False)
    remove_featured.short_description = 'Mark selected projects as not featured'

    actions = [set_featured, remove_featured]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_count', 'projects', 'site_link')
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def project_count(self, obj):
        return str(obj.project_set.count())
    project_count.short_description = 'Projects'

    def projects(self, obj):
        return '<a href="../project/?category=%d">View projects</a>' % obj.id
    projects.short_description = 'View Projects'
    projects.allow_tags = True

    def site_link(self, obj):
        return '<a href="%s">View on site</a>' % obj.get_absolute_url()
    site_link.allow_tags = True


admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
