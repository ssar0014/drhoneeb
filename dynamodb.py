#load boto3 for connecting to AWS dynamodb
import boto3

#load in pandas to get the dataframe
import pandas as pd

#load the csv file as dataframe
data = pd.read_csv('bee_data.csv', index_col=False)
#gather the column names to have as the keys of the database
colname = data.columns.values

# initiate a resource object which is an instance of dynamodb
db = boto3.resource('dynamodb')

#Set the table name and create the table which will store the information
tablename = 'BEEDATA'
table = db.create_table(
            TableName = tablename,
            KeySchema = [
            {
                'AttributeName':colname[0], # Define the filename as the primary key
                'KeyType': 'HASH'
            }
            ],
            AttributeDefinitions= [
            #Define the attribute definitions of the primary key
            {
                'AttributeName': colname[0],
                'AttributeType': 'S' #filenames are in string format
            }
            ],

            ProvisionedThroughput={
            'ReadCapacityUnits':6000,
            'WriteCapacityUnits':6000
            }
        )

print('Table Status: ', table.table_status)
