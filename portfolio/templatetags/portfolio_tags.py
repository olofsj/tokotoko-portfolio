from django import template
from django.core.cache import cache
from django.core.urlresolvers import resolve, reverse, Resolver404
from portfolio.models import Project, Category

register = template.Library()


class GetFeaturedProjectsNode(template.Node):
    """
    Retrieves all features projects
    """
    def __init__(self, varname):
        self.varname = varname.strip()

    def render(self, context):
        projects = Project.objects.filter(featured=True).select_related()
        context[self.varname] = projects
        return ''

@register.tag
def get_featured_projects(parser, token):
    """
    Retrieves a list of featured Project objects for use in a template.
    """

    try:
        tag_name, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('get_featured_projects requires exactly one argument')

    # determine what parameters to use
    return GetFeaturedProjectsNode(varname=varname)


class GetCategoriesNode(template.Node):
    """
    Retrieves all categories
    """
    def __init__(self, varname):
        self.varname = varname.strip()

    def render(self, context):
        categories = Category.objects.all()
        context[self.varname] = categories
        return ''

@register.tag
def get_categories(parser, token):
    """
    Retrieves a list of Category objects for use in a template.
    """

    try:
        tag_name, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('get_featured_projects requires exactly one argument')

    # determine what parameters to use
    return GetCategoriesNode(varname=varname)

@register.simple_tag
def selected(request, pattern):
    """
    Outputs selected if the request path matches pattern
    where pattern can be an absolute url or a named url.
    """
    if pattern.startswith('/'):
        if request.path == pattern:
            return 'selected'
    else:
        if request.path == reverse(pattern):
            return 'selected'

    return ''

