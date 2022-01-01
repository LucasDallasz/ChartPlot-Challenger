from datetime import datetime, timezone


def date_time_now() -> object:
    dt = datetime.now()
    date_time = dt.replace(tzinfo=timezone.utc).__str__().split('+')[0]
    result = date_time.split('.')[0]
    return datetime.strptime(''.join(result), '%Y-%m-%d %H:%M:%S')


def str_to_datetime(string) -> object:
    
    
    def datetime_to_list(string) -> list:
        return string.split(' ')


    def clean(typedt, value) -> dict:
        keys = {'date': ['year', 'month', 'day'], 'time': ['hour', 'minute', 'seconds']}
        separator = '-' if typedt == 'date' else ':'
        return {keys[typedt][k] : int(v) for k, v in enumerate(value.split(separator))}
        
        
    date_time = datetime_to_list(string)
    d = clean('date', date_time[0]) # Date cleaned
    t = clean('time', date_time[1]) # Time cleaned
    
    return datetime(d['year'], d['month'], d['day'], t['hour'], t['minute'], t['seconds'])
    
        
    
  
    
    
