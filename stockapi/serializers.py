from rest_framework import serializers
from stockapi.models import BM


class BMSerializer(serializers.ModelSerializer):
    class Meta:
        model = BM
        fields = ('date',
                  'name',
                  'index',
                  'individual',
                  'foreigner',
                  'institution',)
