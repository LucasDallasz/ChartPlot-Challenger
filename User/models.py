from django.contrib.auth.models import AbstractUser
from django.db.models.query import QuerySet

from ChartPlot.models import ChartPlot


# Create your models here.
class User(AbstractUser):
    
    def __str__(self) -> str:
        return self.username


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
        
