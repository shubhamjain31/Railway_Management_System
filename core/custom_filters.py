def date_format(item):
    return item.time()

def date_time_format(item):
    return str(item.date())+'\n'+str(item.time())