from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from mezzanine.pages.models import Page
from mezzanine.utils.views import paginate
from mezzanine.conf import settings


from .models import Project, ProjectCategory
from mezzanine_people.models import Person

def project_list(request, tag=None, year=None, month=None, 
                   category=None, template="project/project_list.html",
                   extra_context=None):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``blog/blog_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    templates = []
    project_posts = Project.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        project_posts = project_posts.filter(keywords__keyword=tag)
    if year is not None:
        project_posts = project_posts.filter(publish_date__year=year)
        if month is not None:
            project_posts = project_posts.filter(publish_date__month=month)
            try:
                month = _(month_name[int(month)])
            except IndexError:
                raise Http404()
    if category is not None:
        category = get_object_or_404(ProjectCategory, slug=category)
        project_posts = project_posts.filter(categories=category)
        templates.append(u"project/project_list_%s.html" %
                          str(category.slug))
    # author = None
    # if username is not None:
    #     author = get_object_or_404(User, username=username)
    #     project_posts = project_posts.filter(user=author)
    #     templates.append(u"project/project_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    project_posts = project_posts.prefetch_related(*prefetch)
    project_posts = paginate(project_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"project_posts": project_posts, "year": year, "month": month,
               "tag": tag, "category": category,}
    context.update(extra_context or {})
    templates.append(template)
    return TemplateResponse(request, templates, context)


def project_detail(request, slug, year=None, month=None, day=None,
                     template="project/project_detail.html",
                     extra_context=None):
    """. Custom templates are checked for using the name
    ``blog/blog_post_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    project_posts = Project.objects.published(
                                     for_user=request.user).select_related()
    project_post = get_object_or_404(project_posts, slug=slug)
    related_projects = project_post.related_projects.published(for_user=request.user)
    context = {"project_post": project_post, "editable_obj": project_post,
               "related_projects": related_projects}
    context.update(extra_context or {})
    templates = [u"project/project_detail_%s.html" % str(slug), template]
    return TemplateResponse(request, templates, context)


def team_list(request, template="pages/team.html", extra_context=None):
    pages = Page.objects.published(for_user=request.user).select_related()
    page = get_object_or_404(pages, slug="team")
    templates = [ template ]

    team = Person.objects.published()
    context = {"page": page, "team": team}
    return TemplateResponse(request, templates, context)    

def member_detail(request, slug,
                  template="pages/member_detail.html"):
    """
    Custom templates are checked for using the name
    ``mezzanine_people/person_detail_XXX.html`` where ``XXX`` is the
    person's slug.
    """
    people = Person.objects.published()
    person = get_object_or_404(people, slug=slug)
    print vars(person)
    project_posts = Project.objects.published(for_user=request.user)
    project_posts = project_posts.filter(team=person)
    context = {"person": person, "editable_obj": person, "parent_page": "team", "projects": project_posts}
    templates = [ template ]
    return render(request, templates, context)

# Create your views here.
