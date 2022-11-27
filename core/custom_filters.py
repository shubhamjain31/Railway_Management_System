import datetime

def time_format(item):
    t = datetime.datetime.strftime(item, '%H:%M %p')
    return t

def date_format(item):
    t = datetime.datetime.strftime(item, '%Y-%m-%d')
    return t

def replace_underscore_with_space(item):
    return item.replace(" ", "_")