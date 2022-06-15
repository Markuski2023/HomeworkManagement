from django.contrib import admin

from .models import Group, Assignment, Message, Subject

admin.site.register(Group)
admin.site.register(Assignment)
admin.site.register(Message)
admin.site.register(Subject)