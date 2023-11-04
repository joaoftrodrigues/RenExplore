from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import date

# Filename origin
ren_file = 'ren_content.html'

# Input result html 
f = open(ren_file, 'r')
soup = BeautifulSoup(f)

# Storage
durations = []
distances = []
departments = []
arrivals = []
prices = []
types = []

# Individual trips gathered
trips_html = soup.find_all(name = 'div', class_ = 'MuiCardContent-root')

# Convert results to string, to apply regular expressions
trips = [trip.text for trip in trips_html]
print(trips_html[0])

# Information extraction and storage
for trip in trips:

    # Hours of Department and Arrival
    hours = re.findall('[0-2][0-9]:[0-5][0-9]', trip)
    department = hours[0]
    arrival = hours[1]

    duration = re.search('[0-2][0-9]h [0-5][0-9]m', trip)[0]
    distance = re.search('[\d]+km', trip)[0]
    price = re.search('[\d]+,[\d]+€', trip)[0]
    trip_type = re.search('directo|1 ligação|{2-9} ligações', trip)[0]

    # Update Lists
    departments.append(department)
    arrivals.append(arrival)
    durations.append(duration)
    distances.append(distance)
    prices.append(price)
    types.append(trip_type)

# Join lists on a dictionary, 
# with desired column name, 
# to create a Data Frame
data = {
        'Department': departments, 
        'Arrival': arrivals,
        'Duration': durations,
        'Distance': distances,
        'Price': prices,
        'Type': types
}

df = pd.DataFrame(data)
print(df.head())


today = date.today().isoformat()
df.to_csv(today+'.csv', index=False)