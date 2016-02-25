from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
# from mezzanine.pages.admin import PageAdmin
# from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.conf import settings
from mezzanine.core.admin import (DisplayableAdmin, BaseTranslationModelAdmin)
# Register your models here.
from .models import Project, ProjectCategory

project_extra_fieldsets = ((None, {"fields": ("date","categories", "customer","featured_image","content","team",)}),)

project_fieldsets = deepcopy(DisplayableAdmin.fieldsets) + project_extra_fieldsets
project_fieldsets = list(project_fieldsets)
project_fieldsets.insert(1, (_("Other posts"), {
    "classes": ("collapse-closed",),
    "fields": ("related_projects",)}))

project_list_display = ["title", "status", "admin_link"]
project_list_display.insert(0, "admin_thumb")
project_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)

class ProjectAdmin(DisplayableAdmin):
    fieldsets = project_fieldsets
    list_display = project_list_display
    list_filter = project_list_filter
    # filter_horizontal = ("categories", "related_projects",)

class ProjectCategoryAdmin(BaseTranslationModelAdmin):
    """
    Admin class for blog categories. Hides itself from the admin menu
    unless explicitly specified.
    """
    fieldsets = ((None, {"fields": ("title",)}),)

    def in_menu(self):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "blog.ProjectCategory" in items:
                return True
        return False


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
# Register your models here.
