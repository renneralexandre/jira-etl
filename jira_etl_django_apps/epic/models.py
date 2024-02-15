from django.db import models
from django.conf import settings

# Create your models here.
class Epic(models.Model):
    jiraIssueType = models.CharField(max_length=5, default='Epic')
    jiraProject = models.CharField(max_length=100, default= "")
    jiraKey = models.CharField(max_length=20, default= "")
    jiraEpicName = models.CharField(max_length=1000, default= "")
    jiraStatus = models.CharField(max_length=200, default= "")
    jiraAssignee = models.CharField(max_length=200, default= "")
    jiraCreatedDate = models.DateTimeField()
    jiraUpdatedDate = models.DateTimeField()
    jiraResolvedDate = models.DateTimeField()
    classification = models.CharField(max_length=1, default= "")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_%(class)s_set",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="updated_%(class)s_set",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )