from django.db import models

# Create your models here.
class ChartPlot(models.Model):
    events = models.TextField(max_length=10000)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.events