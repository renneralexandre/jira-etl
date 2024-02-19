from django.contrib import admin

# Register your models here.
from .models import Epic


class EpicAdmin(admin.ModelAdmin):
    list_display = ('jiraProject', 'jiraKey', 'jiraStatus', 'jiraEpicName', 'jiraAssignee', 'jiraCreatedDate', 'classification')
    class Media:
        css = {
             'all': ["epic/x.css"]
             
        }

admin.site.register(Epic, EpicAdmin)