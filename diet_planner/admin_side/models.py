from django.db import models

# Create your models here.
class Specialties(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Chronic_conditions(models.Model):
    name = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name