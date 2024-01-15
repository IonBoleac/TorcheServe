# Testing
In this directory, you will find some the tests for the project.
## Locust
This is a load testing tool that can be used to test the performance of the APIs. It can be used to simulate a large number of users and see how the system behaves under load. It can be used to test the APIs in the following way:
1. Install Locust using pip
```bash
pip install locust
```
2. Create a file called `locustfile.py` with the following contents:
```python
from locust import HttpUser, task, between
import pandas as pd

class QuickstartUser(HttpUser):
    wait_time = between(0.2, 0.2)
    @task
    def ping(self):
        id_column = 'id'
        csv_data = pd.read_csv("head2.csv", index_col=id_column)
        data = csv_data.to_csv(index=id_column)
        self.client.post("/predictions/logreg", data=data, headers={'Content-Type': 'text/csv'})
```
3. Run the locust command
```bash
locust
```
4. Open the locust UI in the browser at http://localhost:8089 and see the results

## Test APIs using k6s.io
1. Install k6s.io
```bash
```