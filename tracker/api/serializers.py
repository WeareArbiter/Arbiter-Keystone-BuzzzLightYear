from rest_framework import serializers

from tracker.models import ProjectState


class ProjectStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectState
        fields = ('date',
                  'task_name',
                  'status',
                  'log',
                  'time',)
