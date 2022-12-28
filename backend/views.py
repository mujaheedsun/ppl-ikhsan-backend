from django.http import JsonResponse, HttpResponse, FileResponse
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

@api_view(['GET', 'POST'])
def project_list(request, format=None):

  # get all the project
  # serialize
  # return json

  if request.method == 'GET':
    print('ini mau ngeget')
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    print(Response)
    return Response(serializer.data)

  if request.method == 'POST':
    print('ini mau ngepost')
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      # print(serializer)
      # print(serializer.data)
      string = ''

      with open('test.txt', 'w') as file:
        file.write('Project Details :\n1. Repo Type : {}\n2. Project Type : {}\n'.format(serializer.data['repoType'],serializer.data['projectType']))
        file.write('3. Project Name : {}\n4. Project Description : {}\n'.format(serializer.data['projectName'],serializer.data['projectDescription']))
        file.write('5. Stages : {}'.format(serializer.data['stages']))
        file.close()
      
      with open('test.txt', 'r') as file:
        string = file.read()
        print(string)
        file.close()
      
      response = HttpResponse(string,  content_type= 'text/plain')
      response['Content-Disposition'] = 'attachment; filename=test.txt'
      return response
    


@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, id, format=None):

  try:
    project = Project.objects.get(pk=id)
  except Project.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)


  if request.method == 'GET':
    serializer = ProjectSerializer(project)
    return Response(serializer.data)

  elif request.method == 'PUT':
    serializer = ProjectSerializer(project, data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
