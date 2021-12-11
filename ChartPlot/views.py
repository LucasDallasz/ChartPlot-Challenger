from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import ChartPlotForm
from .functions import generateChartData


# Create your views here.
def chartplot_home(request):
    chartplots = request.user.get_all_chartplot()
    return render(request, 'ChartPlot/home.html', {'chartplots': chartplots})


def chartplot_create(request):
    form = ChartPlotForm(request.POST or None)
    
    if form.is_valid():
        request.user.set_chartplot(form.cleaned_data['entry']['events'])
        return redirect('ChartPlot:home')
        
    return render(request, 'ChartPlot/create.html', {'form': form})


def chartplot_detail(request, id):
    chartplot = request.user.get_chartplot(id)
    form = ChartPlotForm({'entry': chartplot.__str__()})
    context = {'form': form}
    
    if form.is_valid():
        chartData = generateChartData(form.cleaned_data['entry'])
        
        values = []
        for v in chartData['data']:
            values.append(v[0])
            values.append(v[1])

        print(values)
            
        context['labels'] = chartData['labels']
        context['values'] = values
    
    return render(request, 'ChartPlot/detail.html', context)

