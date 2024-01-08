import requests
import pandas as pd
# Read the CSV file and extract a row
id_column = 'id'
csv_data = pd.read_csv("head1.csv", index_col=id_column)
data = csv_data.to_csv(index=id_column)
json_data = csv_data.to_json()
print("json:", json_data, type(json_data))
print("csv_data:", csv_data, type(csv_data))
print("data:", data,  type(data))

# Prepare the data for the request

data = data.encode('utf-8')

# Send the request to the server
url = 'http://localhost:8080/predictions/logreg'
response = requests.post(url, data=data, headers={'Content-Type': 'text/csv'})

# Check the response
if response.status_code == 200:
    print('Request successful')
    print('Response:', response.json()['predictions'])
else:
    print('Request failed')
    print('Status code:', response.status_code)
    print('Error message:', response.text)

