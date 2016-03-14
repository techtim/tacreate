from __future__ import unicode_literals
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Count, Q

from mezzanine.generic.models import Keyword
from mezzanine import template

from ta.models import Project, ProjectCategory

User = get_user_model()

register = template.Library()


@register.as_tag
def project_months(*args):
    """
    Put a list of dates for blog posts into the template context.
    """
    dates = Project.objects.published().values_list("publish_date", flat=True)
    date_dicts = [{"date": datetime(d.year, d.month, 1)} for d in dates]
    month_dicts = []
    for date_dict in date_dicts:
        if date_dict not in month_dicts:
            month_dicts.append(date_dict)
    for i, date_dict in enumerate(month_dicts):
        month_dicts[i]["project_count"] = date_dicts.count(date_dict)
    return month_dicts


@register.as_tag
def project_categories(*args):
    """
    Put a list of categories for blog posts into the template context.
    """
    project_posts = Project.objects.published()
    categories = ProjectCategory.objects.filter(projects__in=project_posts)
    return list(categories.annotate(project_count=Count("projects")))


@register.as_tag
def project_authors(*args):
    """
    Put a list of authors (users) for blog posts into the template context.
    """
    project_posts = Project.objects.published()
    authors = User.objects.filter(projects__in=project_posts)
    return list(authors.annotate(project_count=Count("projects")))


@register.as_tag
def project_recent_posts(limit=5, tag=None, username=None, category=None):
    """
    Put a list of recently published blog posts into the template
    context. A tag title or slug, category title or slug or author's
    username can also be specified to filter the recent posts returned.

    Usage::

        {% project_recent_posts 5 as recent_posts %}
        {% project_recent_posts limit=5 tag="django" as recent_posts %}
        {% project_recent_posts limit=5 category="python" as recent_posts %}
        {% project_recent_posts 5 username=admin as recent_posts %}

    """
    project_posts = Project.objects.published().select_related("user")
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
    if tag is not None:
        try:
            tag = Keyword.objects.get(title_or_slug(tag))
            project_posts = project_posts.filter(keywords__keyword=tag)
        except Keyword.DoesNotExist:
            return []
    if category is not None:
        try:
            category = ProjectCategory.objects.get(title_or_slug(category))
            project_posts = project_posts.filter(categories=category)
        except ProjectCategory.DoesNotExist:
            return []
    if username is not None:
        try:
            author = User.objects.get(username=username)
            project_posts = project_posts.filter(user=author)
        except User.DoesNotExist:
            return []
    return list(project_posts[:limit])


# @register.inclusion_tag("admin/includes/quick_blog.html", takes_context=True)
# def quick_blog(context):
#     """
#     Admin dashboard tag for the quick blog form.
#     """
#     context["form"] = BlogPostForm()
#     return context
