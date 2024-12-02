![Local Deployment Image](image.png)

# URL to production

URL: https://advanced-software-engineering-6oj4rrsdxdctxut2gmvnu8.streamlit.app/

# Analyzation of geo data

On the outer parts of Berlin there are not enough charging stations for the demand. In the center of Berlin there are enough charging stations for the people.

# Documentation

Line 12:
In the first line we are reading the geometry of the postal codes in berlin

Line 14:
Reading the charging stations in Berlin (Adress, Name, Connector Type, etc.)

Line 15:
Preprocessing the data:
    - Selecting only the columns we need
    - Renaming the columns
    - Parsing the coordinates
    - Filtering for Berlin only (we are only interested in Berlin)
    - Sort by postal code
    - Appending geo data (polygon of the PLZ)
    - Converting to GeoDataFrame

Line 16:
Counting the number of charging stations per postal code

Line 18:
Reading in the population data

Line 19:
Same preprocessing as in line 15

Line 21:
Starting the streamlit app with the data we have prepared (two geo data frames)

# Interpretation of results

We have concluded that the inner city of Berlin has a suficient amount of charging stations. The outer parts of Berlin have a lack of charging stations. Also in the east of Berlin where a large amount of people live, there are not enough charging stations. In the outer west (Spandau) there are also not enough charging stations.