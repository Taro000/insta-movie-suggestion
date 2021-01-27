from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class MovieResource(resources.ModelResource):
    class Meta:
        model = Movie


@admin.register(Movie)
class MovieAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'title', 'title_ja', 'year', 'imdb_id', 'img_path')

    resource_class = MovieResource


admin.site.register(Notice)
admin.site.register(SiteConfig)
# fields = ['id', 'title', 'title_ja', 'year', 'imdb_id', 'img_path']
