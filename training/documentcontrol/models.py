from django.db import models
from quiz.models import Department

class Documents(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documentcontrol/documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
