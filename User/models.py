from django.contrib.auth.models import AbstractUser
from django.db.models.query import QuerySet
from django.db import models
from RequestLimiter.utils import date_time_now, str_to_datetime

from ChartPlot.models import ChartPlot


# Create your models here.
class User(AbstractUser):
    
    last_post_request = models.CharField(max_length=255, default=date_time_now())
    punishment_seconds = models.IntegerField(default=2)
    sequence_invalid_requests = models.IntegerField(default=0)
    
    
    # Attributes #
    def __str__(self) -> str:
        return self.username


    # GETTERS #
    def get_all_chartplot(self) -> QuerySet:
        """ Returns the all chartplots of user. """
        return self.chartplot_set.all()
   
    
    def get_chartplot(self, id):
        try:
            chartplot = self.chartplot_set.get(id=id)
        except Exception:
            chartplot = None
        finally:
            return chartplot
 
    
    def set_chartplot(self, name, events):
        ChartPlot.objects.create(
            name = name,
            events = events,
            user = self
        )


    def delete_chartplot(self, id):
        chartplot = self.get_chartplot(id)
        chartplot.delete()
        

    def get_last_post_request(self) -> object:
        return str_to_datetime(self.last_post_request)
    
    
    def get_punishment_seconds(self) -> int:
        return self.punishment_seconds
    
    
    # SETTERS #
    
    def set_last_post_request(self, request):
        self.last_post_request = request
        self.save()
        
        
    def increment_punishment_seconds(self):
        self.punishment_seconds += 5
        self.save()
        
        
    def increment_sequence_invalid_requests(self):
        self.sequence_invalid_requests += 1
        self.save()