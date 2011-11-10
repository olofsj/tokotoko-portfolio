from haystack.indexes import *
from haystack import site
from models import Project


class ProjectIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    rendered = CharField(use_template=True, indexed=False)


site.register(Project, ProjectIndex)

