from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Task
from .serializers import JobSerializer, TaskSerializer, CreateJobSerializer
from .tasks import scrape_coin_data

class StartScrapingView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateJobSerializer(data=request.data)
        if serializer.is_valid():
            job = Job.objects.create()
            coins = serializer.validated_data['coins']
            for coin in coins:
                scrape_coin_data.delay(job.job_id, coin)
            return Response({"job_id": str(job.job_id)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScrapingStatusView(APIView):
    def get(self, request, job_id, *args, **kwargs):
        try:
            job = Job.objects.get(job_id=job_id)
        except Job.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        tasks = Task.objects.filter(job=job)
        tasks_data = TaskSerializer(tasks, many=True).data
        return Response({"job_id": str(job.job_id), "tasks": tasks_data})

