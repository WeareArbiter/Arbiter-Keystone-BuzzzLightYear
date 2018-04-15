from django.db import models


class ProjectState(models.Model):
    date = models.CharField(max_length=10)
    ticker_task_done = models.BooleanField(default=0)

    def __str__(self):
        return '{}'.format(self.date)
