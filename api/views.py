from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Person
from .serializers import PersonSerializer
from django_q.tasks import async_task
import time

def process_person(data):
    # Simulate API call
    time.sleep(30)
    # Save to database
    serializer = PersonSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

class PersonListCreateView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Instead of saving immediately, queue the task
        async_task(process_person, serializer.validated_data)

        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Request queued for processing"}, status=status.HTTP_202_ACCEPTED, headers=headers)