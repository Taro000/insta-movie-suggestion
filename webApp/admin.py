from django.contrib import admin
from .models import *

# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    fields = ['id', 'title', 'title_ja', 'year', 'imdb_id', 'img_path']


admin.site.register(Notice)
admin.site.register(Movie, MovieAdmin)
admin.site.register(SiteConfig)