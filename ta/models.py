from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import resolve, reverse

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import RichText, Orderable, Slugged, Displayable, SiteRelated
from mezzanine.pages.models import Page
from mezzanine.blog.models import BlogPost
from mezzanine.blog import models as blog_models
from mezzanine_people.models import Person
from mezzanine.utils.models import AdminThumbMixin, upload_to
from mezzanine.utils.urls import admin_url, slugify, unique_slug

from pytils import translit
# Create your models here.


class Project(Displayable, RichText, AdminThumbMixin):
	date = models.DateField("Date")
	customer = models.CharField(max_length=100)
	team = models.ManyToManyField(Person, verbose_name="team")
	preview = models.CharField(_("Preview Text"), blank=True, max_length=200)
	content = RichText('Story')
	related_projects = models.ManyToManyField("self",
								 verbose_name=_("Related projects"), blank=True)

	categories = models.ManyToManyField("ProjectCategory",
										verbose_name=_("Categories"),
										blank=True, related_name="projects")
	featured_image = FileField(verbose_name=_("Featured Image"),
		 upload_to=upload_to("ta.Project.featured_image", "Projects"),
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


class ProjectCategory(SiteRelated): #Slugged
	"""
	A category for grouping Projects posts into a series.
	"""
	
	title = models.CharField(_("Title"), blank=True, max_length=50)
	slug = models.CharField(_("URL"), max_length=100, blank=True, null=True,
			help_text=_("Leave blank to have the URL auto-generated from "
						"the title."))
	class Meta:
		verbose_name = _("Project Category")
		verbose_name_plural = _("Project Categories")
		ordering = ("title",)

	# def __str__(self):
	# 	return self.title

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		"""
		If no slug is provided, generates one before saving.
		"""
		if not self.slug:
			self.slug = self.generate_unique_slug()
		super(ProjectCategory, self).save(*args, **kwargs)

	def generate_unique_slug(self):
		"""
		Create a unique slug by passing the result of get_slug() to
		utils.urls.unique_slug, which appends an index if necessary.
		"""
		# For custom content types, use the ``Page`` instance for
		# slug lookup.
		concrete_model = base_concrete_model(ProjectCategory, self)
		slug_qs = concrete_model.objects.exclude(id=self.id)
		return unique_slug(slug_qs, "slug", self.get_slug())

	def get_slug(self):
		"""
		Allows subclasses to implement their own slug creation logic.
		"""
		attr = "title"
		if settings.USE_MODELTRANSLATION:
			from modeltranslation.utils import build_localized_fieldname
			attr = build_localized_fieldname(attr, settings.LANGUAGE_CODE)
		# Get self.title_xx where xx is the default language, if any.
		# Get self.title otherwise.
		return slugify(getattr(self, attr, None) or translit.slugify(self.title))

	def admin_link(self):
		return "<a href='%s'>%s</a>" % (self.get_absolute_url(),
										ugettext("View on site"))
	admin_link.allow_tags = True
	admin_link.short_description = ""

	@models.permalink
	def get_absolute_url(self):
		return ("project_list_category", (), {"category": self.slug})




# class Artist(Page):
# 	heading = models.CharField(max_length=200,
#		 help_text="The heading under the icon blurbs")

