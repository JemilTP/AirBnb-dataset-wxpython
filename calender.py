def return_calendar(id, start_date, end_date): #function that true if a user entered start and end date are availble the calender for a specific listing
    import datetime as datetime                 #calender_dec18.csv was too large and could not be read, freezing my computer at times
    s = datetime.strptime(start_date, "%m/%d/%Y")       #therefor this funciton was not used, but inlcluded for reference
    e = datetime.strptime(end_date, "%m/%d/%Y")         #the parameter host_since in listings_dec18.csv was used to create a time period 
    delta = e - s                                       # as Joun suggested
    for i in range(delta.days + 1):
        day = s + timedelta(days=i)
        dates.append(day)
    checked = False 
    id_itr = 0
    date = 1
    ava = 2
    for calender in pd.read_csv(name, delimiter=',', chunksize= 1000, usecols= ['listing_id', 'date', 'available'], low_memory= True):              
        for  row in calender.iterrows():           
            if row[1][id_itr] == id:                 
                current_date = datetime.strptime(row[1][date], "%Y-%m-%d") #get the date
                if current_date >= s and current_date <= e :                      
                    checked = True                       
                    dates.remove(current_date)
                    if row[1][ava] == 'f':
                        return(False)                  
            elif checked and len(dates) == 0:
                return(True)    
