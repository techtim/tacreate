from django.db import models

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import RichText, Orderable, Slugged
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to
# Create your models here.

# class Projects(Page):
#     dob = models.DateField("Date of birth")


# class Project(Page):
#     dob = models.DateField("Date of birth")

# class Artist(Page):
# 	heading = models.CharField(max_length=200,
#         help_text="The heading under the icon blurbs")

