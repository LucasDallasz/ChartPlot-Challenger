import json5

def cleanEntry(entry, *args, **kwargs) -> list or None:
    """ This function checks if the input is valid. """
    result, objects = [], entry.split('\n')
    for obj in objects:
        try:
            result.append(json5.loads(obj))
        except Exception:
            return None
    return result


def checkTypes(jsonData, *args, **kwargs) -> bool:
    """ This function checks if the types are valid. """
    valid_types = ['start', 'span', 'data', 'stop']
    for value in jsonData:
        if value['type'] not in valid_types:
            return False
    return True


def checkSpan(jsonData, *args, **kwargs) -> bool:
    """ This function checks if the period is valid. """
    event_span = [x for x in jsonData if x['type'] == 'span'][0]
    begin, end = event_span['begin'], event_span['end']
    return begin <= end


def checkStartEvent(jsonData, *args, **kwargs) -> bool:
    firstEvent = jsonData[0]
    return firstEvent['type'] == 'start'
 
 
def checkStopEvent(jsonData, *args, **kwargs) -> bool:
    firstEvent = jsonData[-1]
    return firstEvent['type'] == 'stop'

