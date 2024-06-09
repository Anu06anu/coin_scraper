from rest_framework import serializers
from .models import Job, Task

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['job_id', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['coin', 'output', 'created_at']

class CreateJobSerializer(serializers.Serializer):
    coins = serializers.ListField(child=serializers.CharField(max_length=10))

    def validate_coins(self, value):
        if not all(isinstance(coin, str) for coin in value):
            raise serializers.ValidationError("All coins must be strings.")
        return value
