from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import resolve, reverse

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import RichText, Orderable, Slugged, Displayable
from mezzanine.pages.models import Page
from mezzanine.utils.models import AdminThumbMixin, upload_to
from mezzanine.blog.models import BlogPost
from mezzanine.blog import models as blog_models
from mezzanine.pages import models as pages_models
from mezzanine_people.models import Person

# Create your models here.


class Project(Displayable, RichText, AdminThumbMixin):
	date = models.DateField("Date")
	customer = models.CharField(max_length=100)
	team = models.ManyToManyField(Person, verbose_name="team")
	content = RichText('Story')
	related_projects = models.ManyToManyField("self",
								 verbose_name=_("Related projects"), blank=True)

	categories = models.ManyToManyField("ProjectCategory",
										verbose_name=_("Categories"),
										blank=True, related_name="projects")
	featured_image = FileField(verbose_name=_("Featured Image"),
		 upload_to=upload_to("blog.BlogPost.featured_image", "blog"),
		 format="Image", max_length=255, null=True, blank=True)
	admin_thumb_field = "featured_image"

	class Meta:
		verbose_name = _("Project")
		verbose_name_plural = _("Projects")
		ordering = ("-publish_date",)

	def get_absolute_url(self):
		url_name = "project_detail"
		kwargs = {"slug": self.slug}
		return reverse(url_name, kwargs=kwargs)


class ProjectCategory(Slugged):
	"""
	A category for grouping Projects posts into a series.
	"""

	class Meta:
		verbose_name = _("Project Category")
		verbose_name_plural = _("Project Categories")
		ordering = ("title",)

	@models.permalink
	def get_absolute_url(self):
		return ("project_list_category", (), {"category": self.slug})




# class Artist(Page):
# 	heading = models.CharField(max_length=200,
#		 help_text="The heading under the icon blurbs")

