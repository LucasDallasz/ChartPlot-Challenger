from django.shortcuts import render, redirect
from django.urls import reverse

from .decorators import owner_required
from .forms import ChartPlotForm
from .functions import setColorByGroup

from Utils.decorators import object_exists


# Create your views here.
def chartplot_home(request):
    chartplots = request.user.get_all_chartplot()
    return render(request, 'ChartPlot/home.html', {'chartplots': chartplots})


def chartplot_create(request):
    form = ChartPlotForm(request.POST or None)
    
    if form.is_valid():
        request.user.set_chartplot(form.cleaned_data['name'], form.cleaned_data['entry']['events'])
        return redirect(f"{reverse('ChartPlot:home')}?newChartPlot=1")
        
    return render(request, 'ChartPlot/create.html', {'form': form})


@object_exists('ChartPlot')
@owner_required
def chartplot_delete(request, id):
    request.user.delete_chartplot(id)
    return redirect(f"{reverse('ChartPlot:home')}?chartPlotDeleted=1")
    


@object_exists('ChartPlot')
@owner_required
def chartplot_detail(request, id):
    chartplot = request.user.get_chartplot(id)
    form = ChartPlotForm({'name': chartplot.__str__(), 'entry': chartplot.events})
    
    context = {'form': form, 'chartplot': chartplot}
    
    if form.is_valid():
        result = form.cleaned_data['entry']
        chartData = result['chartData']
        
        values = []
        for v in chartData['data']:
            values.append(v[0])
            values.append(v[1])
            
        groups = setColorByGroup(values)
        context['labels'] = chartData['labels']
        context['values'] = groups
    
    return render(request, 'ChartPlot/detail.html', context)


@object_exists('ChartPlot')
@owner_required
def chartplot_edit(request, id):
    chartplot = request.user.get_chartplot(id)
    form = ChartPlotForm(
        request.POST or None, 
        initial={
            'name': chartplot.__str__(),
            'entry': chartplot.events,
        }
    )
    
    if request.method == 'POST':
        if form.is_valid():
            changed = '0'
            if form.has_changed():
                setattr(chartplot, 'name', form.cleaned_data['name'])
                setattr(chartplot, 'events', form.cleaned_data['entry']['events'])        
                chartplot.save()
                changed = '1'
            return redirect(f"{reverse('ChartPlot:detail', kwargs={'id': id})}?chartPlotUpdated={changed}")
    
    context = {'form': form, 'chartplot': chartplot}
    return render(request, 'ChartPlot/edit.html', context)


def chartplot_tutorial(request):
    return render(request, 'ChartPlot/tutorial.html')

