from django.db import models


class ProjectState(models.Model):
    date = models.CharField(max_length=10)
    task_name = models.CharField(max_length=30)
    status = models.BooleanField(default=0)
    log = models.CharField(max_length=50
                           blank=True,
                           null=True)
    time = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.date, self.task_name)
