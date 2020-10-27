
#from sklearn.preprocessing import StandardScaler


import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import string
from datetime import datetime as dates
import os
#directoies of files , change to whereever files are

name_listings = 'C:\\Users\\Admin\\Documents\\school t1\\Software Tech\\Project\\data\\listings_dec18.csv'
reviews = 'C:\\Users\\Admin\\Documents\\school t1\\Software Tech\\Project\\data\\reviews_dec18.csv'
#name_listings = str()
#reviews = str()

while len(name_listings) == 0 or len(reviews) == 0:
    if len(name_listings) == 0:
        name_listings = input("Enter listings_dec18.csv full directory: ")
        if os.path.exists(name_listings) == False:
            print("Directory not found or listings_dec18.csv file does not exits")
            name_listings = str()
    if len(reviews) == 0:
        reviews = input("Enter reviews_dec18.csv full directory: ")
        if os.path.exists(reviews) == False:
            print("Directory not found or reviews_dec18.csv file does not exits")
            reviews = str()


def format(date): #check is date is in yyyy/mm/dd format

    for i in range(len(date)):
        try: #if the date are not numbers
            int(date[i])
        except:
            return False
    if len(date) != 3:
        return False
    if int(date[1]) > 12 or int(date[2]) > 31:
        return False
    if len(date[0]) != 4 or len(date[1]) > 2  or len(date[1]) > 2 :
        return False
    return True

def compare_date( date1,date2): #compares two dates , returns true of date1 is ahead of date2
    if pd.isna(date1) or pd.isna(date2) : #if the dates are not nan, meaning the host_since date of a listings in empty [    ]
        
        return False
    
    date1 = str(date1)
    date2 = str(date2)
    date1 = date1.replace('/',' ').replace('-',' ')
    date2 = date2.replace('/',' ').replace('-',' ')
    date1 = date1.split()
    date2 = date2.split()
    
    if format(date1) == False or format(date2) == False:
        print('Format')
        return False
     
    if  int(date1[0]) > int(date2[0]):
        return True    
    if int(date1[0]) ==  int(date2[0]) and int(date1[1]) > int(date2[1]) :
        return True
    if int(date1[1]) == int(date2[1]) and int(date1[2]) > int(date2[2]):
        return(True)
    print('greater')
    return(False)

def listings_in_suburb(suburb,s,e, chunk): #return listings in a given suburb, within a user-selected period
    noDate = False                       
    if len(s) == 0 or len(e) ==  0:
        noDate = True
        dates = True
    if len(suburb) == 0:
        Nosuburb = True
        c = True
    else:
        Nosuburb = False
    l = list() #list of listings as pandas series
    suburb= suburb.split(',')
    skip = list()
    start = chunk*500 #read 500 rows at a time, call this func again with chunk += 1 to view the next 500 listings, this is time and memory efficient
    if chunk > 0:
        for f in range(1,start):
            skip.append(f)   #rows to skip
    listing =  pd.read_csv(name_listings, delimiter=',', skiprows= skip, nrows= 500, engine = 'python')# reads into dataframe
    for  r in range(len(listing)):
        host_since =  listing.iloc[r].iat[22]
    
        for city in suburb:
            city_name =  str(listing.iloc[r].iat[41]).upper()
            if noDate == False:
                dates = compare_date(s, host_since )
            if Nosuburb == False:
                c = (city_name ==  city.upper())
            if  c and dates: 
                l.append(listing.iloc[r])   
    return(l)

def keyword(keyword,s,e, chunk): #return listing based on a keyword(s) and user selected period
    noDate = False                       
    if len(s) == 0 or len(e) ==  0:
        noDate = True
    amenities = list()  #list of listings as pandas series
    keyword = keyword.split(',')
    skip = list()
    start = chunk*600       #reads 600 listings at a time
    for f in range(1,start):
        skip.append(f) #rows to skip
    listings = pd.read_csv(name_listings, delimiter=',', skiprows= skip,  nrows = 600, engine = 'python')
    for i in range(len(listings)):
        amenities_row = str(listings.iat[i,58])
        date =  str(listings.iat[i,22])
        if noDate == False:
            dates = compare_date(s, date )
        else:
            dates = True
        for word in keyword:
            if amenities_row.upper().find(word.upper()) != -1 : #if keyword/s in listing
                if word == keyword[-1] and dates :                    
                    amenities.append(listings.iloc[i])      #add listing to list         
            else:
                break        
    return(amenities)

