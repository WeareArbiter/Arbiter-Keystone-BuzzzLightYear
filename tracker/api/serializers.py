from rest_framework import serializers

from tracker.models import ProjectState


class ProjectStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectState
        fields = ('date',
                  'ticker_task_done',)
