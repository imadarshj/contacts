from django.contrib import admin

#for removing authentications and authorizations
from django.contrib.auth.models import Group
# Register your models here.

#we import the Contact models that we wrote so.
from .models import Contact

from import_export.admin import ImportExportModelAdmin


class ContactAdmin(ImportExportModelAdmin):
    list_display = ('id' , 'name', 'gender' , 'email' , 'info' , 'phone') #we can add 'date_added'
    list_display_links = ('id' , 'name')
    list_editable = ('info',)
    list_per_page = 2
    search_fields = ('name', 'gender' , 'email' , 'info' , 'phone' )
    list_filter = ('gender', 'date_added')

admin.site.register(Contact,ContactAdmin)

admin.site.unregister(Group)
