def generateChartData(groupsData) -> dict or None:
    """ This function separates the values ​​for each day. If a key error occurs, it will return false. """
    
    def generateData(groups) -> list or None:
        
        def getDataSet(event, groups) -> tuple or None:
            result = [[event['min_response_time']], [event['max_response_time']]]

            is_valid = False
            for group in groups:
                for ev in group:
                    os, browser = event['os'], event['browser']
                    if ev['os'] == os and ev['browser'] == browser:
                        is_valid = True
                        result[0].append(ev['min_response_time'])
                        result[1].append(ev['max_response_time'])
                        break
            
            return result if is_valid else None
        
        result = []
        
        initialEvents = list(groups.items())[0][1]
        lastEvents = list(groups.values())[1:]
        
        for event in initialEvents:
            data = getDataSet(event, lastEvents)
            if data is None:
                return None
            result.append(data)  
        
        
        """
        The algorithm organizes the data like this:
        
            [[0.1, 0.2], [1.3, 0.9]]
            [[0.2, 0.1], [1.2, 1.0]]
            [[0.3, 0.2], [1.2, 1.1]]
            [[0.1, 0.3], [1.0, 1.4]]    
        """
        
        return result
        
    data = generateData(groupsData['groups'])    
    
    if data is not None:
        return {'labels': [x for x in range(0, groupsData['labels'])], 'data': data}
    
    return None
        
        
def setColorByGroup(values) -> list:
    result = []
    colors = [
        {'bg': 'rgba(255, 99, 132, 0.2)', 'border': 'rgba(255, 99, 132, 1)'},
        {'bg': 'rgba(54, 162, 235, 0.2)', 'border': 'rgba(54, 162, 235, 1)'},
        {'bg': 'rgba(255, 206, 86, 0.2)', 'border': 'rgba(255, 206, 86, 1)'},
        {'bg': 'rgba(75, 192, 192, 0.2)', 'border': 'rgba(75, 192, 192, 1)'},
        {'bg': 'rgba(153, 102, 255, 0.2)', 'border': 'rgba(153, 102, 255, 1)'},
        {'bg': 'rgba(255, 159, 64, 0.2)', 'border': 'rgba(255, 159, 64, 1)'},
        {'bg': 'rgb(7, 107, 0, 0.2)', 'border': 'rgb(7, 107, 0, 1)'},
        {'bg': 'rgb(255, 0, 1, 0.2)', 'border': ' rgb(255, 0, 1, 1)'},
    ]
    
    pos = 0
    for value in values:
        if pos >= len(colors): 
            pos = 0
        color = colors[pos]
        result.append({'data': value, 'bg': color['bg'], 'border': color['border']})
        pos+= 1
        
    return result
            
