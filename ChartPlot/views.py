from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import ChartPlotForm
from .decorators import owner_required


# Create your views here.
def chartplot_home(request):
    chartplots = request.user.get_all_chartplot()
    return render(request, 'ChartPlot/home.html', {'chartplots': chartplots})


def chartplot_create(request):
    form = ChartPlotForm(request.POST or None)
    
    if form.is_valid():
        request.user.set_chartplot(form.cleaned_data['name'], form.cleaned_data['entry']['events'])
        return redirect('ChartPlot:home')
        
    return render(request, 'ChartPlot/create.html', {'form': form})


@owner_required
def chartplot_detail(request, id):
    chartplot = request.user.get_chartplot(id)
    form = ChartPlotForm(
        {'name': chartplot.__str__(), 'entry': chartplot.events}
    )
    context = {'form': form, 'chartplot': chartplot}
    
    if form.is_valid():
        result = form.cleaned_data['entry']
        chartData = result['chartData']
        
        values = []
        for v in chartData['data']:
            values.append(v[0])
            values.append(v[1])
            
        context['labels'] = chartData['labels']
        context['values'] = values
    
    return render(request, 'ChartPlot/detail.html', context)


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

