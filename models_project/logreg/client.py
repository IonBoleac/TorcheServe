import requests
import pandas as pd
import sys
# Read the CSV file and extract a row
id_column = 'id'
csv_data = pd.read_csv("head2.csv", index_col=id_column)
data = csv_data.to_csv(index=id_column)
'''json_data = csv_data.to_json()
print("json:", json_data, type(json_data))
print("csv_data:", csv_data, type(csv_data))
print("data:", data,  type(data))'''

# Prepare the data for the request

data = data.encode('utf-8')

# Send the request to the server
host = 'torchserve.predictions.192.168.56.102.nip.io'
url = f'http://{host}/predictions/logreg'
for i in range(int(sys.argv[1])):
        
    response = requests.post(url, data=data, headers={'Content-Type': 'text/csv'})

    # Check the response
    if response.status_code == 200:
        print(f'{i}: Request successful\n')
        print(f'{i}: Response:\n', response.json()['predictions'])
    else:
        print('Request failed')
        print('Status code:', response.status_code)
        print('Error message:', response.text)

