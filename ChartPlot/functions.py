def generateChartData(groupsData) -> dict or None:
    def generateData(groups) -> list or None:
        
        def getDataSet(event, groups) -> tuple or None:
            result = [[event['min_response_time']], [event['max_response_time']]]
        
            for group in groups:
                for ev in group:
                    os, browser = event['os'], event['browser']
                    if ev['os'] == os and ev['browser'] == browser:
                        result[0].append(ev['min_response_time'])
                        result[1].append(ev['max_response_time'])
                        break
                    
            return result if len(result) != 0 else None
        
        result = []
        
        initialEvents = list(groups.items())[0][1]
        lastEvents = list(groups.values())[1:]
        
        for event in initialEvents:
            data = getDataSet(event, lastEvents)
            if data is None:
                return None
            result.append(data)  
        
        return result
        
    data = generateData(groupsData['groups'])    
    
    if data is not None:
        return {'labels': [x for x in range(0, groupsData['labels'])], 'data': data}
    
    return None
        