import json5

def cleanEntry(entry, *args, **kwargs) -> list or None:
    result, objects = [], entry.split('\n')
    for obj in objects:
        try:
            result.append(json5.loads(obj))
        except Exception:
            return None
    return result


def checkTypes(jsonData, *args, **kwargs) -> bool:
    valid_types = ['start', 'span', 'data', 'stop']
    for value in jsonData:
        if value['type'] not in valid_types:
            return False
    return True


def checkSpan(jsonData, *args, **kwargs) -> bool:
    event_span = [x for x in jsonData if x['type'] == 'span'][0]
    begin, end = event_span['begin'], event_span['end']
    return begin <= end