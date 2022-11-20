from django.db import models
from collectdata.models import BaseData, SaveData

# Create your models here.





class StreamlitPort(models.Model):
    basedata = models.OneToOneField(BaseData, on_delete=models.CASCADE)
    port_number = models.IntegerField(unique=True)

    def __str__(self):
        return self.basedata.file_name