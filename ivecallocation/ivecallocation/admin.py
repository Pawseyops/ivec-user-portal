from django.contrib import admin

import django.contrib.auth.admin
import django.contrib.auth.models
import django.contrib.sites.admin
import django.contrib.sites.models

import allocation.admin
import allocation.adminsite

class GroupAdmin(django.contrib.auth.admin.GroupAdmin):
    pass

class UserAdmin(django.contrib.auth.admin.UserAdmin):
    pass

site = allocation.adminsite.IvecAdminSite(name="iVEC Allocation Administration")

# Django Auth.
site.register(django.contrib.auth.models.Group, GroupAdmin)
site.register(django.contrib.auth.models.User, UserAdmin)

from allocation.admin import register
register(site)
