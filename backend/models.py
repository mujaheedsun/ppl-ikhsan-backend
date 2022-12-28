from django.db import models
import json

class Project(models.Model):
    repoType = models.CharField(max_length = 30, default='000000')
    projectType = models.CharField(max_length= 30, default='000000')
    projectName = models.CharField(max_length=30)
    projectDescription = models.CharField(max_length=200)
    stages = models.TextField(max_length=50, default='000000')

    def set_stages(self, array):
        self.stages = json.dumps(array)

    def get_array(self):
        return json.load(self.stages)

    def __str__(self) -> str:
        return self.projectName + ', status : ' + self.projectDescription