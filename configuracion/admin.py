# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import FotosPortada,LinkVideos,SiteConfiguration
# Register your models here.
class FotosInlines(admin.TabularInline):
    model = FotosPortada
    extra = 1
    max_num = 5

class VideosInlines(admin.TabularInline):
    model = LinkVideos
    extra = 1
    max_num = 5

class SiteConfigAdmin(SingletonModelAdmin):
    inlines = [FotosInlines, VideosInlines]

admin.site.register(SiteConfiguration, SiteConfigAdmin)