def comments(): #how many customers commented on factors related to clealiness
    import matplotlib.pyplot as plt # plotting
    import numpy as np
    cleanliness = {'CLEAN' : 0,'DIRTY'  : 0,'HYGENIC'  : 0,'UNHYGENIC'  : 0,'HEALTHY'  : 0,'NEAT'  : 0,'UNCLEAN' : 0 } #words related to clealiness and their frequency
    total = 0
    s = 0
    nexts = True
    for listing in pd.read_csv(reviews, delimiter=',', usecols= ['comments'], chunksize= 1000): #reads 1000 reviews at a time, only uses column comments
        for review in listing.iterrows():
            nexts = True
            for w in cleanliness:
                if w in str(review[1]['comments']).upper():
                    cleanliness[w] += 1 #for the number of times a word in the dict 'cleanlines' was mentioned
                    if nexts:
                        total += 1 #only for the # of customers that commented about cleanliness
                        nexts = False
                    break
        s += 1000    
    ind = np.arange(0,len(cleanliness)*15,15)            #postion of bars of the x-axis
    width = 5                              #width of bar
    plt.bar(ind, cleanliness.values(), width)
    plt.xlabel('Words related to cleanliness')
    plt.ylabel('Total')
    plt.title(f'Frequency of Customers commenting on clealiness  total: {total}')
    plt.xticks(ind, cleanliness.keys())  
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\' +'cleanliness.jpg' # save plot to where this py file is saved
    
    plt.savefig(dir_path)
    return(dir_path)

def price_distribution(suburb, s,e,name):     #price distribution
    noDate = False                       
    if len(s) == 0 or len(e) ==  0:
        noDate = True
    import matplotlib.pyplot as plt # plotting
    import numpy as np # linear algebra
    listings = pd.read_csv(name_listings, delimiter=',', usecols= ['city', 'price','host_since','id'])
    prices = list()                                     #list of all prices of listings in suburb
    suburb = suburb.upper()
    t = False  
    if suburb == '':
        t = True  
        suburb = 'Sydney'                         #change into capital letters
    suburb = suburb.split(',')
    compare = True 
    for x in range(len(listings)):
        host_since = listings.at[x,'host_since']                      #loop through listings
        if noDate == False: #if date is provided
            
            compare  = compare_date(s, host_since)
        for sub in suburb:
            #if no date was given and prices for all of the suburb was to be couted
            if (str(listings.at[x,'city']).upper() == sub or t) and compare:
                p = listings.at[x,'price'].replace('$','').replace(',','')  #remove commas and dollar sign $, to convert to int
                prices.append(int(float(p)))                         # add price to list


    prices = sorted(prices)                                       #sort prces from low to high
    if len(prices) == 0:
        return(-1)
    n = 100                    #price ranges incremting by 100, 0 - 100, 100 - 200, 300 - 400 ....
    temp_sum = 1                  #sum of all prices within a given range
    dist = list()             #list of total listings with ranges
    
    labels = list()                               #labels of each bar on x-axis
    for y in range(len(prices)):                    #loop through list of prices
        if int(prices[y]) <=  n or n > 500:        #if the pries is with the range n or greater than 500, stops coutning after 500        
            temp_sum += 1           
        else:
            dist.append(temp_sum)               #add total of listings with the range to list         
            
            temp_sum = 1                          #reset sum
            labels.append(f'<{n}')                #add label to list e.g. <100,<200 ...etc
            while n <= prices[y]:                 #loop to next range, e.g. if current range 100-200 and next value is 430, n needs to be 500 (400-500)
                n += 100
            
        if y == len(prices) - 1:                #if at the last price in the list
            dist.append(temp_sum)                 # add total
            labels.append('500+')              #add last label

    ind = np.arange(0,len(dist)*3,3)            #postion of bars of the x-axis
    width = 2                              #width of bar
    plt.bar(ind, dist, width)
    plt.xlabel('Prices per night $')
    plt.ylabel('Total')
  


    user_input = suburb
    if len(user_input) == 1:
        user_input = user_input[0][0].upper() + user_input[0][1:]
    else:
        user_input_copy = user_input
        user_input = str()
        for k in range(len(user_input_copy)):
            user_input_copy[k] = user_input_copy[k].lower()
            user_input_copy[k] = user_input_copy[k][0].upper() + user_input_copy[k][1:]
            if k != len(user_input_copy) - 1 and k != 0:
                user_input += ', ' + user_input_copy[k] 
            elif k == 0:
                user_input += user_input_copy[k]
            else:
                user_input +=  ' and ' + user_input_copy[k]


    if noDate:
        title = f'Price Distribution for all of {user_input}' #if no date was given
    else:
        title = f'Price Distribution for {user_input}, {s} to {e}' #if dates were given, show dates in title 


    plt.title(title)
    plt.xticks(ind,labels)  
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\' + name + '.jpg'
    plt.savefig(dir_path)
    return(dir_path)
