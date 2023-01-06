from django.http import JsonResponse, HttpResponse, FileResponse
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import yaml
import os

@api_view(['GET', 'POST'])
def project_list(request, format=None):
  # get all the project
  # serialize
  # return json

    if request.method == 'GET':
        print('ini mau ngeget')
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
      
        data = serializer.data
        data['stages'] = json.loads(data['stages'])
        pipeline_json = None

        def add_stage_to_pipeline(stage_json):
            pipeline_json['stages'].append(stage_json["stage"])
            pipeline_json[stage_json['name']] = 0
            copy = stage_json.copy()
            copy.pop('name')
            pipeline_json[stage_json['name']] = copy

        if data['repoType'] == 'Gitlab':            
            print('sampe sini 1 gitlab', data, os.getcwd())

            if data['projectType'] == 'React':

                PATH_TO_REACT_TEMPLATE = "assets/Gitlab/React/"

                with open(PATH_TO_REACT_TEMPLATE + 'react.template.json') as f:
                    pipeline_json = json.load(f)
                    f.close()

                print('sampe sini 1.5', pipeline_json)
                    
                if 'Build' in data['stages']:
                    with open(PATH_TO_REACT_TEMPLATE + 'react-build.template.json') as f:
                        build_json_temp = json.load(f)
                        add_stage_to_pipeline(build_json_temp)
                        f.close()

                if 'Test' in data['stages']:
                    with open(PATH_TO_REACT_TEMPLATE + 'react-test.template.json') as f:
                        test_json_temp = json.load(f)
                        add_stage_to_pipeline(test_json_temp)
                        f.close()

                if 'Deploy' in data['stages']:
                    with open(PATH_TO_REACT_TEMPLATE + 'react-deploy.template.json') as f:
                        deploy_json_temp = json.load(f)
                        add_stage_to_pipeline(deploy_json_temp)
                        f.close()

                print('sampe sini 2 react', pipeline_json)
            
            elif data['projectType'] == 'Django':

                PATH_TO_DJANGO_TEMPLATE = "assets/Gitlab/Django/"

                with open(PATH_TO_DJANGO_TEMPLATE + 'django.template.json') as f:
                    pipeline_json = json.load(f)
                    f.close()

                print('sampe sini 1.5', pipeline_json)
                    
                if 'Build' in data['stages']:
                    with open(PATH_TO_DJANGO_TEMPLATE + 'django-build.template.json') as f:
                        build_json_temp = json.load(f)
                        add_stage_to_pipeline(build_json_temp)
                        f.close()

                if 'Test' in data['stages']:
                    with open(PATH_TO_DJANGO_TEMPLATE + 'django-test.template.json') as f:
                        test_json_temp = json.load(f)
                        add_stage_to_pipeline(test_json_temp)
                        f.close()

                if 'Deploy' in data['stages']:
                    with open(PATH_TO_DJANGO_TEMPLATE + 'django-deploy.template.json') as f:
                        deploy_json_temp = json.load(f)
                        add_stage_to_pipeline(deploy_json_temp)
                        f.close()

                print('sampe sini 2 django', pipeline_json)

            elif data['projectType'] == 'Springboot':

                PATH_TO_SPRINGBOOT_TEMPLATE = "assets/Gitlab/Springboot/"

                with open(PATH_TO_SPRINGBOOT_TEMPLATE + 'springboot.template.json') as f:
                    pipeline_json = json.load(f)
                    f.close()

                print('sampe sini 1.5', pipeline_json)
                    
                if 'Build' in data['stages']:
                    with open(PATH_TO_SPRINGBOOT_TEMPLATE + 'springboot-build.template.json') as f:
                        build_json_temp = json.load(f)
                        add_stage_to_pipeline(build_json_temp)
                        f.close()

                if 'Test' in data['stages']:
                    with open(PATH_TO_SPRINGBOOT_TEMPLATE + 'springboot-test.template.json') as f:
                        test_json_temp = json.load(f)
                        add_stage_to_pipeline(test_json_temp)
                        f.close()

                if 'Deploy' in data['stages']:
                    with open(PATH_TO_SPRINGBOOT_TEMPLATE + 'springboot-deploy.template.json') as f:
                        deploy_json_temp = json.load(f)
                        add_stage_to_pipeline(deploy_json_temp)
                        f.close()

                print('sampe sini 2 springboot', pipeline_json)

        
        elif data['repoType'] == 'Github':            
            print('sampe sini 1 github', data, os.getcwd())

            if data['projectType'] == 'React':

                PATH_TO_REACT_TEMPLATE = "assets/Github/React/"

                with open(PATH_TO_REACT_TEMPLATE + 'react.template.json') as f:
                    pipeline_json = json.load(f)
                    f.close()

                print('sampe sini 1.5', pipeline_json)
                    
                if 'Build' in data['stages']:
                    build_json_1 = {
                        "run" : "npm ci"
                    }

                    build_json_2 = {
                        "run" : "npm run build --if-present"
                    }

                    pipeline_json['jobs']["build"]['steps'].append(build_json_1)
                    pipeline_json['jobs']["build"]['steps'].append(build_json_2)
                    

                if 'Test' in data['stages']:
                    test_json = {
                        "run" : "npm test"
                    }

                    pipeline_json['jobs']["build"]['steps'].append(test_json)

                if 'Deploy' in data['stages']:
                    pass
                    

                print('sampe sini 2 react', pipeline_json)
            
            elif data['projectType'] == 'Django':

                PATH_TO_DJANGO_TEMPLATE = "assets/Github/Django/"

                with open(PATH_TO_DJANGO_TEMPLATE + 'django.template.json') as f:
                    pipeline_json = json.load(f)
                    f.close()

                print('sampe sini 1.5', pipeline_json)
                    
                if 'Build' in data['stages']:
                    build_json = {
                        "name" : "Install Dependencies",
                        "run" : [
                            "python -m pip install --upgrade pip",
                            "pip install -r requirements.txt"
                        ]
                    }
                    
                    pipeline_json["jobs"]["build"]["steps"].append(build_json)

                if 'Test' in data['stages']:
                    test_json = {
                        "name" : "Runs Test",
                        "run" : "python manage.py test"
                    }
                    
                    pipeline_json["jobs"]["build"]["steps"].append(test_json)
                    

                if 'Deploy' in data['stages']:
                    pass

                print('sampe sini 2 django', pipeline_json)

            elif data['projectType'] == 'Springboot':
                pass



        with open('gitlab-ci.yml', 'w+') as yaml_file:
            yaml.dump(pipeline_json, yaml_file, sort_keys=False)
            yaml_file.close()

        with open('gitlab-ci.yml', 'r') as file:
            file_data = file.read()
            file.close()

        response = HttpResponse(file_data, content_type='text/x-yaml')
        response['Content-Disposition'] = 'attachment; filename="gitlab-ci.yml"'

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