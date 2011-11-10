from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic import DetailView, ListView
from models import *

urlpatterns = patterns('djangosite.portfolio.views',
    url(r'^$', ListView.as_view(model=Category),
        name='portfolio'),
    url(r'^categories/(?P<slug>[-\w]+)/$',
        DetailView.as_view(model=Category),
        name='portfolio_category'),
    url(r'^project/(?P<slug>[-\w]+)/$',
        DetailView.as_view(model=Project),
        name='portfolio_project'),
)
