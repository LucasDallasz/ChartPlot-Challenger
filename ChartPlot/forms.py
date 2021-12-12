from django import forms

from .models import ChartPlot
from .validators import *
from .functions import generateChartData

import json5


class ChartPlotForm(forms.Form):
    
    validators = [
        {'func': checkTypes, 'errorMessage': 'There is an incorrect event type. Please, check all types.'},
        {'func': checkSpan, 'errorMessage': 'The span is incorrect. Please, check the timestamp.'},
    ]
    
    
    error_messages = {
        'DataEntryIncorrect': 'Input data is invalid.',
        'RangeDaysIncorrect': 'Incorrect range of days. Check timestamp events.',
        'MinRangeDays': 'An interval of at least 2 days is required.',
        'MinEventPerGroup': 'It is essential that every day have the same amount of events.',
        'KeyError': 'There is an incorrect event key name. Please, check the events..',
    }
    
    
    name = forms.CharField(
        label='Name',
        max_length=1000,
        widget=forms.TextInput(attrs={
            'class': 'mb-2 form-control',
        })
    )
    
    entry = forms.CharField(
        label='',
        max_length=10000,
        widget=forms.Textarea(attrs={
            'id': 'entryEvents',
            'class': 'md-textarea form-control mb-1',
            'rows': 10, 'cols': 100,
        })
    )
        
    
    def clean_entry(self):
        entry = self.cleaned_data['entry']
        entry_cleaned = self._cleanEntry(entry)
        
        if entry_cleaned is None:
            raise forms.ValidationError(self.error_messages['DataEntryIncorrect'])
        
        for validator in self.validators:
            if not validator['func'](entry_cleaned):
                raise forms.ValidationError(validator['errorMessage'])
        
        eventsData = list(filter(lambda x: x['type'] == 'data', entry_cleaned))
        allTimestamp = [{'timestamp': x['timestamp']} for x in eventsData]
        
        if not self._validateAllTimestamp(allTimestamp):
            """ Checking if the timestamp range is valid. """
            raise forms.ValidationError(self.error_messages['RangeDaysIncorrect'])
        
        cleaned_timestamp = self._cleanTimestamp(allTimestamp)
        
        if len(cleaned_timestamp) <= 1:
            raise forms.ValidationError(self.error_messages['MinRangeDays'])
        
        """ Here are the groups. Each group is a day and each day contains its events. """
        groups = self._generateGroups(cleaned_timestamp, eventsData)
        
        """ Here is the amount needed for each group. """
        amountRequiredByGroup = self._amountRequired(entry_cleaned, eventsData)
        
        """ If all groups have the requested amount, returns true. """
        groupsAreValid = self._checkAmountPerGroup(groups, amountRequiredByGroup)

        if not groupsAreValid:
            raise forms.ValidationError(self.error_messages['MinEventPerGroup'])
        
        try:
            chartData = generateChartData({'groups': groups, 'labels': len(cleaned_timestamp)})
        except KeyError:
            raise forms.ValidationError(self.error_messages['KeyError'])
        
        return {'chartData': chartData, 'events': entry}
        

    def _cleanEntry(self, entry) -> list or None:
        result, objects = [], entry.split('\n')
        for obj in objects:
            try:
                result.append(json5.loads(obj))
            except Exception:
                return None
        return result
    
    
    def _cleanTimestamp(self, allTimestamp):
        return sorted(list({x['timestamp'] for x in allTimestamp}))

    
    def _validateAllTimestamp(self, allTimestamp) -> bool:
        """ 
            Checks if the days based on the timestamp are valid.
            Each day corresponds to a value of 6.000 added to the current timestamp. 
        """
        cleanedTimestamp = self._cleanTimestamp(allTimestamp)
        
        for pos, timestamp in enumerate(cleanedTimestamp):
            if pos > 0:
                if (timestamp - cleanedTimestamp[pos - 1]) != 60000:
                    return False
        return True 
    
    
    def _generateGroups(self, allTimestamp, eventsData):
        groups = {x: [] for x in allTimestamp}
        for event in eventsData:
            groups[event['timestamp']].append(event)
        return groups

    
    def _amountRequired(self, jsonData, eventsData) -> int:
        eventStart = jsonData[1]
        begin = eventStart['begin']
        return len(list(filter(lambda x: x['timestamp'] == begin, eventsData)))
    
    
    def _checkAmountPerGroup(self, groups, amountRequired):
        for _, value in groups.items():
            amount_group = len(value)
            if amount_group != amountRequired:
                return False
        return True