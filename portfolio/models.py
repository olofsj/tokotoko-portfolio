from django.db import models
from django.contrib.markup.templatetags import markup

MARKUP_MARKDOWN = 'm'
MARKUP_HTML = 'h'
MARKUP_REST = 'r'
MARKUP_TEXTILE = 't'
MARKUP_OPTIONS = (
        (MARKUP_HTML, 'HTML/Plain Text'),
        (MARKUP_MARKDOWN, 'Markdown'),
        (MARKUP_REST, 'ReStructured Text'),
        (MARKUP_TEXTILE, 'Textile'),
    )
MARKUP_DEFAULT = 'm'
MARKUP_HELP = """Select the type of markup you are using for the description.
<ul>
<li><a href="http://daringfireball.net/projects/markdown/basics" target="_blank">Markdown Guide</a></li>
<li><a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target="_blank">ReStructured Text Guide</a></li>
<li><a href="http://thresholdstate.com/articles/4312/the-textile-reference-manual" target="_blank">Textile Guide</a></li>
</ul>"""


class Project(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    short_description = models.TextField()
    markup = models.CharField(max_length=1, choices=MARKUP_OPTIONS, default=MARKUP_DEFAULT, help_text=MARKUP_HELP)
    description = models.TextField()
    rendered_description = models.TextField()
    tagline = models.CharField(max_length=400)
    client = models.CharField(max_length=200, blank=True)
    site_url = models.URLField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    category = models.ForeignKey('Category')
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date', '-end_date', ]

    def save(self, *args, **kwargs):
        """Renders the description using the appropriate markup language."""
        self.render_markup()

        super(Project, self).save(*args, **kwargs)

    def render_markup(self):
        """Turns any markup into HTML"""

        original = self.rendered_description
        if self.markup == MARKUP_MARKDOWN:
            self.rendered_description = markup.markdown(self.description)
        else:
            self.rendered_description = self.description

        return (self.rendered_description != original)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('portfolio_project', (), {'slug': str(self.slug), })


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    position = models.PositiveIntegerField()
    short_description = models.TextField(default='')
    description = models.TextField(default='')

    class Meta:
        ordering = ["position"]
        verbose_name_plural = "categories"

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('portfolio_category', (), {'slug': str(self.slug), })


class ProjectImage(models.Model):
    project = models.ForeignKey('Project')
    image = models.ImageField(upload_to="project_image/%Y/%m/%d")

    def __unicode__(self):
        return self.image.name

    def get_absolute_url(self):
        return self.image.url
