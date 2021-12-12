from django.shortcuts import redirect
from django.urls import reverse

import functools

def owner_required(view):
    """ This decorator verifies that the user is the owner of ChartPlot."""
    @functools.wraps(view)
    def wrapper(request, id, *args, **kwargs):
        chartPlot = request.user.get_chartplot(id)
        if chartPlot is None:
            return redirect(f"{reverse('ChartPlot:home')}?invalidChartPlot=1")
        return view(request, id, *args, **kwargs)
    return wrapper