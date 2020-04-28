#load boto3 for connecting to AWS dynamodb
import boto3

#load in pandas to get the dataframe
import pandas as pd

#load the csv file as dataframe
data = pd.read_csv('bee_data.csv', index_col=False)
#get the total number of rows
rows = data.shape[0]
#gather the column names to have as the keys of the database
colname = data.columns.values

# read all the data into separate arrays
filenames = data.file.values
dates = data.date.values
time = data.time.values
location = data.location.values
zip = data['zip code'].values
subspecies = data.subspecies.values
health = data.health.values
pollen_carrying = data.pollen_carrying.values
caste = data.caste.values

# initiate a resource object which is an instance of dynamodb
db = boto3.resource('dynamodb')
tablename = 'BEEDATA'
table = db.Table(tablename)


# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)
colname

# use batch_writer to write a bunch of files onto the databse
with table.batch_writer() as batch:
    for i in range(rows):
        batch.put_item(
            Item = {
                'file' : str(filenames[i]),
                'date' : str(dates[i]),
                'time' : str(time[i]),
                'location' : str(location[i]),
                'zipcode' : str(zip[i]),
                'subspecies' : str(subspecies[i]),
                'health' : str(health[i]),
                'pollen_carrying' : str(pollen_carrying[i]),
                'caste': str(caste[i])
            }
        )
print('Uploaded all data to the table')
